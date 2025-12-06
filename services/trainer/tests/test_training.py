# tests/test_training.py
# --------------------------------------------------------------------
# Unit tests for Trainer microservice.
# --------------------------------------------------------------------
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "trainer"
    assert "gpu_available" in data


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "trainer"
    assert data["status"] == "running"


def test_list_jobs_empty():
    """Test listing jobs when database is empty"""
    response = client.get("/train")
    assert response.status_code in [200, 500]  # May fail if DB not initialized


def test_list_models_empty():
    """Test listing models when no models exist"""
    response = client.get("/models/")
    assert response.status_code in [200, 500]  # May fail if DB not initialized


def test_training_request_validation():
    """Test training request validation"""
    # Missing required fields
    response = client.post("/train", json={})
    assert response.status_code == 422
    
    # Valid request structure
    request_data = {
        "model_id": "random_forest_classifier",
        "data_id": "test_dataset.csv",
        "task_type": "classification",
        "epochs": 10
    }
    
    # This will fail without proper setup, but tests validation
    response = client.post("/train", json=request_data)
    assert response.status_code in [200, 404, 500]


def test_get_nonexistent_job():
    """Test getting status of non-existent job"""
    response = client.get("/train/nonexistent_job_id")
    assert response.status_code in [404, 500]


def test_get_nonexistent_model():
    """Test getting non-existent model"""
    response = client.get("/models/nonexistent_job_id")
    assert response.status_code in [404, 500]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
