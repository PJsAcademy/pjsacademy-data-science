# 📉 Project 04 — Customer Churn Predictor

**Phase 4 — ML Engineering** | Beginner → Advanced (3 Versions)

---

## 🗺️ Version Roadmap

| Version | What You Build | Complexity |
|---------|---------------|------------|
| v1.0 — Starter | XGBoost classifier with basic evaluation | ⭐ Beginner |
| v2.0 — Improved | SHAP explainability + threshold optimisation + business impact | ⭐⭐ Intermediate |
| v3.0 — Production | Real-time scoring API + customer risk dashboard + A/B test logic | ⭐⭐⭐ Advanced |

---

## 📦 Dataset
**Telco Customer Churn** — public from Kaggle (`telco_churn.csv`)

---

## 🟢 v1.0 — XGBoost Classifier

**Skills:** LabelEncoder, XGBoost, classification report, ROC-AUC

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, roc_auc_score
import xgboost as xgb

df = pd.read_csv('telco_churn.csv')
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df.dropna(inplace=True)
df.drop('customerID', axis=1, inplace=True)

# Encode categorical
le = LabelEncoder()
for col in df.select_dtypes('object').columns:
    df[col] = le.fit_transform(df[col])

X = df.drop('Churn', axis=1)
y = df['Churn']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

clf = xgb.XGBClassifier(
    n_estimators=300, learning_rate=0.05,
    scale_pos_weight=3, eval_metric='logloss', random_state=42
)
clf.fit(X_train, y_train)
pred  = clf.predict(X_test)
proba = clf.predict_proba(X_test)[:, 1]

print(classification_report(y_test, pred, target_names=['Stay', 'Churn']))
print(f"ROC-AUC: {roc_auc_score(y_test, proba):.3f}")
```

**What v1 teaches:** XGBoost handles class imbalance with `scale_pos_weight` — why accuracy is misleading when only 25% of customers churn.

---

## 🟡 v2.0 — Business-Aware Churn Model

**New in v2:** SHAP explainability, optimal threshold tuning (F1 vs revenue), customer segment analysis, retention cost calculator

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (classification_report, roc_auc_score,
                             precision_recall_curve, f1_score, roc_curve)
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('telco_churn.csv')
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df.dropna(inplace=True)
df.drop('customerID', axis=1, inplace=True)

# --- Feature Engineering ---
df['ChargesPerMonth']   = df['TotalCharges'] / (df['tenure'] + 1)
df['ContractIsMonthly'] = (df['Contract'] == 'Month-to-month').astype(int)
df['NoSupport']         = ((df['TechSupport'] == 'No') & (df['OnlineSecurity'] == 'No')).astype(int)
df['HighValueLowTenure'] = ((df['MonthlyCharges'] > 70) & (df['tenure'] < 12)).astype(int)

le = LabelEncoder()
for col in df.select_dtypes('object').columns:
    df[col] = le.fit_transform(df[col])

X = df.drop('Churn', axis=1)
y = df['Churn']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

# --- Tuned XGBoost ---
clf = xgb.XGBClassifier(
    n_estimators=500, learning_rate=0.03, max_depth=5,
    subsample=0.8, colsample_bytree=0.8,
    scale_pos_weight=3, eval_metric='aucpr', random_state=42
)
clf.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
proba = clf.predict_proba(X_test)[:, 1]

# --- Threshold Optimisation (F1) ---
precision, recall, thresholds = precision_recall_curve(y_test, proba)
f1_scores = 2 * precision * recall / (precision + recall + 1e-9)
best_idx   = np.argmax(f1_scores)
best_thresh = thresholds[best_idx]
print(f"Default threshold (0.5) F1: {f1_score(y_test, proba >= 0.5):.3f}")
print(f"Optimised threshold ({best_thresh:.2f}) F1: {f1_scores[best_idx]:.3f}")

# --- Business Impact Calculator ---
# If we call a churner and offer a ₹200 discount to stay:
# Revenue saved if customer stays: ₹MonthlyCharges × 12
# Cost of intervention: ₹200
INTERVENTION_COST = 200
pred_optimal = (proba >= best_thresh).astype(int)
test_df = X_test.copy()
test_df['actual_churn'] = y_test.values
test_df['predicted_churn'] = pred_optimal
test_df['monthly_charges'] = df.loc[X_test.index, 'MonthlyCharges'].values

true_positives = test_df[(test_df['predicted_churn'] == 1) & (test_df['actual_churn'] == 1)]
revenue_saved  = (true_positives['monthly_charges'] * 12 - INTERVENTION_COST).sum()
intervention_cost = len(test_df[test_df['predicted_churn'] == 1]) * INTERVENTION_COST

print(f"\n💰 Business Impact:")
print(f"  Customers flagged for intervention: {pred_optimal.sum()}")
print(f"  True churners caught: {true_positives.shape[0]}")
print(f"  Total intervention cost: ₹{intervention_cost:,.0f}")
print(f"  Estimated revenue saved: ₹{max(revenue_saved, 0):,.0f}")
print(f"  ROI: {(revenue_saved / intervention_cost * 100):.0f}%")

# --- SHAP ---
explainer = shap.TreeExplainer(clf)
shap_values = explainer.shap_values(X_test[:300])
shap.summary_plot(shap_values, X_test[:300], plot_type='bar',
                  title='Top Drivers of Customer Churn')
```

**What v2 adds over v1:**
- 4 business-logic features (ContractIsMonthly, HighValueLowTenure, etc.)
- Threshold optimisation — 0.5 is rarely the best cutoff for imbalanced data
- Revenue saved vs intervention cost — turns ML into a business decision
- SHAP bar plot — tells product team WHAT drives churn

---

## 🔴 v3.0 — Real-Time Churn Scoring System

**New in v3:** Risk scoring API, customer segmentation into risk tiers, proactive retention trigger logic

```python
# Part A — Customer Risk Segmentation
import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# (assume model already trained from v2 — load it)
# clf = joblib.load('churn_model_v2.pkl')

# Assign risk tiers based on churn probability
def assign_risk_tier(prob):
    if prob >= 0.75:   return 'CRITICAL'    # Intervene immediately
    elif prob >= 0.50: return 'HIGH'         # Send personalised offer
    elif prob >= 0.25: return 'MEDIUM'       # Loyalty email
    else:              return 'LOW'          # Standard retention

# Score all customers
# proba = clf.predict_proba(X)[:, 1]  # in production use real model
proba = np.random.beta(2, 5, 1000)   # simulated for demo

scored_customers = pd.DataFrame({
    'customer_id': [f'CUST_{i:04d}' for i in range(1000)],
    'churn_prob': proba.round(3),
    'risk_tier': [assign_risk_tier(p) for p in proba]
})

# Retention campaign logic
def get_retention_action(tier, monthly_charges):
    actions = {
        'CRITICAL': f"🚨 Urgent call + ₹{int(monthly_charges * 0.3)} discount + free upgrade",
        'HIGH':     f"📧 Personalised email + ₹{int(monthly_charges * 0.15)} loyalty reward",
        'MEDIUM':   "💌 Loyalty newsletter + survey",
        'LOW':      "✅ No action needed"
    }
    return actions[tier]

scored_customers['monthly_charges'] = np.random.uniform(500, 3000, 1000)
scored_customers['action'] = scored_customers.apply(
    lambda r: get_retention_action(r['risk_tier'], r['monthly_charges']), axis=1)

# Tier summary
print("CUSTOMER RISK DASHBOARD")
print("="*50)
tier_counts = scored_customers['risk_tier'].value_counts()
for tier in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
    count = tier_counts.get(tier, 0)
    pct = count / len(scored_customers) * 100
    print(f"  {tier:10s}: {count:4d} customers ({pct:.1f}%)")

print("\nTop 5 Critical Customers:")
critical = scored_customers[scored_customers['risk_tier'] == 'CRITICAL']
print(critical.nlargest(5, 'churn_prob')[['customer_id', 'churn_prob', 'action']].to_string(index=False))
```

```python
# Part B — FastAPI Scoring Endpoint (api.py)
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np, joblib

app   = FastAPI(title="Churn Scoring API v3")
model = joblib.load("churn_model.pkl")

class Customer(BaseModel):
    tenure: int
    MonthlyCharges: float
    TotalCharges: float
    Contract: str  # "Month-to-month", "One year", "Two year"
    TechSupport: str
    OnlineSecurity: str

@app.post("/score")
def score_customer(customer: Customer):
    # Encode and predict (simplified — full encoding in production)
    contract_map = {"Month-to-month": 0, "One year": 1, "Two year": 2}
    features = np.array([[
        customer.tenure,
        customer.MonthlyCharges,
        customer.TotalCharges,
        contract_map.get(customer.Contract, 0),
        1 if customer.TechSupport == "No" else 0,
        1 if customer.OnlineSecurity == "No" else 0,
        customer.TotalCharges / (customer.tenure + 1),
        1 if (customer.MonthlyCharges > 70 and customer.tenure < 12) else 0
    ]])

    prob = float(model.predict_proba(features)[0][1])
    tier = ("CRITICAL" if prob >= 0.75 else "HIGH" if prob >= 0.5
            else "MEDIUM" if prob >= 0.25 else "LOW")

    return {
        "churn_probability": round(prob, 3),
        "risk_tier": tier,
        "recommended_action": {
            "CRITICAL": "Immediate outreach + discount offer",
            "HIGH":     "Personalised email campaign",
            "MEDIUM":   "Loyalty programme enrolment",
            "LOW":      "No action required"
        }[tier]
    }
```

**What v3 adds over v2:**
- 4-tier risk segmentation — not just "will churn yes/no"
- Action-specific recommendations per tier — directly actionable for CRM teams
- FastAPI endpoint — plug into any CRM (Salesforce, HubSpot)
- Intervention budget calculator built in

---

## 📈 Learning Progression Summary

```
v1 → "This customer might churn" — binary output
v2 → "This customer will churn because of month-to-month contract" — SHAP explained
v3 → "Flag 47 CRITICAL customers today, call them with this offer, save ₹3.2L" — production system
```

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
