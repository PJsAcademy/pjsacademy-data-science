# 📉 Project 04 — Customer Churn Predictor

**Phase 4 — ML Engineering** | Intermediate

---

## 🎯 What You'll Build
Predict which customers will leave a telecom company — a real business problem worth millions.

## 🛠️ Skills Practiced
- XGBoost Classification
- Class imbalance handling
- Feature importance analysis
- SHAP values for explainability

## 📦 Dataset
**Telco Customer Churn Dataset** (public, from Kaggle)

## 🚀 Steps
1. Load and clean data
2. Encode categorical features
3. Handle class imbalance
4. Train XGBoost classifier
5. Evaluate with F1, AUC-ROC
6. Interpret with feature importance

## 💻 Code
```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, roc_auc_score
import xgboost as xgb

# Load
df = pd.read_csv('telco_churn.csv')
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df.dropna(inplace=True)

# Encode
le = LabelEncoder()
cat_cols = df.select_dtypes('object').columns
for col in cat_cols:
    df[col] = le.fit_transform(df[col])

# Split
X = df.drop('Churn', axis=1)
y = df['Churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                      stratify=y, random_state=42)

# Train
clf = xgb.XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    scale_pos_weight=3,  # handle imbalance
    use_label_encoder=False,
    eval_metric='logloss'
)
clf.fit(X_train, y_train)

# Evaluate
pred = clf.predict(X_test)
proba = clf.predict_proba(X_test)[:, 1]
print(classification_report(y_test, pred))
print(f"ROC-AUC: {roc_auc_score(y_test, proba):.3f}")

# Feature importance
import pandas as pd
importance = pd.Series(clf.feature_importances_, index=X.columns)
print(importance.sort_values(ascending=False).head(10))
```

## 📈 What You'll Learn
- Real business ML use case
- Handling imbalanced classes
- Model explainability with feature importance

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
