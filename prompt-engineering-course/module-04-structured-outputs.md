# Module 04 — Structured Outputs & Tool Calling

> The bridge from "cool demo" to "real software." If you can't parse the output reliably, you can't build on it.

---

## 4.1 Why Structured Output Matters

A chatbot can return prose. An **application** needs data it can parse — JSON, a category label, a number. The whole game here is **reliability**: the output must be machine-readable *every single time*, not 95% of the time.

## 4.2 Getting Clean JSON

**Level 1 — Ask for it (weak):**
```
Return the answer as JSON with keys "name" and "age".
```
Problem: the model may wrap it in prose ("Here's the JSON: ...") or use markdown fences.

**Level 2 — Constrain hard (better):**
```
Respond with ONLY a valid JSON object, no markdown, no explanation.
Schema: {"name": string, "age": number, "verified": boolean}
If a value is unknown, use null.
```

**Level 3 — Use the API's JSON/structured mode (best):**
Most providers now offer a **JSON mode** or **structured outputs** that *guarantee* valid JSON matching a schema.

```python
# OpenAI structured outputs example
from pydantic import BaseModel
class Person(BaseModel):
    name: str
    age: int
    verified: bool

resp = client.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[{"role":"user","content":"Extract: John, 34, confirmed."}],
    response_format=Person,
)
person = resp.choices[0].message.parsed   # guaranteed valid Person
```

> **Rule:** if your provider has structured-output mode, use it. Prompt-only JSON always eventually breaks.

## 4.3 Always Validate

Even with JSON mode, validate in code before trusting it:
```python
import json
try:
    data = json.loads(raw)
    assert "name" in data and isinstance(data["age"], int)
except (json.JSONDecodeError, AssertionError):
    # retry, repair, or fall back
    ...
```
**Never** feed raw LLM output straight into a database, API, or `eval()`. Treat it as untrusted input.

## 4.4 Schema-First Prompting with Pydantic

Define the shape you want, then let the schema drive the prompt. This makes outputs self-documenting and validated:

```python
from pydantic import BaseModel, Field
from typing import Literal

class Ticket(BaseModel):
    category: Literal["Billing","Technical","Account"]
    priority: Literal["low","medium","high"]
    summary: str = Field(max_length=120)
    needs_human: bool
```
The `Literal` types force the model into valid categories — no more "Billng" typos breaking your pipeline.

## 4.5 Tool / Function Calling

Instead of guessing, the model can **call functions you define** — the mechanism behind agents, plugins, and "AI that does things."

**How it works:**
1. You describe available tools (name, description, parameters) to the model.
2. The model, when appropriate, returns a **structured request** to call a tool with arguments.
3. **Your code runs the tool** and returns the result.
4. The model uses the result to answer.

```python
tools = [{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get current weather for a city",
    "parameters": {
      "type": "object",
      "properties": {"city": {"type": "string"}},
      "required": ["city"]
    }
  }
}]

# Model returns: {"name": "get_weather", "arguments": {"city": "Mumbai"}}
# YOU run get_weather("Mumbai"), send the result back, model answers.
```

**Critical points:**
- The model **does not run the tool** — it only asks. Your code executes and returns results. (This is also a safety boundary.)
- Great tool **descriptions** matter as much as prompts — the model chooses tools based on them.
- The model can call multiple tools, in sequence or parallel.

## 4.6 Writing Great Tool Descriptions

The description is a prompt. Be precise about *when* to use the tool and what each parameter means:

```
name: search_orders
description: Look up a customer's orders by email. Use ONLY when the user asks
            about their order status, history, or a specific order. Do not use
            for general product questions.
parameters:
  email (string, required): the customer's email address
  status (string, optional): filter by "shipped" | "pending" | "delivered"
```

## 4.7 Handling Failures Gracefully

- **Retry with repair:** if JSON is malformed, send it back: "This JSON is invalid: {err}. Return corrected JSON only."
- **Fallbacks:** if the model can't produce valid output twice, degrade gracefully (ask a human, return a default).
- **Idempotency:** design tools so a repeated call is safe.

---

## ✅ Key Takeaways
1. Applications need **machine-readable output** — reliability is the whole game.
2. Use the provider's **structured-output/JSON mode**; prompt-only JSON eventually breaks.
3. **Always validate** LLM output in code — treat it as untrusted.
4. **Pydantic + Literal types** force valid categories and shapes.
5. **Tool calling** lets the model request actions; *your code* executes them.
6. Tool **descriptions are prompts** — write them carefully.

## 🏋️ Exercises
1. Prompt an LLM to extract 3 fields as JSON, then parse it in Python. Break it, then fix with stricter instructions.
2. Define a Pydantic model with `Literal` categories and use it for structured extraction.
3. Design (on paper) 3 tools for a food-delivery assistant with precise descriptions and parameters.

**Next:** [Module 05 — RAG & Context Engineering →](module-05-rag-context.md)

---

*🧠 Prompt Engineering Mastery — [PJ's Academy](https://pjsacademy.com)*
