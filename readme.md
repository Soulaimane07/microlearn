🧠🚀 MicroLearn — Orchestrateur AutoML par microservices

Projet académique – Plateforme AutoML distribuée par microservices, développée en mode startup par une équipe de 4 personnes.
Objectif : automatiser et orchestrer le cycle complet de Machine Learning (préparation → sélection → entraînement → évaluation → déploiement) via API et dashboard web.

📘 Sommaire

🎯 Objectif du projet

🏗️ Architecture & Microservices

👥 Organisation de l’équipe

💡 User Stories

📁 Structure du projet

🧩 Technologies & Outils

⚙️ Installation & Exécution

🧪 Tests & Qualité

📅 Planning & Méthodologie Agile

🎓 Présentation finale

📞 Contacts encadrants

🎯 Objectif du projet

MicroLearn vise à automatiser le processus de Machine Learning grâce à une architecture microservices.
Chaque étape du cycle ML (de la préparation des données au déploiement du modèle) est encapsulée dans un microservice indépendant, communiquant via REST APIs et NATS (event bus).

Objectifs principaux :

Composer et exécuter des pipelines AutoML définis en YAML.

Sélectionner, entraîner, optimiser et évaluer automatiquement plusieurs modèles ML.

Fournir un dashboard React pour visualiser runs, métriques et modèles déployés.

Offrir une architecture scalable, reproductible et modulaire.

🏗️ Architecture & Microservices
🧩 Schéma global
DataPreparer → ModelSelector → Trainer → Evaluator → Deployer  
                      ↑                 ↓  
                 HyperOpt ← Orchestrator → Dashboard

Microservice	Stack principale	Description
DataPreparer	FastAPI + Pandas + PostgreSQL + MinIO	Upload et nettoyage des datasets
ModelSelector	Scikit-learn + PyCaret	Sélection automatique de modèles adaptés
Trainer	PyTorch Lightning + Ray + MLflow	Entraînement parallèle et suivi des runs
HyperOpt	Optuna + Redis + FastAPI	Optimisation des hyperparamètres
Evaluator	Scikit-learn + Plotly	Calcul et visualisation des métriques
Deployer	TorchServe + Flask + Docker	Déploiement des modèles via API REST
Orchestrator	Node.js + NATS + Redis	Exécution asynchrone de pipelines YAML
Dashboard	React + D3.js + Chart.js	Interface visuelle pour runs et métriques