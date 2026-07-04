# Module 05 — RAG & Context Engineering

> The #1 way to stop hallucination and make LLMs useful on *your* data: give them the facts. This module is the heart of building trustworthy AI.

---

## 5.1 The Core Idea

An LLM only knows its training data (frozen, general, sometimes outdated). **RAG (Retrieval-Augmented Generation)** fixes this: retrieve the relevant facts *at query time* and put them in the prompt, so the model answers from **provided context** instead of memory.

```
User question → Retrieve relevant docs → Stuff into prompt → LLM answers from them
```

**Why it works:** answering from text you gave it is a task LLMs are *excellent* at (reading comprehension). Recalling exact facts from training is a task they're *bad* at. RAG converts the hard task into the easy one.

## 5.2 The RAG Pipeline

```
INDEXING (once):
  Documents → Chunk → Embed → Store in vector DB

QUERYING (each request):
  Question → Embed → Similarity search → Top-k chunks → Prompt → Answer
```

**Step by step:**
1. **Chunk** documents into passages (e.g., 300–800 tokens with slight overlap).
2. **Embed** each chunk into a vector (a list of numbers capturing meaning).
3. **Store** vectors in a vector database (Chroma, FAISS, Pinecone, pgvector, or Snowflake Cortex Search).
4. At query time, **embed the question**, find the most similar chunks (cosine similarity), and inject them.

## 5.3 The Grounding Prompt (this is where prompt engineering lives)

Retrieval gets the facts; the **prompt** makes the model use them faithfully.

```
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't have that information."
Do not use outside knowledge. Cite the source number in [brackets].

Context:
[1] {chunk 1}
[2] {chunk 2}
[3] {chunk 3}

Question: {user question}
Answer:
```

Every line here does a job:
- **"ONLY the context"** — prevents mixing in hallucinated memory.
- **"say I don't have it"** — the abstention out (kills confident wrong answers).
- **"cite the source"** — makes answers verifiable and traceable.

## 5.4 Chunking Strategy (make-or-break)

Bad chunking = bad retrieval, no matter how good the model.

- **Too small:** loses context ("it increased 20%" — increased *what*?).
- **Too large:** dilutes relevance, wastes tokens, buries the answer.
- **Sweet spot:** semantically coherent passages (a section, a few paragraphs), with **overlap** (~10–20%) so ideas aren't cut mid-thought.
- **Structure-aware chunking:** split on headings/sections, not blind character counts. Keep tables and lists intact.

## 5.5 Retrieval Quality

Getting the *right* chunks matters more than the model:
- **Top-k:** retrieve 3–8 chunks. More isn't always better (noise + "lost in the middle").
- **Hybrid search:** combine semantic (vector) + keyword (BM25) search — catches both meaning and exact terms (names, IDs, error codes).
- **Re-ranking:** retrieve 20 candidates, then use a cross-encoder to re-rank and keep the best 4. Big quality boost.
- **Metadata filtering:** filter by date, source, or permissions before/after retrieval.

## 5.6 Context Engineering (beyond RAG)

"Context engineering" = deliberately managing everything in the context window:

- **Order matters:** put the most important info at the **start or end** (models under-use the middle).
- **Compress:** summarise long histories instead of re-sending everything.
- **Relevance over volume:** 3 great chunks beat 15 mediocre ones. Filler *hurts*.
- **Structure the context:** label sections clearly (`## Retrieved Docs`, `## Conversation History`, `## Task`).
- **Budget tokens:** reserve room for the answer; don't fill 100% of the window with input.

## 5.7 Common RAG Failure Modes & Fixes

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Answers ignore the docs | Weak grounding prompt | Add "ONLY use context" + abstention |
| Retrieves irrelevant chunks | Bad chunking/embeddings | Fix chunk size, add re-ranking |
| Misses exact terms (IDs, names) | Pure semantic search | Add keyword/hybrid search |
| Confidently wrong | No abstention instruction | "Say I don't know if not present" |
| Cites wrong source | No source labels | Number chunks, require citation |

## 5.8 When to Use RAG vs Fine-Tuning vs Long Context

- **RAG:** knowledge that changes, is large, or needs citations/permissions. **Default choice.**
- **Fine-tuning:** teaching a *style/format/behaviour*, not facts. Doesn't add fresh knowledge well.
- **Just paste it in (long context):** small, one-off documents that fit easily — simplest, no infra.

---

## ✅ Key Takeaways
1. **RAG** turns "recall from memory" (hard) into "read the provided text" (easy) — the anti-hallucination workhorse.
2. Pipeline: chunk → embed → store → retrieve → **ground in the prompt**.
3. The **grounding prompt** ("ONLY the context", abstain, cite) is where prompt engineering earns its keep.
4. **Chunking + retrieval quality** matter more than the model choice.
5. Use **hybrid search + re-ranking** for serious systems.
6. **Context engineering:** relevance over volume, important info at the edges.

## 🏋️ Exercises
1. Paste a document into an LLM with the grounding prompt from 5.3. Ask something not in it — confirm it abstains.
2. Chunk a long doc two ways (500 chars vs section-based). Compare which gives better answers.
3. Write a grounding prompt that forces `[source]` citations and test it.

**Next:** [Module 06 — Production & Agents →](module-06-production-agents.md)

---

*🧠 Prompt Engineering Mastery — [PJ's Academy](https://pjsacademy.com)*
