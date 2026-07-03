# 📊 Project 01 — Exploratory Data Analysis (EDA)

**Phase 3 — Data Science** | Beginner Friendly

---

## 🎯 What You'll Build
A complete EDA on a real-world dataset — uncovering patterns, trends and insights using Python.

## 🛠️ Skills Practiced
- Pandas — data loading, cleaning, groupby
- Matplotlib & Seaborn — visualisations
- Statistics — mean, median, correlation
- Data Cleaning — handling nulls, duplicates

## 📦 Dataset
We use the **Netflix Movies & TV Shows** dataset (public, from Kaggle).

## 🚀 Steps
1. Load and explore the dataset
2. Clean missing values
3. Analyse content by country, genre, year
4. Visualise trends
5. Write key insights

## 💻 Code
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('netflix_titles.csv')

# Basic exploration
print(df.shape)
print(df.info())
print(df.isnull().sum())

# Clean
df['date_added'] = pd.to_datetime(df['date_added'].str.strip())
df['year_added'] = df['date_added'].dt.year

# Top countries
top_countries = df['country'].value_counts().head(10)
sns.barplot(x=top_countries.values, y=top_countries.index)
plt.title('Top 10 Countries by Content')
plt.show()

# Content type split
df['type'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Movies vs TV Shows')
plt.show()
```

## 📈 What You'll Learn
- How to approach any new dataset
- Pattern recognition through visualisation
- Telling a story with data

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
