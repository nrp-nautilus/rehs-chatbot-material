# Week 6 — Make It Good & The Bake-Off

> **Goal:** By Friday, every pair's bot is scored on a **shared cohort eval set**, and the cohort has decided — with evidence — which pieces of which bots get merged into the single team product next week.

**The vibe:** *the optimization arc, then the showdown.* First half of the week: stop adding features and start making your bot *good* — same code, better numbers, by outsmarting yourself. Second half: **the bake-off.** All four bots line up against the same held-out questions, scores go on the board, and the cohort decides — objectively, by the numbers — whose ingest, whose retrieval, whose prompt, and whose UI go into the team bot we ship. This is the most fun week. It's also where you learn the most painful truth in ML: *the model gets the credit when it's right, and you get the blame when it's wrong.* Welcome to the job.

The big lesson: **"the LLM" is not your only knob.** Quality comes from chunk size, retrieval `k`, prompt design, and — above all — the eval loop that tells you whether a change helped or hurt.

---

## 📅 Live sessions this week (remote)

~3 sync hours; the other ~17 are pair work with your partner. Times are pinned in `#rehs-2026`.

| Session | Required? | What happens |
|---|---|---|
| **Weekly call** (1 hr) | ✅ Yes | Demos of last week's bots (5 min/pair) → build the shared eval set together → **read real eval failures + live prompt-tuning** → unblock |
| **Office hours #1 — drop-in** (1 hr) | Optional, strongly encouraged | Bring a blocker or a screen to share |
| **Office hours #2 — 🔥 THE BAKE-OFF** (1 hr) | ✅ Come if you can | All four bots scored live on the held-out test set; cohort picks the merge plan |

**Before the call:** make sure your bot answers end-to-end. **After the bake-off:** the cohort writes the Week 7 merge plan.

> The bake-off is the demo this week. New to the remote rhythm? See [the README](../README.md#how-the-program-runs).

---

## This week's milestone

The **bake-off**, where each pair shows:

1. Your bot runs `python scripts/eval.py` live and reports a score on the **shared** eval set
2. You walk through **one** retrieval failure and explain *why* it failed (bad chunk? bad query? missing doc?)
3. You walk through **one** improvement you made and show before/after numbers
4. The cohort agrees a written **merge plan**: which component (ingest / retrieval / prompt / UI) comes from which pair, based on the scores

Target to be competitive: **≥15/20** on the shared train set. But the real prize is being the bot whose piece gets picked for the merge.

---

## The shared eval set (built together, used by everyone)

For the bake-off to be fair, **every bot is judged on the exact same questions.** So the cohort builds one shared eval set.

- **Monday, in the call (90 min, whole cohort):** brainstorm 30 real NRP questions. Examples:
  - "How do I request a GPU pod?" · "What's the difference between qwen3 and gpt-oss?"
  - "How do I mount a PVC?" · "Why is my pod in CrashLoopBackOff?" · "How do I get an LLM token?"
- For each: the question, the expected source doc(s), a 1-sentence ideal answer, and a category.
- Save as `eval/questions.jsonl` (one JSON object per line):
  ```json
  {"q": "How do I request a GPU pod?", "expected_source": "running/gpu-pods/", "ideal": "Add nvidia.com/gpu: 1 to the pod's resources", "category": "gpu"}
  ```
- **20 train + 10 held-out test.** Nobody tunes against the test set. (Real ML discipline — the bake-off scores on test.)
- This shared file is the one thing every pair pulls into their own repo.

---

## Build the eval script (each pair, in your own bot)

```python
import json
from src.embed.search import search
from src.ui.chat import answer_question   # returns {"answer", "chunks"}

questions = [json.loads(l) for l in open("eval/questions.jsonl")]
train, test = questions[:20], questions[20:]

scores = {"retrieval_hit": 0, "answer_ok": 0}
for item in train:                       # swap to `test` only at the bake-off
    chunks = search(item["q"], k=5)
    if any(item["expected_source"] in c["source_url"] for c in chunks):
        scores["retrieval_hit"] += 1

    result = answer_question(item["q"])   # -> {"answer": str, "chunks": [...]}
    print(f"\nQ: {item['q']}\nA: {result['answer'][:200]}...\nIdeal: {item['ideal']}")
    if input("OK? [y/N]: ").lower() == "y":
        scores["answer_ok"] += 1

print(f"\nRetrieval: {scores['retrieval_hit']}/20   Answers: {scores['answer_ok']}/20")
```
- Run it, write down your **baseline** before changing anything.
- Pin `temperature=0.0` for eval runs so scores are stable.

---

## Suggested daily flow

### Monday — build the shared eval set (cohort) + baseline (pair)
- [ ] In the call, build `eval/questions.jsonl` together. Split 20 train / 10 test.
- [ ] Each pair wires `scripts/eval.py` and records a baseline score.

### Tuesday — tune retrieval
- [ ] Look at every retrieval miss. Try chunk sizes (300/500/800), overlap (0/100/200), `k` (5 vs 10), and putting the page title in the chunk text.
- [ ] Re-ingest, re-embed, re-run eval. Keep the winning config. Log experiments in `eval/EXPERIMENTS.md` — even failures.

### Wednesday — tune prompts
- [ ] Iterate the RAG template: an explicit "if the docs don't say, reply 'I don't know'"; numbered sources `[1][2][3]` with inline citations; "expert NRP support engineer" vs "friendly tutor"; try `qwen3` vs `gpt-oss`.
- [ ] **Hallucination check:** ask 5 questions the docs *don't* cover. Does your bot say "I don't know" or make things up?

### Thursday — freeze + dry-run the bake-off
- [ ] Lock your best config. Do a practice run on the train set. Get your one-failure and one-improvement stories ready.

### Friday — 🔥 THE BAKE-OFF
- [ ] **Every bot runs on the held-out test set, live.** Scores on the board. No more tuning.
- [ ] Walk your failure + improvement.
- [ ] **Cohort decides the merge plan:** best ingest, best retrieval, best prompt, best UI — by the numbers, not by ego. Write it in `MERGE-PLAN.md`. This is Week 7's marching orders.

---

## How the merge decision works (so it's fair, not a popularity contest)

Pick components on **evidence**, not vibes:

- **Best retrieval** → highest retrieval-hit rate on the test set.
- **Best ingest** → cleanest chunks + best coverage (did its chunks contain the answers?).
- **Best prompt/answer** → highest answer-OK / LLM-judge score, and best "I don't know" behavior.
- **Best UI** → cohort vote, but it must honor the interfaces so it drops in cleanly.

A pair can win more than one category — or none, and still have built the bot that taught everyone the most. The point of building four was to *have* four good options to choose from.

---

## Stretch goals

- 🤖 **LLM-as-judge:** replace human eyeballing with an LLM grader (rate correctness + groundedness 1–5). Compare to your human grades on 10 questions.
- 🔍 **Per-category scores:** maybe you're great at GPU questions and terrible at storage. Find the weak spot.
- 🔁 **Query rewriting:** ask the LLM to rewrite the user's question into a better search query before retrieval. Often a big win.
- 🧪 **CI:** GitHub Action that runs `scripts/eval.py` on every PR and fails if the score drops.

---

## Resources

- [How to evaluate RAG systems (Pinecone)](https://www.pinecone.io/learn/series/rag/)
- [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents) — the prompt patterns section is gold
- [Promptfoo](https://www.promptfoo.dev/docs/intro/) — a mature prompt-eval tool (optional)
- [LLM-as-judge paper (Zheng et al., MT-Bench)](https://arxiv.org/abs/2306.05685)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Eval scores differ on re-runs | Temperature too high | `temperature=0.0` for eval; keep it higher for the live UI |
| Bot hallucinates fake URLs | Weak grounding | System prompt: "Only cite source_urls that appear in the DOCS section" |
| Great retrieval, bad answers | LLM ignoring context | Make context prominent; try a more capable model |
| Says "I don't know" to easy questions | Over-aggressive instruction | Soften the prompt; show more sources |
| Eval takes 30 min | Re-embedding every run | Cache embeddings on disk; only re-embed when chunks change |

---

**Next:** [Week 7 — Merge & Deploy to NRP](week-07-deploy.md)
