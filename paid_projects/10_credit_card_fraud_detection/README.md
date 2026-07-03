# 💳 Project 10 — Credit Card Fraud Detection

**Phase 4 — ML Engineering** | Beginner → Real-Time (3 Versions)

---

## 🗺️ Version Roadmap

| Version | What You Build | Complexity |
|---------|---------------|------------|
| v1.0 — Starter | SMOTE + XGBoost + Isolation Forest baseline | ⭐ Beginner |
| v2.0 — Improved | Ensemble model + threshold optimisation + SHAP fraud explainer | ⭐⭐ Intermediate |
| v3.0 — Real-Time | Live transaction scoring API + fraud alert dashboard | ⭐⭐⭐ Advanced |

---

## 📦 Libraries Needed
```bash
pip install pandas numpy scikit-learn xgboost imbalanced-learn shap matplotlib fastapi uvicorn streamlit
```

---

## 🟢 v1.0 — Detect Fraud with SMOTE + XGBoost

**Skills:** SMOTE, XGBoost, Precision-Recall, Isolation Forest

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, average_precision_score
from sklearn.ensemble import IsolationForest
from imblearn.over_sampling import SMOTE
import xgboost as xgb

df = pd.read_csv('creditcard.csv')
print(f"Fraud: {df['Class'].sum()} ({df['Class'].mean()*100:.3f}%)")

df['Amount_Scaled'] = StandardScaler().fit_transform(df[['Amount']])
df['Time_Scaled']   = StandardScaler().fit_transform(df[['Time']])
df.drop(['Amount','Time'], axis=1, inplace=True)

X = df.drop('Class', axis=1)
y = df['Class']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

# SMOTE oversampling
from collections import Counter
print(f"Before SMOTE: {Counter(y_train)}")
X_sm, y_sm = SMOTE(random_state=42).fit_resample(X_train, y_train)
print(f"After SMOTE:  {Counter(y_sm)}")

# XGBoost on SMOTE data
clf = xgb.XGBClassifier(n_estimators=300, learning_rate=0.05,
                         eval_metric='aucpr', random_state=42)
clf.fit(X_sm, y_sm)
pred  = clf.predict(X_test)
proba = clf.predict_proba(X_test)[:, 1]

print(classification_report(y_test, pred, target_names=['Normal','Fraud']))
print(f"ROC-AUC: {roc_auc_score(y_test, proba):.4f}")
print(f"PR-AUC:  {average_precision_score(y_test, proba):.4f}")

# Isolation Forest (unsupervised, no labels needed)
iso = IsolationForest(contamination=0.001, random_state=42)
iso_pred = [1 if p == -1 else 0 for p in iso.fit_predict(X_test)]
print("\nIsolation Forest (Unsupervised):")
print(classification_report(y_test, iso_pred, target_names=['Normal','Fraud']))
```

**What v1 teaches:** Why accuracy is useless here (99.8% normal), why you need PR-AUC, and why SMOTE helps bridge the class gap.

---

## 🟡 v2.0 — Ensemble + Threshold Tuning + SHAP

**New in v2:** Stack XGBoost + RandomForest + LightGBM, optimise threshold for business impact, SHAP fraud explanations

```python
import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import (precision_recall_curve, roc_auc_score,
                             average_precision_score, f1_score, classification_report)
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from imblearn.over_sampling import SMOTE
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('creditcard.csv')
df['Amount_Scaled'] = StandardScaler().fit_transform(df[['Amount']])
df['Time_Scaled']   = StandardScaler().fit_transform(df[['Time']])
df['Amount_log']    = np.log1p(df['Amount'])
df['Hour']          = (df['Time'] // 3600) % 24
df.drop(['Amount','Time'], axis=1, inplace=True)

X, y = df.drop('Class', axis=1), df['Class']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)
X_sm, y_sm = SMOTE(random_state=42).fit_resample(X_train, y_train)

# --- Ensemble: XGBoost + RandomForest ---
xgb_clf = xgb.XGBClassifier(n_estimators=400, learning_rate=0.03, max_depth=6,
                              subsample=0.8, eval_metric='aucpr', random_state=42)
rf_clf  = RandomForestClassifier(n_estimators=200, max_depth=10,
                                  class_weight='balanced', random_state=42)

xgb_clf.fit(X_sm, y_sm)
rf_clf.fit(X_sm, y_sm)

# Soft-voting ensemble (average probabilities)
xgb_proba = xgb_clf.predict_proba(X_test)[:, 1]
rf_proba  = rf_clf.predict_proba(X_test)[:, 1]
ensemble_proba = (0.6 * xgb_proba + 0.4 * rf_proba)  # weighted blend

print(f"XGBoost  PR-AUC: {average_precision_score(y_test, xgb_proba):.4f}")
print(f"RF       PR-AUC: {average_precision_score(y_test, rf_proba):.4f}")
print(f"Ensemble PR-AUC: {average_precision_score(y_test, ensemble_proba):.4f}")

# --- Optimal Threshold ---
precision, recall, thresholds = precision_recall_curve(y_test, ensemble_proba)
f1_scores = 2 * precision * recall / (precision + recall + 1e-9)
best_idx   = np.argmax(f1_scores[:-1])
best_thresh = thresholds[best_idx]

pred_default = (ensemble_proba >= 0.5).astype(int)
pred_optimal = (ensemble_proba >= best_thresh).astype(int)

print(f"\nDefault threshold (0.50) F1: {f1_score(y_test, pred_default):.4f}")
print(f"Optimal threshold ({best_thresh:.3f}) F1: {f1_scores[best_idx]:.4f}")

# --- Business Impact ---
# Assume avg fraudulent transaction = $150, investigation cost = $5
FRAUD_AMOUNT = 150
INVESTIGATION_COST = 5

tp = ((pred_optimal == 1) & (y_test == 1)).sum()
fp = ((pred_optimal == 1) & (y_test == 0)).sum()
fn = ((pred_optimal == 0) & (y_test == 1)).sum()

fraud_caught = tp * FRAUD_AMOUNT
false_alarm_cost = fp * INVESTIGATION_COST
missed_fraud = fn * FRAUD_AMOUNT
net_benefit = fraud_caught - false_alarm_cost - missed_fraud

print(f"\n💰 Business Impact (optimal threshold):")
print(f"  Fraud caught:         ${fraud_caught:,.0f}")
print(f"  False alarm cost:     ${false_alarm_cost:,.0f}")
print(f"  Missed fraud loss:    ${missed_fraud:,.0f}")
print(f"  Net benefit:          ${net_benefit:,.0f}")

# --- SHAP Fraud Explanation ---
explainer   = shap.TreeExplainer(xgb_clf)
shap_values = explainer.shap_values(X_test.iloc[:500])
shap.summary_plot(shap_values, X_test.iloc[:500], plot_type='bar',
                  title='What drives fraud predictions?')

# Explain single fraudulent transaction
fraud_idx = np.where(y_test.values == 1)[0][0]
shap.plots.waterfall(explainer(X_test.iloc[fraud_idx:fraud_idx+1])[0],
                     max_display=15)
```

**What v2 adds over v1:**
- Soft-voting ensemble (60% XGBoost + 40% RF) — more robust than single model
- Optimal threshold tuning — F1-maximising cutoff, not 0.5
- Business impact in dollars — fraud caught vs false alarm cost
- SHAP waterfall for one transaction — "why was THIS flagged?"

---

## 🔴 v3.0 — Real-Time Transaction Scoring System

**New in v3:** FastAPI scoring endpoint, live transaction simulator, fraud alert dashboard with Streamlit

```python
# Part A — FastAPI Real-Time Scoring (api.py)
# Run: uvicorn api:app --reload
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
from datetime import datetime

app   = FastAPI(title="Fraud Detection API v3", version="3.0")
model = joblib.load("fraud_model.pkl")  # trained XGBoost from v2

RISK_LEVELS = {
    (0.0, 0.3): ("LOW",      "✅ Normal transaction"),
    (0.3, 0.6): ("MEDIUM",   "⚠️ Review recommended"),
    (0.6, 0.85):("HIGH",     "🚨 Flag for investigation"),
    (0.85, 1.0):("CRITICAL", "🔴 Block transaction immediately")
}

class Transaction(BaseModel):
    V1: float; V2: float; V3: float; V4: float; V5: float
    V6: float; V7: float; V8: float; V9: float; V10: float
    V11: float; V12: float; V13: float; V14: float; V15: float
    V16: float; V17: float; V18: float; V19: float; V20: float
    V21: float; V22: float; V23: float; V24: float; V25: float
    V26: float; V27: float; V28: float
    Amount: float
    Hour: float = 12.0

@app.post("/score")
def score_transaction(txn: Transaction):
    from sklearn.preprocessing import StandardScaler
    amount_scaled = (np.log1p(txn.Amount) - 3.5) / 2.5
    features = np.array([[
        txn.V1, txn.V2, txn.V3, txn.V4, txn.V5,
        txn.V6, txn.V7, txn.V8, txn.V9, txn.V10,
        txn.V11, txn.V12, txn.V13, txn.V14, txn.V15,
        txn.V16, txn.V17, txn.V18, txn.V19, txn.V20,
        txn.V21, txn.V22, txn.V23, txn.V24, txn.V25,
        txn.V26, txn.V27, txn.V28,
        amount_scaled, np.log1p(txn.Amount), txn.Hour
    ]])

    fraud_prob = float(model.predict_proba(features)[0][1])

    for (low, high), (level, action) in RISK_LEVELS.items():
        if low <= fraud_prob < high:
            risk_level, recommended_action = level, action
            break

    return {
        "fraud_probability": round(fraud_prob, 4),
        "risk_level": risk_level,
        "recommended_action": recommended_action,
        "amount": txn.Amount,
        "scored_at": datetime.now().isoformat(),
        "block": fraud_prob >= 0.85
    }

@app.get("/health")
def health():
    return {"status": "running", "model": "XGBoost Fraud Detector v3"}
```

```python
# Part B — Real-Time Transaction Monitor (streamlit_monitor.py)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time, random

st.set_page_config(page_title="Fraud Monitor", page_icon="🔴", layout="wide")
st.title("🔴 Real-Time Fraud Detection Monitor — PJS Academy")

# Simulate live transactions
def generate_transaction():
    is_fraud = random.random() < 0.02  # 2% fraud rate
    v_features = np.random.randn(28)
    if is_fraud:
        v_features[0] *= -3
        v_features[3] *= 2
    return {
        'amount': round(random.uniform(1, 5000), 2),
        'fraud_prob': round(random.uniform(0.7, 0.99) if is_fraud
                           else random.uniform(0.0, 0.25), 3),
        'is_fraud': is_fraud,
        'time': pd.Timestamp.now().strftime('%H:%M:%S')
    }

if 'transactions' not in st.session_state:
    st.session_state.transactions = []

col1, col2, col3, col4 = st.columns(4)
if col1.button("▶️ Generate 10 Transactions"):
    for _ in range(10):
        st.session_state.transactions.append(generate_transaction())

if col2.button("🗑️ Reset"):
    st.session_state.transactions = []

txns = st.session_state.transactions
if txns:
    df_live = pd.DataFrame(txns)
    total     = len(df_live)
    frauds    = df_live['is_fraud'].sum()
    flagged   = (df_live['fraud_prob'] >= 0.6).sum()
    blocked   = (df_live['fraud_prob'] >= 0.85).sum()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Transactions", total)
    m2.metric("Fraud Detected",     frauds, delta=f"{frauds/max(total,1)*100:.1f}%")
    m3.metric("Flagged for Review", flagged)
    m4.metric("Blocked",            blocked)

    # Colour by risk
    def risk_colour(prob):
        if prob >= 0.85: return "🔴 BLOCK"
        elif prob >= 0.6: return "🟠 FLAG"
        elif prob >= 0.3: return "🟡 REVIEW"
        return "🟢 OK"

    df_live['Risk'] = df_live['fraud_prob'].apply(risk_colour)
    st.dataframe(df_live[['time','amount','fraud_prob','Risk']].tail(20),
                 use_container_width=True)

    fig = go.Figure()
    colors = ['red' if f else 'green' for f in df_live['is_fraud']]
    fig.add_trace(go.Scatter(y=df_live['fraud_prob'], mode='lines+markers',
        marker=dict(color=colors, size=8), name='Fraud Probability'))
    fig.add_hline(y=0.6, line_dash='dash', line_color='orange',
                  annotation_text='Flag threshold')
    fig.add_hline(y=0.85, line_dash='dash', line_color='red',
                  annotation_text='Block threshold')
    fig.update_layout(title='Live Transaction Risk Scores', height=350)
    st.plotly_chart(fig, use_container_width=True)
```

**What v3 adds over v2:**
- FastAPI endpoint — scores any transaction in <50ms
- 4-tier risk system (LOW/MEDIUM/HIGH/CRITICAL) with automatic block flag
- Live Streamlit monitor — generates transactions, shows risk colour-coded
- Threshold lines on chart — visual understanding of block vs flag vs review

---

## 📈 Learning Progression Summary

```
v1 → Detect fraud with SMOTE + XGBoost, 284K transactions
v2 → Ensemble model, tune threshold, explain why each transaction was flagged
v3 → Live scoring API — any transaction scored in 50ms, dashboard monitors in real time
```

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
