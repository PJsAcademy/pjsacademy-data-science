# 📄 Project 12 — Resume Screener (NLP)

**Phase 5 — GenAI & NLP** | Beginner → Real-Time (3 Versions)

---

## 🗺️ Version Roadmap

| Version | What You Build | Complexity |
|---------|---------------|------------|
| v1.0 — Starter | TF-IDF cosine similarity + keyword scoring | ⭐ Beginner |
| v2.0 — Improved | BERT embeddings + SpaCy NER + skill gap analysis | ⭐⭐ Intermediate |
| v3.0 — Real-Time | Full ATS — PDF upload, live scoring, candidate dashboard | ⭐⭐⭐ Advanced |

---

## 📦 Libraries Needed
```bash
pip install pandas scikit-learn spacy PyPDF2 nltk sentence-transformers streamlit plotly
python -m spacy download en_core_web_sm
```

---

## 🟢 v1.0 — TF-IDF Resume Ranker

**Skills:** Text preprocessing, TF-IDF, cosine similarity, keyword scoring

```python
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

stop_words = set(stopwords.words('english'))

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', ' ', text)
    tokens = word_tokenize(text)
    return ' '.join(t for t in tokens if t not in stop_words and len(t) > 2)

job_description = """
Data Scientist with Python, Machine Learning, SQL, TensorFlow or PyTorch.
Experience with NLP, model deployment. 2+ years. Strong communication skills.
"""

resumes = {
    "Alice.txt": "Python Machine Learning SQL TensorFlow Data Science 3 years Google fraud detection XGBoost",
    "Bob.txt":   "Java Spring Boot React AWS 5 years Amazon microservices",
    "Carol.txt": "Python PyTorch NLP Transformers 2 years Flipkart recommendation system deep learning",
}

corpus = [preprocess(job_description)] + [preprocess(t) for t in resumes.values()]
tfidf  = TfidfVectorizer()
matrix = tfidf.fit_transform(corpus)
scores = cosine_similarity(matrix[0], matrix[1:])[0]

results = pd.DataFrame({'Candidate': list(resumes.keys()),
                        'Match%': (scores * 100).round(1)
                        }).sort_values('Match%', ascending=False)
print(results.to_string(index=False))

# Keyword scoring
required = ['python','machine learning','sql','tensorflow','pytorch','nlp']
for name, text in resumes.items():
    found = [k for k in required if k in text.lower()]
    print(f"{name}: {len(found)}/{len(required)} — {found}")
```

**What v1 teaches:** TF-IDF measures how unique a word is to a document — the foundation of search engines and ATS tools.

---

## 🟡 v2.0 — BERT Embeddings + Skill Gap Analysis

**New in v2:** Sentence-BERT semantic similarity (understands meaning, not just words), SpaCy NER, skill gap report

```python
import re
import spacy
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2

nlp   = spacy.load('en_core_web_sm')
sbert = SentenceTransformer('all-MiniLM-L6-v2')

def extract_pdf_text(path):
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return ' '.join(page.extract_text() or '' for page in reader.pages)

def extract_skills(text):
    """Extract technical skills using regex + known skill list."""
    TECH_SKILLS = {
        'languages':   ['python','java','r','sql','scala','go','julia'],
        'ml':          ['machine learning','deep learning','nlp','computer vision',
                        'reinforcement learning'],
        'frameworks':  ['tensorflow','pytorch','keras','sklearn','xgboost','lightgbm'],
        'tools':       ['docker','kubernetes','airflow','spark','hadoop','git'],
        'cloud':       ['aws','azure','gcp','bigquery','s3','ec2'],
        'data':        ['pandas','numpy','matplotlib','seaborn','plotly','tableau'],
    }
    text_lower = text.lower()
    found = {}
    for category, skills in TECH_SKILLS.items():
        found[category] = [s for s in skills if s in text_lower]
    return found

def extract_entities(text):
    doc = nlp(text[:2000])
    return {
        'orgs':   [e.text for e in doc.ents if e.label_ == 'ORG'][:5],
        'years':  [e.text for e in doc.ents if e.label_ == 'DATE'][:5],
    }

job_description = """
Senior Data Scientist — Python, Machine Learning, SQL, PyTorch, NLP,
AWS, Docker. 3+ years. Experience with MLflow, model deployment, A/B testing.
"""

# Demo resumes (replace with actual PDFs in production)
resumes = {
    "Alice": """Python machine learning SQL TensorFlow deep learning AWS Docker
                3 years Google fraud detection XGBoost MLflow deployment A/B testing""",
    "Bob":   """Java Spring Boot React AWS 5 years microservices REST API databases""",
    "Carol": """Python PyTorch NLP Transformers HuggingFace 2 years Flipkart
                recommendation system deep learning Docker deployment""",
}

jd_embedding = sbert.encode([job_description])

results = []
for name, text in resumes.items():
    resume_embedding = sbert.encode([text])
    semantic_score   = float(cosine_similarity(jd_embedding, resume_embedding)[0][0])

    skills = extract_skills(text)
    jd_skills = extract_skills(job_description)
    total_jd_skills  = sum(len(v) for v in jd_skills.values())
    matched_skills   = sum(len(set(skills[k]) & set(jd_skills[k]))
                           for k in skills)
    keyword_score    = matched_skills / max(total_jd_skills, 1)
    final_score      = 0.7 * semantic_score + 0.3 * keyword_score

    entities = extract_entities(text)

    results.append({
        'Candidate':    name,
        'Semantic':     round(semantic_score * 100, 1),
        'Keywords':     round(keyword_score * 100, 1),
        'Final Score':  round(final_score * 100, 1),
        'Companies':    ', '.join(entities['orgs'][:2]),
        'ML Skills':    ', '.join(skills['ml'][:3]),
        'Frameworks':   ', '.join(skills['frameworks'][:3]),
    })

df = pd.DataFrame(results).sort_values('Final Score', ascending=False)
print(df.to_string(index=False))

# Skill gap analysis for top candidate
top = results[0]
print(f"\n📊 Skill Gap Analysis for {top['Candidate']}:")
top_skills = extract_skills(resumes[top['Candidate']])
jd_sk      = extract_skills(job_description)
for cat in jd_sk:
    missing = set(jd_sk[cat]) - set(top_skills[cat])
    if missing:
        print(f"  ❌ Missing {cat}: {list(missing)}")
    else:
        print(f"  ✅ {cat}: All covered")
```

**What v2 adds over v1:**
- Sentence-BERT — "machine learning engineer" matches "ML developer" even without exact words
- Structured skill extraction — languages, frameworks, cloud, tools separately
- SpaCy NER — extracts company names and experience years automatically
- Skill gap report — tells the candidate exactly what's missing for this JD

---

## 🔴 v3.0 — Full ATS: PDF Upload + Live Scoring Dashboard

**New in v3:** Streamlit ATS app, bulk PDF upload, ranked leaderboard, email shortlist generator

```python
# app.py — Applicant Tracking System
# Run: streamlit run app.py
import streamlit as st
import pandas as pd
import numpy as np
import PyPDF2
import re, io
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Resume Screener ATS", page_icon="📄", layout="wide")
st.title("📄 AI Resume Screener — PJS Academy ATS")

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

sbert = load_model()

TECH_SKILLS = ['python','sql','machine learning','deep learning','nlp',
               'tensorflow','pytorch','docker','aws','spark','tableau']

def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    return ' '.join(p.extract_text() or '' for p in reader.pages)

def score_resume(resume_text, jd_text, jd_embedding):
    r_emb  = sbert.encode([resume_text])
    sem    = float(cosine_similarity(jd_embedding, r_emb)[0][0])
    jd_low = jd_text.lower()
    r_low  = resume_text.lower()
    jd_skills = [s for s in TECH_SKILLS if s in jd_low]
    found  = [s for s in jd_skills if s in r_low]
    kw     = len(found) / max(len(jd_skills), 1)
    return round((0.65*sem + 0.35*kw)*100, 1), found

def assign_tier(score):
    if score >= 75: return "🟢 Shortlist"
    elif score >= 55: return "🟡 Review"
    else: return "🔴 Reject"

# --- Input ---
col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("📋 Job Description")
    jd = st.text_area("Paste JD here:", height=250,
                       value="Python Data Scientist with ML, SQL, PyTorch, NLP, Docker, AWS")
with col2:
    st.subheader("📁 Upload Resumes")
    uploaded = st.file_uploader("Upload PDF resumes (multiple allowed):",
                                 type='pdf', accept_multiple_files=True)

if st.button("🔍 Screen Candidates", type="primary") and uploaded and jd:
    jd_embedding = sbert.encode([jd])
    results = []
    progress = st.progress(0)
    for i, f in enumerate(uploaded):
        text  = extract_text(io.BytesIO(f.read()))
        score, skills = score_resume(text, jd, jd_embedding)
        results.append({
            'Candidate': f.name.replace('.pdf',''),
            'Score':     score,
            'Tier':      assign_tier(score),
            'Matched Skills': ', '.join(skills),
        })
        progress.progress((i+1)/len(uploaded))

    df = pd.DataFrame(results).sort_values('Score', ascending=False).reset_index(drop=True)
    df.index += 1

    # Metrics
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Total Screened", len(df))
    m2.metric("Shortlisted 🟢", (df['Tier']=='🟢 Shortlist').sum())
    m3.metric("Review 🟡",      (df['Tier']=='🟡 Review').sum())
    m4.metric("Rejected 🔴",    (df['Tier']=='🔴 Reject').sum())

    st.subheader("🏆 Candidate Leaderboard")
    st.dataframe(df, use_container_width=True)

    # Bar chart
    fig = px.bar(df, x='Candidate', y='Score', color='Score',
                 color_continuous_scale='RdYlGn', range_color=[0,100],
                 title='Candidate Match Scores (%)')
    st.plotly_chart(fig, use_container_width=True)

    # Shortlist email
    shortlist = df[df['Tier']=='🟢 Shortlist']['Candidate'].tolist()
    if shortlist:
        st.subheader("📧 Shortlist Email Draft")
        email = f"""Subject: Interview Invitation — Data Scientist Role

Hi [Candidate Name],

We reviewed your application and are pleased to invite you for an interview.

Shortlisted candidates: {', '.join(shortlist)}

Please reply to schedule a 30-minute call.

Best regards,
PJS Academy Hiring Team
hello@pjsacademy.com"""
        st.code(email, language='text')
        st.download_button("📥 Download Email", email, "shortlist_email.txt")
```

**What v3 adds over v2:**
- Bulk PDF upload — screen 50 resumes in under 30 seconds
- Ranked leaderboard with colour-coded tiers (Shortlist/Review/Reject)
- Skill match breakdown per candidate
- Auto-generated shortlist email — copy and send

---

## 📈 Learning Progression Summary

```
v1 → Rank 3 resumes by TF-IDF word overlap
v2 → Semantic BERT matching + skill gap analysis + NER
v3 → Upload 50 PDFs → ranked leaderboard + shortlist email in under 30 seconds
```

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
