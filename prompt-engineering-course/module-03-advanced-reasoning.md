# Module 03 — Advanced Reasoning Techniques

> How to make an LLM *think* before it answers — the techniques that turn a guesser into a reasoner.

---

## 3.1 Chain-of-Thought (CoT)

Ask the model to **reason step by step** before answering. Because it generates the reasoning as tokens, later tokens can "see" and build on earlier reasoning — dramatically improving accuracy on math, logic, and multi-step tasks.

**Without CoT:**
```
Q: A shop has 23 apples. It sells 8, then buys 12 more. How many now?
A: 27   (often wrong — the model jumps to an answer)
```

**With CoT:**
```
Q: A shop has 23 apples. It sells 8, then buys 12 more. How many now?
Think step by step, then give the final number.

A: Start: 23. After selling 8: 23 - 8 = 15. After buying 12: 15 + 12 = 27. Final: 27.
```

The magic phrase: **"Let's think step by step"** or **"Show your reasoning before answering."**

> ⚠️ In production, CoT reasoning bloats output/cost and you may not want to show it. Ask for reasoning in a hidden field, or use it during development and strip it in prod. Newer "reasoning models" do this internally.

## 3.2 Zero-Shot CoT vs Few-Shot CoT

- **Zero-shot CoT:** just add "think step by step." Cheap, surprisingly effective.
- **Few-shot CoT:** provide examples that *include* the reasoning. More reliable for domain-specific reasoning patterns.

```
Q: [example problem]
A: [worked-out reasoning] → [answer]

Q: [example problem 2]
A: [worked-out reasoning] → [answer]

Q: [real problem]
A:
```

## 3.3 Self-Consistency

Run the same CoT prompt **multiple times at higher temperature**, then take the **majority answer**. Different reasoning paths that converge on the same answer are more likely correct.

```
Generate 5 independent solutions → count the final answers → pick the most common.
```

Costs 5x but meaningfully boosts accuracy on hard problems. Use for high-stakes reasoning where correctness > cost.

## 3.4 Decomposition — Break It Down

Hard task? Split it into sub-tasks, solve each, then combine. Two ways:

**A) In one prompt (prompt chaining by instruction):**
```
1. First, list the key claims in the article.
2. Then, for each claim, judge if the evidence supports it.
3. Finally, give an overall credibility score.
```

**B) Across multiple prompts (real chaining — Module 06):**
Prompt 1 output → feeds into Prompt 2 → feeds into Prompt 3. More control, easier to debug, each step is simpler.

> **Golden rule:** a prompt that does one thing well beats a prompt that does five things poorly. Decompose.

## 3.5 ReAct — Reason + Act (foundation of agents)

ReAct interleaves **reasoning** and **actions** (tool calls). The model thinks, decides to use a tool, sees the result, thinks again.

```
Thought: I need the current population of Tokyo. I don't know it reliably.
Action: search("Tokyo population 2026")
Observation: ~14 million
Thought: Now I can answer.
Answer: About 14 million.
```

This loop is the **core of AI agents** (Module 06). It solves the "LLMs don't know real-time facts" problem by letting the model *fetch* instead of *guess*.

## 3.6 Step-Back Prompting

Before solving a specific problem, ask the model to first state the **general principle**. Then solve using that principle.

```
Before answering, state the relevant physics principle. Then apply it to the problem.
```

This grounds the specific answer in correct fundamentals — great for technical and scientific questions.

## 3.7 Self-Critique & Refinement

Have the model **review its own answer** and improve it.

```
1. Draft an answer.
2. Critique your draft: what's weak, missing, or possibly wrong?
3. Write an improved final answer addressing your critique.
```

Or use a **second model/call as a critic** ("You are a strict reviewer. Find errors in this answer."). This is the basis of many quality-boosting and safety systems.

## 3.8 When NOT to Use These

- Simple tasks (classification, extraction) don't need CoT — it wastes tokens and can even hurt.
- Reasoning models (o-series, thinking models) do CoT internally — adding "think step by step" is often redundant.
- Match the technique to the task's difficulty.

---

## ✅ Key Takeaways
1. **Chain-of-thought** ("think step by step") boosts multi-step accuracy by making reasoning explicit.
2. **Self-consistency** = run CoT several times, take the majority answer.
3. **Decompose** hard tasks — one prompt, one job.
4. **ReAct** interleaves reasoning with tool calls — the foundation of agents.
5. **Self-critique** catches errors before the user sees them.
6. Don't over-apply — simple tasks don't need reasoning scaffolds.

## 🏋️ Exercises
1. Give an LLM a word problem with and without "think step by step." Compare.
2. Run a tricky logic puzzle 5 times at temperature 0.8 and take the majority answer.
3. Turn a complex request into a 3-step decomposed prompt. Note the quality jump.
4. Make the model draft → critique → refine an email. Compare draft vs final.

**Next:** [Module 04 — Structured Outputs & Tools →](module-04-structured-outputs.md)

---

*🧠 Prompt Engineering Mastery — [PJ's Academy](https://pjsacademy.com)*
