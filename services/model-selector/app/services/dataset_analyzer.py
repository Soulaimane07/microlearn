# app/services/dataset_analyzer.py
# --------------------------------------------------------------------
# Service for analyzing datasets and determining their characteristics.
# Used to inform model selection decisions.
# --------------------------------------------------------------------
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List

from app.core.logger import logger


def convert_numpy_types(obj: Any) -> Any:
    """Convert numpy types to Python native types for JSON serialization."""
    if isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif pd.isna(obj):
        return None
    return obj


class DatasetAnalyzer:
    """Analyzes datasets to determine characteristics for model selection"""
    
    # Thresholds for data size categorization
    SIZE_THRESHOLDS = {
        "small": 1000,
        "medium": 10000,
        "large": 100000,
        "very_large": 1000000
    }
    
    def analyze(
        self,
        df: pd.DataFrame,
        task_type: Optional[str] = None,
        target_column: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze a dataset and return its characteristics.
        
        Args:
            df: DataFrame to analyze
            task_type: Override for task type detection
            target_column: Name of target column for supervised learning
            
        Returns:
            Dictionary containing dataset analysis results
        """
        logger.info(f"Analyzing dataset: {df.shape[0]} rows, {df.shape[1]} columns")
        
        analysis = {
            "n_rows": len(df),
            "n_columns": len(df.columns),
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
        }
        
        # Categorize columns by type
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        bool_cols = df.select_dtypes(include=['bool']).columns.tolist()
        
        analysis["numeric_columns"] = numeric_cols
        analysis["categorical_columns"] = categorical_cols
        analysis["datetime_columns"] = datetime_cols
        analysis["boolean_columns"] = bool_cols
        
        # Detect target column if not provided
        if target_column is None:
            target_column = self._detect_target_column(df)
        
        analysis["target_column"] = target_column
        
        # Determine task type
        if task_type:
            analysis["task_type"] = task_type
        else:
            analysis["task_type"] = self._detect_task_type(df, target_column)
        
        # Analyze target column if present
        if target_column and target_column in df.columns:
            target_analysis = self._analyze_target(df[target_column], analysis["task_type"])
            analysis.update(target_analysis)
        
        # Calculate feature count (excluding target)
        feature_cols = [c for c in df.columns if c != target_column]
        analysis["n_features"] = len(feature_cols)
        analysis["feature_columns"] = feature_cols
        
        # Missing values analysis
        missing_info = self._analyze_missing_values(df)
        analysis.update(missing_info)
        
        # Data size categorization
        analysis["data_size_category"] = self._categorize_size(len(df))
        
        # Feature-target ratio (important for overfitting risk)
        if target_column:
            analysis["feature_target_ratio"] = len(feature_cols) / max(1, len(df))
        
        # Statistical summary for numeric columns
        if numeric_cols:
            analysis["numeric_stats"] = self._get_numeric_stats(df[numeric_cols])
        
        # Cardinality for categorical columns
        if categorical_cols:
            analysis["categorical_cardinality"] = {
                col: df[col].nunique() for col in categorical_cols
            }
        
        # Generate warnings and recommendations
        analysis["warnings"] = self._generate_warnings(analysis)
        analysis["recommendations"] = self._generate_recommendations(analysis)
        
        logger.info(f"Analysis complete: task_type={analysis['task_type']}")
        
        # Convert numpy types to Python native types for JSON serialization
        return convert_numpy_types(analysis)
    
    def _detect_target_column(self, df: pd.DataFrame) -> Optional[str]:
        """Attempt to detect the target column heuristically"""
        common_target_names = [
            'target', 'label', 'class', 'y', 'output',
            'prediction', 'result', 'outcome', 'status'
        ]
        
        # Check for exact matches (case-insensitive)
        for col in df.columns:
            if col.lower() in common_target_names:
                logger.info(f"Auto-detected target column: {col}")
                return col
        
        # Check for partial matches
        for col in df.columns:
            for target_name in common_target_names:
                if target_name in col.lower():
                    logger.info(f"Auto-detected target column (partial match): {col}")
                    return col
        
        # If last column is categorical with few unique values, assume it's target
        last_col = df.columns[-1]
        if df[last_col].dtype == 'object' or df[last_col].nunique() < 20:
            logger.info(f"Assuming last column as target: {last_col}")
            return last_col
        
        return None
    
    def _detect_task_type(self, df: pd.DataFrame, target_column: Optional[str]) -> str:
        """Detect whether this is classification, regression, or clustering"""
        if target_column is None or target_column not in df.columns:
            logger.info("No target column - assuming clustering task")
            return "clustering"
        
        target = df[target_column]
        n_unique = target.nunique()
        
        # Check if numeric
        if pd.api.types.is_numeric_dtype(target):
            # If few unique values, likely classification
            if n_unique <= 20 and n_unique < len(df) * 0.05:
                logger.info(f"Numeric target with {n_unique} unique values - classification")
                return "classification"
            else:
                logger.info(f"Numeric target with {n_unique} unique values - regression")
                return "regression"
        else:
            # Categorical target = classification
            logger.info(f"Categorical target with {n_unique} classes - classification")
            return "classification"
    
    def _analyze_target(self, target: pd.Series, task_type: str) -> Dict[str, Any]:
        """Analyze the target column"""
        result = {
            "target_type": str(target.dtype),
            "target_unique_values": target.nunique()
        }
        
        if task_type == "classification":
            result["n_classes"] = target.nunique()
            result["class_distribution"] = target.value_counts().to_dict()
            
            # Check for class imbalance
            counts = target.value_counts()
            if len(counts) > 1:
                imbalance_ratio = counts.max() / counts.min()
                result["class_imbalance_ratio"] = round(imbalance_ratio, 2)
                result["is_imbalanced"] = imbalance_ratio > 3
        
        elif task_type == "regression":
            result["target_mean"] = float(target.mean())
            result["target_std"] = float(target.std())
            result["target_min"] = float(target.min())
            result["target_max"] = float(target.max())
        
        return result
    
    def _analyze_missing_values(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze missing values in the dataset"""
        missing_counts = df.isnull().sum()
        total_missing = missing_counts.sum()
        total_cells = df.shape[0] * df.shape[1]
        
        columns_with_missing = missing_counts[missing_counts > 0].to_dict()
        
        return {
            "has_missing_values": total_missing > 0,
            "missing_percentage": round(total_missing / total_cells * 100, 2) if total_cells > 0 else 0,
            "columns_with_missing": columns_with_missing,
            "n_columns_with_missing": len(columns_with_missing)
        }
    
    def _categorize_size(self, n_rows: int) -> str:
        """Categorize dataset by size"""
        if n_rows < self.SIZE_THRESHOLDS["small"]:
            return "small"
        elif n_rows < self.SIZE_THRESHOLDS["medium"]:
            return "medium"
        elif n_rows < self.SIZE_THRESHOLDS["large"]:
            return "large"
        else:
            return "very_large"
    
    def _get_numeric_stats(self, df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Get basic statistics for numeric columns"""
        stats = {}
        for col in df.columns:
            stats[col] = {
                "mean": float(df[col].mean()) if not df[col].isna().all() else None,
                "std": float(df[col].std()) if not df[col].isna().all() else None,
                "min": float(df[col].min()) if not df[col].isna().all() else None,
                "max": float(df[col].max()) if not df[col].isna().all() else None
            }
        return stats
    
    def _generate_warnings(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate warnings based on analysis"""
        warnings = []
        
        if analysis.get("missing_percentage", 0) > 20:
            warnings.append(f"High percentage of missing values ({analysis['missing_percentage']}%)")
        
        if analysis.get("is_imbalanced"):
            warnings.append(f"Class imbalance detected (ratio: {analysis.get('class_imbalance_ratio')})")
        
        if analysis.get("feature_target_ratio", 0) > 0.1:
            warnings.append("High feature-to-sample ratio - risk of overfitting")
        
        if analysis.get("n_features", 0) > 100:
            warnings.append("High dimensionality - consider feature selection")
        
        if analysis.get("data_size_category") == "small":
            warnings.append("Small dataset - be cautious of overfitting")
        
        return warnings
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        task_type = analysis.get("task_type")
        size = analysis.get("data_size_category")
        
        if task_type == "classification":
            if analysis.get("is_imbalanced"):
                recommendations.append("Consider using class weights or resampling techniques")
            if analysis.get("n_classes", 0) > 10:
                recommendations.append("Multi-class problem - consider OneVsRest or hierarchical approaches")
        
        if task_type == "regression":
            recommendations.append("Consider checking for outliers in target variable")
        
        if size in ["small", "medium"]:
            recommendations.append("Dataset size suitable for most ML algorithms")
        elif size == "large":
            recommendations.append("Consider algorithms with good scalability (e.g., LightGBM, XGBoost)")
        else:
            recommendations.append("Very large dataset - consider sampling or distributed training")
        
        if analysis.get("has_missing_values"):
            recommendations.append("Handle missing values before training (imputation or tree-based models)")
        
        if analysis.get("categorical_columns"):
            recommendations.append("Encode categorical variables (one-hot, label, or target encoding)")
        
        return recommendations
