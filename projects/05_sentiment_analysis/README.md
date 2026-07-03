# 💬 Project 05 — Sentiment Analysis

**Phase 5 — GenAI & LLMs** | Intermediate–Advanced

---

## 🎯 What You'll Build
Classify customer reviews as Positive / Negative / Neutral using both traditional ML and a Transformer model.

## 🛠️ Skills Practiced
- NLP — text preprocessing, TF-IDF
- HuggingFace Transformers
- Fine-tuning BERT
- Model comparison

## 📦 Dataset
**Amazon Product Reviews** (public, from HuggingFace datasets)

## 🚀 Steps
1. Load reviews dataset
2. Preprocess text
3. TF-IDF + Logistic Regression baseline
4. HuggingFace pipeline (zero-shot)
5. Compare results

## 💻 Code
```python
# Method 1 — Traditional ML
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1,2))),
    ('clf', LogisticRegression(max_iter=1000))
])
pipe.fit(X_train, y_train)
print(f"Traditional ML Accuracy: {pipe.score(X_test, y_test):.3f}")

# Method 2 — HuggingFace Transformer (zero-shot, no training!)
from transformers import pipeline

sentiment = pipeline('sentiment-analysis',
                     model='distilbert-base-uncased-finetuned-sst-2-english')

reviews = [
    "This product is absolutely amazing, love it!",
    "Worst purchase I've ever made, complete waste.",
    "It's okay, nothing special but does the job."
]

for review in reviews:
    result = sentiment(review)[0]
    print(f"{result['label']} ({result['score']:.2f}) — {review[:50]}")
```

## 📈 What You'll Learn
- How NLP has evolved from TF-IDF to Transformers
- Using pretrained models without training
- Why BERT outperforms traditional ML on text

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
