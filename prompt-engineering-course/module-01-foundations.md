# Module 01 — Foundations: How LLMs Actually Work

> You can't engineer a system you don't understand. This module gives you the mental model that makes every later technique obvious.

---

## 1.1 What an LLM Really Does

An LLM does **one** thing: given some text, it predicts the next token, over and over. That's it. Everything else — reasoning, coding, translation — is an emergent behaviour of a very good next-token predictor.

**Why this matters for you:** the model has no memory, no intent, and no access to truth. It continues text in a way that *looks* plausible given its training. Your job as a prompt engineer is to shape the input so the most plausible continuation is also the *correct* one.

## 1.2 Tokens — the Unit of Everything

LLMs don't see words or letters — they see **tokens** (chunks of text, roughly ¾ of a word).

- "prompt engineering" ≈ 2 tokens
- "unbelievable" ≈ 3 tokens ("un", "believ", "able")
- Numbers, code, and rare words use more tokens

**Practical consequences:**
- **Cost** is per token (input + output). Shorter prompts = cheaper.
- **Context limits** are measured in tokens (e.g., 128K, 200K).
- Models are worse at **character-level** tasks (counting letters, reversing strings) because they see tokens, not characters.

> 💡 Try it: ask an LLM "how many r's in strawberry?" — the classic failure. Now you know why: it sees tokens, not letters.

## 1.3 The Context Window

The context window is the model's **entire working memory** for one request — your prompt + its reply must fit inside it.

```
[ System prompt ][ Conversation history ][ Your message ][ ← room for the reply ]
└──────────────────── total must fit in the context window ────────────────────┘
```

- The model has **no memory between separate API calls** — each call is stateless. "Memory" in a chatbot is just the app re-sending history every time.
- Information in the **middle** of a long context is often used less reliably than the start or end ("lost in the middle"). Put critical instructions at the start or end.

## 1.4 The Two Dials: Temperature & Top-p

The model produces a probability distribution over the next token. **Sampling settings** control how it picks from that distribution.

| Setting | Low value | High value |
|---------|-----------|------------|
| **Temperature** (0–2) | Deterministic, focused, repetitive | Creative, varied, risky |
| **Top-p** (0–1) | Only the most likely tokens | Wider variety allowed |

**Rules of thumb:**
- **Factual / extraction / code:** temperature **0–0.3** (you want consistency).
- **Brainstorming / creative writing:** temperature **0.7–1.0**.
- Change **one** dial, not both. Start with temperature.

## 1.5 System vs User vs Assistant Roles

Modern chat models take messages with roles:

- **System** — sets behaviour, persona, rules ("You are a careful legal assistant. Never give advice, only summarise."). The highest-priority instruction.
- **User** — the human's request.
- **Assistant** — the model's replies (and where you can put example answers for few-shot).

> The system prompt is your steering wheel. Most "the AI won't behave" problems are solved by a better system prompt.

## 1.6 Why LLMs Hallucinate

A hallucination is the model producing plausible-sounding but false text. It happens because:
1. The model optimises for **plausibility**, not truth.
2. It will always try to answer — it doesn't natively "know" when it doesn't know.
3. Gaps in training data get filled with confident guesses.

**The three cures (previewed here, detailed later):**
1. **Grounding** — give it the facts in the prompt (RAG).
2. **Permission to say "I don't know."**
3. **Verification** — have it check its own or another model's output.

## 1.7 Capabilities & Limits (2026 reality check)

**LLMs are excellent at:** summarising, rewriting, classifying, extracting, drafting, translating, explaining, coding, reasoning over provided text.

**LLMs are unreliable at:** exact arithmetic, counting characters, real-time facts, citing exact sources from memory, anything requiring true up-to-date knowledge. → For these, give them **tools** (calculator, search, code execution) instead of trusting memory.

---

## ✅ Key Takeaways
1. An LLM predicts the next token — shape the input so the right answer is the most plausible continuation.
2. Everything is measured in **tokens** (cost, context, character-level weakness).
3. Each API call is **stateless**; "memory" is re-sent history.
4. **Temperature low** for facts/code, **high** for creativity.
5. The **system prompt** is your main control surface.
6. Hallucination comes from optimising plausibility — fix it with grounding, permission to abstain, and verification.

## 🏋️ Exercises
1. Take any prompt you've written and estimate its token count (use an online tokenizer). Cut it 30% without losing meaning.
2. Ask the same factual question at temperature 0 and temperature 1 (via API or playground). Note the difference in consistency.
3. Write a system prompt that turns a general chatbot into a "concise Python tutor who never gives the full answer, only hints."

**Next:** [Module 02 — Core Techniques →](module-02-core-techniques.md)

---

*🧠 Prompt Engineering Mastery — [PJ's Academy](https://pjsacademy.com)*
