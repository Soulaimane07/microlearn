#!/usr/bin/env python3
"""
Test script for MicroLearn microservices
Tests all 3 services: DataPreparer, ModelSelector, and Trainer
"""

import requests
import time
import json
from typing import Dict, Any

# Service URLs
DATA_PREPARER_URL = "http://localhost:8000"
MODEL_SELECTOR_URL = "http://localhost:8001"
TRAINER_URL = "http://localhost:8002"

def print_section(title: str):
    """Print section separator"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_result(test_name: str, success: bool, details: str = ""):
    """Print test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} - {test_name}")
    if details:
        print(f"  Details: {details}")

def test_health(service_name: str, url: str) -> bool:
    """Test health endpoint"""
    try:
        response = requests.get(f"{url}/health/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_result(f"{service_name} Health Check", True, 
                        f"Status: {data.get('status', 'unknown')}")
            return True
        else:
            print_result(f"{service_name} Health Check", False,
                        f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_result(f"{service_name} Health Check", False, str(e))
        return False

def test_data_preparer():
    """Test DataPreparer service"""
    print_section("TESTING DATA PREPARER SERVICE (Port 8000)")
    
    # Test health
    test_health("DataPreparer", DATA_PREPARER_URL)
    
    # Test root endpoint
    try:
        response = requests.get(f"{DATA_PREPARER_URL}/")
        print_result("DataPreparer Root Endpoint", 
                    response.status_code == 200,
                    response.json().get('message', ''))
    except Exception as e:
        print_result("DataPreparer Root Endpoint", False, str(e))
    
    # Test detect endpoint (without file - should get validation error or method description)
    try:
        response = requests.get(f"{DATA_PREPARER_URL}/detect")
        print_result("DataPreparer Detect Endpoint",
                    response.status_code in [200, 405, 422],
                    f"Status: {response.status_code}")
    except Exception as e:
        print_result("DataPreparer Detect Endpoint", False, str(e))

def test_model_selector():
    """Test ModelSelector service"""
    print_section("TESTING MODEL SELECTOR SERVICE (Port 8001)")
    
    # Test health
    test_health("ModelSelector", MODEL_SELECTOR_URL)
    
    # Test root endpoint
    try:
        response = requests.get(f"{MODEL_SELECTOR_URL}/")
        print_result("ModelSelector Root Endpoint",
                    response.status_code == 200,
                    response.json().get('message', ''))
    except Exception as e:
        print_result("ModelSelector Root Endpoint", False, str(e))
    
    # Test list models endpoint
    try:
        response = requests.get(f"{MODEL_SELECTOR_URL}/models/")
        if response.status_code == 200:
            data = response.json()
            models_count = len(data.get('models', []))
            print_result("ModelSelector List Models",
                        True,
                        f"Found {models_count} models")
            
            # Print first few models
            if models_count > 0:
                print(f"\n  Available models (showing first 5):")
                for model in data['models'][:5]:
                    print(f"    - {model.get('model_id', 'unknown')}: {model.get('name', 'N/A')}")
        else:
            print_result("ModelSelector List Models", False,
                        f"Status code: {response.status_code}")
    except Exception as e:
        print_result("ModelSelector List Models", False, str(e))
    
    # Test select models endpoint
    try:
        payload = {
            "task_type": "classification",
            "dataset_size": 1000,
            "n_features": 10
        }
        response = requests.post(f"{MODEL_SELECTOR_URL}/select", json=payload)
        if response.status_code == 200:
            data = response.json()
            selected_count = len(data.get('selected_models', []))
            print_result("ModelSelector Select Models",
                        True,
                        f"Selected {selected_count} models for classification")
            
            # Print selected models
            if selected_count > 0:
                print(f"  Recommended models:")
                for model in data['selected_models'][:3]:
                    print(f"    - {model.get('model_id', 'unknown')}: Score {model.get('score', 0):.2f}")
        else:
            print_result("ModelSelector Select Models", False,
                        f"Status code: {response.status_code}")
    except Exception as e:
        print_result("ModelSelector Select Models", False, str(e))

def test_trainer():
    """Test Trainer service"""
    print_section("TESTING TRAINER SERVICE (Port 8002)")
    
    # Test health
    try:
        response = requests.get(f"{TRAINER_URL}/health/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            health_status = data.get('status', 'unknown')
            gpu_available = data.get('gpu_available', False)
            postgres_ok = data.get('postgres_connected', False)
            minio_ok = data.get('minio_connected', False)
            
            details = f"GPU: {gpu_available}, PostgreSQL: {postgres_ok}, MinIO: {minio_ok}"
            print_result("Trainer Health Check", True, details)
        else:
            print_result("Trainer Health Check", False,
                        f"Status code: {response.status_code}")
    except Exception as e:
        print_result("Trainer Health Check", False, str(e))
    
    # Test root endpoint
    try:
        response = requests.get(f"{TRAINER_URL}/")
        print_result("Trainer Root Endpoint",
                    response.status_code == 200,
                    response.json().get('message', ''))
    except Exception as e:
        print_result("Trainer Root Endpoint", False, str(e))
    
    # Test list training jobs
    try:
        response = requests.get(f"{TRAINER_URL}/train")
        if response.status_code == 200:
            data = response.json()
            jobs_count = len(data.get('jobs', []))
            print_result("Trainer List Jobs",
                        True,
                        f"Found {jobs_count} training jobs")
        else:
            print_result("Trainer List Jobs", False,
                        f"Status code: {response.status_code}")
    except Exception as e:
        print_result("Trainer List Jobs", False, str(e))
    
    # Test list trained models
    try:
        response = requests.get(f"{TRAINER_URL}/models/")
        if response.status_code == 200:
            data = response.json()
            models_count = data.get('total', 0)
            print_result("Trainer List Trained Models",
                        True,
                        f"Found {models_count} trained models")
        else:
            print_result("Trainer List Trained Models", False,
                        f"Status code: {response.status_code}")
    except Exception as e:
        print_result("Trainer List Trained Models", False, str(e))

def test_integration():
    """Test integration between services"""
    print_section("INTEGRATION TESTS")
    
    print("\n📝 Integration Workflow:")
    print("  1. DataPreparer: Cleans and validates data")
    print("  2. ModelSelector: Recommends best models for task")
    print("  3. Trainer: Trains selected models with prepared data")
    print("\n  Note: Full workflow testing requires sample data upload")
    print("  which would be done through file upload endpoints.")

def main():
    """Main test runner"""
    print("\n" + "="*70)
    print("  🧪 MICROLEARN MICROSERVICES TEST SUITE")
    print("  Testing 3 microservices: DataPreparer, ModelSelector, Trainer")
    print("="*70)
    
    # Wait for services to be fully ready
    print("\n⏳ Waiting for services to be ready...")
    time.sleep(3)
    
    # Test each service
    test_data_preparer()
    test_model_selector()
    test_trainer()
    test_integration()
    
    # Summary
    print_section("TEST SUMMARY")
    print("\n✅ All basic connectivity tests completed!")
    print("\n📚 Next Steps:")
    print("  1. Upload a CSV file to DataPreparer")
    print("  2. Use ModelSelector to find best models")
    print("  3. Submit training job to Trainer")
    print("  4. Monitor training progress and download trained model")
    print("\n📖 Full API documentation:")
    print(f"  - DataPreparer: {DATA_PREPARER_URL}/docs")
    print(f"  - ModelSelector: {MODEL_SELECTOR_URL}/docs")
    print(f"  - Trainer: {TRAINER_URL}/docs")
    print()

if __name__ == "__main__":
    main()
