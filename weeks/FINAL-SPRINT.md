# REHS 2026 — Final 3-Session Sprint

**Dates & times**

| Session | Date | Focus |
|---|---|---|
| **1** | Mon Jul 20 | RAG end-to-end + poster kickoff |
| **2** | Wed Jul 22 | Deploy (no images) + eval for the poster number |
| **3** | Thu Jul 30 | Tool calling + polish for the live demo |

**Poster deadline:** Fri Jul 24 (submit to Ange). Everything for the poster must be done by end of Session 2.

---

## Session 1 (Mon Jul 20) — RAG, end to end

**Goal:** Every student can narrate and run the full RAG pipeline:
`question → embed → search → grounded prompt → answer + citations`

**Notebook:** `notebooks/session-01-rag-end-to-end.ipynb`

### Run of show (60 min)

| Time | What |
|---|---|
| 0:00–0:08 | intros: where everyone is, 40s each |
| 0:08–0:35 | **RAG live:** model hallucinates → paste real doc → embeddings + cosine → chunk → index → `search()` → `answer_question()` with citations. Same question, before/after. |
| 0:35–0:52 | **Poster kickoff:** open the template, walk the 7 bands, assign owners live. 90–130 words per band. Flag Figure 6 (with/without retrieval) as the money shot. |
| 0:52–1:00 | Homework read-back |

### Homework (due before Session 2)

Everyone:
- Turn the notebook pipeline into `ingest.py` (builds index once, skips if already built) and `app.py` (queries only).
- Run both locally: `python ingest.py` then `streamlit run app.py`.
- Start your poster panel text (90–130 words).

| You | Own | Poster figure(s) |
|---|---|---|
| **S1** Ingest | `ingest.py` — pages in, chunks out | Fig 1, 2, 4 |
| **S2** Retrieval | `search()` — compare k=3 vs k=10 | Fig 3 |
| **S3** RAG core | `build_prompt()` — honesty exit | Fig 5, 6 |
| **S4** Interface | `app.py` — sources expander | Fig 7 |
| **S5** Deploy | Read Session 2 manifests; start arch diagram | Fig 8, 9, 10 |
| **S6** Eval | **Write 20 NRP questions + expected answers** | Fig 11, 12 |
| **S7** Frame | Draft INTRODUCTION; assemble PPTX | header, intro |

---

## Session 2 (Wed Jul 22) — Deploy it for real, then measure it

**Goal:** Bot is live at a public URL; eval produces the poster's headline number.

**Notebook:** `notebooks/session-02-deploy-and-evaluate.ipynb`

**Architecture:** No Docker images. Code + docs live in ConfigMaps; PVC holds the index; pod installs deps at startup, builds index once, then serves.

### Run of show (60 min)

| Time | What |
|---|---|
| 0:00–0:08 | Merge PRs; `main` is the bot |
| 0:08–0:35 | **Deploy live:** Secret + ConfigMaps + PVC + Deployment (`replicas: 1`) + Service + Ingress. URL on everyone's phone. |
| 0:35–0:52 | **Eval:** run 20 questions with & without retrieval; hand-grade; produce Figures 11 & 12. |
| 0:52–1:00 | Poster handoff checklist (text + figures due 9pm) |

### Homework (due 9pm)

Panel owners send 90–130 words + figures to S7. S7 assembles draft; mentor approves Thu eve; submit Fri.

---

## Session 3 (Thu Jul 30) — Tool calling + a well-composed chatbot

**Goal:** Live demo polish. Poster is frozen; this session is for the showcase.

**Notebook:** `notebooks/session-03-tools-and-polish.ipynb`

### Run of show (120 min)

| Time | What |
|---|---|
| 0:00–0:15 | System walkthrough: each owner narrates their piece |
| 0:15–0:55 | **Rehearsal:** 90s pitch each, two pieces of feedback, re-run shaky ones |
| 0:55–1:05 | Break |
| 1:05–1:45 | **Tools + polish:** give the bot `run_kubectl` + `search_nrp_docs` tools; enforce "call once, then answer"; add sources expander and honesty exit |
| 1:45–2:00 | Retro + what's next (fine-tuning, agents, keeping NRP access) |

### Demo scenarios to practice

- "What pods are running in my namespace?" → calls `run_kubectl` live
- "How do I request a GPU?" → searches docs, cites sources
- "What is the airspeed velocity of an unladen swallow?" → honest "I don't know"

---

## Non-negotiables

- **No images.** Everything runs from ConfigMaps + PVC.
- **`replicas: 1`** for Streamlit (websockets break with >1).
- **Never commit secrets.** Token in a Secret, not in code or ConfigMap.
- **No push to `main`.** Branch + PR only.
- **Poster frozen Jul 24.** Session 3 improvements are for the live demo only.
