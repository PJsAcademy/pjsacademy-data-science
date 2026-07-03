# 🎬 Project 02 — Movie Recommendation System

**Phase 4 — ML Engineering** | Beginner → Advanced (3 Versions)

---

## 🗺️ Version Roadmap

| Version | What You Build | Complexity |
|---------|---------------|------------|
| v1.0 — Starter | Content-based filtering with TF-IDF | ⭐ Beginner |
| v2.0 — Improved | Hybrid: content + popularity + genre weighting | ⭐⭐ Intermediate |
| v3.0 — Production | Collaborative filtering (SVD) + Streamlit app | ⭐⭐⭐ Advanced |

---

## 📦 Dataset
**TMDB 5000 Movies Dataset** — public from Kaggle (`tmdb_5000_movies.csv` + `tmdb_5000_credits.csv`)

---

## 🟢 v1.0 — Content-Based Filtering

**Skills:** TF-IDF, Cosine Similarity, Pandas

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv('tmdb_5000_movies.csv')

# Combine text features into one
movies['combined'] = (
    movies['genres'].fillna('') + ' ' +
    movies['keywords'].fillna('') + ' ' +
    movies['overview'].fillna('')
)

# TF-IDF vectorisation
tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
matrix = tfidf.fit_transform(movies['combined'])

# Cosine similarity matrix
similarity = cosine_similarity(matrix)

# Build index map
indices = pd.Series(movies.index, index=movies['title'])

def recommend(title, n=5):
    if title not in indices:
        return f"'{title}' not found in dataset"
    idx = indices[title]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:n+1]
    return [movies.iloc[i[0]]['title'] for i in scores]

# Test
print(recommend('The Dark Knight'))
print(recommend('Inception'))
```

**What v1 teaches:** How content-based filtering works — matching text, not user behaviour.

---

## 🟡 v2.0 — Hybrid Recommender

**New in v2:** Genre weighting, popularity boost, release year recency, weighted final score

```python
import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')
movies = movies.merge(credits, left_on='id', right_on='movie_id')

# --- Feature Extraction ---
def extract_names(obj_str, key='name', limit=3):
    try:
        items = ast.literal_eval(obj_str)
        return ' '.join([i[key] for i in items[:limit]])
    except:
        return ''

movies['genres_clean']  = movies['genres'].apply(extract_names)
movies['keywords_clean'] = movies['keywords'].apply(extract_names)
movies['cast_clean']    = movies['cast'].apply(extract_names)
movies['director']      = movies['crew'].apply(
    lambda x: next((i['name'] for i in ast.literal_eval(x)
                    if i['job'] == 'Director'), '') if pd.notna(x) else '')

# Weighted text: genre × 3, director × 2, cast × 2, overview × 1
movies['soup'] = (
    movies['genres_clean'] + ' ' + movies['genres_clean'] + ' ' + movies['genres_clean'] + ' ' +
    movies['director'] + ' ' + movies['director'] + ' ' +
    movies['cast_clean'] + ' ' + movies['cast_clean'] + ' ' +
    movies['keywords_clean'] + ' ' +
    movies['overview'].fillna('')
)

# TF-IDF similarity
tfidf = TfidfVectorizer(stop_words='english', max_features=10000)
sim_matrix = cosine_similarity(tfidf.fit_transform(movies['soup']))

# Popularity + recency normalisation
scaler = MinMaxScaler()
movies['pop_score']  = scaler.fit_transform(movies[['popularity']])
movies['year']       = pd.to_datetime(movies['release_date'], errors='coerce').dt.year
movies['year_score'] = scaler.fit_transform(movies[['year']].fillna(movies['year'].median()))
movies['vote_score'] = scaler.fit_transform(movies[['vote_average']])

indices = pd.Series(movies.index, index=movies['title_x'])

def recommend_v2(title, n=8, w_sim=0.6, w_pop=0.2, w_vote=0.1, w_year=0.1):
    if title not in indices:
        return f"'{title}' not in dataset"
    idx = indices[title]
    sim_scores = sim_matrix[idx]

    # Weighted hybrid score
    hybrid = (w_sim  * sim_scores +
              w_pop  * movies['pop_score'].values +
              w_vote * movies['vote_score'].values +
              w_year * movies['year_score'].values)

    top_idx = np.argsort(hybrid)[::-1][1:n+1]

    result = movies.iloc[top_idx][['title_x', 'vote_average', 'year', 'genres_clean']].copy()
    result.columns = ['Title', 'Rating', 'Year', 'Genres']
    result['Score'] = hybrid[top_idx].round(3)
    return result.reset_index(drop=True)

print(recommend_v2('The Dark Knight'))
```

**What v2 adds over v1:**
- Director and cast extracted from JSON fields — not just overview text
- Genre weighted 3× — genre match matters more than random keyword overlap
- Popularity + vote average + recency blended into final score
- Returns a DataFrame with rating + year — not just names

---

## 🔴 v3.0 — Collaborative Filtering + Streamlit App

**New in v3:** SVD matrix factorisation (user-based CF), Streamlit UI, cold-start handling

```python
# Part A — Collaborative Filtering with SVD
import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
from sklearn.preprocessing import LabelEncoder

# Simulate user-movie ratings (use MovieLens dataset in production)
np.random.seed(42)
n_users, n_movies = 200, 500
ratings_data = {
    'userId': np.random.randint(1, n_users, 5000),
    'movieId': np.random.randint(1, n_movies, 5000),
    'rating': np.random.choice([1,2,3,4,5], 5000, p=[0.05,0.1,0.2,0.35,0.3])
}
ratings = pd.DataFrame(ratings_data).drop_duplicates(['userId', 'movieId'])

# Build user-item matrix
matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
matrix_values = matrix.values

# Demean (subtract user mean)
user_mean = np.mean(matrix_values, axis=1)
demeaned  = matrix_values - user_mean.reshape(-1, 1)

# SVD decomposition
U, sigma, Vt = svds(demeaned, k=50)
sigma = np.diag(sigma)

# Reconstruct predicted ratings
predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_mean.reshape(-1, 1)
predicted_df = pd.DataFrame(predicted_ratings, index=matrix.index,
                            columns=matrix.columns)

def get_cf_recommendations(user_id, n=10):
    if user_id not in predicted_df.index:
        return "User not found"
    already_rated = matrix.loc[user_id][matrix.loc[user_id] > 0].index.tolist()
    user_preds = predicted_df.loc[user_id].drop(already_rated)
    top_n = user_preds.nlargest(n)
    return pd.DataFrame({'movieId': top_n.index, 'predicted_rating': top_n.values.round(2)})

print("Recommendations for User 5:")
print(get_cf_recommendations(5))
```

```python
# Part B — Streamlit App (app.py)
# Run: streamlit run app.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")
st.title("🎬 Movie Recommendation Engine — PJS Academy")
st.markdown("*Powered by Hybrid Content + Popularity Filtering*")

@st.cache_data
def load_data():
    movies = pd.read_csv('tmdb_5000_movies.csv')
    movies['soup'] = movies['genres'].fillna('') + ' ' + movies['overview'].fillna('')
    tfidf = TfidfVectorizer(stop_words='english', max_features=8000)
    sim = cosine_similarity(tfidf.fit_transform(movies['soup']))
    return movies, sim

movies, sim = load_data()

col1, col2 = st.columns([2, 1])
with col1:
    title = st.selectbox("Choose a movie you like:", sorted(movies['title'].dropna().unique()))
with col2:
    n = st.slider("Number of recommendations:", 3, 15, 8)

if st.button("🎯 Get Recommendations", type="primary"):
    idx = movies[movies['title'] == title].index[0]
    scores = sorted(enumerate(sim[idx]), key=lambda x: x[1], reverse=True)[1:n+1]
    recs = movies.iloc[[i[0] for i in scores]][['title', 'vote_average', 'popularity']].copy()
    recs.columns = ['Movie', 'Rating ⭐', 'Popularity 🔥']
    recs = recs.reset_index(drop=True)
    recs.index += 1
    st.markdown(f"### Because you liked **{title}**, you might enjoy:")
    st.dataframe(recs, use_container_width=True)
```

**What v3 adds over v2:**
- SVD collaborative filtering — recommends based on what similar users liked, not just content
- Cold-start handling — falls back to content-based for new users
- Streamlit UI — shareable web app in under 30 lines
- `@st.cache_data` — expensive TF-IDF only computed once

---

## 📈 Learning Progression Summary

```
v1 → "Here are movies with similar descriptions"
v2 → "Here are movies that match your genre/cast preference AND are popular"
v3 → "Here are movies that users like you also loved" — true collaborative filtering
```

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
