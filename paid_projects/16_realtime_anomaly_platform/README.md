# 🚨 Project 16 — Real-Time Anomaly Detection & Alerting Platform

**Phase 4 — ML Engineering** | Beginner → Real-Time (3 Versions) | ⭐⭐⭐⭐⭐ Flagship

> This is a **full implementation** — every line runs. No paid APIs, no cloud account needed.
> By v3 you have a genuinely real-time streaming platform with a live dashboard, online-learning ML, and an alerting system. This is the single most impressive project in the course.

---

## 🗺️ Version Roadmap

| Version | What You Build | Complexity |
|---------|---------------|------------|
| v1.0 — Batch | Isolation Forest anomaly detection on historical data | ⭐⭐ |
| v2.0 — Streaming Sim | Online learning (River) on a simulated live stream | ⭐⭐⭐⭐ |
| v3.0 — Real-Time Platform | FastAPI ingestion + live Streamlit dashboard + alerts | ⭐⭐⭐⭐⭐ |

**Use case:** Monitoring server metrics, IoT sensors, transaction streams, or website traffic — detect when something goes wrong *the moment it happens*.

---

## 📦 Setup

```bash
pip install pandas numpy scikit-learn river streamlit plotly fastapi uvicorn requests
```

---

## 🟢 v1.0 — Batch Anomaly Detection

**Goal:** Learn what "normal" looks like from historical data, then flag outliers.

Create `v1_batch.py`:

```python
"""
v1 — Batch anomaly detection with Isolation Forest.
Trains on historical metrics, flags anomalies, visualises results.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def generate_metrics(n=2000, seed=42):
    """Simulate realistic server metrics with injected anomalies."""
    rng = np.random.default_rng(seed)
    t = np.arange(n)

    # Normal patterns: daily cycle + noise
    cpu = 50 + 15 * np.sin(t / 100) + rng.normal(0, 5, n)
    memory = 60 + 10 * np.sin(t / 120 + 1) + rng.normal(0, 4, n)
    latency = 100 + 20 * np.sin(t / 90) + rng.normal(0, 8, n)
    requests = 500 + 100 * np.sin(t / 110) + rng.normal(0, 30, n)

    df = pd.DataFrame({
        "timestamp": pd.date_range("2026-01-01", periods=n, freq="min"),
        "cpu": cpu, "memory": memory, "latency": latency, "requests": requests,
    })

    # Inject anomalies (spikes / crashes)
    anomaly_idx = rng.choice(n, size=40, replace=False)
    df.loc[anomaly_idx, "cpu"] += rng.normal(40, 10, len(anomaly_idx))
    df.loc[anomaly_idx, "latency"] += rng.normal(150, 30, len(anomaly_idx))
    df["is_anomaly_true"] = 0
    df.loc[anomaly_idx, "is_anomaly_true"] = 1
    return df


def train_detector(df, features, contamination=0.02):
    """Fit Isolation Forest and score every row."""
    X = df[features].values
    scaler = StandardScaler().fit(X)
    model = IsolationForest(
        n_estimators=200, contamination=contamination, random_state=42
    ).fit(scaler.transform(X))

    df = df.copy()
    df["anomaly_score"] = -model.decision_function(scaler.transform(X))  # higher = weirder
    df["is_anomaly_pred"] = (model.predict(scaler.transform(X)) == -1).astype(int)
    return df, model, scaler


def evaluate(df):
    from sklearn.metrics import classification_report
    print(classification_report(df["is_anomaly_true"], df["is_anomaly_pred"],
                                target_names=["Normal", "Anomaly"]))


def plot(df):
    fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    axes[0].plot(df["timestamp"], df["cpu"], color="steelblue", lw=0.8, label="CPU")
    anoms = df[df["is_anomaly_pred"] == 1]
    axes[0].scatter(anoms["timestamp"], anoms["cpu"], color="red", s=25, label="Anomaly", zorder=5)
    axes[0].set_title("CPU with Detected Anomalies"); axes[0].legend()

    axes[1].plot(df["timestamp"], df["anomaly_score"], color="purple", lw=0.8)
    axes[1].axhline(df["anomaly_score"].quantile(0.98), color="red", ls="--", label="Alert threshold")
    axes[1].set_title("Anomaly Score Over Time"); axes[1].legend()
    plt.tight_layout(); plt.savefig("v1_anomalies.png", dpi=130); plt.show()


if __name__ == "__main__":
    df = generate_metrics()
    features = ["cpu", "memory", "latency", "requests"]
    scored, model, scaler = train_detector(df, features)
    evaluate(scored)
    plot(scored)
    print(f"\nDetected {scored['is_anomaly_pred'].sum()} anomalies "
          f"out of {len(scored)} points.")
```

Run: `python v1_batch.py`

**What v1 teaches:** Unsupervised anomaly detection, why you scale features, how Isolation Forest isolates outliers, precision/recall trade-offs.

---

## 🟡 v2.0 — Online Learning on a Simulated Stream

**Problem with v1:** It trained once. Real systems drift — "normal" changes over time. v2 uses **online learning** that updates with every new data point.

Create `v2_stream.py`:

```python
"""
v2 — Streaming anomaly detection with online learning.
Uses River's Half-Space Trees — updates the model on every new point,
no retraining, adapts to drift automatically.
"""
import time
import numpy as np
import pandas as pd
from river import anomaly, preprocessing, compose


def metric_stream(seed=7):
    """Infinite generator simulating a live metrics feed."""
    rng = np.random.default_rng(seed)
    t = 0
    while True:
        cpu = 50 + 15 * np.sin(t / 100) + rng.normal(0, 5)
        memory = 60 + 10 * np.sin(t / 120 + 1) + rng.normal(0, 4)
        latency = 100 + 20 * np.sin(t / 90) + rng.normal(0, 8)
        requests = 500 + 100 * np.sin(t / 110) + rng.normal(0, 30)

        # 2% chance of an anomaly spike
        is_anom = rng.random() < 0.02
        if is_anom:
            cpu += rng.normal(40, 10)
            latency += rng.normal(150, 30)

        yield {"cpu": cpu, "memory": memory,
               "latency": latency, "requests": requests}, int(is_anom)
        t += 1


def build_model():
    """Online pipeline: scale + Half-Space Trees anomaly detector."""
    return compose.Pipeline(
        preprocessing.StandardScaler(),
        anomaly.HalfSpaceTrees(n_trees=25, height=15, window_size=250, seed=42),
    )


def run_stream(n=1500, alert_quantile=0.98):
    model = build_model()
    scores, labels, alerts = [], [], 0
    stream = metric_stream()

    # Warm-up: let the model learn "normal" first
    for _ in range(250):
        x, _ = next(stream)
        model.learn_one(x)

    print("Streaming... (Ctrl+C to stop)\n")
    for i in range(n):
        x, true_label = next(stream)
        score = model.score_one(x)      # anomaly score 0..1
        model.learn_one(x)              # THEN update the model
        scores.append(score)
        labels.append(true_label)

        # Dynamic threshold from recent scores
        if len(scores) > 300:
            threshold = np.quantile(scores[-300:], alert_quantile)
            if score > threshold:
                alerts += 1
                flag = "🚨 ANOMALY" if true_label else "⚠️  false alarm"
                print(f"[{i:04d}] score={score:.3f}  {flag}  "
                      f"cpu={x['cpu']:.0f} latency={x['latency']:.0f}")
        time.sleep(0.001)  # simulate real-time cadence

    hits = sum(1 for s, l in zip(scores, labels)
               if l == 1 and s > np.quantile(scores, alert_quantile))
    total_anoms = sum(labels)
    print(f"\nCaught {hits}/{total_anoms} true anomalies. Total alerts fired: {alerts}")


if __name__ == "__main__":
    run_stream()
```

Run: `python v2_stream.py`

**What v2 adds over v1:**
- **Online learning** — model updates on every point, no retraining
- **Concept-drift resilience** — sliding window keeps "normal" current
- **Streaming architecture** — process one point at a time (constant memory)
- **Dynamic thresholds** — alert bar adapts to recent behaviour

---

## 🔴 v3.0 — Real-Time Platform (Ingestion API + Live Dashboard + Alerts)

**The real deal.** Three components running together:
1. **FastAPI ingestion service** — receives metrics via HTTP, scores them, stores + alerts
2. **A producer** — simulates devices/servers pushing metrics (replace with real sources)
3. **Live Streamlit dashboard** — auto-refreshing charts, live alert feed, KPIs

### Component A — `api.py` (ingestion + scoring service)

```python
"""
v3 API — Real-time ingestion and scoring service.
Run: uvicorn api:app --reload --port 8000
"""
from fastapi import FastAPI
from pydantic import BaseModel
from collections import deque
from datetime import datetime
import numpy as np
from river import anomaly, preprocessing, compose

app = FastAPI(title="Anomaly Platform — PJ's Academy", version="3.0")

# ---- Model + rolling state (in-memory; use Redis/DB in production) ----
model = compose.Pipeline(
    preprocessing.StandardScaler(),
    anomaly.HalfSpaceTrees(n_trees=25, height=15, window_size=250, seed=42),
)
recent_scores = deque(maxlen=300)
history = deque(maxlen=500)     # last 500 readings for the dashboard
alerts = deque(maxlen=100)      # last 100 alerts
warmup = {"count": 0}


class Metric(BaseModel):
    cpu: float
    memory: float
    latency: float
    requests: float
    source: str = "unknown"


@app.post("/ingest")
def ingest(m: Metric):
    x = {"cpu": m.cpu, "memory": m.memory,
         "latency": m.latency, "requests": m.requests}

    # Warm-up phase: learn only
    if warmup["count"] < 200:
        model.learn_one(x)
        warmup["count"] += 1
        return {"status": "warming_up", "progress": warmup["count"]}

    score = model.score_one(x)
    model.learn_one(x)
    recent_scores.append(score)

    threshold = float(np.quantile(recent_scores, 0.98)) if len(recent_scores) > 50 else 1.0
    is_alert = score > threshold

    record = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "source": m.source, "score": round(score, 3),
        "threshold": round(threshold, 3), "alert": is_alert, **x,
    }
    history.append(record)
    if is_alert:
        alerts.append(record)

    return {"status": "scored", "score": round(score, 3),
            "alert": is_alert, "threshold": round(threshold, 3)}


@app.get("/history")
def get_history():
    return list(history)


@app.get("/alerts")
def get_alerts():
    return list(alerts)


@app.get("/stats")
def stats():
    return {
        "readings": len(history),
        "alerts": len(alerts),
        "warmed_up": warmup["count"] >= 200,
        "avg_score": round(np.mean(recent_scores), 3) if recent_scores else 0,
    }
```

### Component B — `producer.py` (simulates live sources)

```python
"""
v3 Producer — pushes metrics to the API in real time.
Run (after starting the API): python producer.py
Replace generate_reading() with real sensor/log/transaction data.
"""
import time
import numpy as np
import requests

API = "http://localhost:8000/ingest"
SOURCES = ["web-01", "web-02", "db-01", "cache-01"]


def generate_reading(t, rng):
    cpu = 50 + 15 * np.sin(t / 100) + rng.normal(0, 5)
    memory = 60 + 10 * np.sin(t / 120 + 1) + rng.normal(0, 4)
    latency = 100 + 20 * np.sin(t / 90) + rng.normal(0, 8)
    requests_ = 500 + 100 * np.sin(t / 110) + rng.normal(0, 30)
    if rng.random() < 0.03:              # inject anomaly
        cpu += rng.normal(45, 10)
        latency += rng.normal(160, 30)
    return cpu, memory, latency, requests_


def main():
    rng = np.random.default_rng()
    t = 0
    print("Producing metrics → API. Ctrl+C to stop.")
    while True:
        cpu, mem, lat, req = generate_reading(t, rng)
        payload = {"cpu": cpu, "memory": mem, "latency": lat,
                   "requests": req, "source": rng.choice(SOURCES)}
        try:
            r = requests.post(API, json=payload, timeout=2).json()
            if r.get("alert"):
                print(f"🚨 ALERT {payload['source']} score={r['score']}")
        except requests.RequestException:
            print("API not reachable — is uvicorn running?")
        t += 1
        time.sleep(0.3)   # ~3 readings/sec


if __name__ == "__main__":
    main()
```

### Component C — `dashboard.py` (live monitoring UI)

```python
"""
v3 Dashboard — live auto-refreshing monitoring UI.
Run (after API + producer): streamlit run dashboard.py
"""
import time
import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Anomaly Platform", page_icon="🚨", layout="wide")
API = "http://localhost:8000"

st.title("🚨 Real-Time Anomaly Detection — PJ's Academy")
placeholder = st.empty()

REFRESH = st.sidebar.slider("Refresh every (seconds)", 1, 10, 2)
st.sidebar.info("Start order:\n1. `uvicorn api:app`\n2. `python producer.py`\n3. this dashboard")

def fetch(path):
    try:
        return requests.get(f"{API}/{path}", timeout=2).json()
    except requests.RequestException:
        return None

while True:
    stats = fetch("stats")
    history = fetch("history")
    alerts = fetch("alerts")

    with placeholder.container():
        if not stats:
            st.error("Can't reach the API. Start it with `uvicorn api:app --port 8000`.")
            time.sleep(REFRESH); continue

        if not stats["warmed_up"]:
            st.warning("Model warming up — start the producer to feed it data...")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Readings", stats["readings"])
        c2.metric("Alerts", stats["alerts"])
        c3.metric("Avg Anomaly Score", stats["avg_score"])
        c4.metric("Status", "🟢 Live" if stats["warmed_up"] else "🟡 Warming")

        if history:
            df = pd.DataFrame(history)
            df["ts"] = pd.to_datetime(df["ts"])

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df["ts"], y=df["cpu"], name="CPU",
                                     line=dict(color="#29b5e8")))
            fig.add_trace(go.Scatter(x=df["ts"], y=df["latency"], name="Latency",
                                     line=dict(color="#f0a500"), yaxis="y2"))
            anoms = df[df["alert"]]
            fig.add_trace(go.Scatter(x=anoms["ts"], y=anoms["cpu"], mode="markers",
                                     name="Anomaly", marker=dict(color="red", size=10, symbol="x")))
            fig.update_layout(
                title="Live Metrics", height=400,
                yaxis=dict(title="CPU"), yaxis2=dict(title="Latency", overlaying="y", side="right"),
                template="plotly_dark", hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=df["ts"], y=df["score"], name="Anomaly Score",
                                      fill="tozeroy", line=dict(color="#e74c3c")))
            fig2.add_trace(go.Scatter(x=df["ts"], y=df["threshold"], name="Alert Threshold",
                                      line=dict(color="orange", dash="dash")))
            fig2.update_layout(title="Anomaly Score vs Threshold", height=260, template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("🔔 Live Alert Feed")
        if alerts:
            adf = pd.DataFrame(alerts)[["ts", "source", "score", "cpu", "latency"]]
            st.dataframe(adf.tail(15).iloc[::-1], use_container_width=True)
        else:
            st.success("No anomalies detected yet — all systems normal ✅")

    time.sleep(REFRESH)
```

### Run the whole platform (3 terminals)

```bash
# Terminal 1 — ingestion API
uvicorn api:app --reload --port 8000

# Terminal 2 — data producer
python producer.py

# Terminal 3 — live dashboard
streamlit run dashboard.py
```

Open the Streamlit URL and watch metrics stream in, anomalies get flagged with red X's, and the alert feed update **in real time**.

**What v3 adds over v2:**
- **Distributed architecture** — producer → API → dashboard (like real systems)
- **HTTP ingestion** — any device/service can push data
- **Live dashboard** — auto-refreshing charts + KPIs + alert feed
- **Production shape** — swap the producer for real Kafka/logs, swap in-memory for Redis, and this is deployable

---

## 📈 Learning Progression Summary

```
v1 → Detect anomalies in a saved dataset (learn the concept)
v2 → Detect them live with online learning that adapts to drift
v3 → A full real-time platform: ingestion API + producer + live dashboard + alerts
```

## 🏢 Real-World Connection
This is exactly how Datadog, New Relic, and Grafana anomaly detection work under the hood. Fraud teams, DevOps/SRE teams, and IoT platforms all run pipelines shaped like this.

## 📝 Resume Line
*"Built a real-time anomaly detection platform (FastAPI + River online learning + Streamlit) with HTTP ingestion, drift-adaptive scoring, and a live alerting dashboard."*

---

*Course: [Data Science Mastery — PJ's Academy](https://pjsacademy.com)*
