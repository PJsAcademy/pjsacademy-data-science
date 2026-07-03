# 🎬 Project 13 — YouTube Comment Analyser

**Phase 5 — GenAI & NLP** | Beginner → Real-Time (3 Versions)

---

## 🗺️ Version Roadmap

| Version | What You Build | Complexity |
|---------|---------------|------------|
| v1.0 — Starter | VADER sentiment + WordCloud + toxic detection | ⭐ Beginner |
| v2.0 — Improved | Topic clustering + engagement analysis + creator PDF report | ⭐⭐ Intermediate |
| v3.0 — Real-Time | Live comment monitor + trend alerts + auto-reply suggestions | ⭐⭐⭐ Advanced |

---

## 📦 Libraries Needed
```bash
pip install google-api-python-client vaderSentiment textblob wordcloud matplotlib pandas scikit-learn streamlit plotly reportlab
```

---

## 🟢 v1.0 — Sentiment + WordCloud + Toxic Flag

**Skills:** YouTube API, VADER, WordCloud, keyword toxicity detection

```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import re

vader = SentimentIntensityAnalyzer()

# Demo comments (replace with real API fetch)
df = pd.DataFrame({
    'author': ['User1','User2','User3','User4','User5','User6','User7'],
    'text': [
        "This tutorial is absolutely amazing! Best content ever.",
        "I don't understand anything here, very confusing.",
        "Great video! Subscribed and shared.",
        "Terrible, you're wasting my time.",
        "Could be better with more examples but overall good.",
        "You are an idiot! This is completely wrong!!!",
        "Loved it, very clear and well explained. Thank you!"
    ],
    'likes': [45, 3, 28, 1, 7, 0, 62]
})

def analyse(text):
    v = vader.polarity_scores(text)
    c = v['compound']
    return {
        'compound': c,
        'label': 'Positive' if c >= 0.05 else 'Negative' if c <= -0.05 else 'Neutral',
        'subjectivity': TextBlob(text).sentiment.subjectivity
    }

df = pd.concat([df, df['text'].apply(analyse).apply(pd.Series)], axis=1)

counts = df['label'].value_counts()
colors = {'Positive':'#27ae60','Neutral':'#f39c12','Negative':'#e74c3c'}
fig, axes = plt.subplots(1, 3, figsize=(16, 4))

counts.plot(kind='pie', ax=axes[0], colors=[colors[l] for l in counts.index],
            autopct='%1.0f%%', startangle=90)
axes[0].set_title('Sentiment Split'); axes[0].set_ylabel('')

wc = WordCloud(width=400, height=200, background_color='white').generate(
    ' '.join(df['text']))
axes[1].imshow(wc, interpolation='bilinear')
axes[1].set_title('Comment Word Cloud'); axes[1].axis('off')

TOXIC = ['idiot','terrible','hate','awful','garbage','wrong','useless']
df['toxic'] = df['text'].str.lower().apply(lambda t: any(w in t for w in TOXIC))
df['toxic'].value_counts().plot(kind='bar', ax=axes[2],
    color=['green','red'], title='Toxic vs Normal Comments')
axes[2].set_xticklabels(['Normal','Toxic'], rotation=0)
plt.tight_layout(); plt.show()

print(f"Toxic comments: {df['toxic'].sum()}/{len(df)}")
print(f"Avg sentiment: {df['compound'].mean():.3f}")
```

**What v1 teaches:** VADER — rule-based sentiment that handles exclamation marks, capitals, and emojis without any training.

---

## 🟡 v2.0 — Topic Clustering + Engagement Analysis + PDF Report

**New in v2:** KMeans topic clustering, engagement score (likes × sentiment), top questions detection, PDF creator report

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pdf_backend
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from wordcloud import WordCloud
import re

vader = SentimentIntensityAnalyzer()

# Simulated larger dataset
np.random.seed(42)
sentiments = ['positive'] * 60 + ['negative'] * 25 + ['neutral'] * 15
topics = {
    'positive': ["Great tutorial! Very helpful.", "Amazing content, subscribed!",
                 "Best explanation I've seen.", "Love this channel!",
                 "Clear and concise, thanks!"],
    'negative': ["Couldn't understand anything.", "Too fast, very confusing.",
                 "Missing important concepts.", "Audio quality is bad.",
                 "Please slow down next time."],
    'neutral':  ["When is the next video?", "Can you do a video on SQL?",
                 "What about deep learning?", "How long did this take?",
                 "First comment here!"],
}
comments = []
for s in sentiments:
    text   = np.random.choice(topics[s])
    likes  = max(0, int(np.random.normal(20 if s == 'positive' else 3, 5)))
    score  = vader.polarity_scores(text)['compound']
    label  = 'Positive' if score >= 0.05 else 'Negative' if score <= -0.05 else 'Neutral'
    comments.append({'text': text, 'likes': likes, 'compound': score, 'label': label})

df = pd.DataFrame(comments)

# Engagement score = likes × (1 + compound)
df['engagement'] = df['likes'] * (1 + df['compound'])

# --- KMeans Topic Clustering ---
tfidf = TfidfVectorizer(max_features=50, stop_words='english')
X = tfidf.fit_transform(df['text'])
km = KMeans(n_clusters=4, random_state=42, n_init=10)
df['topic_cluster'] = km.fit_predict(X)

# Topic labels (top terms per cluster)
terms = tfidf.get_feature_names_out()
topic_labels = {}
for i in range(4):
    top_terms = terms[km.cluster_centers_[i].argsort()[-3:][::-1]]
    topic_labels[i] = ' / '.join(top_terms)
df['topic'] = df['topic_cluster'].map(topic_labels)

print("Topic Clusters:")
for t, g in df.groupby('topic'):
    print(f"  [{t}] — {len(g)} comments, avg sentiment: {g['compound'].mean():.2f}")

# --- Questions Detection ---
df['is_question'] = df['text'].str.contains(r'\?')
questions = df[df['is_question']].nlargest(5, 'likes')
print(f"\nTop Questions ({len(df[df['is_question']])} total):")
print(questions[['text','likes']].to_string(index=False))

# --- Creator Dashboard Plot ---
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Sentiment
counts = df['label'].value_counts()
axes[0][0].pie(counts, labels=counts.index, autopct='%1.0f%%',
               colors=['#27ae60','#f39c12','#e74c3c'])
axes[0][0].set_title('Sentiment Split')

# Topic cluster sizes
topic_counts = df['topic'].value_counts()
axes[0][1].barh(topic_counts.index, topic_counts.values, color='steelblue')
axes[0][1].set_title('Comment Topics')

# Engagement by sentiment
df.groupby('label')['engagement'].mean().plot(kind='bar', ax=axes[1][0],
    color=['#27ae60','#e74c3c','#f39c12'])
axes[1][0].set_title('Avg Engagement Score by Sentiment')
axes[1][0].tick_params(axis='x', rotation=0)

# Top 10 comments by likes
top_liked = df.nlargest(10, 'likes')
axes[1][1].barh(range(10), top_liked['likes'], color='purple')
axes[1][1].set_yticks(range(10))
axes[1][1].set_yticklabels([t[:40] for t in top_liked['text']], fontsize=7)
axes[1][1].set_title('Top 10 Most Liked Comments')

plt.suptitle('YouTube Comment Analysis Dashboard', fontsize=14)
plt.tight_layout()
plt.savefig('creator_report.png', dpi=150, bbox_inches='tight')
plt.show()
print("Report saved: creator_report.png")
```

**What v2 adds over v1:**
- KMeans topic clustering — automatically groups "audio complaints", "content praise", "questions"
- Engagement score — likes × sentiment, finds comments that both perform well AND feel good
- Question detection — find what viewers are asking most (content ideas!)
- PNG report export — creator can share it with their team

---

## 🔴 v3.0 — Live Comment Monitor + Auto-Reply Suggestions

**New in v3:** Real-time comment stream, trend alerts, GPT-powered reply suggestions, Streamlit creator dashboard

```python
# app.py — Live YouTube Comment Analyser
# Run: streamlit run app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time, re

st.set_page_config(page_title="YouTube Comment Monitor", page_icon="🎬", layout="wide")
st.title("🎬 YouTube Comment Analyser — PJS Academy")

vader = SentimentIntensityAnalyzer()

TOXIC_KEYWORDS = ['idiot','stupid','terrible','awful','garbage','hate','worst','trash']

def analyse_comment(text):
    score = vader.polarity_scores(text)['compound']
    label = 'Positive' if score >= 0.05 else 'Negative' if score <= -0.05 else 'Neutral'
    toxic = any(w in text.lower() for w in TOXIC_KEYWORDS)
    is_q  = '?' in text
    return {'score': score, 'label': label, 'toxic': toxic, 'question': is_q}

def get_reply_suggestion(comment_text, sentiment):
    """Rule-based reply suggestions (replace with OpenAI for real suggestions)."""
    if sentiment == 'Negative':
        return "Thank you for the feedback! Could you tell me more about what was unclear? I'll improve it. 🙏"
    elif '?' in comment_text:
        return "Great question! I'll cover this in a future video — stay tuned! 😊"
    else:
        return "Thank you so much! More videos coming soon. Don't forget to subscribe! 🔔"

# Simulate real-time comment stream
def generate_live_comment():
    samples = [
        ("Amazing tutorial! Really helped me understand.", 45),
        ("Can you make a video on Pandas?", 12),
        ("Too fast, couldn't follow at all.", 2),
        ("Best Python channel on YouTube!", 89),
        ("This is terrible content, waste of time.", 0),
        ("When's the next video coming?", 8),
        ("Subscribed! Keep it up!", 34),
        ("Audio is a bit low but content is great.", 15),
    ]
    text, likes = samples[np.random.randint(len(samples))]
    result = analyse_comment(text)
    return {'text': text, 'likes': likes, 'time': datetime.now().strftime('%H:%M:%S'),
            **result}

# --- Session State ---
if 'comments' not in st.session_state:
    st.session_state.comments = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []

with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("▶️ Load 20 Comments"):
        for _ in range(20):
            st.session_state.comments.append(generate_live_comment())
    if st.button("🔄 Add 5 More"):
        for _ in range(5):
            st.session_state.comments.append(generate_live_comment())
    if st.button("🗑️ Reset"):
        st.session_state.comments = []
        st.session_state.alerts = []

    alert_threshold = st.slider("Alert if negative % exceeds:", 20, 80, 40)
    show_toxic = st.checkbox("Flag toxic comments", value=True)

if st.session_state.comments:
    df = pd.DataFrame(st.session_state.comments)
    total    = len(df)
    pos_pct  = (df['label']=='Positive').mean() * 100
    neg_pct  = (df['label']=='Negative').mean() * 100
    toxic_n  = df['toxic'].sum()
    questions = df['question'].sum()

    # Alert
    if neg_pct > alert_threshold:
        st.error(f"🚨 ALERT: {neg_pct:.0f}% negative comments! Threshold: {alert_threshold}%")

    # Metrics
    m1,m2,m3,m4,m5 = st.columns(5)
    m1.metric("Total Comments", total)
    m2.metric("Positive 😊", f"{pos_pct:.0f}%")
    m3.metric("Negative 😠", f"{neg_pct:.0f}%", delta=f"Alert>{alert_threshold}%")
    m4.metric("Toxic 🚨", toxic_n)
    m5.metric("Questions ❓", questions)

    col1, col2 = st.columns(2)
    # Sentiment over time
    fig1 = px.line(df.reset_index(), x='index', y='score',
                   color='label', title='Sentiment Score Over Time')
    col1.plotly_chart(fig1, use_container_width=True)

    # Distribution
    fig2 = px.pie(df, names='label', title='Sentiment Distribution',
                  color_discrete_map={'Positive':'green','Negative':'red','Neutral':'gray'})
    col2.plotly_chart(fig2, use_container_width=True)

    # Live feed
    st.subheader("💬 Live Comment Feed")
    for _, row in df.tail(10).iloc[::-1].iterrows():
        color = {'Positive':'🟢','Negative':'🔴','Neutral':'🟡'}[row['label']]
        toxic_tag = " 🚫" if row['toxic'] else ""
        q_tag     = " ❓" if row['question'] else ""
        with st.expander(f"{color} {row['text'][:60]}... | {row['likes']} likes{toxic_tag}{q_tag}"):
            st.write(f"**Full comment:** {row['text']}")
            st.write(f"**Sentiment:** {row['label']} ({row['score']:.3f})")
            if show_toxic and row['toxic']:
                st.error("⚠️ Contains potentially toxic language")
            st.info(f"💬 **Suggested reply:** {get_reply_suggestion(row['text'], row['label'])}")
```

**What v3 adds over v2:**
- Real-time comment stream with running sentiment metrics
- Alert system — fires when negative % exceeds your threshold
- Auto-reply suggestions per comment (upgrade to GPT-4o for production)
- Expandable live feed — see full comment + suggested reply in one click

---

## 📈 Learning Progression Summary

```
v1 → Analyse 7 sample comments, make a WordCloud, flag toxic ones
v2 → Cluster 100 comments by topic, measure engagement, export PNG report
v3 → Live dashboard — alerts fire, reply suggestions appear, monitors in real time
```

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
