# 🤖 Phase 3 — Advanced Machine Learning Projects

10 ML projects that go beyond fit/predict. Real modelling challenges: imbalance, interpretability, novel features, and deployment-ready models.

---

## 1. 🎯 Customer Lifetime Value Predictor (Probabilistic)
**Difficulty:** ⭐⭐⭐⭐ | **Skills:** BG/NBD, Gamma-Gamma models, lifetimes lib, survival analysis

Predict how much a customer will be worth over their lifetime using probabilistic models (not just regression) — the technique used by e-commerce giants.

- **v1:** RFM segmentation
- **v2:** BG/NBD purchase-frequency model
- **v3:** Full CLV = frequency × monetary × survival, with cohort dashboards
- **Innovation:** Probabilistic CLV instead of naive averages
- **Resume line:** *"Modelled customer lifetime value using BG/NBD and Gamma-Gamma probabilistic models."*

---

## 2. 🩺 Medical Diagnosis with Uncertainty
**Difficulty:** ⭐⭐⭐⭐ | **Skills:** Bayesian deep learning, calibration, conformal prediction

A diagnosis model that says "I'm not sure — refer to a doctor" when uncertain. Calibrated probabilities + conformal prediction intervals.

- **v1:** Baseline classifier
- **v2:** Probability calibration (Platt/isotonic)
- **v3:** Conformal prediction — guaranteed coverage + abstention on uncertain cases
- **Innovation:** Model that knows what it doesn't know
- **Resume line:** *"Built a calibrated diagnosis model with conformal prediction for guaranteed uncertainty bounds."*

---

## 3. 🛒 Real-Time Recommendation Engine (Hybrid)
**Difficulty:** ⭐⭐⭐⭐ | **Skills:** matrix factorisation, deep learning, embeddings, FAISS

Combine collaborative filtering, content-based, and neural embeddings into one recommender with sub-100ms retrieval via FAISS.

- **v1:** Collaborative filtering (SVD)
- **v2:** Neural collaborative filtering + content hybrid
- **v3:** Two-tower model + FAISS approximate nearest neighbour for real-time
- **Innovation:** Two-tower architecture with vector search
- **Resume line:** *"Built a two-tower recommender with FAISS vector search delivering sub-100ms recommendations."*

---

## 4. 📉 Fraud Detection with Graph Neural Networks
**Difficulty:** ⭐⭐⭐⭐⭐ | **Skills:** PyTorch Geometric, GNNs, graph construction, imbalance

Catch fraud rings that traditional models miss by modelling transactions as a **graph** and using Graph Neural Networks.

- **v1:** Tabular fraud baseline
- **v2:** Build transaction graph + node features
- **v3:** GraphSAGE/GAT fraud-ring detection + explainability
- **Innovation:** Fraud *ring* detection (not just single transactions)
- **Resume line:** *"Detected fraud rings using Graph Neural Networks (GraphSAGE) on transaction graphs."*

---

## 5. 🎨 Neural Style Transfer Studio
**Difficulty:** ⭐⭐⭐ | **Skills:** CNNs, transfer learning, optimisation, PyTorch

Turn photos into art in any style. Build the classic optimisation-based version, then a fast feed-forward network for real-time transfer.

- **v1:** Gatys optimisation-based style transfer
- **v2:** Fast neural style transfer (feed-forward)
- **v3:** Multi-style network + video style transfer + web app
- **Innovation:** Real-time video style transfer
- **Resume line:** *"Implemented fast neural style transfer achieving real-time video stylisation."*

---

## 6. 🗣️ Speech Emotion Recognition
**Difficulty:** ⭐⭐⭐⭐ | **Skills:** librosa, CNNs/LSTMs, audio features, data augmentation

Detect emotion from voice tone (not words) — anger, joy, sadness, fear — using spectrograms + deep learning.

- **v1:** MFCC features + classic ML
- **v2:** Spectrogram CNN
- **v3:** CNN-LSTM hybrid + real-time mic inference + augmentation
- **Innovation:** Real-time emotion detection from live microphone
- **Resume line:** *"Built a real-time speech-emotion recogniser using CNN-LSTM on mel-spectrograms."*

---

## 7. ⚡ Energy Demand Forecasting (Multi-Horizon)
**Difficulty:** ⭐⭐⭐⭐ | **Skills:** time series, DeepAR, temporal fusion transformers, probabilistic forecasting

Forecast electricity demand hours-to-days ahead with prediction intervals — the technique power grids actually use.

- **v1:** Classical (SARIMA + XGBoost)
- **v2:** DeepAR probabilistic forecasting
- **v3:** Temporal Fusion Transformer + weather covariates + quantile forecasts
- **Innovation:** Probabilistic multi-horizon forecasts with attention
- **Resume line:** *"Forecast energy demand with Temporal Fusion Transformers producing calibrated quantile predictions."*

---

## 8. 🧠 AutoML From Scratch
**Difficulty:** ⭐⭐⭐⭐⭐ | **Skills:** hyperparameter optimisation, Bayesian optimisation, meta-learning

Build your own AutoML — automated feature engineering, model selection, and hyperparameter tuning via Bayesian optimisation.

- **v1:** Grid search wrapper
- **v2:** Bayesian optimisation (Optuna) + auto feature selection
- **v3:** Full pipeline search + automated feature engineering + ensembling
- **Innovation:** Automated feature engineering with genetic operators
- **Resume line:** *"Built an AutoML system with Bayesian hyperparameter search and automated feature engineering."*

---

## 9. 👁️ Object Detection for Indian Roads
**Difficulty:** ⭐⭐⭐⭐ | **Skills:** YOLO, custom training, annotation, edge deployment

Train YOLO to detect Indian-specific objects — autos, cycle-rickshaws, cattle, potholes — that Western models miss.

- **v1:** Pre-trained YOLO inference
- **v2:** Fine-tune on custom Indian road dataset
- **v3:** Pothole severity scoring + edge deployment (Raspberry Pi/mobile)
- **Innovation:** India-specific classes + severity estimation
- **Resume line:** *"Fine-tuned YOLOv8 for Indian road objects including pothole severity classification."*

---

## 10. 🎲 Reinforcement Learning Game Agent
**Difficulty:** ⭐⭐⭐⭐⭐ | **Skills:** RL, DQN, PPO, OpenAI Gym, reward shaping

Train an agent to master a game from scratch — start with CartPole, end with an agent that plays a custom game better than you.

- **v1:** DQN on CartPole
- **v2:** PPO on Atari/Lunar Lander
- **v3:** Custom environment + self-play agent + training dashboard
- **Innovation:** Self-play in a custom-built environment
- **Resume line:** *"Trained RL agents (DQN, PPO) and built a self-play system in a custom Gym environment."*

---

## 🎯 Phase 3 Challenge
Take any project here and **write a blog post explaining it**. Teaching forces mastery, and a technical blog is a portfolio multiplier.

---

*Course: [Data Science Mastery — PJ's Academy](https://pjsacademy.com)*
