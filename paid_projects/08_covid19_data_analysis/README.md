# 🦠 Project 08 — COVID-19 Data Analysis

**Phase 3 — Data Science** | Beginner → Real-Time (3 Versions)

---

## 🗺️ Version Roadmap

| Version | What You Build | Complexity |
|---------|---------------|------------|
| v1.0 — Starter | Static choropleth map + country comparison charts | ⭐ Beginner |
| v2.0 — Improved | Animated map over time + wave detection + vaccine impact analysis | ⭐⭐ Intermediate |
| v3.0 — Real-Time | Live data pipeline + auto-updating dashboard + predictive alert | ⭐⭐⭐ Advanced |

---

## 📦 Libraries Needed
```bash
pip install pandas plotly requests streamlit scipy
```

---

## 🟢 v1.0 — Static Global Analysis

**Skills:** Pandas, Plotly choropleth, groupby, time series line charts

```python
import pandas as pd
import plotly.express as px

url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
df = pd.read_csv(url)
df = df[df['continent'].notna()]  # remove continent rows

cols = ['location','date','total_cases','new_cases','total_deaths','people_vaccinated','population']
df = df[cols].copy()
df['date'] = pd.to_datetime(df['date'])
df['cases_per_million'] = (df['total_cases'] / df['population']) * 1_000_000
df.fillna(0, inplace=True)

# Latest snapshot per country
latest = df.groupby('location').last().reset_index()

# World map
fig = px.choropleth(latest, locations='location', locationmode='country names',
                    color='cases_per_million',
                    title='COVID-19 Cases per Million Population',
                    color_continuous_scale='Reds')
fig.show()

# Top 10 countries
top10 = latest.nlargest(10, 'total_cases')
fig2 = px.bar(top10, x='location', y='total_cases',
              title='Top 10 Countries by Total Cases',
              color='total_cases', color_continuous_scale='Reds')
fig2.show()

# 4-country time series
countries = ['India', 'United States', 'United Kingdom', 'Brazil']
fig3 = px.line(df[df['location'].isin(countries)],
               x='date', y='new_cases', color='location',
               title='Daily New Cases — Country Comparison')
fig3.show()
```

**What v1 teaches:** How to work with 200K+ row real-world data — cleaning, groupby, choropleth maps.

---

## 🟡 v2.0 — Animated Maps + Wave Detection + Vaccine Impact

**New in v2:** Animated choropleth over time, wave detection algorithm, vaccination vs death rate correlation

```python
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import find_peaks

url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
df = pd.read_csv(url, parse_dates=['date'])
df = df[df['continent'].notna()].fillna(0)

# --- Animated World Map (cases per million over time) ---
monthly = df.copy()
monthly['month'] = monthly['date'].dt.to_period('M').astype(str)
monthly_agg = (monthly.groupby(['location', 'month'])
               .agg(cases_pm=('total_cases', 'max'),
                    population=('population', 'first'))
               .reset_index())
monthly_agg['cases_per_million'] = (monthly_agg['cases_pm'] /
                                     monthly_agg['population'].replace(0,1)) * 1e6

fig_anim = px.choropleth(monthly_agg, locations='location',
                          locationmode='country names',
                          color='cases_per_million',
                          animation_frame='month',
                          color_continuous_scale='Reds',
                          title='COVID-19 Spread — Month by Month Animation',
                          range_color=[0, 150000])
fig_anim.show()

# --- Wave Detection for India ---
india = df[df['location'] == 'India'][['date', 'new_cases_smoothed']].dropna()
india = india.set_index('date').resample('W').sum().reset_index()
india['smoothed'] = india['new_cases_smoothed'].rolling(4, center=True).mean()

peaks, properties = find_peaks(india['smoothed'].fillna(0),
                                distance=8, prominence=50000)
print(f"India COVID Waves detected: {len(peaks)}")
for i, p in enumerate(peaks):
    print(f"  Wave {i+1}: {india.iloc[p]['date'].strftime('%b %Y')} — "
          f"{india.iloc[p]['smoothed']:,.0f} cases/week")

fig_waves = go.Figure()
fig_waves.add_trace(go.Scatter(x=india['date'], y=india['smoothed'],
    name='Weekly Cases', line=dict(color='red')))
fig_waves.add_trace(go.Scatter(
    x=india.iloc[peaks]['date'], y=india.iloc[peaks]['smoothed'],
    mode='markers', marker=dict(size=12, color='gold', symbol='star'),
    name='Wave Peaks'))
fig_waves.update_layout(title='India COVID Waves — Auto-Detected')
fig_waves.show()

# --- Vaccine Impact: Did vaccination reduce deaths? ---
vacc_death = df[df['date'] >= '2021-01-01'].copy()
vacc_death['vacc_rate'] = (vacc_death['people_vaccinated'] /
                            vacc_death['population'].replace(0,1)) * 100
vacc_death['death_rate'] = (vacc_death['total_deaths'] /
                             vacc_death['total_cases'].replace(0,1)) * 100

latest_vd = vacc_death.groupby('location').last().reset_index()
latest_vd = latest_vd[(latest_vd['vacc_rate'] > 5) & (latest_vd['death_rate'] > 0)]

corr = latest_vd['vacc_rate'].corr(latest_vd['death_rate'])
fig_vacc = px.scatter(latest_vd, x='vacc_rate', y='death_rate',
                      hover_name='location', trendline='ols',
                      title=f'Vaccination Rate vs Death Rate (correlation: {corr:.3f})',
                      labels={'vacc_rate': 'Vaccination Rate (%)',
                              'death_rate': 'Case Fatality Rate (%)'})
fig_vacc.show()
print(f"\nCorrelation (vaccination vs death rate): {corr:.3f}")
print("Negative correlation = more vaccination → fewer deaths ✅" if corr < 0
      else "Weak/positive correlation — other factors dominant")
```

**What v2 adds over v1:**
- Animated choropleth — watch the pandemic spread month by month
- `find_peaks` algorithm — automatically detects wave peaks from the data
- Vaccination impact analysis — proves (or disproves) vaccine effectiveness with correlation

---

## 🔴 v3.0 — Live Auto-Updating Dashboard

**New in v3:** Auto-fetches latest data daily, trend prediction, country comparison selector, Streamlit live app

```python
# app.py — Live COVID Dashboard
# Run: streamlit run app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.signal import find_peaks
from datetime import datetime, timedelta
import requests

st.set_page_config(page_title="COVID-19 Live Dashboard", page_icon="🦠", layout="wide")
st.title("🦠 COVID-19 Live Global Dashboard — PJS Academy")

@st.cache_data(ttl=3600)  # Refresh data every hour
def load_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(url, parse_dates=['date'])
    df = df[df['continent'].notna()].fillna(0)
    df['cases_per_million'] = (df['total_cases'] / df['population'].replace(0,1)) * 1e6
    df['vacc_rate'] = (df['people_vaccinated'] / df['population'].replace(0,1)) * 100
    return df

with st.spinner("Loading latest COVID data..."):
    df = load_data()

latest = df.groupby('location').last().reset_index()
data_date = df['date'].max().strftime('%d %B %Y')
st.caption(f"Data as of: {data_date} | Source: Our World in Data")

# --- Global Metrics ---
st.subheader("🌍 Global Summary")
g1, g2, g3, g4 = st.columns(4)
g1.metric("Total Cases",  f"{latest['total_cases'].sum()/1e9:.2f}B")
g2.metric("Total Deaths", f"{latest['total_deaths'].sum()/1e6:.1f}M")
g3.metric("Vaccinated",   f"{latest['people_vaccinated'].sum()/1e9:.2f}B")
g4.metric("Countries",    f"{latest['location'].nunique()}")

# --- World Map ---
metric = st.selectbox("Map metric:", ['cases_per_million', 'total_cases', 'vacc_rate'])
fig_map = px.choropleth(latest, locations='location', locationmode='country names',
                         color=metric, color_continuous_scale='Reds',
                         title=f'World — {metric.replace("_"," ").title()}')
st.plotly_chart(fig_map, use_container_width=True)

# --- Country Comparison ---
st.subheader("🔍 Country Comparison")
available = sorted(df['location'].unique())
selected = st.multiselect("Select countries:", available,
                           default=['India', 'United States', 'United Kingdom'])
metric2 = st.selectbox("Compare by:", ['new_cases', 'new_deaths', 'people_vaccinated'])

if selected:
    filtered = df[df['location'].isin(selected)]
    fig_comp = px.line(filtered, x='date', y=metric2, color='location',
                       title=f'{metric2.replace("_"," ").title()} — Country Comparison')
    st.plotly_chart(fig_comp, use_container_width=True)

# --- Wave Detection ---
st.subheader("🌊 Wave Detection")
wave_country = st.selectbox("Detect waves for:", available, index=available.index('India'))
country_df = df[df['location'] == wave_country][['date','new_cases_smoothed']].dropna()
country_df = country_df.set_index('date').resample('W').sum().reset_index()
country_df['smooth'] = country_df['new_cases_smoothed'].rolling(4, center=True).mean().fillna(0)

peaks, _ = find_peaks(country_df['smooth'], distance=8,
                       prominence=country_df['smooth'].max() * 0.1)
fig_wave = go.Figure()
fig_wave.add_trace(go.Scatter(x=country_df['date'], y=country_df['smooth'],
    name='Weekly Cases', fill='tozeroy', line=dict(color='red')))
if len(peaks):
    fig_wave.add_trace(go.Scatter(
        x=country_df.iloc[peaks]['date'], y=country_df.iloc[peaks]['smooth'],
        mode='markers+text',
        text=[f"Wave {i+1}" for i in range(len(peaks))],
        textposition='top center',
        marker=dict(size=12, color='gold', symbol='star'), name='Wave Peaks'))
fig_wave.update_layout(title=f'{wave_country} — COVID Waves')
st.plotly_chart(fig_wave, use_container_width=True)
st.info(f"🌊 {len(peaks)} waves detected in {wave_country}")
```

**What v3 adds over v2:**
- `@st.cache_data(ttl=3600)` — live data that refreshes every hour automatically
- Dynamic map metric selector — switch between cases, deaths, vaccination rate
- Interactive country multiselect — compare any countries in real time
- Wave detection runs instantly on any country the user picks

---

## 📈 Learning Progression Summary

```
v1 → Static map + bar chart of COVID data
v2 → Animated spread over time + wave detection + vaccine impact proven with correlation
v3 → Live dashboard refreshing from OWID daily, any country, any metric, instant wave detection
```

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
