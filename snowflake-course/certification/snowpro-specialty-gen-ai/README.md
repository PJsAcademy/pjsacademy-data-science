# 🎯 SnowPro Specialty: Gen AI — Prep Guide

**PJ's Academy · Prove you can build GenAI apps on Snowflake Cortex.**

The Gen AI Specialty exam (GES-C01) validates skills in building LLM-powered applications on Snowflake using **Cortex** — LLM functions, RAG with Cortex Search, agents, and Snowflake Intelligence.

> **Prerequisite:** SnowPro Core certified.

---

## 📋 Exam At A Glance

| Item | Detail |
|------|--------|
| Exam code | GES-C01 |
| Questions | ~55 |
| Duration | 85 minutes |
| Cost | $225 USD |
| Prerequisite | SnowPro Core |

### Domain Weightings

| # | Domain | Weight |
|---|--------|--------|
| 1 | Snowflake Gen AI & LLM Fundamentals | 25% |
| 2 | Cortex LLM Functions & Prompting | 30% |
| 3 | RAG, Cortex Search & Agents | 30% |
| 4 | Governance, Cost & Evaluation | 15% |

---

## 🤖 Domain 1 — Gen AI Fundamentals (25%)

- LLM basics: tokens, context window, temperature, embeddings, hallucination.
- Snowflake Cortex overview — serverless, governed, in-platform GenAI.
- Available models (Cortex hosts multiple LLMs — Llama, Mistral, Snowflake Arctic, Claude, etc.).
- When to use prompting vs RAG vs fine-tuning.

## 💬 Domain 2 — Cortex LLM Functions & Prompting (30%)

### Core functions
```sql
SELECT SNOWFLAKE.CORTEX.COMPLETE('llama3.1-70b', 'Explain micro-partitions simply');
SELECT SNOWFLAKE.CORTEX.SENTIMENT(review) FROM reviews;
SELECT SNOWFLAKE.CORTEX.SUMMARIZE(article) FROM docs;
SELECT SNOWFLAKE.CORTEX.TRANSLATE(text, 'en', 'hi') FROM messages;
SELECT SNOWFLAKE.CORTEX.EXTRACT_ANSWER(context, 'What is the refund policy?');
SELECT SNOWFLAKE.CORTEX.EMBED_TEXT_768('e5-base-v2', content) FROM docs;
```

### Prompting
- Structured prompts, few-shot examples, JSON-mode / structured outputs.
- `COMPLETE` with options (temperature, max_tokens, response_format, guardrails).
- Cortex **AISQL** — `AI_COMPLETE`, `AI_CLASSIFY`, `AI_FILTER`, `AI_AGG`, `AI_SUMMARIZE_AGG`.

## 🔎 Domain 3 — RAG, Cortex Search & Agents (30%)

### Cortex Search
- Fully-managed hybrid (vector + keyword) search service for RAG.
- Create a search service over a table; query for relevant chunks.

```sql
CREATE CORTEX SEARCH SERVICE docs_search
  ON content ATTRIBUTES title
  WAREHOUSE = search_wh TARGET_LAG = '1 hour'
  AS SELECT content, title FROM knowledge_base;
```

### RAG pattern
1. Chunk & embed documents (or use Cortex Search which manages this).
2. Retrieve relevant chunks for a question.
3. `COMPLETE` with retrieved context → grounded answer.

### Cortex Analyst & Agents
- **Cortex Analyst** — text-to-SQL over a semantic model (natural-language BI).
- **Cortex Agents / Snowflake Intelligence** — orchestrate tools (Search + Analyst) to answer complex questions.

## 🛡️ Domain 4 — Governance, Cost & Evaluation (15%)

- Data stays in Snowflake — RBAC/masking still apply to GenAI.
- Cost model — Cortex functions billed by tokens/credits.
- **Cortex Guard** — safety filtering.
- Evaluation — relevance, groundedness, hallucination checks; `AI_*` eval helpers.

---

## 🧠 High-Yield Facts

- **Cortex Search** = managed hybrid retrieval for RAG (no external vector DB needed).
- **Cortex Analyst** = text-to-SQL over a semantic model.
- **COMPLETE** is the general LLM call; task functions (SENTIMENT, SUMMARIZE) are shortcuts.
- **EMBED_TEXT_768 / EMBED_TEXT_1024** generate embeddings for similarity.
- **Cortex Guard** filters unsafe content.
- Data never leaves Snowflake — governance (RBAC, masking) still applies to GenAI.
- **AISQL** (`AI_CLASSIFY`, `AI_FILTER`, `AI_AGG`) brings LLMs into set-based SQL.

---

## 📝 Practice Questions (10)

**Q1.** The general-purpose Cortex LLM call is:
A) SUMMARIZE  B) COMPLETE  C) SENTIMENT  D) TRANSLATE

**Q2.** Managed hybrid retrieval for RAG is provided by:
A) Cortex Search  B) Snowpipe  C) Streams  D) Marketplace

**Q3.** Natural-language-to-SQL over a semantic model is:
A) Cortex Search  B) Cortex Analyst  C) Cortex Guard  D) COMPLETE

**Q4.** Which generates text embeddings?
A) COMPLETE  B) EMBED_TEXT_768  C) SENTIMENT  D) EXTRACT_ANSWER

**Q5.** RAG grounds an LLM answer by:
A) Fine-tuning  B) Retrieving relevant context then completing  C) Higher temperature  D) More tokens

**Q6.** Unsafe-content filtering in Cortex is:
A) Cortex Guard  B) Masking policy  C) Row policy  D) Network policy

**Q7.** Cortex functions are billed primarily by:
A) Rows  B) Tokens/credits  C) Storage  D) Warehouses

**Q8.** Data used by Cortex:
A) Leaves Snowflake  B) Stays in Snowflake (governed)  C) Goes to OpenAI  D) Is public

**Q9.** Which brings LLM classification into set-based SQL?
A) AI_CLASSIFY  B) COPY  C) FLATTEN  D) PIVOT

**Q10.** Orchestrating Search + Analyst as tools describes:
A) Cortex Agents  B) Snowpipe  C) Streams  D) Clone

### ✅ Answers
1-B · 2-A · 3-B · 4-B · 5-B · 6-A · 7-B · 8-B · 9-A · 10-A

---

## 🗓️ 2-Week Plan
- **Week 1:** LLM fundamentals + Cortex functions + prompting.
- **Week 2:** RAG (Cortex Search), Analyst/Agents, governance + practice.

---

*❄️ Snowflake Mastery — [PJ's Academy](https://pjsacademy.com)*
