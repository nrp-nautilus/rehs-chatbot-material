# Week 5 — Build Your Own RAG Bot

> **Goal:** By the end of the week, **each pair has its own complete, working RAG chatbot** — it scrapes NRP docs, embeds them, retrieves the relevant ones, prompts the LLM, and answers with citations. Ugly is fine. End-to-end is the bar.

**The vibe:** *this is the hackathon.* Four pairs, four chatbots, one weekend-energy sprint. Until now everyone learned the same lesson; this week you and your partner build **the whole thing** — the scraping, the embeddings, the retrieval, the prompt engineering, the UI, all of it. Nobody is "the frontend person" and nobody is stuck on plumbing. Every pair touches the actual AI core, because that's what you came here for. Next week the bots go head-to-head and we cherry-pick the best pieces of all four into one team bot — so build something you'd be proud to put in the ring.

**Why build four bots instead of one?** Two reasons. First, you only really learn RAG by building *all* of it yourself, not one slice. Second, four independent attempts beat one — different pairs will crack different parts, and in Week 7 we merge the best ingest + best retrieval + best prompt + best UI into a single product. Competition now, collaboration later.

---

## 📅 Live sessions this week (remote)

~3 sync hours; the other ~17 are pair work with your partner. Times are pinned in `#rehs-2026`.

| Session | Required? | What happens |
|---|---|---|
| **Weekly call** (1 hr) | ✅ Yes | Demo last week (5 min/pair) → this week's goals → **agree the cohort-wide interfaces so every bot is mergeable in Week 7** → unblock |
| **Office hours #1 — drop-in** (1 hr) | Optional, strongly encouraged | Bring a blocker or a screen to share |
| **Office hours #2 — co-working lab** (1 hr) | Optional, strongly encouraged | Build alongside everyone; mentor present |

**Before the call:** read this whole file with your pair. **After the call:** post your pair's build plan in `#rehs-2026`.

> Your **weekly milestone** is the deadline; you'll **demo it in next week's call** — which is also the bake-off. New to the remote rhythm? See [the README](../README.md#how-the-program-runs).

---

## This week's milestone

**Your pair's own RAG bot, working end to end on your laptop.** At the bake-off next week you'll show:

1. Your bot ingested real NRP docs (≥100 chunks)
2. A user asks a question → your bot retrieves relevant chunks → prompts the LLM → answers
3. The answer shows **citations** back to the source NRP pages
4. It runs from a clean clone (`streamlit run app.py`) on a teammate's machine

Polish is *not* the bar this week. **End-to-end is the bar.** A bot that answers one question with one citation beats a beautiful UI that retrieves nothing.

---

## The one thing the whole cohort does together: agree the interfaces

Even though each pair builds independently, **on Monday the whole cohort agrees on three shared interfaces.** This is the single most important coordination of the summer, because it's what makes the Week 7 merge possible — if every bot uses the same chunk format and the same `search()` signature, we can drop *your* retrieval into *their* bot without rewriting anything.

The three contracts (full detail in your starter repo's [`docs/INTERFACES.md`](../starter-repo/docs/INTERFACES.md)):

1. **The chunk JSON schema** — what one chunk of doc looks like on disk:
   ```json
   {
     "id": "running_gpu-pods__003",
     "source_url": "https://nrp.ai/documentation/userdocs/running/gpu-pods/",
     "title": "Running GPU pods",
     "text": "To request a GPU, add nvidia.com/gpu: 1 to the resources section..."
   }
   ```
2. **The `search()` signature** — how retrieval is called:
   ```python
   def search(query: str, k: int = 5) -> list[dict]:
       # returns up to k dicts, each: {text, source_url, title, score}
   ```
3. **The `answer_question()` shape** — the RAG core the UI and eval both call:
   ```python
   def answer_question(query: str) -> dict:
       # returns {"answer": str, "chunks": list[dict]}
   ```

Agree these as a cohort, write them down, and **don't deviate** — a bot that breaks the contract can't compete in the bake-off merge.

---

## What each pair builds (the whole pipeline)

```
   ┌──────────────────────────────────────────────────────────────┐
   │  YOUR PAIR builds ALL of this — the whole vertical            │
   │                                                              │
   │  nrp.ai docs ─► scrape+clean+chunk ─► data/chunks/*.json     │
   │                                            │                 │
   │                                  embed + index (Chroma)      │
   │                                            │                 │
   │                                   search(query) ─► chunks    │
   │                                            │                 │
   │  user ─► Streamlit UI ─► build prompt ─► NRP LLM ─► answer   │
   │                                       + citations            │
   └──────────────────────────────────────────────────────────────┘
```

### Part 1 — Ingest (scrape + chunk)
**Produce ≥100 clean chunks in `data/chunks/` matching the agreed schema.**
- Easiest path: use the bundled corpus in `notebooks/nrp-docs/` — 85 real NRP pages, already markdown, each with its `Source:` URL.
- Or scrape `nrp.ai/documentation/` with `requests` + `beautifulsoup4`.
- **Clean** the text (strip nav/menus), keep each page's `source_url` for citations.
- **Chunk** to ~500 tokens (~2000 chars) with ~100-token overlap. Use LangChain's `RecursiveCharacterTextSplitter` (one line) or write your own.
- Wrap it as `scripts/ingest.py` → runs the whole thing with `python scripts/ingest.py`.

### Part 2 — Embed + retrieve
**Index your chunks in Chroma and implement `search()`.**
```python
pip install chromadb

from openai import OpenAI
client = OpenAI(api_key=TOKEN, base_url=BASE_URL)

def embed(text: str) -> list[float]:
    return client.embeddings.create(model="qwen3-embedding", input=[text]).data[0].embedding

import chromadb
coll = chromadb.PersistentClient(path="./chroma_db").get_or_create_collection("nrp_docs")
coll.add(
    ids=[c["id"] for c in chunks],
    documents=[c["text"] for c in chunks],
    embeddings=[embed(c["text"]) for c in chunks],
    metadatas=[{"source_url": c["source_url"], "title": c["title"]} for c in chunks],
)

def search(query: str, k: int = 5) -> list[dict]:
    res = coll.query(query_embeddings=[embed(query)], n_results=k)
    return [
        {"text": d, "source_url": m["source_url"], "title": m["title"], "score": s}
        for d, m, s in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])
    ]
```
- **Use the same model to index and to query** (bake it into one `embed()` function).
- Write 10 test queries and eyeball the results — is the right doc coming back?

### Part 3 — The RAG core + UI
**Wire retrieval into a Streamlit chat that answers with citations.** Start from your Week 4 `app.py`.
```python
from src.embed.search import search

if prompt := st.chat_input("Ask about NRP..."):
    with st.spinner("Searching NRP docs..."):
        chunks = search(prompt, k=5)

    context = "\n\n---\n\n".join(f"[Source: {c['title']}]\n{c['text']}" for c in chunks)
    grounded = f"""Use the NRP documentation below to answer. If the docs don't contain the
answer, say so honestly.

DOCS:
{context}

QUESTION: {prompt}"""

    # stream the answer (same as Week 4) ...

    with st.expander("📚 Sources"):
        for c in chunks:
            st.markdown(f"- [{c['title']}]({c['source_url']})  *(score: {c['score']:.3f})*")
```
- Put the RAG logic behind `answer_question(query) -> {"answer", "chunks"}` (the agreed contract) so next week's eval can call it.
- Test with 5 real NRP questions. When it's wrong, can you tell *why* — bad retrieval or bad prompt?

### Part 4 — Run it clean
- A `requirements.txt` and a `Dockerfile` so it runs from a fresh clone. (Deploying to the cluster is Week 7 — this week, local is fine.)

---

## Suggested daily flow (each pair)

### Monday — interfaces + plan
- [ ] **Weekly call:** the cohort agrees the three interfaces above. Write them into your `docs/INTERFACES.md`.
- [ ] With your pair, plan the week: who drives which part first, and your co-working blocks (see [the README](../README.md#how-the-program-runs) on remote pairing).

### Tuesday — ingest + embed
- [ ] Get ≥100 chunks on disk in the agreed schema.
- [ ] Index them in Chroma; get `search()` returning sane results for 10 test queries.

### Wednesday — the RAG core
- [ ] Wire `search()` → prompt → LLM → answer. Get *one* question answered with a citation. That's the magic moment; celebrate it.

### Thursday — make it answer well
- [ ] Try 10 real NRP questions. Improve chunking/retrieval/prompt where it's weak.
- [ ] Add the citations expander and a friendly empty-state.

### Friday — clean + freeze for the bake-off
- [ ] Make it run from a clean clone. Write a 3-line README. Commit. You're entering this in the ring next week.

---

## Pair check-ins

- Can your bot answer a question your bot has *never seen* using only the docs?
- When it's wrong, do you know whether it's retrieval or the prompt? (They need different fixes.)
- Does your code honor the three shared interfaces *exactly*? (If not, you can't compete in the merge.)
- Are you actually pair-programming (one screen, switching), or silently splitting? Fix it if it's the latter.

---

## Stretch goals

- 🧪 **Hybrid retrieval:** combine BM25 (keyword) + embeddings (semantic). Often beats either alone.
- 📝 **Markdown answers:** make sure code blocks, lists, and links render in Streamlit.
- 🐳 **Slim Docker image:** multi-stage build, ruthless `.dockerignore`.
- 🕷️ **Better scraper:** preserve code blocks and tables from the docs.
- 📊 **Telemetry:** log every query + retrieved chunks + answer to a JSONL file — you'll use it next week for eval.

---

## Resources

- [Chroma docs](https://docs.trychroma.com/)
- [LangChain text splitters](https://docs.langchain.com/oss/python/integrations/splitters)
- [What is RAG? (Pinecone explainer)](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- Bundled corpus: `notebooks/nrp-docs/` — already scraped and cleaned for you
- [Docker get started](https://docs.docker.com/get-started/)
- Your starter repo's [`docs/INTERFACES.md`](../starter-repo/docs/INTERFACES.md) — the contracts, in full

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Scraped text has `\n\n\n` everywhere | HTML stripping artifacts | `BeautifulSoup(html, 'html.parser').get_text(separator='\n')` + normalize whitespace |
| Chroma "ID already exists" | Re-running indexer without delete | `get_or_create_collection` + idempotent ids, or `coll.delete()` first |
| Search returns garbage | Different model used to index vs. query | Use the **same** model for both — one `embed()` function |
| Citations show but URLs are empty | Chunk metadata missing `source_url` | Check your `data/chunks/*.json` actually has it |
| Bot ignores the docs | Context not prominent in the prompt | Make the DOCS block clear; try a more capable model |
| `python scripts/eval.py` can't import `src` | Running without repo root on path | The starter scripts add it automatically; run from the repo root |

---

**Next:** [Week 6 — Make It Good & The Bake-Off](week-06-integration-eval.md)
