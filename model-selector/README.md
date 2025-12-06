# 🤖 ModelSelector - Service de Sélection de Modèles ML

## 📋 Description

**ModelSelector** est un microservice de la plateforme MicroLearn qui analyse automatiquement les datasets et recommande les modèles de Machine Learning les plus adaptés. Il fait partie de l'architecture AutoML et permet aux utilisateurs de gagner du temps en identifiant les algorithmes optimaux pour leurs données.

## 🏗️ Architecture

```
model-selector/
├── app/
│   ├── main.py                 # Point d'entrée FastAPI
│   ├── api/
│   │   ├── health_router.py    # Endpoints de santé
│   │   ├── select_router.py    # Endpoints de sélection
│   │   └── models_router.py    # Endpoints catalogue modèles
│   ├── core/
│   │   ├── config.py           # Configuration
│   │   └── logger.py           # Logging
│   ├── models/
│   │   ├── request_models.py   # Modèles de requête Pydantic
│   │   └── response_models.py  # Modèles de réponse Pydantic
│   ├── services/
│   │   ├── dataset_analyzer.py # Analyse des datasets
│   │   ├── model_catalog.py    # Catalogue de 20+ modèles ML
│   │   └── model_selector.py   # Logique de sélection
│   └── storage/
│       ├── minio_client.py     # Client MinIO
│       └── postgres_client.py  # Client PostgreSQL
├── tests/
│   ├── test_select.py
│   └── test_catalog.py
├── Dockerfile
└── requirements.txt
```

## 🚀 Fonctionnalités

### 1. Analyse Automatique des Datasets
Le service analyse automatiquement vos données pour déterminer :
- **Type de tâche** : Classification, Régression ou Clustering
- **Caractéristiques** : Nombre de lignes, colonnes, types de données
- **Qualité des données** : Valeurs manquantes, déséquilibre des classes
- **Colonne cible** : Détection automatique de la variable à prédire

### 2. Catalogue de Modèles ML
Plus de **20 modèles** disponibles répartis en catégories :

| Catégorie | Modèles |
|-----------|---------|
| **Ensemble** | Random Forest, XGBoost, LightGBM |
| **Linéaire** | Logistic Regression, Linear Regression, Ridge, Lasso |
| **Arbre** | Decision Tree |
| **SVM** | SVC, SVR |
| **Instance** | K-Nearest Neighbors |
| **Probabiliste** | Naive Bayes |
| **Clustering** | K-Means, DBSCAN, Hierarchical |
| **Neural Network** | MLP Classifier, MLP Regressor |

### 3. Sélection Intelligente
L'algorithme de sélection prend en compte :
- Taille du dataset (petit, moyen, grand)
- Type de tâche ML
- Métrique d'optimisation souhaitée
- Complexité d'entraînement
- Interprétabilité requise

## 📡 API Endpoints

### Santé
```http
GET /health/
```
Vérifie que le service fonctionne.

**Réponse :**
```json
{
  "status": "ok",
  "service": "model-selector"
}
```

### Liste des Modèles
```http
GET /models/
```
Retourne le catalogue complet des modèles disponibles.

**Paramètres optionnels :**
- `task_type` : Filtrer par type (classification, regression, clustering)
- `category` : Filtrer par catégorie (ensemble, linear, tree, etc.)

### Sélection de Modèles (avec fichier)
```http
POST /select
```
Upload un fichier CSV et obtient des recommandations de modèles.

**Paramètres :**
| Paramètre | Type | Description |
|-----------|------|-------------|
| `file` | File | Fichier CSV à analyser |
| `metric` | string | Métrique d'optimisation (accuracy, f1, rmse, mae, r2) |
| `task_type` | string | Type de tâche (optionnel, auto-détecté) |
| `target_column` | string | Colonne cible (optionnel, auto-détecté) |
| `max_models` | int | Nombre max de modèles à retourner (défaut: 5) |

**Exemple avec cURL :**
```bash
curl -X POST "http://localhost:8001/select" \
  -F "file=@mon_dataset.csv" \
  -F "metric=accuracy" \
  -F "task_type=classification" \
  -F "target_column=target" \
  -F "max_models=5"
```

**Réponse :**
```json
{
  "dataset_analysis": {
    "n_rows": 1000,
    "n_columns": 10,
    "task_type": "classification",
    "target_column": "target",
    "n_classes": 3,
    "has_missing_values": false,
    "data_size_category": "medium",
    "warnings": [],
    "recommendations": []
  },
  "metric": "accuracy",
  "candidates": [
    {
      "model_id": "lightgbm_classifier",
      "model_name": "LightGBM Classifier",
      "model_class": "lightgbm.LGBMClassifier",
      "compatibility_score": 0.85,
      "ranking": 1,
      "default_params": {...},
      "tunable_params": {...}
    }
  ]
}
```

### Sélection via MinIO
```http
GET /select?minio_object=path/to/dataset.csv
```
Analyse un dataset déjà stocké dans MinIO.

## ⚙️ Configuration

Variables d'environnement :

| Variable | Description | Défaut |
|----------|-------------|--------|
| `SERVICE_NAME` | Nom du service | model-selector |
| `SERVICE_HOST` | Hôte d'écoute | 0.0.0.0 |
| `SERVICE_PORT` | Port d'écoute | 8001 |
| `POSTGRES_HOST` | Hôte PostgreSQL | postgres |
| `POSTGRES_PORT` | Port PostgreSQL | 5432 |
| `POSTGRES_USER` | Utilisateur DB | postgres |
| `POSTGRES_PASSWORD` | Mot de passe DB | postgres |
| `POSTGRES_DB` | Nom de la base | microlearn |
| `MINIO_ENDPOINT` | Endpoint MinIO | minio:9000 |
| `MINIO_ACCESS_KEY` | Clé d'accès MinIO | minioadmin |
| `MINIO_SECRET_KEY` | Clé secrète MinIO | minioadmin |

## 🐳 Lancement avec Docker

### Avec Docker Compose (recommandé)
```bash
cd microlearn
docker-compose up -d
```

Le service sera accessible sur : `http://localhost:8001`

### Documentation API Interactive
Accédez à Swagger UI : `http://localhost:8001/docs`

## 🔄 Flux de Travail

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Upload CSV    │────▶│  Dataset Analyzer │────▶│  Model Selector │
│   ou MinIO      │     │                  │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │                         │
                               ▼                         ▼
                        ┌──────────────┐         ┌──────────────┐
                        │  Détection   │         │  Scoring &   │
                        │  Task Type   │         │  Ranking     │
                        │  Target Col  │         │  des Modèles │
                        └──────────────┘         └──────────────┘
                                                        │
                                                        ▼
                                                 ┌──────────────┐
                                                 │  Top N       │
                                                 │  Candidats   │
                                                 └──────────────┘
```

## 📊 Algorithme de Scoring

Le score de compatibilité (0-1) est calculé selon :

1. **Compatibilité de taille** (30%)
   - Petit dataset → Modèles simples (Decision Tree, KNN)
   - Grand dataset → Modèles robustes (XGBoost, LightGBM)

2. **Compatibilité de tâche** (40%)
   - Le modèle doit supporter le type de tâche détecté

3. **Gestion des données** (20%)
   - Valeurs manquantes
   - Variables catégorielles
   - Besoin de normalisation

4. **Complexité** (10%)
   - Trade-off entre performance et temps d'entraînement

## 🧪 Tests

```bash
# Lancer les tests
cd model-selector
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=app
```

## 📚 Dépendances Principales

- **FastAPI** : Framework API REST
- **Pandas** : Manipulation de données
- **NumPy** : Calculs numériques
- **scikit-learn** : Modèles ML de base
- **XGBoost** : Gradient Boosting
- **LightGBM** : Fast Gradient Boosting
- **Pydantic** : Validation de données
- **psycopg2** : Driver PostgreSQL
- **minio** : Client MinIO

## 🔗 Intégration avec MicroLearn

ModelSelector s'intègre avec les autres microservices :

1. **DataPreparer** (port 8000) : Prépare les données avant analyse
2. **ModelSelector** (port 8001) : Sélectionne les modèles ← *Vous êtes ici*
3. **HyperparameterTuner** (à venir) : Optimise les hyperparamètres
4. **ModelTrainer** (à venir) : Entraîne les modèles sélectionnés

## 📝 Exemple Complet

```python
import requests

# 1. Vérifier la santé du service
response = requests.get("http://localhost:8001/health/")
print(response.json())  # {"status": "ok", "service": "model-selector"}

# 2. Lister les modèles disponibles
response = requests.get("http://localhost:8001/models/")
models = response.json()["models"]
print(f"Nombre de modèles: {len(models)}")

# 3. Sélectionner des modèles pour un dataset
with open("mon_dataset.csv", "rb") as f:
    response = requests.post(
        "http://localhost:8001/select",
        files={"file": f},
        data={
            "metric": "accuracy",
            "max_models": 3
        }
    )

result = response.json()
print(f"Task Type: {result['dataset_analysis']['task_type']}")
print("Modèles recommandés:")
for candidate in result["candidates"]:
    print(f"  {candidate['ranking']}. {candidate['model_name']} "
          f"(score: {candidate['compatibility_score']:.2f})")
```

## 👥 Auteurs

Développé dans le cadre du projet **MicroLearn** - Plateforme AutoML Microservices.

## 📄 Licence

Ce projet fait partie de MicroLearn - Projet académique 5IIR.
