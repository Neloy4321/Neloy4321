# Machine Learning Engineering Case Study
### End-to-End Sleep Health Prediction System

**Domain:** Applied ML and deployment-oriented software engineering  
**Core tools:** Python · pandas · scikit-learn · FastAPI · MongoDB · Docker · AWS EC2/ECR · GitHub Actions  
**Source:** [End-to-End ML Project](https://github.com/Neloy4321/END-to-END-ML-Project)

---

## The problem

A survey-driven ML system needs consistent data processing between **model training** and **inference**. Sleep and lifestyle fields can be heterogeneous: demographics, bed and wake times, sleep duration, breathing symptoms and medical-history categories. The challenge is to organize them into a repeatable ML workflow with clear application boundaries.

## System architecture

```text
Dataset acquisition
       |
Validation & transformation
       |
Feature engineering / encoding
       |
Model training & evaluation
       |
Versioned prediction pipeline
       |
FastAPI prediction service
       |
Containerized application
       |
GitHub Actions → AWS ECR → EC2
```

The repository documents both the ML stages and its application/deployment workflow. This overview represents its **documented architecture**; it does not claim that a live public endpoint is presently operating.

## Implementation layers

| Layer | What's demonstrated |
| :--- | :--- |
| Data pipeline | Ingestion, validation, transformation and feature preparation |
| ML pipeline | Training, evaluation and prediction structure |
| Service | FastAPI application and HTML interface |
| Data integration | MongoDB integration |
| Delivery | Dockerfile, GitHub Actions workflow and AWS EC2/ECR deployment steps |

**Example outcome classes in the repository:** No Condition, Sleep Respiratory Disorders, Health Issues, Mental Health Issues and Others.

## What matters to an engineering reviewer

1. **Training/inference consistency:** new records should go through the same preparation logic used for the model.
2. **Separation of concerns:** model code, configuration, services and delivery mechanisms should be inspectable independently.
3. **Operational reproducibility:** dependencies, environment variables, containers and workflow files make the application easier to reason about.
4. **Safety and scope:** the application is a **research/software project**, not a medical device or clinically validated diagnostic system.

No externally verified clinical accuracy, production uptime or live URL is claimed here.

## Evidence & implementation

- [ML repository README](https://github.com/Neloy4321/END-to-END-ML-Project)
- [Training and prediction components](https://github.com/Neloy4321/END-to-END-ML-Project/tree/main/sleep_project)
- [GitHub Actions workflow](https://github.com/Neloy4321/END-to-END-ML-Project/tree/main/.github/workflows)
- [Dockerfile](https://github.com/Neloy4321/END-to-END-ML-Project/blob/main/Dockerfile)

---

[← Profile](../../README.md) · [All public projects](../PROJECT_ATLAS.md) · [Networking case study](./NETWORK_ARCHITECTURE.md)
