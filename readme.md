![1154063f-43da-45d8-9c77-8e3c269fdee9](https://github.com/user-attachments/assets/dfaded76-2e6e-4270-b47d-a2fa1c05245b)# MicroLearn — Orchestrateur AutoML par microservices  

> **Projet académique** – Plateforme AutoML distribuée par microservices, développée en mode startup par une équipe de 4 personnes.  
> Objectif : automatiser et orchestrer le cycle complet de Machine Learning (préparation → sélection → entraînement → évaluation → déploiement) via API et dashboard web.  



---

Azure devops: https://dev.azure.com/SoulaimaneOuhmida/MicroLearn


---

## Lien Video
https://drive.google.com/file/d/16LNtocx52XeOrJTs5PAYD2aQ5muyvRnh/view?usp=drive_link

---
# Architecture
![Architecture](https://github.com/user-attachments/assets/ce749a4b-f5e0-4f43-a4d3-7c2c83044a55)


## 1. Orchestrator
- receives a pipeline definition (YAML/JSON),
- executes ML steps in order:
    - DataPreparer → ModelSelector → Trainer → Evaluator → HyperOpt → Deployer
- communicates asynchronously with microservices,
- tracks state and progress,
- exposes an API for execution & monitoring.

## 4. Evaluator
- Takes a trained model (or checkpoint)
- Runs evaluation on a validation/test dataset
- Computes metrics (AUC, F1, RMSE, Accuracy…)
- Generates plots (ROC curve, confusion matrix, error curves)
- Saves:
    - Metrics → PostgreSQL
    - Plots → MinIO





---
---
# How to run
## Infrastructure
```
cd infrastracture 
docker-compose up -d
```

## Micro7 - Orchestrator
```
cd services/micro7-orchestrator
npm start
```

## Micro1 - Data_preparer
```
cd services/micro1-data_preparer
venv\Scripts\activate     
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Micro2 - Model_selector
```
cd services/micro2-model_selector
venv\Scripts\activate     
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## Micro3 - Trainer
```
cd services/micro3-trainer
venv\Scripts\activate     
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```
