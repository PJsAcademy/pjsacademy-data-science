# Power BI 2027 Prep: Agentic, AI-Ready Development

A preparation tutorial for Power BI developers who want to stay employable
through 2027. The industry is moving from "build reports" to
"engineer AI-ready analytics solutions," and the skill stack is widening
fast. This course walks through what to learn, in what order, and how to
actually practice each piece.

> **Reality check up front.** You cannot learn most of this by reading.
> TMDL view, PBIP, Visual Calculations, MCP, Copilot — all require Power
> BI Desktop (Windows) and, for several topics, a Fabric or Power BI
> Premium / PPU workspace. This doc gives you the mental model, the setup
> checklist, the commands/code, and the exercises. Follow it with
> hands-on practice or it won't stick.

## Who this is for

- Power BI developers who shipped reports in 2023–2025 and now feel the
  ground shifting under them.
- Analytics engineers who use Power BI as a presentation layer on top of
  dbt / Fabric / Snowflake and want to speak the modern Power BI dialect.
- Data scientists who need to hand models to a BI team and want to
  understand what "semantic model" and "agentic authoring" actually mean.

## The learning order

Learn the four foundational skills from the infographic **in order**.
Each one makes the next easier.

| # | Skill | Why it's first | Module |
|---|-------|----------------|--------|
| 1 | **TMDL view** | Your whole semantic model as plain text. Pre-req for Git, code review, and anything agentic. | [01-tmdl-view.md](./01-tmdl-view.md) |
| 2 | **User-defined functions (UDFs)** | Write a DAX calc once, reuse everywhere. Shrinks model size and makes AI-generated DAX reviewable. | [02-udfs.md](./02-udfs.md) |
| 3 | **PBIP + Git** | File-based project format. Diffs, pull requests, CI/CD — the software-engineering practices Power BI was missing. | [03-pbip-git.md](./03-pbip-git.md) |
| 4 | **MCP + AI agents** | Tell an agent what you need; it edits the model for you. Only safe once you can read TMDL and review Git diffs. | [04-mcp-ai-agents.md](./04-mcp-ai-agents.md) |

Then widen into the ecosystem:

| # | Topic | Module |
|---|-------|--------|
| 5 | Copilot + Fabric IQ | [05-copilot-fabric-iq.md](./05-copilot-fabric-iq.md) |
| 6 | Service features: DirectQuery semantic models, Visual Calculations, Design ribbon, Outlook live visuals, Initial axis scroll | [06-service-and-ux.md](./06-service-and-ux.md) |
| 7 | The 2027 skill stack and a 90-day roadmap | [07-roadmap-and-skill-stack.md](./07-roadmap-and-skill-stack.md) |

## What's GA vs Preview (as of late 2025 / 2026)

GA = generally available, safe for production.
Preview = usable but can change; don't bet a client deliverable on it.

| Feature | Status |
|---|---|
| Power BI Projects (PBIP) + TMDL | GA |
| Visual Calculations | GA |
| Initial Axis Scroll Position | GA |
| New Design Ribbon | GA |
| Power BI Agentic Experiences (Authoring, Desktop Bridge) | GA |
| User-defined functions (DAX UDFs) | GA |
| Microsoft 365 Copilot + Power BI | Preview |
| Fabric IQ + Power BI Copilot | Rolling GA |
| Remote Power BI Authoring MCP | Preview |
| DirectQuery semantic models in Service | GA |
| Live Power BI visuals in Outlook | Preview |

Always double-check the Power BI release wave notes before telling a
client "this is GA" — Microsoft shifts status between monthly releases.

## Setup you need before Module 1

1. **Windows machine or VM** (Power BI Desktop is Windows-only; Mac users:
   Parallels, a cloud Windows VM, or Fabric web authoring).
2. **Power BI Desktop** — current month's release.
   Download: `https://aka.ms/pbidesktopstore`.
3. **A Fabric or Power BI PPU workspace** for the Service-side features
   (Modules 5, 6). A free Fabric trial works.
4. **Git** — any client. Command line is enough.
   `git --version` should return something.
5. **VS Code** with the "Power BI Projects" extension (search `pbip`).
   You will edit TMDL in VS Code more than in Desktop.
6. **An AI coding assistant that speaks MCP** — Claude Code, Cursor, or
   Copilot in VS Code. Needed for Module 4.

Nice-to-have:

- **Tabular Editor 3** (paid) or **Tabular Editor 2** (free) for
  advanced TMDL and best-practice analyzer rules.
- **DAX Studio** for query plans and performance tuning.

## How to use this course

Each module is self-contained and follows the same shape:

1. **What it is** — one paragraph, no jargon.
2. **Why it matters now** — the problem it solves.
3. **The mental model** — the one picture or table that unlocks the topic.
4. **Hands-on walkthrough** — step-by-step, with commands and code.
5. **Exercises** — do these. Don't skip.
6. **Common traps** — mistakes I've seen cost people days.
7. **Further reading** — Microsoft Learn + community links.

Pace yourself: one module per weekend is reasonable. Rushing through TMDL
to get to the "fun" MCP module is the fastest way to deploy an agent that
quietly breaks your semantic model.

## The bigger picture

> Power BI + Fabric + Copilot + MCP + PBIP + TMDL + Git + AI Agents

is the stack. The semantic model is the bridge between enterprise data
and AI. If you own that bridge, you are valuable through 2027 and beyond.
If you only know the ribbon in Desktop, you are not.

Start with [Module 1: TMDL view](./01-tmdl-view.md).
