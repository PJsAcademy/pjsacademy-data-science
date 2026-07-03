# 🏠 Project 03 — House Price Predictor

**Phase 4 — ML Engineering** | Beginner → Advanced (3 Versions)

---

## 🗺️ Version Roadmap

| Version | What You Build | Complexity |
|---------|---------------|------------|
| v1.0 — Starter | Linear Regression vs XGBoost baseline | ⭐ Beginner |
| v2.0 — Improved | Feature engineering + hyperparameter tuning + SHAP | ⭐⭐ Intermediate |
| v3.0 — Production | AutoML + cross-validation + FastAPI deployment | ⭐⭐⭐ Advanced |

---

## 📦 Dataset
**California Housing Dataset** — built into sklearn, no download needed

---

## 🟢 v1.0 — Baseline Models

**Skills:** Linear Regression, XGBoost, train/test split, R², RMSE

```python
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb

data = fetch_california_housing(as_frame=True)
df = data.frame

X = df.drop('MedHouseVal', axis=1)
y = df['MedHouseVal']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Baseline — Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_test)

# XGBoost
xgb_model = xgb.XGBRegressor(n_estimators=200, learning_rate=0.05, random_state=42)
xgb_model.fit(X_train, y_train)
xgb_pred = xgb_model.predict(X_test)

print(f"Linear R²:   {r2_score(y_test, lr_pred):.3f}")
print(f"Linear RMSE: {np.sqrt(mean_squared_error(y_test, lr_pred)):.3f}")
print(f"XGBoost R²:   {r2_score(y_test, xgb_pred):.3f}")
print(f"XGBoost RMSE: {np.sqrt(mean_squared_error(y_test, xgb_pred)):.3f}")
```

**What v1 teaches:** Why XGBoost almost always beats Linear Regression on tabular data — and what R² actually means.

---

## 🟡 v2.0 — Feature Engineering + SHAP Explainability

**New in v2:** 8 new engineered features, hyperparameter tuning, SHAP waterfall plots, residual analysis

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import xgboost as xgb

data = fetch_california_housing(as_frame=True)
df = data.frame

# --- Feature Engineering ---
df['rooms_per_person']    = df['AveRooms'] / df['AveOccup']
df['bedrooms_per_room']   = df['AveBedrms'] / df['AveRooms']
df['income_per_room']     = df['MedInc'] / df['AveRooms']
df['population_density']  = df['Population'] / df['AveOccup']
df['income_squared']      = df['MedInc'] ** 2
df['age_income']          = df['HouseAge'] * df['MedInc']
# Proximity to coast (simple lat/lon features)
df['lat_lon']             = df['Latitude'] * df['Longitude']
df['coord_dist']          = np.sqrt(df['Latitude']**2 + df['Longitude']**2)

print(f"Features: {df.shape[1] - 1} (was 8, now {df.shape[1] - 1})")

X = df.drop('MedHouseVal', axis=1)
y = df['MedHouseVal']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Tuned XGBoost ---
model = xgb.XGBRegressor(
    n_estimators=500,
    learning_rate=0.03,
    max_depth=7,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=1.0,
    random_state=42
)
model.fit(X_train, y_train, eval_set=[(X_test, y_test)],
          verbose=False)

pred = model.predict(X_test)
r2   = r2_score(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))
mae  = mean_absolute_error(y_test, pred)
cv   = cross_val_score(model, X, y, cv=5, scoring='r2')

print(f"\nR²:    {r2:.4f}")
print(f"RMSE:  {rmse:.4f}")
print(f"MAE:   {mae:.4f}")
print(f"CV R² (5-fold): {cv.mean():.4f} ± {cv.std():.4f}")

# --- Residual Analysis ---
residuals = y_test - pred
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].scatter(pred, residuals, alpha=0.3, color='steelblue')
axes[0].axhline(0, color='red', linestyle='--')
axes[0].set_xlabel('Predicted')
axes[0].set_ylabel('Residual')
axes[0].set_title('Residual Plot — Should be random scatter')
axes[1].hist(residuals, bins=50, color='steelblue', edgecolor='white')
axes[1].set_title('Residual Distribution — Should be normal')
plt.tight_layout()
plt.show()

# --- SHAP Explainability ---
explainer   = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test[:500])

shap.summary_plot(shap_values, X_test[:500])         # Global: which features matter?
shap.plots.waterfall(explainer(X_test.iloc[:1])[0])  # Local: why THIS prediction?
```

**What v2 adds over v1:**
- 8 hand-crafted features — rooms_per_person, income_per_room, etc.
- Tuned XGBoost (5 hyperparameters vs 2 in v1)
- 5-fold cross validation — not just one test set
- Residual analysis — diagnosing where the model fails
- SHAP — explains WHY each prediction was made (critical for interviews)

---

## 🔴 v3.0 — Production: AutoML + Model Comparison + API

**New in v3:** Compare 5 models automatically, stacking ensemble, FastAPI deployment, prediction confidence intervals

```python
# Part A — Multi-Model AutoML Comparison
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, StackingRegressor
from sklearn.metrics import r2_score, mean_squared_error
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')

data = fetch_california_housing(as_frame=True)
df = data.frame
df['rooms_per_person']   = df['AveRooms'] / df['AveOccup']
df['income_per_room']    = df['MedInc'] / df['AveRooms']
df['bedrooms_per_room']  = df['AveBedrms'] / df['AveRooms']

X = df.drop('MedHouseVal', axis=1)
y = df['MedHouseVal']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define 5 models
models = {
    'Ridge':           Pipeline([('sc', StandardScaler()), ('m', Ridge(alpha=1.0))]),
    'Lasso':           Pipeline([('sc', StandardScaler()), ('m', Lasso(alpha=0.01))]),
    'RandomForest':    RandomForestRegressor(n_estimators=200, random_state=42),
    'GradientBoosting': GradientBoostingRegressor(n_estimators=300, learning_rate=0.05, random_state=42),
    'XGBoost':         xgb.XGBRegressor(n_estimators=400, learning_rate=0.03, random_state=42),
}

results = []
for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    cv = cross_val_score(model, X, y, cv=5, scoring='r2')
    results.append({
        'Model': name,
        'R²': r2_score(y_test, pred),
        'RMSE': np.sqrt(mean_squared_error(y_test, pred)),
        'CV Mean': cv.mean(),
        'CV Std': cv.std()
    })

results_df = pd.DataFrame(results).sort_values('R²', ascending=False)
print(results_df.round(4).to_string(index=False))

# --- Stacking Ensemble ---
stacking = StackingRegressor(
    estimators=[
        ('rf',  RandomForestRegressor(n_estimators=100, random_state=42)),
        ('xgb', xgb.XGBRegressor(n_estimators=200, random_state=42)),
        ('gb',  GradientBoostingRegressor(n_estimators=100, random_state=42)),
    ],
    final_estimator=Ridge(alpha=1.0)
)
stacking.fit(X_train, y_train)
stack_pred = stacking.predict(X_test)
print(f"\nStacking Ensemble R²:   {r2_score(y_test, stack_pred):.4f}")
print(f"Stacking Ensemble RMSE: {np.sqrt(mean_squared_error(y_test, stack_pred)):.4f}")
```

```python
# Part B — FastAPI (save as api.py, run: uvicorn api:app --reload)
from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib, numpy as np

app   = FastAPI(title="House Price API v3", version="3.0")
model = joblib.load("model_v3.pkl")

class House(BaseModel):
    MedInc: float = Field(..., example=5.0, description="Median income ($10k units)")
    HouseAge: float = Field(..., example=20.0)
    AveRooms: float = Field(..., example=6.0)
    AveBedrms: float = Field(..., example=1.1)
    Population: float = Field(..., example=1500.0)
    AveOccup: float = Field(..., example=3.0)
    Latitude: float = Field(..., example=37.8)
    Longitude: float = Field(..., example=-122.4)

@app.post("/predict")
def predict(house: House):
    features = np.array([[
        house.MedInc, house.HouseAge, house.AveRooms, house.AveBedrms,
        house.Population, house.AveOccup, house.Latitude, house.Longitude,
        house.AveRooms / house.AveOccup,
        house.MedInc / house.AveRooms,
        house.AveBedrms / house.AveRooms
    ]])
    pred = model.predict(features)[0]
    return {
        "predicted_price_usd": round(pred * 100_000, 0),
        "predicted_price_inr": round(pred * 100_000 * 83.5, 0),
        "confidence_band": {
            "low": round((pred - 0.3) * 100_000, 0),
            "high": round((pred + 0.3) * 100_000, 0)
        }
    }
```

**What v3 adds over v2:**
- 5 models compared side-by-side automatically
- Stacking ensemble — combines all models for best accuracy
- Production FastAPI with input validation via Pydantic
- Confidence band — gives price range, not just a point estimate

---

## 📈 Learning Progression Summary

```
v1 → Predict a house price with 2 models
v2 → Engineer features + explain the model with SHAP
v3 → Compare 5 models, build a stacking ensemble, deploy as an API
```

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
