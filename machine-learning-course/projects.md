# 🛠️ Machine Learning — 15 Hands-On Projects

Portfolio-worthy projects, ordered from beginner to advanced. Each lists what you build, the modules it uses, the dataset, and a resume line. Every dataset is free/public.

---

## Beginner (Modules 1–4)

### 1. House Price Predictor ⭐
**Build:** Predict house prices with linear → Ridge regression.
**Data:** California Housing (in sklearn). **Uses:** M2, M3.
**Steps:** EDA → engineer features → baseline linear → Ridge with tuned alpha → residual analysis.
**Resume:** *"Built a regularized regression model predicting house prices with engineered features, cutting RMSE 18%."*

### 2. Titanic Survival Classifier ⭐
**Build:** Predict who survived. **Data:** Titanic (Kaggle). **Uses:** M2, M4.
**Steps:** impute missing → encode → logistic regression → decision tree → compare F1.
**Resume:** *"Classified survival with logistic regression and decision trees, handling missing data and categorical encoding."*

### 3. Iris / Wine Multi-class Classifier ⭐
**Build:** Classify flower/wine types. **Data:** Iris, Wine (sklearn). **Uses:** M4, M6.
**Steps:** kNN vs logistic → confusion matrix → cross-validation.
**Resume:** *"Built a multi-class classifier with cross-validated model selection."*

### 4. Student Score Predictor ⭐
**Build:** Predict exam scores from study hours/attendance. **Uses:** M3.
**Steps:** simple + multiple regression → interpret coefficients.
**Resume:** *"Modelled academic performance and quantified each factor's impact via regression coefficients."*

---

## Intermediate (Modules 5–7)

### 5. Customer Churn Predictor ⭐⭐
**Build:** Predict telecom churn. **Data:** Telco Churn (Kaggle). **Uses:** M4, M5, M6.
**Steps:** logistic baseline → XGBoost → threshold tuning for business cost → SHAP.
**Resume:** *"Built an XGBoost churn model with business-tuned thresholds and SHAP explainability."*

### 6. Credit Card Fraud Detection ⭐⭐
**Build:** Detect fraud on imbalanced data. **Data:** Kaggle creditcard. **Uses:** M4, M5, M6.
**Steps:** handle imbalance (class_weight/SMOTE) → XGBoost → PR-AUC → cost analysis.
**Resume:** *"Detected fraud on 284K imbalanced transactions using SMOTE + XGBoost, optimizing PR-AUC."*

### 7. Loan Default Risk Model ⭐⭐
**Build:** Predict loan defaults. **Uses:** M2, M5, M6.
**Steps:** feature engineering → ensemble → calibration → explainability for approval decisions.
**Resume:** *"Built a calibrated credit-risk model with explainable approve/deny decisions."*

### 8. Customer Segmentation ⭐⭐
**Build:** Segment customers with K-Means. **Data:** Mall Customers. **Uses:** M7.
**Steps:** RFM features → elbow method → profile segments → marketing action per segment.
**Resume:** *"Segmented customers via K-Means on RFM features, driving targeted marketing strategies."*

### 9. Sales Forecasting ⭐⭐⭐
**Build:** Forecast retail sales. **Data:** Rossmann/Walmart. **Uses:** M2, M5, M6.
**Steps:** lag & date features → time-series split → XGBoost → MAPE evaluation.
**Resume:** *"Forecast store sales with lag-feature engineering and time-series-validated XGBoost."*

---

## Advanced (Modules 8–10)

### 10. Handwritten Digit Recognizer ⭐⭐⭐
**Build:** Classify digits with a neural net. **Data:** MNIST. **Uses:** M9.
**Steps:** neural net in Keras → >97% accuracy → compare vs Random Forest.
**Resume:** *"Built a neural network achieving 98% accuracy on MNIST digit classification."*

### 11. Movie Recommendation System ⭐⭐⭐
**Build:** Recommend movies. **Data:** MovieLens. **Uses:** M7, M8.
**Steps:** content-based (TF-IDF + cosine) → collaborative filtering (SVD) → hybrid.
**Resume:** *"Built a hybrid recommender combining content-based and collaborative filtering."*

### 12. Image Classifier (CNN) ⭐⭐⭐⭐
**Build:** Classify images. **Data:** CIFAR-10. **Uses:** M9.
**Steps:** CNN from scratch → data augmentation → transfer learning (ResNet).
**Resume:** *"Trained a CNN + transfer learning for image classification, reaching 90%+ accuracy."*

### 13. AutoML Tuning Pipeline ⭐⭐⭐⭐
**Build:** Automated model+hyperparameter search. **Uses:** M6, M8.
**Steps:** compare 5 models → Optuna Bayesian tuning → stacking ensemble → leaderboard.
**Resume:** *"Built an AutoML pipeline with Bayesian tuning and stacking, automating model selection."*

### 14. End-to-End Deployed Model ⭐⭐⭐⭐ (Capstone)
**Build:** Take any model to production. **Uses:** M8, M10.
**Steps:** pipeline → joblib → FastAPI → Docker → monitoring script → retraining plan → MLflow tracking.
**Resume:** *"Deployed an ML model as a FastAPI + Docker service with drift monitoring and MLflow tracking."*

### 15. Kaggle Competition Entry ⭐⭐⭐⭐⭐
**Build:** Enter a live Kaggle competition end-to-end. **Uses:** everything.
**Steps:** EDA → feature engineering → CV strategy → ensemble → leaderboard submission.
**Resume:** *"Competed on Kaggle, applying feature engineering, cross-validation, and ensembling end-to-end."*

---

## 🎯 Portfolio Advice
- Put **#5, #6, #12, #14** on GitHub + your resume — churn, fraud, CNNs, and a *deployed* model are exactly what employers screen for.
- Write a short README per project explaining your **decisions** (why this model, this metric, this threshold) — that reasoning proves mastery more than the score.
- One **deployed** model (#14) beats ten notebooks.

---

*🤖 Machine Learning Mastery — [PJ's Academy](https://pjsacademy.com) · hello@pjsacademy.com*
