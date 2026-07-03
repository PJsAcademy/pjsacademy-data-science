# 🎬 Project 02 — Movie Recommendation System

**Phase 4 — ML Engineering** | Intermediate

---

## 🎯 What You'll Build
A content-based movie recommender — type a movie name, get 5 similar recommendations. Just like Netflix!

## 🛠️ Skills Practiced
- Pandas — data processing
- Sklearn — TF-IDF, Cosine Similarity
- NLP — text vectorisation
- Feature Engineering — combining text features

## 📦 Dataset
**TMDB 5000 Movies Dataset** (public, from Kaggle)

## 🚀 Steps
1. Load and merge movie datasets
2. Extract useful features (genre, cast, director, keywords)
3. Combine into one text feature
4. Vectorise with TF-IDF
5. Compute cosine similarity
6. Build recommend() function

## 💻 Code
```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load
movies = pd.read_csv('tmdb_5000_movies.csv')

# Feature engineering
movies['combined'] = (
    movies['genres'] + ' ' +
    movies['keywords'] + ' ' +
    movies['overview'].fillna('')
)

# Vectorise
tfidf = TfidfVectorizer(stop_words='english')
matrix = tfidf.fit_transform(movies['combined'])

# Similarity
similarity = cosine_similarity(matrix)

# Recommend function
def recommend(title, n=5):
    idx = movies[movies['title'] == title].index[0]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:n+1]
    return [movies.iloc[i[0]]['title'] for i in scores]

# Test
print(recommend('The Dark Knight'))
```

## 📈 What You'll Learn
- How Netflix/Spotify recommendations work
- TF-IDF and cosine similarity
- Building a real ML product from scratch

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
