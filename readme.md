# MicroLearn — Orchestrateur AutoML par microservices  

> **Projet académique** – Plateforme AutoML distribuée par microservices, développée en mode startup par une équipe de 4 personnes.  
> Objectif : automatiser et orchestrer le cycle complet de Machine Learning (préparation → sélection → entraînement → évaluation → déploiement) via API et dashboard web.  

---

Azure devops: https://dev.azure.com/SoulaimaneOuhmida/MicroLearn


---
---
# Architecture
![Architecture](./Files//architecture.png)

## 1. Orchestrator
- receives a pipeline definition (YAML/JSON),
- executes ML steps in order:
    - DataPreparer → ModelSelector → Trainer → Evaluator → HyperOpt → Deployer
- communicates asynchronously with microservices,
- tracks state and progress,
- exposes an API for execution & monitoring.




---
---
# How to run
## Infrastructure
```
cd infrastracture 
docker-compose up -d
```
