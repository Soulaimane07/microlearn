# 🚀 Trainer - Service d'Entraînement de Modèles ML

## 📋 Description

**Trainer** est le troisième microservice de la plateforme MicroLearn qui gère l'**entraînement parallèle** des modèles de Machine Learning sélectionnés. Il supporte l'accélération GPU, l'entraînement distribué avec Ray, et le suivi des expériences avec MLflow.

## 🏗️ Architecture

```
trainer/
├── app/
│   ├── main.py                          # Point d'entrée FastAPI
│   ├── api/
│   │   ├── health_router.py             # Endpoints de santé
│   │   ├── train_router.py              # Endpoints d'entraînement
│   │   └── models_router.py             # Endpoints modèles entraînés
│   ├── core/
│   │   ├── config.py                    # Configuration
│   │   └── logger.py                    # Logging
│   ├── models/
│   │   ├── request_models.py            # Modèles de requête
│   │   └── response_models.py           # Modèles de réponse
│   ├── services/
│   │   ├── training_orchestrator.py     # Orchestrateur principal
│   │   ├── model_factory.py             # Factory de modèles ML
│   │   └── mlflow_tracker.py            # Intégration MLflow
│   └── storage/
│       ├── minio_client.py              # Client MinIO
│       └── postgres_client.py           # Client PostgreSQL
├── tests/
│   └── test_training.py
├── Dockerfile
└── requirements.txt
```

## 🚀 Fonctionnalités

### 1. Entraînement Asynchrone
- Soumission de jobs d'entraînement en arrière-plan
- Suivi en temps réel de la progression
- Support de l'annulation de jobs en cours

### 2. Accélération GPU
- Détection automatique des GPU disponibles
- Allocation intelligente des GPUs aux jobs
- Support multi-GPU avec distribution équitable
- Fallback CPU si pas de GPU disponible

### 3. Gestion des Modèles
Plus de **20 modèles** supportés :
- **Classification** : Random Forest, XGBoost, LightGBM, SVM, KNN, etc.
- **Régression** : Linear, Ridge, Lasso, Random Forest, XGBoost, etc.
- **Clustering** : K-Means, DBSCAN, Hierarchical

### 4. Suivi avec MLflow
- Journalisation automatique des hyperparamètres
- Tracking des métriques par epoch
- Sauvegarde des artefacts
- Comparaison d'expériences

### 5. Stockage Distribué
- **MinIO** : Sauvegarde des modèles entraînés et checkpoints
- **PostgreSQL** : Métadonnées, jobs, et métriques
- Téléchargement sécurisé des modèles

## 📡 API Endpoints

### Santé
```http
GET /health/
```
Vérifie l'état du service et des ressources.

**Réponse :**
```json
{
  "status": "ok",
  "service": "trainer",
  "gpu_available": true,
  "ray_initialized": false,
  "mlflow_connected": true,
  "postgres_connected": true,
  "minio_connected": true
}
```

### Entraînement

#### Démarrer un entraînement
```http
POST /train
```

**Body (JSON) :**
```json
{
  "model_id": "xgboost_classifier",
  "data_id": "dataset_123.csv",
  "task_type": "classification",
  "epochs": 100,
  "batch_size": 32,
  "learning_rate": 0.001,
  "hyperparameters": {
    "n_estimators": 100,
    "max_depth": 6
  },
  "target_column": "target",
  "use_gpu": true,
  "early_stopping": true,
  "patience": 10,
  "experiment_name": "my_experiment",
  "tags": {
    "team": "data-science"
  }
}
```

**Réponse :**
```json
{
  "job_id": "train_a1b2c3d4e5f6",
  "status": "pending",
  "model_id": "xgboost_classifier",
  "data_id": "dataset_123.csv",
  "created_at": "2025-12-02T10:00:00",
  "total_epochs": 100,
  "mlflow_run_id": "abc123def456"
}
```

#### Obtenir le statut d'un job
```http
GET /train/{job_id}
```

**Réponse :**
```json
{
  "job_id": "train_a1b2c3d4e5f6",
  "status": "running",
  "model_id": "xgboost_classifier",
  "current_epoch": 45,
  "total_epochs": 100,
  "progress_percentage": 45.0,
  "gpu_allocated": "cuda:0",
  "best_metrics": {
    "val_accuracy": 0.92,
    "train_accuracy": 0.95
  }
}
```

#### Progression détaillée
```http
GET /train/{job_id}/progress
```

Retourne les métriques par epoch et les checkpoints sauvegardés.

#### Lister les jobs
```http
GET /train?status=running&limit=10
```

**Paramètres :**
- `status` : Filtrer par statut (pending, running, completed, failed)
- `limit` : Nombre max de résultats (1-100)

#### Annuler un job
```http
DELETE /train/{job_id}
```

### Modèles Entraînés

#### Lister les modèles
```http
GET /models/?page=1&page_size=10
```

**Réponse :**
```json
{
  "models": [
    {
      "model_id": "xgboost_classifier",
      "job_id": "train_a1b2c3d4e5f6",
      "model_name": "Xgboost Classifier",
      "task_type": "classification",
      "minio_path": "trained-models/xgboost_classifier/train_a1b2c3d4e5f6_20251202.pkl",
      "file_size_mb": 2.5,
      "metrics": {
        "val_accuracy": 0.92
      },
      "created_at": "2025-12-02T11:30:00"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10
}
```

#### Détails d'un modèle
```http
GET /models/{job_id}
```

#### Télécharger un modèle
```http
GET /models/{job_id}/download
```

Télécharge le fichier `.pkl` du modèle entraîné.

#### Supprimer un modèle
```http
DELETE /models/{job_id}
```

## ⚙️ Configuration

Variables d'environnement :

| Variable | Description | Défaut |
|----------|-------------|--------|
| `SERVICE_NAME` | Nom du service | trainer |
| `SERVICE_PORT` | Port d'écoute | 8002 |
| `POSTGRES_HOST` | Hôte PostgreSQL | postgres |
| `POSTGRES_DB` | Base de données | microlearn |
| `MINIO_ENDPOINT` | Endpoint MinIO | minio:9000 |
| `MINIO_BUCKET_MODELS` | Bucket des modèles | trained-models |
| `MINIO_BUCKET_DATA` | Bucket des données | data-preparer |
| `MLFLOW_TRACKING_URI` | URI MLflow | http://mlflow:5000 |
| `MAX_PARALLEL_JOBS` | Jobs parallèles max | 3 |
| `DEFAULT_EPOCHS` | Epochs par défaut | 100 |
| `EARLY_STOPPING_PATIENCE` | Patience early stopping | 10 |
| `CUDA_VISIBLE_DEVICES` | GPUs visibles | None (tous) |

## 🐳 Lancement

### Avec Docker Compose
```bash
cd microlearn
docker-compose up -d trainer
```

Le service sera accessible sur : `http://localhost:8002`

### Avec GPU (Docker Compose)
Décommentez la section GPU dans `docker-compose.yml` :
```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
```

Puis :
```bash
docker-compose up -d --build trainer
```

### Documentation API
Swagger UI : `http://localhost:8002/docs`

## 🔄 Flux de Travail

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Requête       │────▶│  Training        │────▶│  PostgreSQL     │
│   d'entraînement│     │  Orchestrator    │     │  (metadata)     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │  Allocation  │
                        │  GPU/CPU     │
                        └──────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │  Chargement  │
                        │  Dataset     │◀─── MinIO (data-preparer)
                        └──────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │  Model       │
                        │  Factory     │
                        └──────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │  Entraînement│
                        │  + Metrics   │────▶ MLflow
                        └──────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │  Sauvegarde  │
                        │  Modèle      │────▶ MinIO (trained-models)
                        └──────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │  Job         │
                        │  Completed   │
                        └──────────────┘
```

## 📊 Suivi avec MLflow

Le service s'intègre avec MLflow pour le suivi des expériences :

1. **Paramètres journalisés** :
   - model_id, task_type, epochs, batch_size, learning_rate
   - Tous les hyperparamètres personnalisés

2. **Métriques trackées** :
   - train_loss, val_loss
   - train_accuracy, val_accuracy (classification)
   - train_rmse, val_rmse, val_r2 (régression)

3. **Tags** :
   - Tags personnalisés via l'API
   - job_id, data_id automatiques

## 🧪 Tests

```bash
# Lancer les tests
cd trainer
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=app --cov-report=html
```

## 📚 Dépendances Principales

- **PyTorch** : Framework deep learning avec support GPU
- **PyTorch Lightning** : Simplification de l'entraînement
- **Ray** : Calcul distribué et parallélisation
- **MLflow** : Suivi d'expériences
- **FastAPI** : API REST
- **scikit-learn, XGBoost, LightGBM** : Modèles ML
- **MinIO** : Stockage d'objets
- **PostgreSQL** : Base de données relationnelle

## 🔗 Intégration avec MicroLearn

Trainer s'intègre avec les autres microservices :

1. **DataPreparer** (port 8000) : Source des datasets nettoyés
2. **ModelSelector** (port 8001) : Fournit les modèles recommandés
3. **Trainer** (port 8002) : Entraîne les modèles ← *Vous êtes ici*
4. **Deployer** (à venir) : Déploiement des modèles entraînés

## 📝 Exemple Complet

```python
import requests

BASE_URL = "http://localhost:8002"

# 1. Vérifier la santé
health = requests.get(f"{BASE_URL}/health/").json()
print(f"GPU disponible: {health['gpu_available']}")

# 2. Démarrer un entraînement
training_request = {
    "model_id": "random_forest_classifier",
    "data_id": "iris_prepared.csv",
    "task_type": "classification",
    "epochs": 50,
    "hyperparameters": {
        "n_estimators": 100,
        "max_depth": 10
    },
    "target_column": "species",
    "use_gpu": False,
    "experiment_name": "iris_classification"
}

response = requests.post(f"{BASE_URL}/train", json=training_request)
job = response.json()
job_id = job['job_id']
print(f"Job créé: {job_id}")

# 3. Surveiller la progression
import time
while True:
    status = requests.get(f"{BASE_URL}/train/{job_id}").json()
    print(f"Status: {status['status']}, Progress: {status.get('progress_percentage', 0)}%")
    
    if status['status'] in ['completed', 'failed']:
        break
    
    time.sleep(5)

# 4. Récupérer le modèle entraîné
if status['status'] == 'completed':
    model_info = requests.get(f"{BASE_URL}/models/{job_id}").json()
    print(f"Modèle: {model_info['model_name']}")
    print(f"Métriques: {model_info['metrics']}")
    
    # Télécharger le modèle
    model_file = requests.get(f"{BASE_URL}/models/{job_id}/download")
    with open(f"{job_id}_model.pkl", "wb") as f:
        f.write(model_file.content)
    print("Modèle téléchargé!")
```

## 🎯 Cas d'Usage

### 1. Entraînement Batch
Entraîner plusieurs modèles en parallèle pour comparer les performances.

### 2. Hyperparameter Tuning
Lancer plusieurs jobs avec différents hyperparamètres et comparer dans MLflow.

### 3. Production Pipeline
Intégrer dans un pipeline CI/CD pour réentraîner automatiquement les modèles.

### 4. Expérimentation Rapide
Tester rapidement différents algorithmes sur un nouveau dataset.

## 🐛 Débogage

### Logs
```bash
# Logs du conteneur
docker logs trainer -f

# Logs d'erreurs (dans le conteneur)
tail -f /app/logs/trainer_errors.log
```

### Problèmes Courants

**GPU non détecté** :
- Vérifier `nvidia-docker` installé
- Décommenter la section GPU dans `docker-compose.yml`
- Vérifier `CUDA_VISIBLE_DEVICES`

**MLflow non connecté** :
- Démarrer le service MLflow
- Vérifier `MLFLOW_TRACKING_URI`

**Dataset non trouvé** :
- Vérifier que le fichier existe dans MinIO bucket `data-preparer`
- Vérifier le chemin `data_id`

## 👥 Auteurs

Développé dans le cadre du projet **MicroLearn** - Plateforme AutoML Microservices.

## 📄 Licence

Ce projet fait partie de MicroLearn - Projet académique 5IIR.
