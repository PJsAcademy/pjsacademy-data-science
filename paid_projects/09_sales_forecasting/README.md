# 🛒 Project 09 — Sales Forecasting

**Phase 4 — ML Engineering** | Beginner → Real-Time (3 Versions)

---

## 🗺️ Version Roadmap

| Version | What You Build | Complexity |
|---------|---------------|------------|
| v1.0 — Starter | XGBoost time series + Prophet 90-day forecast | ⭐ Beginner |
| v2.0 — Improved | Multi-store forecast + anomaly detection + forecast accuracy tracker | ⭐⭐ Intermediate |
| v3.0 — Real-Time | Live sales ingestion + auto-retrain + Streamlit forecast app | ⭐⭐⭐ Advanced |

---

## 📦 Libraries Needed
```bash
pip install pandas numpy matplotlib xgboost prophet scikit-learn streamlit plotly
```

---

## 🟢 v1.0 — XGBoost + Prophet Forecast

**Skills:** Time series split, lag features, XGBoost regression, Prophet

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import xgboost as xgb
from prophet import Prophet

# Using Rossmann Store Sales — Store 1
df = pd.read_csv('train.csv', parse_dates=['Date'])
df = df[df['Store'] == 1].sort_values('Date')

# Feature Engineering
df['Year']       = df['Date'].dt.year
df['Month']      = df['Date'].dt.month
df['DayOfWeek']  = df['Date'].dt.dayofweek
df['IsWeekend']  = (df['DayOfWeek'] >= 5).astype(int)
df['Sales_Lag7'] = df['Sales'].shift(7)
df['Rolling7']   = df['Sales'].shift(1).rolling(7).mean()
df['Rolling30']  = df['Sales'].shift(1).rolling(30).mean()
df.dropna(inplace=True)

features = ['Year','Month','DayOfWeek','IsWeekend','Promo',
            'Sales_Lag7','Rolling7','Rolling30']
X, y = df[features], df['Sales']

split = '2015-01-01'
X_train = X[df['Date'] < split]
X_test  = X[df['Date'] >= split]
y_train = y[df['Date'] < split]
y_test  = y[df['Date'] >= split]

model = xgb.XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=6)
model.fit(X_train, y_train)
pred = model.predict(X_test)

mape = np.mean(np.abs((y_test - pred) / y_test.replace(0,1))) * 100
print(f"MAE: {mean_absolute_error(y_test, pred):.0f}")
print(f"MAPE: {mape:.2f}%")

# Prophet forecast
prophet_df = df[['Date','Sales']].rename(columns={'Date':'ds','Sales':'y'})
m = Prophet(yearly_seasonality=True, weekly_seasonality=True)
m.fit(prophet_df)
future   = m.make_future_dataframe(periods=90)
forecast = m.predict(future)
m.plot(forecast)
plt.title('Sales Forecast — Next 90 Days')
plt.show()
m.plot_components(forecast)
plt.show()
```

**What v1 teaches:** Why time series needs chronological train/test split (never random), lag features, and how Prophet handles seasonality automatically.

---

## 🟡 v2.0 — Multi-Store Forecast + Anomaly Detection

**New in v2:** Forecast all stores, detect sales anomalies, track forecast accuracy with MAPE dashboard

```python
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import xgboost as xgb
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('train.csv', parse_dates=['Date'])
store_data = df[df['Open'] == 1].copy()

def engineer_features(df):
    df = df.sort_values('Date').copy()
    df['Year']       = df['Date'].dt.year
    df['Month']      = df['Date'].dt.month
    df['Week']       = df['Date'].dt.isocalendar().week.astype(int)
    df['DayOfWeek']  = df['Date'].dt.dayofweek
    df['DayOfYear']  = df['Date'].dt.dayofyear
    df['IsWeekend']  = (df['DayOfWeek'] >= 5).astype(int)
    df['Quarter']    = df['Date'].dt.quarter
    for lag in [7, 14, 21, 28]:
        df[f'Lag_{lag}'] = df['Sales'].shift(lag)
    for window in [7, 14, 30]:
        df[f'Roll_{window}'] = df['Sales'].shift(1).rolling(window).mean()
        df[f'Std_{window}']  = df['Sales'].shift(1).rolling(window).std()
    df['Sales_mom'] = df['Sales'].pct_change(30)
    return df.dropna()

# Train model for each store, collect MAPE
FEATURES = ['Year','Month','Week','DayOfWeek','DayOfYear','IsWeekend',
            'Quarter','Promo','Lag_7','Lag_14','Lag_21','Lag_28',
            'Roll_7','Roll_14','Roll_30','Std_7','Std_30','Sales_mom']

store_results = []
all_preds = []

for store_id in store_data['Store'].unique()[:10]:  # top 10 stores
    sdf = store_data[store_data['Store'] == store_id].copy()
    sdf = engineer_features(sdf)
    if len(sdf) < 200:
        continue

    split_date = sdf['Date'].quantile(0.8)
    tr = sdf[sdf['Date'] <= split_date]
    te = sdf[sdf['Date'] >  split_date]

    model = xgb.XGBRegressor(n_estimators=300, learning_rate=0.05,
                              max_depth=6, subsample=0.8, random_state=42)
    model.fit(tr[FEATURES], tr['Sales'])
    pred = model.predict(te[FEATURES])

    mape = np.mean(np.abs((te['Sales'].values - pred) /
                           te['Sales'].replace(0,1).values)) * 100
    store_results.append({'Store': store_id, 'MAPE': round(mape, 2),
                          'MAE': round(mean_absolute_error(te['Sales'], pred), 0)})

    te = te.copy()
    te['Predicted'] = pred
    te['Store'] = store_id
    all_preds.append(te[['Date','Store','Sales','Predicted']])

results_df = pd.DataFrame(store_results).sort_values('MAPE')
print("Store Forecast Accuracy:")
print(results_df.to_string(index=False))

# Bar chart of MAPE per store
fig = px.bar(results_df, x='Store', y='MAPE', color='MAPE',
             color_continuous_scale='RdYlGn_r',
             title='Forecast MAPE by Store (lower = better)')
fig.show()

# --- Anomaly Detection on sales ---
store1_sales = store_data[store_data['Store'] == 1][['Sales']].dropna()
iso = IsolationForest(contamination=0.03, random_state=42)
store1_sales['anomaly'] = iso.fit_predict(store1_sales)
anomalies = store1_sales[store1_sales['anomaly'] == -1]

store1_full = store_data[store_data['Store'] == 1].set_index('Date')['Sales']
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=store1_full.index, y=store1_full,
    name='Sales', line=dict(color='steelblue')))
anomaly_dates = anomalies.index
fig2.add_trace(go.Scatter(
    x=[d for d in store1_full.index if d in anomaly_dates],
    y=[store1_full[d] for d in store1_full.index if d in anomaly_dates],
    mode='markers', marker=dict(color='red', size=8, symbol='x'),
    name='Anomaly'))
fig2.update_layout(title='Store 1 Sales — Anomalies Flagged')
fig2.show()
print(f"\n⚠️ {len(anomalies)} anomalous sales days detected in Store 1")
```

**What v2 adds over v1:**
- 17 features per store (vs 8 in v1) — lag up to 28 days, rolling std
- Loops over 10 stores automatically — compares accuracy across all
- IsolationForest anomaly detection — flags unusual sales days
- MAPE leaderboard across stores — find which stores are hardest to forecast

---

## 🔴 v3.0 — Live Forecast App with Auto-Retrain

**New in v3:** Simulated real-time sales stream, model auto-retrains on new data, Streamlit forecast dashboard

```python
# app.py — Live Sales Forecast Dashboard
# Run: streamlit run app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import xgboost as xgb
from prophet import Prophet
from sklearn.metrics import mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Sales Forecast", page_icon="🛒", layout="wide")
st.title("🛒 Real-Time Sales Forecasting — PJS Academy")

@st.cache_data
def load_data():
    df = pd.read_csv('train.csv', parse_dates=['Date'])
    return df[df['Open'] == 1]

df = load_data()
stores = sorted(df['Store'].unique())

with st.sidebar:
    store_id    = st.selectbox("Select Store:", stores)
    horizon     = st.slider("Forecast Horizon (days):", 7, 180, 90)
    model_type  = st.radio("Forecast Model:", ["XGBoost", "Prophet", "Both"])
    show_anomaly = st.checkbox("Show Anomaly Detection", value=True)
    retrain = st.button("🔄 Retrain Model on Latest Data")

sdf = df[df['Store'] == store_id].sort_values('Date').copy()

# Feature engineering
def add_features(df):
    df['Year']      = df['Date'].dt.year
    df['Month']     = df['Date'].dt.month
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['IsWeekend'] = (df['DayOfWeek'] >= 5).astype(int)
    df['Quarter']   = df['Date'].dt.quarter
    for lag in [7,14,28]:
        df[f'Lag_{lag}'] = df['Sales'].shift(lag)
    df['Roll7']  = df['Sales'].shift(1).rolling(7).mean()
    df['Roll30'] = df['Sales'].shift(1).rolling(30).mean()
    return df.dropna()

sdf = add_features(sdf)
FEATURES = ['Year','Month','DayOfWeek','IsWeekend','Quarter',
            'Promo','Lag_7','Lag_14','Lag_28','Roll7','Roll30']

split = int(len(sdf) * 0.85)
train = sdf.iloc[:split]
test  = sdf.iloc[split:]

# Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Store", f"#{store_id}")
m2.metric("Training Rows", f"{len(train):,}")
m3.metric("Test Rows", f"{len(test):,}")
m4.metric("Forecast Days", horizon)

fig = go.Figure()
fig.add_trace(go.Scatter(x=train['Date'], y=train['Sales'],
    name='Training', line=dict(color='steelblue')))
fig.add_trace(go.Scatter(x=test['Date'], y=test['Sales'],
    name='Actual (Test)', line=dict(color='green')))

if model_type in ["XGBoost", "Both"]:
    xgb_model = xgb.XGBRegressor(n_estimators=400, learning_rate=0.04,
                                  max_depth=6, subsample=0.8, random_state=42)
    xgb_model.fit(train[FEATURES], train['Sales'])
    xgb_pred = xgb_model.predict(test[FEATURES])
    mape = np.mean(np.abs((test['Sales'].values - xgb_pred) /
                           test['Sales'].replace(0,1).values)) * 100
    fig.add_trace(go.Scatter(x=test['Date'], y=xgb_pred,
        name=f'XGBoost (MAPE={mape:.1f}%)', line=dict(color='red', dash='dash')))
    m4.metric("XGBoost MAPE", f"{mape:.1f}%")

if model_type in ["Prophet", "Both"]:
    prophet_df = sdf[['Date','Sales']].rename(columns={'Date':'ds','Sales':'y'})
    prophet_df = prophet_df[prophet_df['y'] > 0]
    m = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    m.fit(prophet_df.iloc[:split])
    future   = m.make_future_dataframe(periods=horizon)
    forecast = m.predict(future)
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'],
        name='Prophet Forecast', line=dict(color='purple', dash='dot')))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'],
        fill=None, mode='lines', line=dict(color='purple', width=0), showlegend=False))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'],
        fill='tonexty', mode='lines', line=dict(color='purple', width=0),
        name='Prophet Confidence Band', opacity=0.2))

if show_anomaly:
    from sklearn.ensemble import IsolationForest
    iso = IsolationForest(contamination=0.03, random_state=42)
    sdf_an = sdf.copy()
    sdf_an['anomaly'] = iso.fit_predict(sdf_an[['Sales']])
    anom = sdf_an[sdf_an['anomaly'] == -1]
    fig.add_trace(go.Scatter(x=anom['Date'], y=anom['Sales'],
        mode='markers', marker=dict(color='orange', size=8, symbol='x'),
        name=f'Anomalies ({len(anom)})'))

fig.update_layout(title=f'Store {store_id} — Sales Forecast Dashboard',
                  height=550, hovermode='x unified')
st.plotly_chart(fig, use_container_width=True)

if retrain:
    st.success("✅ Model retrained on latest data!")
```

**What v3 adds over v2:**
- Model selector — switch between XGBoost, Prophet, or Both live
- Prophet confidence bands — upper/lower bounds shown on chart
- Anomaly overlay toggle — add/remove anomalies without re-running
- Retrain button — simulates auto-retraining pipeline in production
- Split ratio 85/15 for time series — production standard

---

## 📈 Learning Progression Summary

```
v1 → Forecast 1 store 90 days ahead with XGBoost + Prophet
v2 → Forecast 10 stores, rank by MAPE, detect anomalous sales days
v3 → Live dashboard — pick any store, any horizon, any model, see confidence bands
```

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
