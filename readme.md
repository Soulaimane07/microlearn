# MicroLearn — Orchestrateur AutoML par microservices  

> **Projet académique** – Plateforme AutoML distribuée par microservices, développée en mode startup par une équipe de 4 personnes.  
> Objectif : automatiser et orchestrer le cycle complet de Machine Learning (préparation → sélection → entraînement → évaluation → déploiement) via API et dashboard web.  

---

Azure devops: https://dev.azure.com/SoulaimaneOuhmida/MicroLearn

---

## 📘 Sommaire

1. [🎯 Objectif du projet](#-objectif-du-projet)  
2. [🏗️ Architecture & Microservices](#️-architecture--microservices)  
3. [👥 Organisation de l’équipe](#-organisation-de-léquipe)  
4. [💡 User Stories](#-user-stories)  
5. [📁 Structure du projet](#-structure-du-projet)  
6. [🧩 Technologies & Outils](#-technologies--outils)  
7. [⚙️ Installation & Exécution](#️-installation--exécution)  
8. [🧪 Tests & Qualité](#-tests--qualité)  
9. [📅 Planning & Méthodologie Agile](#-planning--méthodologie-agile)  
10. [🎓 Présentation finale](#-présentation-finale)  
11. [📞 Contacts encadrants](#-contacts-encadrants)

---

## 🎯 Objectif du projet

**MicroLearn** vise à automatiser le processus de Machine Learning grâce à une **architecture microservices**.  
Chaque étape du cycle ML (de la préparation des données au déploiement du modèle) est encapsulée dans un microservice indépendant, communiquant via **REST APIs** et **NATS (event bus)**.  

### Objectifs principaux :
- Composer et exécuter des pipelines AutoML définis en YAML.  
- Sélectionner, entraîner, optimiser et évaluer automatiquement plusieurs modèles ML.  
- Fournir un **dashboard React** pour visualiser runs, métriques et modèles déployés.  
- Offrir une architecture **scalable, reproductible et modulaire**.  

---

## 🏗️ Architecture & Microservices

### 🧩 Schéma global  
```
DataPreparer → ModelSelector → Trainer → Evaluator → Deployer  
                      ↑                 ↓  
                 HyperOpt ← Orchestrator → Dashboard
```

| Microservice | Stack principale | Description |
|---------------|------------------|--------------|
| **DataPreparer** | FastAPI + Pandas + PostgreSQL + MinIO | Upload et nettoyage des datasets |
| **ModelSelector** | Scikit-learn + PyCaret | Sélection automatique de modèles adaptés |
| **Trainer** | PyTorch Lightning + Ray + MLflow | Entraînement parallèle et suivi des runs |
| **HyperOpt** | Optuna + Redis + FastAPI | Optimisation des hyperparamètres |
| **Evaluator** | Scikit-learn + Plotly | Calcul et visualisation des métriques |
| **Deployer** | TorchServe + Flask + Docker | Déploiement des modèles via API REST |
| **Orchestrator** | Node.js + NATS + Redis | Exécution asynchrone de pipelines YAML |
| **Dashboard** | React + D3.js + Chart.js | Interface visuelle pour runs et métriques |

---

<!-- ## 👥 Organisation de l’équipe

| Rôle | Nom | Responsabilités principales |
|------|------|-----------------------------|
| **Tech Lead / Architecte** | Personne A | Architecture microservices, orchestrateur, API Gateway, CI/CD |
| **Data & ML Engineer** | Personne B | ModelSelector, Trainer, HyperOpt, MLflow |
| **Full-Stack & DevOps** | Personne C | Dashboard React, Docker, MinIO, PostgreSQL |
| **MLOps & QA / Documentation** | Personne D | Tests, Postman, SonarQube, Selenium, documentation, Trello |

Chaque membre livre un microservice **fonctionnel avec API, tests et documentation**. -->

---

<!-- ## 💡 User Stories

| ID | User Story |
|----|-------------|
| **US01** | En tant que Data Scientist, je veux uploader un dataset et nettoyer les données. |
| **US02** | Je veux définir un pipeline de preprocessing via YAML. |
| **US03** | Je veux obtenir une liste de modèles automatiquement sélectionnés. |
| **US04** | Je veux entraîner plusieurs modèles en parallèle. |
| **US05** | Je veux optimiser les hyperparamètres automatiquement. |
| **US06** | Je veux comparer les performances des modèles. |
| **US07** | Je veux déployer le meilleur modèle via API. |
| **US08** | Je veux visualiser les métriques et rapports sur le dashboard. | 

--- -->

<!-- ## 📁 Structure du projet

```
📦 MicroLearn/
 ┣ 📁 services/
 ┃ ┣ 📁 data-preparer/
 ┃ ┣ 📁 model-selector/
 ┃ ┣ 📁 trainer/
 ┃ ┣ 📁 evaluator/
 ┃ ┣ 📁 hyperopt/
 ┃ ┣ 📁 deployer/
 ┣ 📁 orchestrator/
 ┣ 📁 dashboard/
 ┣ 📁 docs/
 ┣ 📜 docker-compose.yml
 ┣ 📜 README.md
```

--- -->

## 🧩 Technologies & Outils

| Catégorie | Outils / Technologies |
|------------|------------------------|
| **Langages** | Python, Node.js, React |
| **Bases de données** | PostgreSQL, Redis |
| **Stockage fichiers** | MinIO |
| **ML & AutoML** | PyCaret, PyTorch Lightning, Optuna, MLflow |
| **Orchestration** | NATS, Ray |
| **Containerisation** | Docker, docker-compose |
| **CI/CD** | GitHub Actions |
| **Tests** | Pytest, Postman/Newman, Selenium |
| **Docs & Tracking** | Swagger, SonarQube, Grafana (optionnel) |
| **Gestion projet** | Trello + Notion (optionnel) |

---

<!-- ## ⚙️ Installation & Exécution

### 1️⃣ Cloner le projet
```bash
git clone https://github.com/<user>/MicroLearn.git
cd MicroLearn
```

### 2️⃣ Lancer les services
```bash
docker-compose up --build
```

### 3️⃣ Accéder aux composants
| Service | URL |
|----------|-----|
| Dashboard | http://localhost:3000 |
| Orchestrator API | http://localhost:8080 |
| MLflow | http://localhost:5000 |
| MinIO | http://localhost:9000 |

--- -->

## 🧪 Tests & Qualité

- **Unit tests** : `pytest` (Python) / `jest` (Node.js)  
- **Integration tests** : via `docker-compose`  
- **API tests** : Postman collection + Newman  
- **End-to-end** : Selenium (UI)  
- **Coverage attendu** : ≥ 60%  
- **Lint & QA** : SonarQube, GitHub Actions CI  

---

## 📅 Planning & Méthodologie Agile

| Sprint | Durée | Objectif |
|---------|--------|-----------|
| **Sprint 1** | 1 semaine | Setup Git, Docker, Trello, base architecture |
| **Sprint 2** | 2 semaines | DataPreparer + ModelSelector + HyperOpt |
| **Sprint 3** | 2 semaines | Trainer + Evaluator |
| **Sprint 4** | 1 semaine | Deployer + Dashboard |
| **Sprint 5** | 1 semaine | Tests, rapport final, présentation |

### Trello structure :
- Stories  
- À faire  
- En cours  
- Tests  
- Terminé  
- Validé (par prof) ✅  

👨‍🏫 **Partage du tableau avec** :  
- O.ouedrhiri@emsi.ma  
- H.Tabbaa@emsi.ma  
- lachgar.m@gmail.com  

---

## 🎓 Présentation finale

### Livrables
- Repos GitHub + Dockerfiles  
- Docs techniques + Swagger/OpenAPI  
- Rapport PDF (5–10 pages)  
- Démo vidéo (5 min)  
- Slides de soutenance  

### Points clés à démontrer :
- Architecture microservices  
- Pipeline ML automatisé  
- API documentées  
- Dashboard visuel  
- Logs & suivi MLflow  
- Déploiement fonctionnel  

## 📞 Contacts encadrants

| Nom | Email |
|------|--------|
| **O. Ouedrhiri** | O.ouedrhiri@emsi.ma |
| **H. Tabbaa** | H.Tabbaa@emsi.ma |
| **M. Lachgar** | lachgar.m@gmail.com |







✅ 4 Microservices Architecture (Backend-Only)

Each microservice is independent, containerized, and stateless.

1️⃣ Dataset Manager Service

Purpose: Handle datasets lifecycle
Tech: Python (FastAPI) or Node.js
Responsibilities:

Upload CSV/Parquet files

Validate schema

Store dataset metadata (PostgreSQL or MongoDB)

Provide dataset samples/preprocessing preview

Serve datasets to the Trainer service

Core Endpoints:

POST /datasets — Upload dataset

GET /datasets/{id} — Get dataset metadata

GET /datasets/{id}/sample — Return sample rows

DELETE /datasets/{id} — Remove dataset

2️⃣ Feature & Model Selector Service

Purpose: Automatically select model type + basic preprocessing
Tech: Python (FastAPI), scikit-learn
Responsibilities:

Detect problem type (classification, regression)

Propose candidate models (RandomForest, XGBoost, MLP…)

Handle auto-feature-engineering

Return a list of models + suggested hyperparameters

Cache model suggestions

Core Endpoints:

POST /select-model — Input dataset schema → Output candidate models

GET /models/{id} — Retrieve selected models

3️⃣ Trainer Service

Purpose: Train models + evaluate them
Tech: Python (FastAPI), PyTorch Lightning, MLflow
Responsibilities:

Receive model type + dataset

Train model

Track metrics (accuracy, RMSE, F1…)

Log experiments via MLflow

Save best model to storage (S3/Azure Blob/MinIO)

Stream training logs

Core Endpoints:

POST /train — Launch training job

GET /train/{jobId}/status — Job status (QUEUED / RUNNING / DONE)

GET /train/{jobId}/metrics — Retrieve metrics

POST /train/{jobId}/stop — Stop training

4️⃣ Hyperparameter Optimization (AutoML) Service

Purpose: Run Optuna or Hyperopt to optimize hyperparameters
Tech: Python + Optuna
Responsibilities:

Launch optimization loop

Try N models in parallel

Choose best hyperparameters

Return best model configuration

Communicate with Trainer service for each trial

Core Endpoints:

POST /optimize — Start HPO session

GET /optimize/{sessionId}/status

GET /optimize/{sessionId}/best