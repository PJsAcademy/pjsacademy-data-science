# 📈 Project 07 — Stock Price Dashboard

**Phase 3 — Data Science** | Beginner → Real-Time (3 Versions)

---

## 🗺️ Version Roadmap

| Version | What You Build | Complexity |
|---------|---------------|------------|
| v1.0 — Starter | Fetch historical data + candlestick chart | ⭐ Beginner |
| v2.0 — Improved | Technical indicators + multi-stock comparison + Streamlit app | ⭐⭐ Intermediate |
| v3.0 — Real-Time | Live WebSocket price feed + auto-refresh dashboard + alerts | ⭐⭐⭐ Advanced |

---

## 📦 Libraries Needed
```bash
pip install yfinance plotly streamlit pandas ta websocket-client requests
```

---

## 🟢 v1.0 — Historical Dashboard

**Skills:** yfinance, Pandas, Plotly candlestick, moving averages

```python
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Fetch 1 year of Apple data
ticker = yf.Ticker("AAPL")
df = ticker.history(period="1y")

# Moving averages
df['MA20'] = df['Close'].rolling(20).mean()
df['MA50'] = df['Close'].rolling(50).mean()

# Candlestick + volume
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])

fig.add_trace(go.Candlestick(x=df.index,
    open=df['Open'], high=df['High'],
    low=df['Low'], close=df['Close'], name='AAPL'), row=1, col=1)

fig.add_trace(go.Scatter(x=df.index, y=df['MA20'],
    name='MA20', line=dict(color='blue', width=1)), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['MA50'],
    name='MA50', line=dict(color='orange', width=1)), row=1, col=1)

fig.add_trace(go.Bar(x=df.index, y=df['Volume'],
    name='Volume', marker_color='lightblue'), row=2, col=1)

fig.update_layout(title='AAPL — 1 Year Stock Dashboard',
                  xaxis_rangeslider_visible=False, height=600)
fig.show()

print(f"Current Price: ${df['Close'].iloc[-1]:.2f}")
print(f"52W High: ${df['High'].max():.2f}")
print(f"52W Low:  ${df['Low'].min():.2f}")
```

**What v1 teaches:** How to fetch real financial data, build an OHLCV candlestick chart, and overlay moving averages.

---

## 🟡 v2.0 — Technical Analysis + Multi-Stock App

**New in v2:** RSI, MACD, Bollinger Bands, multi-stock comparison, Streamlit dashboard

```python
# Technical indicators with 'ta' library
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ta  # Technical Analysis library

def get_stock_data(symbol, period='1y'):
    df = yf.Ticker(symbol).history(period=period)
    df.index = df.index.tz_localize(None)

    # Trend indicators
    df['MA20']  = df['Close'].rolling(20).mean()
    df['MA50']  = df['Close'].rolling(50).mean()
    df['MA200'] = df['Close'].rolling(200).mean()

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(df['Close'], window=20, window_dev=2)
    df['BB_upper'] = bb.bollinger_hband()
    df['BB_lower'] = bb.bollinger_lband()
    df['BB_mid']   = bb.bollinger_mavg()

    # RSI (0-100, overbought >70, oversold <30)
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()

    # MACD
    macd = ta.trend.MACD(df['Close'])
    df['MACD']        = macd.macd()
    df['MACD_signal'] = macd.macd_signal()
    df['MACD_hist']   = macd.macd_diff()

    # Daily return + volatility
    df['Return']     = df['Close'].pct_change() * 100
    df['Volatility'] = df['Return'].rolling(20).std()
    return df

df = get_stock_data('AAPL')

# 4-panel chart
fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                    row_heights=[0.45, 0.2, 0.2, 0.15],
                    subplot_titles=['Price + Bollinger Bands', 'Volume', 'RSI', 'MACD'])

# Panel 1 — Candlestick + Bollinger
fig.add_trace(go.Candlestick(x=df.index, open=df['Open'],
    high=df['High'], low=df['Low'], close=df['Close']), row=1, col=1)
for band, color in [('BB_upper','rgba(255,100,100,0.3)'),
                    ('BB_mid','blue'), ('BB_lower','rgba(100,255,100,0.3)')]:
    fig.add_trace(go.Scatter(x=df.index, y=df[band], name=band,
        line=dict(color=color, width=1)), row=1, col=1)

# Panel 2 — Volume
fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume'), row=2, col=1)

# Panel 3 — RSI with overbought/oversold lines
fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI',
    line=dict(color='purple')), row=3, col=1)
fig.add_hline(y=70, line_dash='dash', line_color='red', row=3, col=1)
fig.add_hline(y=30, line_dash='dash', line_color='green', row=3, col=1)

# Panel 4 — MACD
fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD'), row=4, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['MACD_signal'],
    name='Signal', line=dict(dash='dash')), row=4, col=1)
fig.add_trace(go.Bar(x=df.index, y=df['MACD_hist'], name='Histogram'), row=4, col=1)

fig.update_layout(height=900, title='AAPL — Full Technical Analysis',
                  xaxis_rangeslider_visible=False)
fig.show()

# Multi-stock performance comparison
symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
comparison = pd.DataFrame()
for sym in symbols:
    d = yf.Ticker(sym).history(period='1y')['Close']
    comparison[sym] = (d / d.iloc[0] - 1) * 100  # Normalised % return

fig2 = go.Figure()
for sym in symbols:
    fig2.add_trace(go.Scatter(x=comparison.index, y=comparison[sym], name=sym))
fig2.update_layout(title='1-Year Performance Comparison (%)',
                   yaxis_title='Return %', height=450)
fig2.show()
```

**What v2 adds over v1:**
- RSI — shows when a stock is overbought or oversold
- MACD — momentum signal used by professional traders
- Bollinger Bands — volatility envelope around price
- Normalised multi-stock comparison on one chart

---

## 🔴 v3.0 — Real-Time Dashboard with Price Alerts

**New in v3:** Auto-refresh every 60 seconds, price alert system, portfolio tracker, Streamlit live dashboard

```python
# app.py — Real-Time Streamlit Dashboard
# Run: streamlit run app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ta, time
from datetime import datetime

st.set_page_config(page_title="Live Stock Dashboard", page_icon="📈", layout="wide")
st.title("📈 Real-Time Stock Dashboard — PJS Academy")

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Settings")
    symbol    = st.text_input("Stock Symbol", "AAPL").upper()
    period    = st.selectbox("Period", ["1d","5d","1mo","3mo","6mo","1y","2y"])
    interval  = st.selectbox("Interval", ["1m","5m","15m","1h","1d"])
    refresh   = st.slider("Auto-refresh (seconds)", 30, 300, 60)

    st.header("🚨 Price Alerts")
    alert_high = st.number_input("Alert if price ABOVE ($)", value=0.0)
    alert_low  = st.number_input("Alert if price BELOW ($)", value=0.0)

    st.header("💼 Portfolio")
    portfolio_input = st.text_area("Tickers + Shares (one per line)",
                                    "AAPL 10\nMSFT 5\nGOOGL 2")

# --- Fetch Data ---
@st.cache_data(ttl=refresh)
def fetch(sym, per, intv):
    df = yf.Ticker(sym).history(period=per, interval=intv)
    df.index = df.index.tz_localize(None) if df.index.tz else df.index
    if len(df) > 0:
        df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
        df['MA20'] = df['Close'].rolling(20).mean()
    return df

df = fetch(symbol, period, interval)

if df.empty:
    st.error(f"No data for {symbol}")
    st.stop()

current_price = df['Close'].iloc[-1]
prev_price    = df['Close'].iloc[-2] if len(df) > 1 else current_price
change        = current_price - prev_price
change_pct    = (change / prev_price) * 100

# --- Price Alerts ---
if alert_high > 0 and current_price > alert_high:
    st.error(f"🚨 ALERT: {symbol} is ABOVE ${alert_high:.2f}! Current: ${current_price:.2f}")
if alert_low > 0 and current_price < alert_low:
    st.warning(f"🚨 ALERT: {symbol} is BELOW ${alert_low:.2f}! Current: ${current_price:.2f}")

# --- Metrics Row ---
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Current Price", f"${current_price:.2f}", f"{change:+.2f} ({change_pct:+.2f}%)")
m2.metric("Day High", f"${df['High'].iloc[-1]:.2f}")
m3.metric("Day Low",  f"${df['Low'].iloc[-1]:.2f}")
m4.metric("RSI", f"{df['RSI'].iloc[-1]:.1f}",
          "Overbought" if df['RSI'].iloc[-1] > 70 else "Oversold" if df['RSI'].iloc[-1] < 30 else "Neutral")
m5.metric("Volume", f"{df['Volume'].iloc[-1]:,.0f}")

# --- Chart ---
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])
fig.add_trace(go.Candlestick(x=df.index, open=df['Open'],
    high=df['High'], low=df['Low'], close=df['Close']), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='MA20',
    line=dict(color='orange', width=1)), row=1, col=1)
fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume'), row=2, col=1)
fig.update_layout(height=500, xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

# --- Portfolio Tracker ---
st.markdown("---")
st.subheader("💼 Portfolio Summary")
rows = []
for line in portfolio_input.strip().split('\n'):
    parts = line.strip().split()
    if len(parts) == 2:
        sym2, shares = parts[0].upper(), float(parts[1])
        try:
            price2 = yf.Ticker(sym2).history(period='1d')['Close'].iloc[-1]
            rows.append({'Ticker': sym2, 'Shares': shares,
                         'Price': f"${price2:.2f}",
                         'Value': f"${price2 * shares:,.2f}"})
        except:
            pass
if rows:
    port_df = pd.DataFrame(rows)
    st.dataframe(port_df, use_container_width=True)
    total = sum(float(r['Value'].replace('$','').replace(',','')) for r in rows)
    st.metric("Total Portfolio Value", f"${total:,.2f}")

# Auto-refresh
st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')} | Refreshes every {refresh}s")
st.button("🔄 Refresh Now")
time.sleep(0)
```

**What v3 adds over v2:**
- `ttl=refresh` caching — auto-fetches new data every N seconds
- Price alert system — highlights when your target is hit
- Portfolio tracker — shows total portfolio value live
- RSI overbought/oversold signal in the metrics row

---

## 📈 Learning Progression Summary

```
v1 → Plot 1 year of historical stock price with candlestick + MA
v2 → Full technical analysis (RSI, MACD, Bollinger Bands) + multi-stock comparison
v3 → Live dashboard auto-refreshing with price alerts + portfolio tracker
```

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
