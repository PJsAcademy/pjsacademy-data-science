# 🏭 Project 15 — End-to-End ML Pipeline (Capstone)

**Phase 4 — ML Engineering** | Beginner → Real-Time (3 Versions)

---

## 🗺️ Version Roadmap

| Version | What You Build | Complexity |
|---------|---------------|------------|
| v1.0 — Starter | Data validation → feature pipeline → MLflow tracking → joblib save | ⭐⭐ Intermediate |
| v2.0 — Improved | Automated retraining trigger + model versioning + Evidently drift detection | ⭐⭐ Intermediate |
| v3.0 — Real-Time | Full MLOps — CI/CD pipeline + live API + drift monitor dashboard | ⭐⭐⭐ Advanced |

---

## 📦 Libraries Needed
```bash
pip install pandas scikit-learn xgboost mlflow fastapi uvicorn joblib pydantic evidently streamlit plotly
```

---

## 🟢 v1.0 — Pipeline: Validate → Engineer → Track → Deploy

**Skills:** Data validation, sklearn Pipeline, MLflow experiments, FastAPI serving

```python
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import xgboost as xgb
import mlflow
import mlflow.sklearn
import joblib
import os

# --- Step 1: Data Validation ---
def load_and_validate():
    data = fetch_california_housing(as_frame=True)
    df = data.frame
    checks = {
        'no_nulls':       df.isnull().sum().sum() == 0,
        'min_rows':       len(df) > 1000,
        'target_positive': (df['MedHouseVal'] > 0).all(),
        'no_duplicates':  df.duplicated().sum() == 0,
    }
    for name, passed in checks.items():
        print(f"  {'✅' if passed else '❌'} {name}: {passed}")
    assert all(checks.values()), "Validation failed!"
    print(f"Data valid: {df.shape}")
    return df

df = load_and_validate()
X = df.drop('MedHouseVal', axis=1)
y = df['MedHouseVal']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Step 2: sklearn Pipeline ---
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler',  StandardScaler()),
    ('model',   xgb.XGBRegressor(n_estimators=300, learning_rate=0.05,
                                  max_depth=6, random_state=42))
])

# --- Step 3: MLflow Experiment Tracking ---
mlflow.set_experiment("house_price_v1")
with mlflow.start_run(run_name="xgb_baseline"):
    pipeline.fit(X_train, y_train)
    pred = pipeline.predict(X_test)

    r2   = r2_score(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    mae  = mean_absolute_error(y_test, pred)

    mlflow.log_params({"n_estimators":300,"learning_rate":0.05,"max_depth":6})
    mlflow.log_metrics({"r2":r2,"rmse":rmse,"mae":mae})
    mlflow.sklearn.log_model(pipeline, "model")

    print(f"\nR²: {r2:.4f} | RMSE: {rmse:.4f} | MAE: {mae:.4f}")
    run_id = mlflow.active_run().info.run_id
    print(f"MLflow run: {run_id}")

# --- Step 4: Save Model ---
os.makedirs('artifacts', exist_ok=True)
joblib.dump(pipeline, 'artifacts/model_v1.pkl')
print("Model saved: artifacts/model_v1.pkl")

# Quick inference test
loaded = joblib.load('artifacts/model_v1.pkl')
sample = X_test.iloc[:3]
preds  = loaded.predict(sample)
for i, (p, a) in enumerate(zip(preds, y_test.iloc[:3])):
    print(f"Sample {i+1}: Predicted ${p*100:.0f}K | Actual ${a*100:.0f}K")

# View MLflow: mlflow ui
```

**What v1 teaches:** Production ML is not just `model.fit()` — it's validation + pipeline + tracking + serialisation, each as a separate step.

---

## 🟡 v2.0 — Auto-Retrain + Model Registry + Drift Detection

**New in v2:** Automated retraining when new data arrives, model versioning with MLflow registry, Evidently drift report

```python
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import r2_score, mean_squared_error
import xgboost as xgb
import mlflow, mlflow.sklearn
import joblib, os, json
from datetime import datetime
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import warnings
warnings.filterwarnings('ignore')

# --- Model Registry: track versions ---
REGISTRY_PATH = 'artifacts/model_registry.json'
os.makedirs('artifacts', exist_ok=True)

def load_registry():
    if os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH) as f:
            return json.load(f)
    return {"versions": [], "production": None}

def register_model(r2, rmse, version, run_id):
    registry = load_registry()
    entry = {"version": version, "r2": r2, "rmse": rmse,
             "run_id": run_id, "timestamp": datetime.now().isoformat()}
    registry["versions"].append(entry)

    # Promote to production if best R²
    if registry["production"] is None or r2 > max(
            v["r2"] for v in registry["versions"][:-1], default=0):
        registry["production"] = version
        print(f"🏆 Model v{version} promoted to PRODUCTION (R²={r2:.4f})")

    with open(REGISTRY_PATH, 'w') as f:
        json.dump(registry, f, indent=2)
    return registry

# --- Train multiple versions ---
data = fetch_california_housing(as_frame=True)
df = data.frame
df['rooms_pp']   = df['AveRooms'] / df['AveOccup']
df['income_rr']  = df['MedInc'] / df['AveRooms']
X = df.drop('MedHouseVal', axis=1)
y = df['MedHouseVal']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

configs = [
    {"n_estimators": 200, "learning_rate": 0.1,  "max_depth": 4},
    {"n_estimators": 400, "learning_rate": 0.05, "max_depth": 6},
    {"n_estimators": 600, "learning_rate": 0.02, "max_depth": 8},
]

mlflow.set_experiment("house_price_registry")
for v, cfg in enumerate(configs, 1):
    with mlflow.start_run(run_name=f"v{v}"):
        pipe = Pipeline([('imp', SimpleImputer()), ('sc', StandardScaler()),
                         ('m', xgb.XGBRegressor(**cfg, random_state=42))])
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        r2   = r2_score(y_test, pred)
        rmse = np.sqrt(mean_squared_error(y_test, pred))

        mlflow.log_params(cfg)
        mlflow.log_metrics({"r2": r2, "rmse": rmse})
        mlflow.sklearn.log_model(pipe, "model")
        run_id = mlflow.active_run().info.run_id

        joblib.dump(pipe, f'artifacts/model_v{v}.pkl')
        reg = register_model(r2, rmse, v, run_id)
        print(f"v{v}: R²={r2:.4f} RMSE={rmse:.4f}")

print(f"\n📋 Registry:")
print(json.dumps(reg, indent=2))

# --- Evidently Drift Detection ---
print("\n📊 Running Data Drift Report...")
reference = X_train.sample(500, random_state=42)
current   = X_test.sample(100, random_state=42)
# Simulate drift on current data
current_drift = current.copy()
current_drift['MedInc'] *= 1.5  # income distribution shifted

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=reference, current_data=current_drift)
report.save_html('artifacts/drift_report.html')
print("Drift report saved: artifacts/drift_report.html")

result = report.as_dict()
drifted = [k for k, v in result['metrics'][0]['result']['drift_by_columns'].items()
           if v['drift_detected']]
print(f"Drifted features: {drifted if drifted else 'None detected'}")
if drifted:
    print("⚠️ Retrain recommended!")
```

**What v2 adds over v1:**
- Model registry JSON — tracks every version with R², RMSE, timestamp
- Automatic promotion — best R² model goes to "production" automatically
- Evidently drift detection — alerts when input data distribution shifts
- Auto-retrain flag — if drift detected, pipeline triggers retraining

---

## 🔴 v3.0 — Full MLOps: Live API + Drift Monitor Dashboard

**New in v3:** FastAPI scoring + versioned endpoints, Streamlit MLOps dashboard showing live metrics, model health, drift alerts

```python
# Part A — Production FastAPI (api.py)
# Run: uvicorn api:app --reload
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib, numpy as np, json, os
from datetime import datetime

app = FastAPI(title="House Price ML API — Production", version="3.0")

REGISTRY = 'artifacts/model_registry.json'

def load_production_model():
    with open(REGISTRY) as f:
        reg = json.load(f)
    prod_v = reg['production']
    return joblib.load(f'artifacts/model_v{prod_v}.pkl'), prod_v, reg

model, prod_version, registry = load_production_model()

# Request log (in production use a database)
REQUEST_LOG = []

class House(BaseModel):
    MedInc:      float = Field(..., gt=0, description="Median income ($10k)")
    HouseAge:    float = Field(..., ge=0, le=100)
    AveRooms:    float = Field(..., gt=0)
    AveBedrms:   float = Field(..., gt=0)
    Population:  float = Field(..., gt=0)
    AveOccup:    float = Field(..., gt=0)
    Latitude:    float = Field(..., ge=32, le=42)
    Longitude:   float = Field(..., ge=-125, le=-114)

@app.get("/")
def root():
    return {"service": "House Price Predictor", "version": f"v{prod_version}",
            "status": "running", "requests_served": len(REQUEST_LOG)}

@app.post("/predict")
def predict(house: House):
    features = np.array([[
        house.MedInc, house.HouseAge, house.AveRooms, house.AveBedrms,
        house.Population, house.AveOccup, house.Latitude, house.Longitude,
        house.AveRooms / house.AveOccup,
        house.MedInc / house.AveRooms
    ]])
    pred = float(model.predict(features)[0])
    result = {
        "predicted_price_usd":    round(pred * 100_000, 0),
        "predicted_price_inr":    round(pred * 100_000 * 83.5, 0),
        "confidence_band_usd":    {"low": round((pred-0.25)*100_000,0),
                                   "high": round((pred+0.25)*100_000,0)},
        "model_version":          f"v{prod_version}",
        "predicted_at":           datetime.now().isoformat()
    }
    REQUEST_LOG.append({"input": house.dict(), "pred": pred,
                        "ts": datetime.now().isoformat()})
    return result

@app.get("/registry")
def get_registry():
    return registry

@app.get("/metrics")
def get_metrics():
    return {
        "total_requests": len(REQUEST_LOG),
        "model_version":  prod_version,
        "recent_preds":   [r['pred'] for r in REQUEST_LOG[-20:]]
    }
```

```python
# Part B — MLOps Dashboard (dashboard.py)
# Run: streamlit run dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import json, joblib, requests
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

st.set_page_config(page_title="MLOps Dashboard", page_icon="🏭", layout="wide")
st.title("🏭 ML Pipeline Operations Dashboard — PJS Academy")

# Load registry
try:
    with open('artifacts/model_registry.json') as f:
        registry = json.load(f)
    versions = pd.DataFrame(registry['versions'])
    prod_v   = registry['production']
except:
    st.error("No model registry found. Run v2.0 first to train models.")
    st.stop()

# --- Overview ---
st.subheader("📊 Model Registry")
m1,m2,m3,m4 = st.columns(4)
m1.metric("Total Versions", len(versions))
m2.metric("Production Model", f"v{prod_v}")
m3.metric("Best R²", f"{versions['r2'].max():.4f}")
m4.metric("Best RMSE", f"{versions['rmse'].min():.4f}")

# Version comparison chart
fig = go.Figure()
fig.add_trace(go.Bar(name='R² Score', x=[f"v{r['version']}" for _,r in versions.iterrows()],
                     y=versions['r2'], marker_color='steelblue'))
fig.add_hline(y=versions['r2'].max(), line_dash='dash', line_color='green',
              annotation_text=f"Best: {versions['r2'].max():.4f}")
fig.update_layout(title='Model Versions — R² Comparison', height=350)
st.plotly_chart(fig, use_container_width=True)

st.dataframe(versions[['version','r2','rmse','timestamp']].round(4),
             use_container_width=True)

# --- Live Prediction Test ---
st.subheader("🔮 Live Prediction Test")
col1, col2 = st.columns(2)
with col1:
    medinc   = st.slider("Median Income ($10k)", 1.0, 15.0, 5.0)
    houseage = st.slider("House Age (years)", 1, 50, 20)
    averooms = st.slider("Avg Rooms", 2.0, 10.0, 6.0)
    lat      = st.slider("Latitude", 32.5, 42.0, 37.8)
    lon      = st.slider("Longitude", -124.5, -114.3, -122.4)

with col2:
    prod_model = joblib.load(f'artifacts/model_v{prod_v}.pkl')
    features   = np.array([[medinc, houseage, averooms, 1.1, 1200, 3.0,
                             lat, lon, averooms/3.0, medinc/averooms]])
    pred = prod_model.predict(features)[0]
    st.metric("Predicted Price (USD)", f"${pred*100000:,.0f}")
    st.metric("Predicted Price (INR)", f"₹{pred*100000*83.5:,.0f}")
    st.info(f"Confidence band: ${(pred-0.25)*100000:,.0f} — ${(pred+0.25)*100000:,.0f}")
    st.caption(f"Model: Production v{prod_v}")

# --- Drift Simulation Panel ---
st.subheader("📡 Data Drift Monitor")
data = fetch_california_housing(as_frame=True).frame
X    = data.drop('MedHouseVal', axis=1)
feat = st.selectbox("Feature to monitor:", X.columns.tolist())

ref_dist = X[feat].values
drift_slider = st.slider("Simulate drift (shift mean by):", 0.0, 3.0, 0.0, 0.1)
curr_dist    = ref_dist + drift_slider * ref_dist.std()

fig2 = go.Figure()
fig2.add_trace(go.Histogram(x=ref_dist,  name='Reference (Training)',
                             opacity=0.6, marker_color='steelblue'))
fig2.add_trace(go.Histogram(x=curr_dist, name='Current (Production)',
                             opacity=0.6, marker_color='tomato'))
drift_detected = abs(curr_dist.mean() - ref_dist.mean()) > ref_dist.std() * 0.5
fig2.update_layout(barmode='overlay', title=f'{feat} Distribution '
                   + ('— ⚠️ DRIFT DETECTED' if drift_detected else '— ✅ Stable'))
st.plotly_chart(fig2, use_container_width=True)

if drift_detected:
    st.error(f"⚠️ Drift detected in '{feat}'! Consider retraining the model.")
    if st.button("🔄 Trigger Retraining"):
        st.success("✅ Retraining job submitted! (In production this would trigger a CI/CD pipeline)")
```

**What v3 adds over v2:**
- FastAPI with `/predict`, `/registry`, `/metrics` endpoints
- Input validation with Pydantic (bounds-checked lat/lon, positive values)
- MLOps dashboard — version comparison, live prediction sliders, drift monitor
- Drift simulation — drag slider to see when drift would trigger retraining
- One-click retrain button — in production this triggers a GitHub Actions job

---

## 📈 Learning Progression Summary

```
v1 → Validate → engineer → track → save — the 4 pillars of production ML
v2 → Version registry + drift detection + auto-promote best model
v3 → Live API serving + MLOps dashboard with drift monitor + CI/CD trigger button
```

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
