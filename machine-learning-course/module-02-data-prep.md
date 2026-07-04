# Module 02 — Data & Feature Engineering

> "Garbage in, garbage out." Models are only as good as the data you feed them. This is where 80% of real ML work happens.

---

## 2.1 Why Data Prep Is the Real Job

A fancy algorithm on bad data loses to a simple algorithm on well-prepared data — every time. Real data is messy: missing values, wrong types, different scales, text where you need numbers. Fixing that is the job.

## 2.2 Exploratory Data Analysis (EDA) First

Before modelling, **look** at your data:
```python
import pandas as pd
df = pd.read_csv("data.csv")
df.head()          # first rows — what does it look like?
df.info()          # types + non-null counts
df.describe()      # min/max/mean/std of numeric columns
df.isnull().sum()  # missing values per column
df['target'].value_counts()  # class balance (for classification)
```
Ask: What's the target? Which features look useful? What's missing? Any weird values?

## 2.3 Handling Missing Values

Options, in rough order of preference:
```python
# 1. Drop rows/columns if few and non-critical
df.dropna(subset=['age'])

# 2. Impute numeric with median (robust to outliers)
df['age'] = df['age'].fillna(df['age'].median())

# 3. Impute categorical with the mode (most common)
df['city'] = df['city'].fillna(df['city'].mode()[0])

# 4. Smarter: sklearn imputers (fit on TRAIN only!)
from sklearn.impute import SimpleImputer
imp = SimpleImputer(strategy='median')
X_train_imp = imp.fit_transform(X_train)
X_test_imp  = imp.transform(X_test)   # transform only — no re-fitting
```
> ⚠️ **Fit imputers/scalers on the training set only, then apply to test.** Fitting on all data leaks test information.

## 2.4 Encoding Categorical Variables

Models need numbers, not text. Two main tools:

**One-Hot Encoding** — for categories with no order (city, colour). Each category becomes a 0/1 column.
```python
pd.get_dummies(df, columns=['city'])   # city_Mumbai, city_Delhi, ...
```

**Ordinal/Label Encoding** — for ordered categories (low < medium < high).
```python
df['size'] = df['size'].map({'S': 0, 'M': 1, 'L': 2})
```
> Don't label-encode unordered categories with integers — the model wrongly assumes 2 > 1 > 0 has meaning.

## 2.5 Feature Scaling

Features on wildly different scales (age 0–100 vs income 0–1,000,000) confuse distance- and gradient-based models (kNN, SVM, neural nets, linear models). Put them on a comparable scale.

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler
# Standardization: mean 0, std 1 (most common)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)   # fit on train
X_test_s  = scaler.transform(X_test)        # apply to test
```
- **StandardScaler** (z-score): centres to mean 0, std 1. Default choice.
- **MinMaxScaler**: squashes to [0, 1]. Good for bounded/image data.
- **Tree-based models** (Random Forest, XGBoost) **don't need scaling** — they split on thresholds, scale-invariant.

## 2.6 Feature Engineering — the Highest-Leverage Skill

Creating better features from existing ones often beats any model upgrade.

```python
# Ratios and interactions
df['rooms_per_person'] = df['rooms'] / df['occupants']
df['price_per_sqft']   = df['price'] / df['area']

# Date features
df['order_date'] = pd.to_datetime(df['order_date'])
df['dayofweek']  = df['order_date'].dt.dayofweek
df['is_weekend'] = (df['dayofweek'] >= 5).astype(int)
df['month']      = df['order_date'].dt.month

# Binning a continuous variable
df['age_group'] = pd.cut(df['age'], bins=[0,18,35,60,100],
                         labels=['teen','young','adult','senior'])

# Text length, counts, flags
df['name_length'] = df['name'].str.len()
```
Domain knowledge shines here: *what would a human expert look at?* Encode that.

## 2.7 Outliers

Extreme values can distort models (especially linear ones).
```python
# Detect with the IQR rule
Q1, Q3 = df['income'].quantile([0.25, 0.75])
IQR = Q3 - Q1
low, high = Q1 - 1.5*IQR, Q3 + 1.5*IQR
outliers = df[(df['income'] < low) | (df['income'] > high)]
```
Options: remove (if errors), cap/winsorize (clip to a limit), or keep (if genuine — e.g. fraud *is* the outlier). Decide with domain sense, not reflex.

## 2.8 Putting It Together with a Pipeline

Pipelines bundle preprocessing + model so the same steps apply consistently and leak-free:
```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

numeric = ['age', 'income']
categorical = ['city']

pre = ColumnTransformer([
    ('num', Pipeline([('imp', SimpleImputer(strategy='median')),
                      ('sc', StandardScaler())]), numeric),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical),
])
# pre.fit_transform(X_train) then pre.transform(X_test) — or drop into a full model Pipeline
```
> Pipelines are the professional standard — they make preprocessing reproducible and prevent leakage automatically.

---

## ✅ Key Takeaways
1. **EDA first** — understand data before modelling.
2. **Impute** missing values (median/mode); fit on train only.
3. **One-hot** unordered categories, **ordinal-encode** ordered ones.
4. **Scale** features for distance/gradient models; trees don't need it.
5. **Feature engineering** (ratios, dates, bins) is the highest-leverage move.
6. Use **pipelines** to apply steps consistently and avoid leakage.

## 🏋️ Exercises
1. Take any CSV, run the 5 EDA commands, and write 3 things you learned.
2. One-hot encode a categorical column and ordinal-encode an ordered one. Explain why each choice.
3. Engineer 3 new features from a dataset and argue why each might help.
4. Build a `ColumnTransformer` that imputes + scales numerics and one-hots categoricals.

**Next:** [Module 03 — Regression →](module-03-regression.md)

---

*🤖 Machine Learning Mastery — [PJ's Academy](https://pjsacademy.com)*
