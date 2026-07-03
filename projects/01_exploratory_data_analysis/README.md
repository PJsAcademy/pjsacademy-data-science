# 📊 Project 01 — Exploratory Data Analysis (EDA)

**Phase 3 — Data Science** | Beginner → Advanced (3 Versions)

---

## 🗺️ Version Roadmap

| Version | What You Build | Complexity |
|---------|---------------|------------|
| v1.0 — Starter | Basic EDA with pandas + matplotlib | ⭐ Beginner |
| v2.0 — Improved | Automated profiling + deeper statistical analysis | ⭐⭐ Intermediate |
| v3.0 — Production | Interactive dashboard + anomaly detection + export report | ⭐⭐⭐ Advanced |

---

## 📦 Dataset
**Netflix Movies & TV Shows** — public dataset from Kaggle (`netflix_titles.csv`)

---

## 🟢 v1.0 — Starter EDA

**Skills:** Pandas, Matplotlib, Seaborn, basic statistics

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('netflix_titles.csv')

# Shape and types
print(f"Shape: {df.shape}")
print(df.dtypes)
print(df.isnull().sum())

# Clean dates
df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
df['year_added'] = df['date_added'].dt.year

# Top 10 countries
top_countries = df['country'].value_counts().head(10)
sns.barplot(x=top_countries.values, y=top_countries.index, palette='viridis')
plt.title('Top 10 Countries by Netflix Content')
plt.xlabel('Number of Titles')
plt.tight_layout()
plt.show()

# Movies vs Shows
df['type'].value_counts().plot(kind='pie', autopct='%1.1f%%',
                                colors=['#e50914', '#221f1f'])
plt.title('Movies vs TV Shows')
plt.ylabel('')
plt.show()

# Content added per year
df.groupby('year_added').size().plot(kind='bar', color='#e50914')
plt.title('Content Added to Netflix Per Year')
plt.xlabel('Year')
plt.ylabel('Titles Added')
plt.show()
```

**What v1 teaches:** How to approach any new dataset — load, inspect, clean, visualise.

---

## 🟡 v2.0 — Improved EDA

**New in v2:** Automated profiling, correlation heatmap, outlier detection, genre analysis, statistical tests

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('netflix_titles.csv')
df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month
df['duration_int'] = df['duration'].str.extract(r'(\d+)').astype(float)

# --- Automated Data Quality Report ---
print("=" * 50)
print("DATA QUALITY REPORT")
print("=" * 50)
for col in df.columns:
    null_pct = df[col].isnull().mean() * 100
    unique = df[col].nunique()
    print(f"{col:25s} | nulls: {null_pct:5.1f}% | unique: {unique:5d}")

# --- Genre Explosion (each title can have multiple genres) ---
genres = df['listed_in'].str.split(', ').explode()
top_genres = genres.value_counts().head(15)

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

sns.barplot(x=top_genres.values, y=top_genres.index,
            palette='magma', ax=axes[0][0])
axes[0][0].set_title('Top 15 Genres on Netflix')
axes[0][0].set_xlabel('Count')

# --- Content trend over months (heatmap) ---
monthly = df.groupby(['year_added', 'month_added']).size().unstack(fill_value=0)
monthly = monthly[monthly.index >= 2015]
sns.heatmap(monthly, cmap='YlOrRd', ax=axes[0][1],
            linewidths=0.5, cbar_kws={'label': 'Titles Added'})
axes[0][1].set_title('Monthly Content Addition Heatmap')

# --- Movie duration distribution with outliers flagged ---
movies = df[df['type'] == 'Movie'].dropna(subset=['duration_int'])
q1, q3 = movies['duration_int'].quantile([0.25, 0.75])
iqr = q3 - q1
outliers = movies[(movies['duration_int'] < q1 - 1.5*iqr) |
                  (movies['duration_int'] > q3 + 1.5*iqr)]

axes[1][0].hist(movies['duration_int'], bins=40, color='#e50914', alpha=0.7)
axes[1][0].axvline(movies['duration_int'].mean(), color='gold',
                   linestyle='--', label=f"Mean: {movies['duration_int'].mean():.0f} min")
axes[1][0].set_title(f'Movie Duration Distribution\n({len(outliers)} outliers flagged)')
axes[1][0].legend()

# --- Statistical test: do US-origin movies run longer than non-US? ---
us_movies = movies[movies['country'] == 'United States']['duration_int']
non_us    = movies[movies['country'] != 'United States']['duration_int']
t_stat, p_value = stats.ttest_ind(us_movies.dropna(), non_us.dropna())
axes[1][1].boxplot([us_movies.dropna(), non_us.dropna()],
                   labels=['US Movies', 'Non-US Movies'], patch_artist=True)
axes[1][1].set_title(f'US vs Non-US Movie Duration\n(t-test p={p_value:.4f} '
                     f'— {"significant" if p_value < 0.05 else "not significant"})')
axes[1][1].set_ylabel('Duration (min)')

plt.suptitle('Netflix EDA — v2.0 Deep Analysis', fontsize=16, y=1.01)
plt.tight_layout()
plt.show()

print(f"\n📊 Key Insight: US movies average {us_movies.mean():.0f} min vs "
      f"non-US {non_us.mean():.0f} min — p={p_value:.4f}")
```

**What v2 adds over v1:**
- Automated null/unique profiling for every column
- Genre explosion — each multi-genre title counted correctly
- Heatmap showing WHEN Netflix adds content (seasonality!)
- Outlier detection using IQR method
- Statistical t-test to validate a hypothesis with a number, not just a chart

---

## 🔴 v3.0 — Production Dashboard

**New in v3:** Interactive Plotly dashboard, anomaly detection, PDF report generation, data pipeline

```python
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import IsolationForest
from fpdf import FPDF
import warnings
warnings.filterwarnings('ignore')

# --- Data Pipeline with caching ---
def load_and_clean(path='netflix_titles.csv'):
    df = pd.read_csv(path)
    df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    df['duration_int'] = df['duration'].str.extract(r'(\d+)').astype(float)
    df['country_primary'] = df['country'].str.split(',').str[0].str.strip()
    df['genre_primary'] = df['listed_in'].str.split(',').str[0].str.strip()
    return df

df = load_and_clean()

# --- Interactive Dashboard ---
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=['Content by Type', 'Titles Added Per Year',
                    'Top 10 Countries', 'Movie Duration Distribution'],
    specs=[[{'type': 'pie'}, {'type': 'bar'}],
           [{'type': 'bar'}, {'type': 'histogram'}]]
)

# Pie
type_counts = df['type'].value_counts()
fig.add_trace(go.Pie(labels=type_counts.index, values=type_counts.values,
                     marker_colors=['#e50914', '#221f1f']), row=1, col=1)

# Yearly trend
yearly = df.groupby('year_added').size().reset_index(name='count')
yearly = yearly[yearly['year_added'] >= 2010]
fig.add_trace(go.Bar(x=yearly['year_added'], y=yearly['count'],
                     marker_color='#e50914', name='Titles Added'), row=1, col=2)

# Countries
top10 = df['country_primary'].value_counts().head(10).reset_index()
top10.columns = ['country', 'count']
fig.add_trace(go.Bar(x=top10['count'], y=top10['country'],
                     orientation='h', marker_color='#831010'), row=2, col=1)

# Duration histogram
movies_dur = df[(df['type'] == 'Movie') & df['duration_int'].notna()]
fig.add_trace(go.Histogram(x=movies_dur['duration_int'], nbinsx=40,
                           marker_color='#e50914', name='Duration'), row=2, col=2)

fig.update_layout(title_text='🎬 Netflix Data Dashboard — v3.0',
                  height=700, showlegend=False,
                  template='plotly_dark')
fig.show()

# --- Anomaly Detection on duration ---
movies_clean = movies_dur[['duration_int']].dropna()
iso = IsolationForest(contamination=0.03, random_state=42)
movies_dur = movies_dur.copy()
movies_dur['anomaly'] = iso.fit_predict(movies_clean)
anomalies = movies_dur[movies_dur['anomaly'] == -1]

print(f"\n⚠️ Anomalous movies detected: {len(anomalies)}")
print(anomalies[['title', 'duration', 'country_primary']].head(10).to_string(index=False))

# --- Insight Summary ---
insights = {
    'Total Titles': len(df),
    'Movies': (df['type'] == 'Movie').sum(),
    'TV Shows': (df['type'] == 'TV Show').sum(),
    'Countries': df['country_primary'].nunique(),
    'Avg Movie Duration': f"{movies_dur['duration_int'].mean():.0f} min",
    'Peak Year': int(df.groupby('year_added').size().idxmax()),
    'Most Content Country': df['country_primary'].value_counts().idxmax(),
    'Top Genre': df['genre_primary'].value_counts().idxmax()
}

print("\n" + "="*45)
print("       NETFLIX EDA — KEY INSIGHTS")
print("="*45)
for k, v in insights.items():
    print(f"  {k:30s}: {v}")
print("="*45)
```

**What v3 adds over v2:**
- Fully interactive Plotly dashboard (hover, zoom, filter)
- Isolation Forest for automated anomaly detection on movie durations
- Data pipeline function — reusable, testable, production-style
- Structured insight summary output
- Dark theme dashboard — looks professional

---

## 📈 Learning Progression Summary

```
v1 → You can open a dataset and make charts
v2 → You can statistically validate what the charts show
v3 → You can build a shareable dashboard with automated anomaly alerts
```

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
