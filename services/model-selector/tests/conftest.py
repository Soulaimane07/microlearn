# tests/conftest.py
# --------------------------------------------------------------------
# Pytest configuration and fixtures for model-selector tests.
# --------------------------------------------------------------------
import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_classification_data():
    """Generate sample classification dataset"""
    np.random.seed(42)
    n_samples = 200
    
    return pd.DataFrame({
        "feature1": np.random.randn(n_samples),
        "feature2": np.random.randn(n_samples),
        "feature3": np.random.randn(n_samples),
        "category1": np.random.choice(["A", "B", "C"], n_samples),
        "category2": np.random.choice(["X", "Y"], n_samples),
        "target": np.random.choice([0, 1], n_samples)
    })


@pytest.fixture
def sample_regression_data():
    """Generate sample regression dataset"""
    np.random.seed(42)
    n_samples = 200
    
    X1 = np.random.randn(n_samples)
    X2 = np.random.randn(n_samples)
    noise = np.random.randn(n_samples) * 0.1
    
    return pd.DataFrame({
        "feature1": X1,
        "feature2": X2,
        "feature3": np.random.randn(n_samples),
        "target": 2 * X1 + 3 * X2 + noise
    })


@pytest.fixture
def sample_clustering_data():
    """Generate sample clustering dataset"""
    np.random.seed(42)
    n_samples = 150
    
    # Generate 3 clusters
    cluster1 = np.random.randn(50, 2) + [0, 0]
    cluster2 = np.random.randn(50, 2) + [5, 5]
    cluster3 = np.random.randn(50, 2) + [10, 0]
    
    data = np.vstack([cluster1, cluster2, cluster3])
    
    return pd.DataFrame({
        "feature1": data[:, 0],
        "feature2": data[:, 1]
    })


@pytest.fixture
def imbalanced_data():
    """Generate imbalanced classification dataset"""
    np.random.seed(42)
    
    # 90% class 0, 10% class 1
    n_class0 = 180
    n_class1 = 20
    
    return pd.DataFrame({
        "feature1": np.random.randn(n_class0 + n_class1),
        "feature2": np.random.randn(n_class0 + n_class1),
        "target": [0] * n_class0 + [1] * n_class1
    })


@pytest.fixture
def missing_data():
    """Generate dataset with missing values"""
    np.random.seed(42)
    n_samples = 100
    
    df = pd.DataFrame({
        "feature1": np.random.randn(n_samples),
        "feature2": np.random.randn(n_samples),
        "feature3": np.random.randn(n_samples),
        "target": np.random.choice([0, 1], n_samples)
    })
    
    # Add missing values
    mask = np.random.random(n_samples) < 0.2
    df.loc[mask, "feature1"] = np.nan
    
    mask = np.random.random(n_samples) < 0.1
    df.loc[mask, "feature2"] = np.nan
    
    return df


@pytest.fixture
def high_dimensional_data():
    """Generate high-dimensional dataset"""
    np.random.seed(42)
    n_samples = 100
    n_features = 150
    
    data = {f"feature_{i}": np.random.randn(n_samples) for i in range(n_features)}
    data["target"] = np.random.choice([0, 1], n_samples)
    
    return pd.DataFrame(data)
