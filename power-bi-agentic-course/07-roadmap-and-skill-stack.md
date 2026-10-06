# Module 7 — The 2027 skill stack and a 90-day roadmap

The thesis of this course in one sentence: **Power BI development is
becoming analytics engineering with an AI pair.** The job description
that paid in 2022 does not pay in 2027.

## The 2027 skill stack

```mermaid
mindmap
  root((Power BI Dev<br/>2027))
    Core Power BI
      Semantic modelling
      DAX fluency
      Report design
      Visual calculations
    Data
      SQL
      Fabric
        Lakehouse
        Warehouse
        DirectQuery
      Dimensional modelling
    Engineering
      Git
      PBIP + TMDL
      CI / CD
      Code review
      Testing
    APIs and integration
      Fabric REST
      Power BI REST
      Service principals
    AI
      MCP
      Copilot
      Agentic authoring
      Prompt design
      Governance of AI edits
    Soft
      Stakeholder translation
      Writing for Copilot
      Reviewing AI output
```

If you are strong in two branches and weak in four, you are a 2022
developer. Aim for competence in all six by end of 2026.

## What's dropping out

- **Expertise in `.pbix` as the unit of work.** PBIP replaces it.
- **Clicking through the UI as the primary authoring mode.** Still
  useful; no longer sufficient.
- **"I don't do code reviews."** The industry does.
- **Doing all the DAX writing yourself.** You review DAX now. The agent
  drafts.

## What's rising

- **Semantic model as product.** The model is an API consumed by humans,
  Copilots, agents, and downstream reports. Treat it like one.
- **Writing for Copilot.** Descriptions, synonyms, verified answers.
  Non-trivial craft.
- **Reviewing AI edits.** The highest-leverage skill of the next three
  years. If you can tell "subtly wrong DAX" from "correct DAX", you're
  valuable.
- **Governance.** Who can let the agent write to prod? Auditable how?
  Someone has to answer this. Might as well be you.

## 90-day roadmap

```mermaid
gantt
    title 90-day Power BI 2027 prep
    dateFormat  YYYY-MM-DD
    axisFormat  Day %d
    section Weeks 1-2 (Foundations)
    TMDL view fluency           :a1, 2026-01-01, 10d
    UDFs refactor one model     :a2, after a1, 4d
    section Weeks 3-4 (Engineering)
    PBIP + Git on a real model  :b1, after a2, 7d
    Set up CI validation        :b2, after b1, 3d
    PR workflow with a teammate :b3, after b2, 4d
    section Weeks 5-6 (AI)
    Install MCP client          :c1, after b3, 2d
    Agentic authoring exercises :c2, after c1, 8d
    section Weeks 7-8 (Service)
    DirectQuery model in Service :d1, after c2, 5d
    Visual Calculations          :d2, after d1, 3d
    Design ribbon + themes       :d3, after d2, 2d
    section Weeks 9-10 (Copilot)
    Document a model for Copilot :e1, after d3, 7d
    Register verified answers    :e2, after e1, 3d
    section Weeks 11-13 (Capstone)
    Capstone project             :f1, after e2, 21d
```

### Capstone project

Pick a dataset you care about (public or your own). Deliver:

1. A PBIP in Git with meaningful commits and at least one merged PR.
2. A semantic model with:
   - TMDL you wrote by hand for at least one table.
   - A UDF library of ≥ 3 reusable functions.
   - Descriptions and synonyms on every measure.
   - RLS with two personas.
3. A thin report that uses Visual Calculations where appropriate.
4. One Copilot interaction documented (prompt → DAX → explanation),
   with a short note on how the model's documentation helped.
5. One agent interaction (MCP) that proposes a change, which you review
   and either merge or reject with written reasoning.
6. A CI job that validates TMDL on every PR.

Portfolio piece. Push it to GitHub. Link from your CV.

## How to keep learning after the 90 days

- **Power BI monthly release notes.** Read every one. 15 minutes.
- **Microsoft Fabric blog.** The headline announcements live there.
- **Rui Romano, Chris Webb, Marco Russo / Alberto Ferrari, Reid Havens,
  Guy in a Cube.** Four blogs and one YouTube channel will keep you
  current.
- **MCP spec repo on GitHub.** Watch releases.
- **One side project per quarter.** Reading isn't learning.

## Reality check, closing

A Power BI developer who ignores this stack through 2026 will spend
2027 competing with developers who didn't. The tools are not magic;
they are learnable in a quarter of focused evenings. The hard part is
noticing in time that the ground shifted. You just did. Start Module 1.

[← Back to README](./README.md)
