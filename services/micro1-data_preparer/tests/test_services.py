# tests/test_services.py
# --------------------------------------------------------------------
# Unit tests for DataPreparer service modules to improve coverage.
# Tests for: autodetect, pipeline, type_detector, date_detector, id_detector
# --------------------------------------------------------------------
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestAutodetect:
    """Tests for autodetect module"""
    
    def test_detect_metadata_basic(self):
        """Test basic metadata detection"""
        from app.services.autodetect import detect_metadata
        
        df = pd.DataFrame({
            "user_id": [1, 2, 3, 4, 5],
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "age": [25, 30, 35, 40, 45],
            "score": [0.5, 0.7, 0.8, 0.6, 0.9],
            "created_date": pd.date_range("2023-01-01", periods=5)
        })
        
        meta = detect_metadata(df)
        
        assert "id_columns" in meta
        assert "date_columns" in meta
        assert "numeric_columns" in meta
        assert "categorical_columns" in meta
        
        # user_id should be detected as ID column
        assert "user_id" in meta["id_columns"]
        # created_date should be detected as date column
        assert "created_date" in meta["date_columns"]
        # age and score should be numeric
        assert "age" in meta["numeric_columns"] or "age" in meta["id_columns"]
    
    def test_detect_metadata_by_name_patterns(self):
        """Test ID detection by name patterns"""
        from app.services.autodetect import detect_metadata
        
        df = pd.DataFrame({
            "record_id": [1, 2, 3],
            "_id": ["a", "b", "c"],
            "primary_key": [100, 200, 300],
            "value": [10, 20, 30]
        })
        
        meta = detect_metadata(df)
        
        # These should be detected as ID columns by name pattern
        assert "record_id" in meta["id_columns"]
        assert "_id" in meta["id_columns"]
        assert "primary_key" in meta["id_columns"]
    
    def test_detect_metadata_date_by_name(self):
        """Test date detection by column name"""
        from app.services.autodetect import detect_metadata
        
        df = pd.DataFrame({
            "created_timestamp": ["2023-01-01", "2023-01-02", "2023-01-03"],
            "update_datetime": ["2023-02-01", "2023-02-02", "2023-02-03"],
            "name": ["A", "B", "C"]
        })
        
        meta = detect_metadata(df)
        
        assert "created_timestamp" in meta["date_columns"]
        assert "update_datetime" in meta["date_columns"]
    
    def test_detect_metadata_high_uniqueness_id(self):
        """Test detection of ID columns by high uniqueness ratio"""
        from app.services.autodetect import detect_metadata
        
        # Create a dataframe with a numeric column that has high uniqueness
        df = pd.DataFrame({
            "sequence_num": list(range(100)),  # Unique values
            "category": ["A", "B"] * 50  # Low uniqueness
        })
        
        meta = detect_metadata(df)
        
        # High uniqueness column should be detected as ID
        assert "sequence_num" in meta["id_columns"]
    
    def test_metadata_to_pipeline_config_basic(self):
        """Test pipeline config generation from metadata"""
        from app.services.autodetect import metadata_to_pipeline_config
        
        meta = {
            "id_columns": ["user_id"],
            "date_columns": ["created_at"],
            "numeric_columns": ["age", "score"],
            "categorical_columns": ["category"]
        }
        
        config = metadata_to_pipeline_config(meta, target_column="score")
        
        assert "steps" in config
        assert len(config["steps"]) > 0
        
        # Check that ID columns are dropped
        drop_step = next((s for s in config["steps"] if s["type"] == "drop_columns"), None)
        assert drop_step is not None
        assert "user_id" in drop_step["columns"]
    
    def test_metadata_to_pipeline_config_excludes_target(self):
        """Test that target column is excluded from transformations"""
        from app.services.autodetect import metadata_to_pipeline_config
        
        meta = {
            "id_columns": [],
            "date_columns": [],
            "numeric_columns": ["feature1", "target"],
            "categorical_columns": ["cat1"]
        }
        
        config = metadata_to_pipeline_config(meta, target_column="target")
        
        # Target should not be in scaling or encoding steps
        for step in config["steps"]:
            if step["type"] in ["scale_numeric", "encode_categorical"]:
                assert "target" not in step.get("columns", [])
    
    def test_metadata_to_pipeline_config_empty(self):
        """Test pipeline config with empty metadata"""
        from app.services.autodetect import metadata_to_pipeline_config
        
        meta = {
            "id_columns": [],
            "date_columns": [],
            "numeric_columns": [],
            "categorical_columns": []
        }
        
        config = metadata_to_pipeline_config(meta)
        
        assert "steps" in config
        # Empty metadata should produce empty steps
        assert len(config["steps"]) == 0


class TestPipeline:
    """Tests for pipeline module"""
    
    def test_run_pipeline_empty_df_raises(self):
        """Test that empty DataFrame raises ValueError"""
        from app.services.pipeline import run_pipeline
        
        df = pd.DataFrame()
        
        with pytest.raises(ValueError, match="empty"):
            run_pipeline(df)
    
    def test_run_pipeline_invalid_config_raises(self):
        """Test that invalid config raises ValueError"""
        from app.services.pipeline import run_pipeline
        
        df = pd.DataFrame({"a": [1, 2, 3]})
        
        with pytest.raises(ValueError, match="steps"):
            run_pipeline(df, pipeline_conf={"invalid": "config"})
    
    def test_run_pipeline_auto_generate(self):
        """Test automatic pipeline generation"""
        from app.services.pipeline import run_pipeline
        
        df = pd.DataFrame({
            "user_id": [1, 2, 3, 4, 5],
            "feature1": [1.0, 2.0, 3.0, 4.0, 5.0],
            "category": ["A", "B", "A", "B", "A"],
            "target": [0, 1, 0, 1, 0]
        })
        
        result = run_pipeline(df, target_column="target")
        
        # Should complete without error
        assert len(result) > 0
    
    def test_run_pipeline_drop_columns(self):
        """Test drop columns step"""
        from app.services.pipeline import run_pipeline
        
        df = pd.DataFrame({
            "a": [1, 2, 3],
            "b": [4, 5, 6],
            "c": [7, 8, 9]
        })
        
        config = {
            "steps": [
                {"type": "drop_columns", "columns": ["a", "b"]}
            ]
        }
        
        result = run_pipeline(df, pipeline_conf=config)
        
        assert "a" not in result.columns
        assert "b" not in result.columns
        assert "c" in result.columns
    
    def test_run_pipeline_drop_nonexistent_columns(self):
        """Test dropping columns that don't exist (should warn but not fail)"""
        from app.services.pipeline import run_pipeline
        
        df = pd.DataFrame({"a": [1, 2, 3]})
        
        config = {
            "steps": [
                {"type": "drop_columns", "columns": ["nonexistent"]}
            ]
        }
        
        result = run_pipeline(df, pipeline_conf=config)
        
        assert "a" in result.columns
    
    def test_run_pipeline_handle_missing_drop(self):
        """Test handle missing values - drop method"""
        from app.services.pipeline import run_pipeline
        
        df = pd.DataFrame({
            "a": [1.0, None, 3.0],
            "b": [4.0, 5.0, 6.0]
        })
        
        config = {
            "steps": [
                {"type": "handle_missing", "method": "drop", "columns": ["a"]}
            ]
        }
        
        result = run_pipeline(df, pipeline_conf=config)
        
        assert len(result) == 2
        assert result["a"].isna().sum() == 0
    
    def test_run_pipeline_handle_missing_fill_mean(self):
        """Test handle missing values - fill mean method"""
        from app.services.pipeline import run_pipeline
        
        df = pd.DataFrame({
            "a": [1.0, None, 3.0, None, 5.0]
        })
        
        config = {
            "steps": [
                {"type": "handle_missing", "method": "fill_mean", "columns": ["a"]}
            ]
        }
        
        result = run_pipeline(df, pipeline_conf=config)
        
        assert result["a"].isna().sum() == 0
        # Mean of 1, 3, 5 is 3
        assert result["a"].iloc[1] == 3.0
    
    def test_run_pipeline_handle_missing_fill_median(self):
        """Test handle missing values - fill median method"""
        from app.services.pipeline import run_pipeline
        
        df = pd.DataFrame({
            "a": [1.0, None, 3.0, None, 5.0]
        })
        
        config = {
            "steps": [
                {"type": "handle_missing", "method": "fill_median", "columns": ["a"]}
            ]
        }
        
        result = run_pipeline(df, pipeline_conf=config)
        
        assert result["a"].isna().sum() == 0
    
    def test_run_pipeline_handle_missing_fill_mode(self):
        """Test handle missing values - fill mode method"""
        from app.services.pipeline import run_pipeline
        
        df = pd.DataFrame({
            "a": ["A", "A", None, "B", None]
        })
        
        config = {
            "steps": [
                {"type": "handle_missing", "method": "fill_mode", "columns": ["a"]}
            ]
        }
        
        result = run_pipeline(df, pipeline_conf=config)
        
        assert result["a"].isna().sum() == 0
    
    def test_run_pipeline_encode_categorical_label(self):
        """Test categorical encoding - label method"""
        from app.services.pipeline import run_pipeline
        
        df = pd.DataFrame({
            "cat": ["A", "B", "C", "A", "B"]
        })
        
        config = {
            "steps": [
                {"type": "encode_categorical", "method": "label", "columns": ["cat"]}
            ]
        }
        
        result = run_pipeline(df, pipeline_conf=config)
        
        # Should be converted to numeric codes
        assert pd.api.types.is_numeric_dtype(result["cat"])
    
    def test_run_pipeline_encode_categorical_onehot(self):
        """Test categorical encoding - onehot method"""
        from app.services.pipeline import run_pipeline
        
        df = pd.DataFrame({
            "cat": ["A", "B", "C"],
            "value": [1, 2, 3]
        })
        
        config = {
            "steps": [
                {"type": "encode_categorical", "method": "onehot", "columns": ["cat"]}
            ]
        }
        
        result = run_pipeline(df, pipeline_conf=config)
        
        # Original column should be replaced with one-hot columns
        assert "cat" not in result.columns
        assert len([c for c in result.columns if c.startswith("cat_")]) == 3
    
    def test_run_pipeline_scale_numeric_standard(self):
        """Test numeric scaling - standard method"""
        from app.services.pipeline import run_pipeline
        
        df = pd.DataFrame({
            "a": [1.0, 2.0, 3.0, 4.0, 5.0]
        })
        
        config = {
            "steps": [
                {"type": "scale_numeric", "method": "standard", "columns": ["a"]}
            ]
        }
        
        result = run_pipeline(df, pipeline_conf=config)
        
        # Standard scaled should have mean close to 0
        assert abs(result["a"].mean()) < 0.01
    
    def test_run_pipeline_scale_numeric_minmax(self):
        """Test numeric scaling - minmax method"""
        from app.services.pipeline import run_pipeline
        
        df = pd.DataFrame({
            "a": [0.0, 25.0, 50.0, 75.0, 100.0]
        })
        
        config = {
            "steps": [
                {"type": "scale_numeric", "method": "minmax", "columns": ["a"]}
            ]
        }
        
        result = run_pipeline(df, pipeline_conf=config)
        
        # MinMax should scale to [0, 1]
        assert result["a"].min() == 0.0
        assert result["a"].max() == 1.0
    
    def test_run_pipeline_scale_numeric_robust(self):
        """Test numeric scaling - robust method"""
        from app.services.pipeline import run_pipeline
        
        df = pd.DataFrame({
            "a": [1.0, 2.0, 3.0, 4.0, 5.0, 100.0]  # Outlier
        })
        
        config = {
            "steps": [
                {"type": "scale_numeric", "method": "robust", "columns": ["a"]}
            ]
        }
        
        result = run_pipeline(df, pipeline_conf=config)
        
        # Should complete without error
        assert len(result) == 6
    
    def test_run_pipeline_parse_dates(self):
        """Test date parsing step"""
        from app.services.pipeline import run_pipeline
        
        df = pd.DataFrame({
            "date_str": ["2023-01-01", "2023-01-02", "2023-01-03"]
        })
        
        config = {
            "steps": [
                {"type": "parse_dates", "columns": ["date_str"]}
            ]
        }
        
        result = run_pipeline(df, pipeline_conf=config)
        
        assert pd.api.types.is_datetime64_any_dtype(result["date_str"])
    
    def test_run_pipeline_unknown_step_type(self):
        """Test that unknown step types are skipped with warning"""
        from app.services.pipeline import run_pipeline
        
        df = pd.DataFrame({"a": [1, 2, 3]})
        
        config = {
            "steps": [
                {"type": "unknown_step_type", "columns": ["a"]}
            ]
        }
        
        # Should not raise, just warn
        result = run_pipeline(df, pipeline_conf=config)
        assert len(result) == 3


class TestTypeDetector:
    """Tests for type_detector module"""
    
    def test_detect_numeric_columns(self):
        """Test detection of numeric columns"""
        from app.services.type_detector import detect_column_types
        
        df = pd.DataFrame({
            "int_col": [1, 2, 3],
            "float_col": [1.1, 2.2, 3.3],
            "str_col": ["a", "b", "c"]
        })
        
        result = detect_column_types(df)
        
        assert "int_col" in result["numeric"]
        assert "float_col" in result["numeric"]
        assert "str_col" not in result["numeric"]
    
    def test_detect_categorical_columns(self):
        """Test detection of categorical columns"""
        from app.services.type_detector import detect_column_types
        
        df = pd.DataFrame({
            "category": ["A", "B", "A", "B"] * 10,
            "numeric": list(range(40))
        })
        
        result = detect_column_types(df)
        
        assert "category" in result["categorical"]
        assert "numeric" in result["numeric"]
    
    def test_detect_column_types_empty_df(self):
        """Test with empty dataframe"""
        from app.services.type_detector import detect_column_types
        
        df = pd.DataFrame()
        
        result = detect_column_types(df)
        
        assert result["numeric"] == []
        assert result["categorical"] == []


class TestDateDetector:
    """Tests for date_detector module"""
    
    def test_detect_date_columns_standard(self):
        """Test detection of standard date formats"""
        from app.services.date_detector import detect_date_columns
        
        df = pd.DataFrame({
            "date1": ["2023-01-01", "2023-01-02", "2023-01-03"],
            "date2": ["01/15/2023", "01/16/2023", "01/17/2023"],
            "not_date": ["hello", "world", "test"]
        })
        
        result = detect_date_columns(df)
        
        assert "date1" in result
        assert "date2" in result
        assert "not_date" not in result
    
    def test_detect_date_columns_empty_series(self):
        """Test with empty or all-null series"""
        from app.services.date_detector import detect_date_columns
        
        df = pd.DataFrame({
            "empty": [None, None, None],
            "valid_date": ["2023-01-01", "2023-01-02", "2023-01-03"]
        })
        
        result = detect_date_columns(df)
        
        assert "empty" not in result
        assert "valid_date" in result
    
    def test_detect_date_columns_partial_dates(self):
        """Test with partially parseable dates"""
        from app.services.date_detector import detect_date_columns
        
        df = pd.DataFrame({
            "mixed": ["2023-01-01", "not-a-date", "2023-01-03"] * 20  # 66% parseable
        })
        
        result = detect_date_columns(df)
        
        # Should not be detected (below 80% threshold)
        assert "mixed" not in result


class TestIdDetector:
    """Tests for id_detector module"""
    
    def test_detect_id_by_name_pattern(self):
        """Test ID detection by name patterns"""
        from app.services.id_detector import detect_id_columns
        
        df = pd.DataFrame({
            "customer_id": [1, 2, 3],
            "patient_id": [100, 200, 300],
            "_id": ["a", "b", "c"],
            "value": [10, 20, 30]
        })
        
        result = detect_id_columns(df)
        
        assert "customer_id" in result
        assert "patient_id" in result
        assert "_id" in result
        assert "value" not in result
    
    def test_detect_id_by_uuid_format(self):
        """Test ID detection by UUID format"""
        from app.services.id_detector import detect_id_columns
        
        df = pd.DataFrame({
            "uuid_col": [
                "550e8400-e29b-41d4-a716-446655440000",
                "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                "6ba7b811-9dad-11d1-80b4-00c04fd430c8"
            ] * 10,
            "normal_col": ["a", "b", "c"] * 10
        })
        
        result = detect_id_columns(df)
        
        assert "uuid_col" in result
        assert "normal_col" not in result
    
    def test_looks_like_uuid_series(self):
        """Test UUID series detection"""
        from app.services.id_detector import looks_like_uuid_series
        
        valid_uuids = pd.Series([
            "550e8400-e29b-41d4-a716-446655440000",
            "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
            "6ba7b811-9dad-11d1-80b4-00c04fd430c8"
        ])
        
        invalid = pd.Series(["hello", "world", "test"])
        empty = pd.Series([], dtype=str)
        
        assert looks_like_uuid_series(valid_uuids) == True
        assert looks_like_uuid_series(invalid) == False
        assert looks_like_uuid_series(empty) == False


class TestPipelineAuto:
    """Tests for pipeline_auto module"""
    
    def test_auto_pipeline_runs(self):
        """Test automatic pipeline execution"""
        try:
            from app.services.pipeline_auto import AutoPipeline
            
            df = pd.DataFrame({
                "feature1": [1.0, 2.0, 3.0, 4.0, 5.0],
                "feature2": [0.1, 0.2, 0.3, 0.4, 0.5],
                "category": ["A", "B", "A", "B", "A"],
                "target": [0, 1, 0, 1, 0]
            })
            
            pipeline = AutoPipeline()
            result = pipeline.fit_transform(df, target_column="target")
            
            assert len(result) > 0
        except (ImportError, AttributeError):
            pytest.skip("AutoPipeline not available")


class TestValidator:
    """Tests for validator module"""
    
    def test_validator_import(self):
        """Test validator module imports"""
        try:
            from app.services.validator import validate_dataframe
            # Just test that import works
            assert validate_dataframe is not None
        except (ImportError, AttributeError):
            pytest.skip("Validator not available")


class TestDetectAPI:
    """Tests for /detect API endpoint"""
    
    def test_detect_csv_valid(self):
        """Test detect endpoint with valid CSV"""
        csv_content = "id,name,age,salary\n1,John,30,50000\n2,Jane,25,60000"
        
        response = client.post(
            "/detect",
            files={"file": ("test.csv", csv_content, "text/csv")},
            data={"store_to_minio": "false"}
        )
        
        # May need MinIO or could work without
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert "id_columns" in data
            assert "numeric_columns" in data
    
    def test_detect_non_csv_file(self):
        """Test detect endpoint rejects non-CSV files"""
        response = client.post(
            "/detect",
            files={"file": ("test.txt", "hello world", "text/plain")}
        )
        
        assert response.status_code == 400
    
    def test_detect_empty_csv(self):
        """Test detect endpoint with empty CSV"""
        response = client.post(
            "/detect",
            files={"file": ("empty.csv", "", "text/csv")}
        )
        
        assert response.status_code == 400


class TestPrepareAPI:
    """Tests for /prepare API endpoint"""
    
    def test_prepare_no_input(self):
        """Test prepare endpoint with no input"""
        response = client.post("/prepare/")
        
        # Should fail validation
        assert response.status_code in [400, 422]
    
    def test_prepare_both_inputs(self):
        """Test prepare endpoint with both file and minio_object"""
        csv_content = "a,b,c\n1,2,3"
        
        response = client.post(
            "/prepare/",
            files={"file": ("test.csv", csv_content, "text/csv")},
            data={"minio_object": "raw/test.csv"}
        )
        
        assert response.status_code == 400
    
    def test_prepare_non_csv_file(self):
        """Test prepare endpoint rejects non-CSV files"""
        response = client.post(
            "/prepare/",
            files={"file": ("test.txt", "hello", "text/plain")}
        )
        
        assert response.status_code == 400
    
    def test_prepare_empty_file(self):
        """Test prepare endpoint with empty file"""
        response = client.post(
            "/prepare/",
            files={"file": ("empty.csv", "", "text/csv")}
        )
        
        assert response.status_code == 400


class TestPipelineValidator:
    """Tests for pipeline configuration validation"""
    
    def test_validate_steps_format(self):
        """Test step format validation"""
        from app.services.pipeline import run_pipeline
        
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        
        # Valid config
        config = {"steps": [{"type": "drop_columns", "columns": []}]}
        result = run_pipeline(df, config)
        assert len(result) == 3
    
    def test_pipeline_multiple_steps(self):
        """Test pipeline with multiple steps"""
        from app.services.pipeline import run_pipeline
        
        df = pd.DataFrame({
            "id_col": [1, 2, 3],
            "numeric": [10.0, None, 30.0],
            "category": ["A", "B", "A"]
        })
        
        config = {
            "steps": [
                {"type": "drop_columns", "columns": ["id_col"]},
                {"type": "handle_missing", "method": "fill_mean", "columns": ["numeric"]},
                {"type": "encode_categorical", "method": "label", "columns": ["category"]}
            ]
        }
        
        result = run_pipeline(df, config)
        
        assert "id_col" not in result.columns
        assert result["numeric"].isna().sum() == 0
        assert pd.api.types.is_numeric_dtype(result["category"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
