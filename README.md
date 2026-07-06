# REHS 2026: AI-Powered Support Chatbot for High-Performance Computing

---

## What you're going to build

A **Retrieval-Augmented Generation (RAG) chatbot** for the National Research Platform (NRP). When a researcher asks "How do I request a GPU pod?", your bot will:

1. **Embed** the question into a vector (numbers that capture meaning)
2. **Search** a vector database of NRP documentation for the most relevant chunks
3. **Send** the question + retrieved docs to a Large Language Model (LLM) hosted on NRP
4. **Return** an answer with citations back to the source docs

By week 8 the bot will run as a Kubernetes pod *on the same cluster it answers questions about*. The bot that helps you use NRP runs on NRP. That's the story you'll tell at your final presentation.

---

## How this is organized

```
rehs-curriculum/
├── README.md                          ← you are here (overview + how the program runs)
├── weeks/
│   ├── week-01-onboarding.md          Matrix, namespace, API token, first curl
│   ├── week-02-python-and-git.md      Python fundamentals + git basics
│   ├── week-03-kubernetes.md          Pods, deployments, kubectl (AI tools unlock!)
│   ├── week-04-hpc-and-llm-api.md     GPUs, OpenAI SDK, streaming, prompt design
│   ├── week-05-rag-mvp.md             Each pair builds its OWN full RAG bot
│   ├── week-06-integration-eval.md    Improve it. Eval. The bake-off.
│   ├── week-07-deploy.md              Merge the best bots. Deploy to NRP together.
│   └── week-08-polish-and-present.md  Polish the repo, go live, present, celebrate.
├── notebooks/
│   ├── week-01-first-api-calls.ipynb    interactive: hello_llm → a tool-calling weather bot
│   ├── week-02-python-and-git.ipynb     interactive: Python fundamentals + git, runnable cells
│   └── week-04-streamlit-and-tools.ipynb interactive: Streamlit UI + tool calling → a kubectl bot
├── starter-repo/                     the chatbot scaffold you clone in Week 1
└── resources/
    ├── primer-supercomputing-ai-nrp.md  the "why" behind the program (read for Week 1)
    ├── nrp-cheatsheet.md              NRP-specific quick reference
    ├── python-cheatsheet.md           Syntax you'll use most
    ├── kubectl-cheatsheet.md          K8s commands you'll use most
    └── troubleshooting.md             "It broke" → "here's how to debug"
```

Each week file contains:

- **Goal** — one sentence of what you'll know how to do by Friday
- **This week's milestone** — what must be done & demoed by week's end
- **Concepts** — the new ideas this week
- **Hands-on** — exercises with expected outcomes
- **Pair check-ins** — what to discuss with your pair partner
- **Stretch goals** — for pairs who finish early
- **Resources** — links, docs, videos

---

## Team structure (8 students → 4 pairs)

You work in **pair-programming pairs**. Two brains on every line of code. One drives (types), one navigates (reads + thinks). Switch every 30 min.

**Everyone builds the whole thing.** There are no "frontend people" or "deploy people" — you all came to build an AI chatbot, so you all build the AI core. The arc:

| Weeks | What each pair does |
|------|----------------------|
| 1–4  | Everyone learns the same material: Python, git, Kubernetes, the LLM API |
| 5–6  | **Each pair builds its own complete RAG bot** — scrape, embed, retrieve, prompt, UI. The whole pipeline. |
| 6    | **The bake-off** — all four bots are scored on a shared eval set |
| 7    | **Merge** the best pieces of all four into one team bot, then **everyone deploys** it to NRP |
| 8    | Polish the repo, keep it live on NRP, present — together |

Building four bots and merging the best beats building one: everyone learns *all* of RAG, and the final product is the best of four independent attempts. Competition first, collaboration second.

---

## How the program runs

- **8 students, ~20 hours/week, 8 weeks — fully remote.** All live contact is on Zoom; links are pinned in Matrix `#rehs-2026`.
- Your ~20 hours split into **~3 live hours** (calls + office hours) and **~17 hours** of pair work you schedule yourselves. The calls are the heartbeat; the real building happens between them.

### Weekly rhythm

**Week 1** — three 1-hour Zoom calls: **Kickoff**, **The Big Picture** (why this exists), and **Get Running on NRP** (live setup + first API call). See [Week 1](weeks/week-01-onboarding.md).

**Weeks 2–8** — one mandatory call + two drop-in office hours:

| Session | Required? | What happens |
|---|---|---|
| **Weekly call** (1 hr) | ✅ Yes | Demo last week (5 min/pair) → this week's goals → a short live-coding/concept session → unblock |
| **Office hours #1 — drop-in** (1 hr) | Optional, strongly encouraged | Bring a blocker or a screen to share |
| **Office hours #2 — co-working lab** (1 hr) | Optional, strongly encouraged | Build alongside everyone, mentor present |

Days/times are pinned in `#rehs-2026`. Broken demos are welcome — they teach the most.

### Working remotely

The biggest risk in a remote program is drifting — going quiet and falling behind alone. How we avoid it:

- **Pair for real:** use [VS Code Live Share](https://code.visualstudio.com/learn/collaboration/live-share) or screen-share on a call, with voice on. One drives, one navigates; switch every ~30 min. Pairing silently over chat doesn't work.
- **Give the 17 async hours a shape:** book 2–3 co-working blocks with your pair each week, and post a **3-line standup in `#rehs-2026` at least 3× a week** (did / doing / blocked). Silence is the one thing that worries us.
- **Falling behind? Post it.** The only wrong move is going quiet — say it in `#rehs-2026`, come to office hours, or message the mentor. A milestone you didn't finish but can explain honestly beats a silent week.

### The repos you'll use

Three repos, in order (you create the first; the mentor sets up the others):

1. **Your personal practice repo** (Weeks 1–4) — you create it in [Week 1](weeks/week-01-onboarding.md). Your sandbox: `about-me.md`, Python exercises, your first `chat.py`.
2. **Your pair repo** (Weeks 5–6) — your pair's own complete RAG bot, cloned from the starter scaffold. Your bake-off entry.
3. **The shared team repo** `rehs-nrp-chatbot` (Weeks 7–8) — the merged best-of-four bot you deploy and ship.

**Never push to `main` directly** — always branch → commit → push → Pull Request → review → merge.

### How you'll be assessed

It's a project, not a class — no exams. You're doing well when, each week, you (1) **ship** the milestone (or get close and can explain the gap) and (2) **can explain** what you built and why. Your weekly demo, your PRs, and your presence in `#rehs-2026` are the whole picture.

---

## The 8-week arc at a glance

```
                Python   Real Stuff Starts        Building            Shipping
              ┌────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐
   Week:        1    2     3    4              5    6              7    8

   Topic:    Setup  Py    K8s   HPC+API     Own-bot  Bake-off     Merge   Ship
                          ↑                                          ↑
                          AI tools unlocked                          Live URL
                          (Cursor/Claude Code)                       on NRP

   Deliv:    First  CLI   hello Streamlit  Your     4 bots,      Merged  PR + Demo
             curl   bot   pod   streaming  RAG bot  pick best    & live  to SDSC
```

---

## Working agreements (please read)

### Be kind to your pair

Pair-programming is hard. The navigator is **not** allowed to say "no, do it this way" without explaining *why*. The driver is **not** allowed to grab the keyboard from the navigator. If you're frustrated, take 5 minutes and walk around. If a pair isn't working, tell the mentor — we'll re-pair.

### Ship broken things

The weekly demo rewards **what you learned**, not what works. If your demo crashes live, you get bonus points for explaining what went wrong. We are not optimizing for perfect — we are optimizing for **shipping every week**.

### Read the docs

Every link in this curriculum is intentional. Open them. Skim them. The skill we're really teaching is *learning new technical things on your own* — the chatbot is just the excuse.

### Use AI tools (but only from Week 3)

Weeks 1–2 you write Python by hand. This is the only way to build muscle memory. Starting Week 3 you can use Cursor, Claude Code, GitHub Copilot, or ChatGPT to help write code. **But:** you must be able to explain *every line* of code in your PRs. If your pair partner asks "why does this work?" and you can't answer, the AI wrote it for you — not with you.

### Ask for help in public

When you get stuck, ask in the team Matrix channel before DMing the mentor. Half the time another pair has hit the same problem. Helping each other is part of how you learn.

---

## Prerequisites (what you need on Day 1)

- A laptop you can **install software on** (Mac, Linux, or Windows with WSL2 — admin rights; ~8GB RAM is comfortable)
- **Reliable internet** for a 1-hour Zoom call with screen sharing, plus a quiet-ish hour for the weekly call
- An email address (you'll use it for Matrix, GitHub, and NRP signup)
- Enthusiasm. Seriously, the rest we'll teach you.

> **Don't have the laptop or internet?** Tell the mentor in `#rehs-2026` **before Week 1**, privately if you prefer — it's solvable, but only if we know early.

You do **not** need:
- Prior Python experience (we'll teach it)
- Prior AI/ML knowledge (we'll teach it)
- Prior Kubernetes knowledge (we'll teach it)
- A GPU (NRP has thousands of them)

---

## How to use this curriculum

1. **Read the week file on Monday morning.** All of it. Yes, even the stretch goals.
2. **Plan your week with your pair partner.** The schedule inside each week is a *suggestion* — you and your pair decide when to do what, as long as you hit the weekly milestone.
3. **Check off the milestone items as you go.** Each week has a checklist.
4. **Friday morning: prepare your demo.** 5 minutes per pair, max.
5. **Friday afternoon: retro.** What worked, what didn't, what do you want different next week.

---

## What "done" looks like at the end of Week 8

- ✅ A chatbot deployed at a public URL on NRP
- ✅ A GitHub repo with a clean README, tests, and license
- ✅ A public, polished team repo (`rehs-nrp-chatbot`) — your open-source deliverable
- ✅ A Matrix announcement in `#general:matrix.nrp-nautilus.io` introducing your project to the NRP community
- ✅ A 30-minute presentation to SDSC staff with a live demo
- ✅ A 1-page written project report (motivation, design, results, future work)
- ✅ Eight teenagers who can confidently say: "I built and shipped a real AI system that real researchers use."

Let's go.

---

**Next:** [Week 1 — Onboarding & Your First API Call](weeks/week-01-onboarding.md)
