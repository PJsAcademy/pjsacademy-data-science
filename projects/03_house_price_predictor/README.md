# 🏠 Project 03 — House Price Predictor

**Phase 4 — ML Engineering** | Intermediate

---

## 🎯 What You'll Build
Predict house prices using real estate data — a classic ML regression project used in interviews.

## 🛠️ Skills Practiced
- Feature Engineering — creating new features
- Linear Regression & XGBoost
- Model Evaluation — RMSE, R²
- sklearn Pipelines

## 📦 Dataset
**California Housing Dataset** (built into sklearn — no download needed!)

## 🚀 Steps
1. Load dataset
2. Explore and visualise
3. Feature engineering
4. Train Linear Regression baseline
5. Train XGBoost
6. Compare and evaluate

## 💻 Code
```python
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb

# Load
data = fetch_california_housing(as_frame=True)
df = data.frame

# Feature engineering
df['rooms_per_household'] = df['AveRooms'] / df['HouseAge']
df['bedrooms_per_room'] = df['AveBedrms'] / df['AveRooms']

# Split
X = df.drop('MedHouseVal', axis=1)
y = df['MedHouseVal']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Baseline
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_test)
print(f"Linear R²: {r2_score(y_test, lr_pred):.3f}")

# XGBoost
xgb_model = xgb.XGBRegressor(n_estimators=200, learning_rate=0.05)
xgb_model.fit(X_train, y_train)
xgb_pred = xgb_model.predict(X_test)
print(f"XGBoost R²: {r2_score(y_test, xgb_pred):.3f}")
print(f"XGBoost RMSE: {np.sqrt(mean_squared_error(y_test, xgb_pred)):.3f}")
```

## 📈 What You'll Learn
- Feature engineering impact on model performance
- Why XGBoost beats Linear Regression on tabular data
- How to evaluate regression models properly

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
