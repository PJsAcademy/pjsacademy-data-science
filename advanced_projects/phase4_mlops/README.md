# 🏭 Phase 4 — Advanced ML Engineering / MLOps Projects

10 projects that separate data scientists from ML *engineers*. These are about scale, reliability, deployment, and production systems.

---

## 1. 🔄 Full MLOps Platform (Mini)
**Difficulty:** ⭐⭐⭐⭐⭐ | **Skills:** MLflow, Airflow, Docker, FastAPI, CI/CD

Build a complete ML platform — data ingestion → training → registry → serving → monitoring — all orchestrated and containerised.

- **v1:** Training pipeline + MLflow tracking
- **v2:** Airflow orchestration + model registry + auto-retrain
- **v3:** Full platform — serving API, monitoring, drift alerts, CI/CD via GitHub Actions
- **Innovation:** End-to-end automated retraining triggered by drift
- **Resume line:** *"Built a mini MLOps platform with Airflow orchestration, MLflow registry, and drift-triggered retraining."*

---

## 2. 📡 Real-Time ML Feature Store
**Difficulty:** ⭐⭐⭐⭐⭐ | **Skills:** Feast, Redis, streaming, feature engineering

A feature store serving features to models in real time — the backbone of production ML at scale.

- **v1:** Offline feature store (batch)
- **v2:** Online store with Redis for low-latency serving
- **v3:** Streaming feature computation + point-in-time correctness
- **Innovation:** Point-in-time-correct feature joins (no data leakage)
- **Resume line:** *"Built a real-time feature store with Redis serving and point-in-time-correct feature retrieval."*

---

## 3. 🎯 A/B Testing & Experimentation Platform
**Difficulty:** ⭐⭐⭐⭐ | **Skills:** statistics, bandits, causal inference, dashboards

A platform to run ML model experiments — statistical significance, multi-armed bandits, and guardrail metrics.

- **v1:** Classic A/B test calculator + power analysis
- **v2:** Multi-armed bandit allocation (Thompson sampling)
- **v3:** Full experimentation dashboard + CUPED variance reduction + auto-decisions
- **Innovation:** CUPED for faster, more sensitive experiments
- **Resume line:** *"Built an experimentation platform with Thompson-sampling bandits and CUPED variance reduction."*

---

## 4. 🚀 Model Serving at Scale (Load Testing)
**Difficulty:** ⭐⭐⭐⭐ | **Skills:** TorchServe/Triton, gRPC, batching, load testing, k8s

Serve a model that handles thousands of requests/second — dynamic batching, GPU utilisation, and horizontal scaling.

- **v1:** FastAPI single-model serving
- **v2:** Dynamic batching + gRPC + quantisation
- **v3:** Triton Inference Server + Kubernetes autoscaling + load test to 10K RPS
- **Innovation:** Dynamic request batching for GPU efficiency
- **Resume line:** *"Deployed a model serving 10K RPS with Triton dynamic batching and Kubernetes autoscaling."*

---

## 5. 🔍 ML Monitoring & Observability System
**Difficulty:** ⭐⭐⭐⭐ | **Skills:** Evidently, Prometheus, Grafana, drift detection

Monitor models in production — data drift, concept drift, prediction drift, and performance decay — with alerting.

- **v1:** Batch drift reports (Evidently)
- **v2:** Real-time metrics → Prometheus + Grafana dashboards
- **v3:** Automated alerting + root-cause analysis + auto-retrain triggers
- **Innovation:** Drift root-cause attribution (which feature broke?)
- **Resume line:** *"Built ML observability with drift detection, Grafana dashboards, and root-cause attribution."*

---

## 6. 🧊 Data Pipeline Orchestration (Batch + Stream)
**Difficulty:** ⭐⭐⭐⭐ | **Skills:** Airflow, Kafka, Spark, data quality

Build robust data pipelines — batch ETL with Airflow + streaming with Kafka — with data-quality checks at every stage.

- **v1:** Airflow batch ETL DAG
- **v2:** Kafka streaming ingestion + Spark processing
- **v3:** Lambda architecture (batch + speed layer) + Great Expectations quality gates
- **Innovation:** Data-quality gates that halt bad data before it reaches models
- **Resume line:** *"Built a Lambda-architecture pipeline with Kafka streaming and Great Expectations quality gates."*

---

## 7. 🐳 Containerised ML Microservices
**Difficulty:** ⭐⭐⭐⭐ | **Skills:** Docker, Kubernetes, service mesh, API gateway

Decompose an ML app into microservices — preprocessing, inference, post-processing — each independently scalable.

- **v1:** Dockerise a single model service
- **v2:** Multi-service architecture + API gateway
- **v3:** Kubernetes deployment + service mesh + canary releases
- **Innovation:** Canary deployment for safe model rollouts
- **Resume line:** *"Architected ML microservices on Kubernetes with canary deployments for zero-downtime model updates."*

---

## 8. ⚙️ Automated Model Compression Pipeline
**Difficulty:** ⭐⭐⭐⭐⭐ | **Skills:** quantisation, pruning, distillation, ONNX

Shrink big models to run on phones/edge — quantisation, pruning, and knowledge distillation, automatically.

- **v1:** Post-training quantisation
- **v2:** Structured pruning + fine-tuning
- **v3:** Knowledge distillation + ONNX export + edge benchmarking
- **Innovation:** Automated compression that hits a target latency budget
- **Resume line:** *"Built a model-compression pipeline (quantise + prune + distill) cutting size 10x for edge deployment."*

---

## 9. 🔐 Privacy-Preserving ML (Federated)
**Difficulty:** ⭐⭐⭐⭐⭐ | **Skills:** federated learning, differential privacy, Flower

Train models on data that never leaves users' devices — federated learning with differential privacy guarantees.

- **v1:** Federated averaging simulation
- **v2:** Real federated setup (Flower) across clients
- **v3:** Differential privacy + secure aggregation + non-IID handling
- **Innovation:** Privacy-guaranteed training without centralising data
- **Resume line:** *"Implemented federated learning with differential privacy for training without centralising user data."*

---

## 10. 📦 LLM Deployment & Optimization Stack
**Difficulty:** ⭐⭐⭐⭐⭐ | **Skills:** vLLM, quantisation, KV-cache, streaming, cost optimisation

Deploy an open LLM (Llama/Mistral) efficiently — batched inference, quantisation, streaming, and cost tracking.

- **v1:** Basic LLM serving with transformers
- **v2:** vLLM with continuous batching + streaming responses
- **v3:** Quantised (GPTQ/AWQ) + KV-cache optimisation + cost-per-token dashboard
- **Innovation:** Continuous batching for 20x throughput on LLM serving
- **Resume line:** *"Deployed a quantised LLM with vLLM continuous batching achieving 20x throughput at 4x lower cost."*

---

## 🎯 Phase 4 Challenge
Take a Phase 3 model and **actually deploy it** — real URL, real monitoring, real load test. A deployed model beats 10 notebooks.

---

*Course: [Data Science Mastery — PJ's Academy](https://pjsacademy.com)*
