# 🤖 Project 14 — AI Content Generator

**Phase 5 — GenAI & NLP** | Beginner → Real-Time (3 Versions)

---

## 🗺️ Version Roadmap

| Version | What You Build | Complexity |
|---------|---------------|------------|
| v1.0 — Starter | Generate blog, LinkedIn, Instagram, email content with OpenAI | ⭐ Beginner |
| v2.0 — Improved | Brand voice training + content calendar + A/B headline testing | ⭐⭐ Intermediate |
| v3.0 — Real-Time | Full SaaS content tool — multi-platform, schedule, analytics | ⭐⭐⭐ Advanced |

---

## 📦 Libraries Needed
```bash
pip install openai streamlit pandas plotly python-docx schedule
```

---

## 🟢 v1.0 — Multi-Platform Content Generator

**Skills:** OpenAI API, prompt engineering, zero-shot generation

```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def generate(prompt, max_tokens=500, temperature=0.7):
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        max_tokens=max_tokens,
        temperature=temperature
    ).choices[0].message.content.strip()

topic = "Why Python is the best language for Data Science"

# Blog Post
blog = generate(f"""Write a 300-word blog post about: "{topic}"
Format: H1 headline → intro → 3 sub-headings → conclusion with CTA.
Start directly with the headline.""")
print("=== BLOG POST ===")
print(blog)

# LinkedIn
linkedin = generate(f"""Write a viral LinkedIn post about: "{topic}"
Rules: hook first line, short paragraphs, 3-5 insights, question at end, 5 hashtags.
Under 200 words.""")
print("\n=== LINKEDIN POST ===")
print(linkedin)

# Instagram caption
instagram = generate(f"""Write an Instagram caption about: "{topic}"
Style: educational, emojis, bullet points. Hook first, CTA last, 10 hashtags.""")
print("\n=== INSTAGRAM CAPTION ===")
print(instagram)

# Email subject lines
subjects = generate(f"""Generate 10 email subject lines for: "{topic}"
Mix: curiosity gap, numbers, urgency, personal, question. Numbered list only.""")
print("\n=== EMAIL SUBJECT LINES ===")
print(subjects)
```

**What v1 teaches:** Prompt structure matters more than parameters — specific format instructions give consistent, usable output.

---

## 🟡 v2.0 — Brand Voice + Content Calendar + A/B Testing

**New in v2:** Brand voice profile, consistent tone across all content, content calendar generator, A/B subject line scoring

```python
from openai import OpenAI
import pandas as pd
from datetime import datetime, timedelta
import json

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

# --- Brand Voice Profile ---
BRAND_PROFILE = {
    "name": "PJS Academy",
    "tone": "friendly, educational, empowering — like a senior mentor teaching a junior",
    "avoid": "corporate jargon, passive voice, overpromising",
    "audience": "aspiring data scientists in India, age 20-30",
    "cta_style": "Follow @pjsacademy.datascience | Enrol at pjsacademy.com",
    "signature_phrases": [
        "Learn it once, apply it forever",
        "Data science is not magic — it's math + code + curiosity",
        "From beginner to job-ready in 90 days"
    ]
}

def generate_on_brand(content_type, topic):
    system_prompt = f"""You are the content writer for {BRAND_PROFILE['name']}.
Tone: {BRAND_PROFILE['tone']}
Avoid: {BRAND_PROFILE['avoid']}
Target audience: {BRAND_PROFILE['audience']}
CTA to include: {BRAND_PROFILE['cta_style']}
Occasionally use one of these phrases: {BRAND_PROFILE['signature_phrases']}"""

    prompts = {
        "linkedin": f"""Write a LinkedIn post about: "{topic}"
Rules: strong hook, 3-4 insights, question, 5 relevant hashtags. Under 220 words.""",
        "instagram": f"""Write an Instagram caption about: "{topic}"
Style: educational, emojis, 5 bullet tips, strong CTA, 10 hashtags.""",
        "email": f"""Write a cold email about: "{topic}" for our course launch.
Format: Subject line, greeting, 3 short paragraphs, PS line.""",
        "thread": f"""Write a Twitter/X thread about: "{topic}"
Format: 6 tweets, numbered 1/6 to 6/6. Each tweet under 280 chars."""
    }

    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":prompts[content_type]}
        ],
        temperature=0.7
    ).choices[0].message.content.strip()

topic = "5 Python libraries every Data Scientist must know"
for ctype in ['linkedin','instagram','thread']:
    print(f"\n{'='*50}\n{ctype.upper()}\n{'='*50}")
    print(generate_on_brand(ctype, topic))

# --- 30-Day Content Calendar Generator ---
def generate_content_calendar(themes, start_date=datetime.today()):
    platforms = ['LinkedIn', 'Instagram', 'Email', 'Blog']
    calendar  = []
    for i in range(30):
        date    = start_date + timedelta(days=i)
        theme   = themes[i % len(themes)]
        platform = platforms[i % len(platforms)]
        topic_prompt = (f"Give ONE specific content topic (10 words max) for a "
                        f"{platform} post about the theme: '{theme}'. "
                        f"For a data science education brand. Topic only, no explanation.")
        topic = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":topic_prompt}],
            max_tokens=30
        ).choices[0].message.content.strip()

        calendar.append({'Date': date.strftime('%Y-%m-%d'),
                         'Day': date.strftime('%A'),
                         'Platform': platform,
                         'Theme': theme,
                         'Topic': topic})

    return pd.DataFrame(calendar)

themes = ['Python basics','Data visualisation','Machine learning',
          'Career tips','Real projects','AI & GenAI','Student success']
cal = generate_content_calendar(themes)
print("\n30-Day Content Calendar (first 7 days):")
print(cal.head(7).to_string(index=False))
cal.to_csv('content_calendar.csv', index=False)
print("Saved: content_calendar.csv")

# --- A/B Email Subject Line Scorer ---
def score_subject_lines(lines):
    prompt = f"""Rate these email subject lines from 1-10 for open rate potential.
Consider: curiosity, urgency, personalisation, clarity, length.

Subject lines:
{chr(10).join(f'{i+1}. {l}' for i, l in enumerate(lines))}

Return JSON: [{{"line": "...", "score": 8, "reason": "..."}}]
JSON only, no explanation."""

    result = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.3
    ).choices[0].message.content

    try:
        data = json.loads(result)
        df = pd.DataFrame(data).sort_values('score', ascending=False)
        print("\nSubject Line Scores:")
        print(df[['line','score','reason']].to_string(index=False))
        return df
    except:
        print(result)

test_lines = [
    "New Python course available",
    "I failed 3 job interviews. Here's what I learned.",
    "⚡ 5 Data Science projects you can build this weekend",
    "Last chance: Course closes Friday",
    "Do you know what interviewers actually look for?"
]
score_subject_lines(test_lines)
```

**What v2 adds over v1:**
- Brand voice system prompt — ALL content sounds like your brand, not generic AI
- 30-day content calendar — 30 unique topics across platforms, auto-generated
- A/B subject line scorer — GPT rates your subject lines and explains why

---

## 🔴 v3.0 — Full Content SaaS with Streamlit

**New in v3:** Topic → 4-platform content in one click, history tracker, copy buttons, docx export

```python
# app.py — AI Content Generator SaaS
# Run: streamlit run app.py
import streamlit as st
from openai import OpenAI
import pandas as pd
from datetime import datetime
from docx import Document
import io, json

st.set_page_config(page_title="AI Content Generator", page_icon="✍️", layout="wide")
st.title("✍️ AI Content Generator — PJS Academy")
st.caption("One topic → Blog + LinkedIn + Instagram + Email in 30 seconds")

@st.cache_resource
def get_client():
    return OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", "YOUR_KEY"))

client = get_client()

if 'history' not in st.session_state:
    st.session_state.history = []

BRAND_VOICE = """You are the content writer for PJS Academy — a data science education brand.
Tone: friendly, educational, empowering (like a senior mentor).
Audience: aspiring data scientists in India, age 20-30.
CTA always includes: Follow @pjsacademy.datascience | pjsacademy.com"""

TEMPLATES = {
    "📝 Blog Post":        "Write a 350-word blog post with H1 headline, intro, 3 sub-sections, CTA conclusion.",
    "💼 LinkedIn Post":    "Write a viral LinkedIn post with hook, 4 insights, question, 5 hashtags. Under 220 words.",
    "📸 Instagram Caption":"Write Instagram caption with hook, 5 emoji bullet tips, CTA, 10 hashtags.",
    "📧 Email Newsletter": "Write email newsletter with subject line, greeting, 3 short paragraphs, PS.",
    "🐦 Twitter Thread":   "Write 6-tweet thread, numbered 1/6 to 6/6, each under 280 chars.",
    "📋 Email Subjects":   "Generate 10 high-converting email subject lines. Numbered list only.",
}

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    tone = st.selectbox("Tone:", ["Educational","Motivational","Conversational","Professional"])
    creativity = st.slider("Creativity (temperature):", 0.3, 1.0, 0.7, 0.1)

    st.header("📚 History")
    if st.session_state.history:
        for h in st.session_state.history[-5:][::-1]:
            st.caption(f"🕐 {h['time']} | {h['topic'][:30]}...")
    if st.button("🗑️ Clear History"):
        st.session_state.history = []

# Main
topic    = st.text_input("📌 Content Topic:",
                          placeholder="e.g. 5 Python libraries every Data Scientist needs")
selected = st.multiselect("Select content types:", list(TEMPLATES.keys()),
                           default=["📝 Blog Post","💼 LinkedIn Post","📸 Instagram Caption"])

col1, col2 = st.columns([1,4])
generate_btn = col1.button("✨ Generate All", type="primary")
clear_btn    = col2.button("🔄 Clear")

if generate_btn and topic and selected:
    results = {}
    progress = st.progress(0)

    for i, ctype in enumerate(selected):
        with st.spinner(f"Writing {ctype}..."):
            prompt = f"""Topic: "{topic}"
Tone: {tone}
Task: {TEMPLATES[ctype]}"""
            result = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":BRAND_VOICE},
                    {"role":"user","content":prompt}
                ],
                temperature=creativity,
                max_tokens=600
            ).choices[0].message.content.strip()
            results[ctype] = result
        progress.progress((i+1)/len(selected))

    st.session_state.history.append({
        'time': datetime.now().strftime('%H:%M'),
        'topic': topic,
        'results': results
    })

    for ctype, content in results.items():
        with st.expander(f"✅ {ctype}", expanded=True):
            st.markdown(content)
            col_a, col_b = st.columns(2)
            col_a.download_button(f"📥 Download",
                                   content.encode(), f"{ctype.replace(' ','_')}.txt",
                                   key=f"dl_{ctype}")

    # Export all to Word doc
    if len(results) > 1:
        doc = Document()
        doc.add_heading(f'Content Pack — {topic}', 0)
        for ctype, content in results.items():
            doc.add_heading(ctype, level=1)
            doc.add_paragraph(content)
            doc.add_page_break()
        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)
        st.download_button("📄 Download All as Word Doc",
                            buf, f"content_pack_{datetime.now().strftime('%Y%m%d')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
```

**What v3 adds over v2:**
- Multi-type generator — select Blog + LinkedIn + Instagram + Email → all in one click
- Brand voice baked into system prompt — consistent across everything
- Word doc export — all content types in one formatted document
- History tracker — last 5 sessions saved, never lose a generated piece
- Creativity slider — control how experimental the output is

---

## 📈 Learning Progression Summary

```
v1 → Generate blog/LinkedIn/Instagram/email from one topic
v2 → Brand-consistent content + 30-day calendar + A/B subject scoring
v3 → Full SaaS — pick topic, pick platforms, get 4 pieces + Word export in 30 seconds
```

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
