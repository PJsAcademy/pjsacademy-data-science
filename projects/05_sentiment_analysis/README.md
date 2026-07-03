# 💬 Project 05 — Sentiment Analysis

**Phase 5 — GenAI & NLP** | Beginner → Advanced (3 Versions)

---

## 🗺️ Version Roadmap

| Version | What You Build | Complexity |
|---------|---------------|------------|
| v1.0 — Starter | TF-IDF + Logistic Regression + HuggingFace zero-shot | ⭐ Beginner |
| v2.0 — Improved | Fine-tuned DistilBERT on custom domain | ⭐⭐ Intermediate |
| v3.0 — Production | Multi-label aspect-based sentiment + live review monitor | ⭐⭐⭐ Advanced |

---

## 📦 Dataset
**Amazon Product Reviews** — from HuggingFace datasets (`amazon_polarity`)

---

## 🟢 v1.0 — Traditional ML vs Transformer

**Skills:** TF-IDF, Logistic Regression, HuggingFace pipeline

```python
# --- Method 1: Traditional ML ---
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings('ignore')

dataset = load_dataset('amazon_polarity', split='test[:5000]')
texts  = dataset['content']
labels = dataset['label']  # 0=negative, 1=positive

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42)

pipe = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=10000, ngram_range=(1,2))),
    ('clf',   LogisticRegression(max_iter=1000))
])
pipe.fit(X_train, y_train)
pred = pipe.predict(X_test)
print("Traditional ML:")
print(classification_report(y_test, pred, target_names=['Negative', 'Positive']))

# --- Method 2: HuggingFace (no training!) ---
from transformers import pipeline

sentiment = pipeline('sentiment-analysis',
                     model='distilbert-base-uncased-finetuned-sst-2-english')

reviews = [
    "This product is absolutely amazing, love every bit of it!",
    "Complete waste of money. Broke after 2 days. Terrible quality.",
    "It's okay. Nothing special but gets the job done."
]
for r in reviews:
    result = sentiment(r[:512])[0]
    bar = '█' * int(result['score'] * 20)
    print(f"{result['label']:8s} {bar} {result['score']:.2f} | {r[:60]}")
```

**What v1 teaches:** Traditional ML = fast but misses sarcasm, context, irony. Transformer = understands language as humans do.

---

## 🟡 v2.0 — Fine-Tune DistilBERT on Your Own Data

**New in v2:** Fine-tune a transformer on domain-specific reviews, evaluate with confusion matrix, test on edge cases

```python
import torch
from transformers import (DistilBertTokenizerFast, DistilBertForSequenceClassification,
                          Trainer, TrainingArguments)
from datasets import load_dataset, Dataset
from sklearn.metrics import accuracy_score, f1_score
import numpy as np

# Load a small sample (fine-tuning on CPU — use GPU for full dataset)
dataset = load_dataset('amazon_polarity')
train_data = dataset['train'].select(range(2000))
test_data  = dataset['test'].select(range(500))

tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

def tokenize(batch):
    return tokenizer(batch['content'], padding=True, truncation=True, max_length=128)

train_enc = train_data.map(tokenize, batched=True)
test_enc  = test_data.map(tokenize, batched=True)

# Rename label column for Trainer
train_enc = train_enc.rename_column('label', 'labels')
test_enc  = test_enc.rename_column('label', 'labels')
train_enc.set_format('torch', columns=['input_ids', 'attention_mask', 'labels'])
test_enc.set_format('torch', columns=['input_ids', 'attention_mask', 'labels'])

model = DistilBertForSequenceClassification.from_pretrained(
    'distilbert-base-uncased', num_labels=2)

def compute_metrics(pred):
    labels = pred.label_ids
    preds  = pred.predictions.argmax(-1)
    return {
        'accuracy': accuracy_score(labels, preds),
        'f1':       f1_score(labels, preds, average='weighted')
    }

args = TrainingArguments(
    output_dir='./sentiment_model',
    num_train_epochs=2,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    evaluation_strategy='epoch',
    logging_steps=50,
    report_to='none'
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_enc,
    eval_dataset=test_enc,
    compute_metrics=compute_metrics
)

trainer.train()
results = trainer.evaluate()
print(f"\nFine-tuned DistilBERT — Accuracy: {results['eval_accuracy']:.3f} | F1: {results['eval_f1']:.3f}")

# Save model
model.save_pretrained('./sentiment_model_final')
tokenizer.save_pretrained('./sentiment_model_final')
print("Model saved!")

# --- Test on tricky edge cases ---
tricky_reviews = [
    "Oh great, another product that broke immediately. Just what I needed.",  # Sarcasm
    "Not bad, not great. Just... fine.",                                       # Neutral
    "I hate how much I LOVE this product. Can't stop using it!",              # Positive with hate
]
from transformers import pipeline
finetuned = pipeline('sentiment-analysis', model='./sentiment_model_final')
for r in tricky_reviews:
    result = finetuned(r)[0]
    print(f"[{result['label']}] {result['score']:.2f} — {r}")
```

**What v2 adds over v1:**
- Fine-tuning — adapt a pre-trained model to YOUR domain in 2 epochs
- `Trainer` API — handles batching, logging, evaluation automatically
- Edge case testing — sarcasm, double negatives, mixed sentiment
- Saved model — reuse without retraining

---

## 🔴 v3.0 — Aspect-Based Sentiment + Live Monitor

**New in v3:** Detect sentiment per aspect (battery, screen, delivery), multi-label classification, real-time review monitoring dashboard

```python
# Part A — Aspect-Based Sentiment Analysis (ABSA)
from transformers import pipeline
import pandas as pd
import re

# Aspect keywords map
ASPECTS = {
    'battery':   ['battery', 'charge', 'charging', 'power', 'drain'],
    'screen':    ['screen', 'display', 'resolution', 'brightness', 'touch'],
    'delivery':  ['delivery', 'shipping', 'arrived', 'packaging', 'courier'],
    'quality':   ['quality', 'build', 'material', 'durable', 'sturdy', 'cheap'],
    'price':     ['price', 'cost', 'value', 'worth', 'expensive', 'cheap', 'money'],
    'support':   ['support', 'service', 'customer', 'response', 'refund', 'return']
}

sentiment_pipe = pipeline('sentiment-analysis',
                          model='distilbert-base-uncased-finetuned-sst-2-english')

def analyse_aspects(review):
    review_lower = review.lower()
    results = {}
    for aspect, keywords in ASPECTS.items():
        # Find sentences mentioning this aspect
        sentences = re.split(r'[.!?]', review)
        relevant = [s for s in sentences
                    if any(kw in s.lower() for kw in keywords)]
        if relevant:
            combined = '. '.join(relevant)[:512]
            sentiment = sentiment_pipe(combined)[0]
            results[aspect] = {
                'sentiment': sentiment['label'],
                'score': round(sentiment['score'], 2),
                'snippet': combined[:80]
            }
    return results

# Sample reviews
reviews = [
    """Amazing phone! The screen is crystal clear and super bright.
       Battery life is disappointing though, barely lasts a day.
       Delivery was fast, arrived in 2 days. Build quality feels premium.""",

    """Terrible experience. Screen keeps flickering after 2 weeks.
       Battery is actually great, lasts 2 days easily.
       Customer support refused to help me return it. Never buying again."""
]

for i, review in enumerate(reviews, 1):
    print(f"\n--- Review {i} ---")
    print(f"Text: {review[:100]}...")
    aspects = analyse_aspects(review)
    for aspect, data in aspects.items():
        emoji = "✅" if data['sentiment'] == 'POSITIVE' else "❌"
        print(f"  {emoji} {aspect:10s}: {data['sentiment']} ({data['score']}) — {data['snippet']}")
```

```python
# Part B — Live Review Monitor (Streamlit)
# streamlit run monitor.py
import streamlit as st
from transformers import pipeline
import pandas as pd
import time

st.set_page_config(page_title="Sentiment Monitor", page_icon="💬", layout="wide")
st.title("💬 Live Review Sentiment Monitor — PJS Academy")

@st.cache_resource
def load_model():
    return pipeline('sentiment-analysis',
                    model='distilbert-base-uncased-finetuned-sst-2-english')

model = load_model()

# Input
review = st.text_area("Paste a product review:", height=150,
                       placeholder="Type or paste a customer review here...")
col1, col2 = st.columns(2)

if st.button("🔍 Analyse Sentiment", type="primary") and review:
    with st.spinner("Analysing..."):
        result = model(review[:512])[0]

    sentiment = result['label']
    score     = result['score']
    color     = "green" if sentiment == "POSITIVE" else "red"

    col1.metric("Sentiment", sentiment)
    col1.metric("Confidence", f"{score:.1%}")
    col2.progress(score)
    col2.markdown(f"<h2 style='color:{color}'>"
                  f"{'😊 Positive Review' if sentiment == 'POSITIVE' else '😠 Negative Review'}"
                  f"</h2>", unsafe_allow_html=True)

    # Batch mode
    st.markdown("---")
    st.subheader("📋 Batch Analysis")
    sample_reviews = [
        "Absolutely love this product!",
        "Terrible. Complete waste of money.",
        "It's decent for the price.",
        "Best purchase I've made this year.",
        "Stopped working after one week."
    ]
    results = []
    for r in sample_reviews:
        res = model(r)[0]
        results.append({'Review': r, 'Sentiment': res['label'],
                        'Confidence': f"{res['score']:.1%}"})
    st.dataframe(pd.DataFrame(results), use_container_width=True)
```

**What v3 adds over v2:**
- Aspect-based sentiment — "battery is bad but screen is great" — not just overall positive/negative
- Sentence segmentation — analyses each aspect from the relevant sentence
- Live Streamlit dashboard — demo-able in real time
- Batch analysis — process 100 reviews at once

---

## 📈 Learning Progression Summary

```
v1 → "This review is positive" — rule-based or pre-trained
v2 → Fine-tune on your product domain, handle sarcasm and edge cases
v3 → "Battery: ❌ Negative | Screen: ✅ Positive | Delivery: ✅ Positive" — aspect-level insights
```

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
