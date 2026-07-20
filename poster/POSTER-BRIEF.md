# The Poster — who owns what

**One poster. Seven owners. Your section is the code you built.**

We are building *one* chatbot and presenting *one* poster. You each own a real piece of the
system — and the part of the poster that explains that piece. You don't write about someone
else's work.

- **Template:** `REHS2026-poster-template.pptx` — 24 × 36 inches, portrait.
  **Do not change the size, move the boxes, or shrink the fonts.**
- **Format:** PowerPoint only. REHS returns posters made any other way, because text boxes
  shift when they print. Export a PDF at the end as well.
- **Layout:** full-width horizontal bands, matching the 2025 REHS poster. Explanatory text
  on the left of each band, figures on the right.
- **The 3-foot rule:** readable from 3 feet away. The template's sizes already pass. If your
  text doesn't fit, **cut words — never shrink type.**
- **Image credits:** credit anything that isn't yours, right next to the figure.

---

## The seven jobs

| Owner | Poster section | Code you own | Your figures |
|---|---|---|---|
| **S1** | Building the Knowledge Base *(shared)* | `scripts/ingest.py` | 1, 2, 4 |
| **S2** | Building the Knowledge Base *(shared)* | `src/embed/search.py` | 3 |
| **S3** | Answering Questions with RAG *(shared)* | `answer_question()` | 5, 6 |
| **S4** | Answering Questions with RAG *(shared)* | `app.py` | 7 |
| **S5** | Deploying on the NRP | `deploy/k8s/*` | 8, 9, 10 |
| **S6** | Evaluation: Does It Work? | `scripts/eval.py` | 11, 12 |
| **S7** | Title, Introduction, Abstract, Conclusions | `README.md` + **the poster file** | — |

Write names into the template's OWNER lines on Monday's call.

**S7 is not the easy job.** You own the framing of the whole poster, you're the only person
who edits the master `.pptx`, and you write the abstract *last* — after S6 has the number.

---

## What each section needs

Each band gets **90–130 words total**, plus its figures. That's genuinely all that fits.

### Building the Knowledge Base — S1 & S2
Where the chatbot's knowledge comes from, and how it finds the right piece.

- **S1:** how many doc pages we collected and cleaned; what chunking is and why ~500 tokens
  rather than whole pages.
- **S2:** what an embedding is, in two sentences a stranger understands; why similar meaning
  lands nearby; how `search()` returns the closest five.
- **Figures:** 1 ingest pipeline diagram · 2 an example chunk · 3 a real query and what it
  retrieved · 4 a table of pages in / chunks out / embedding model.

### Answering Questions with RAG — S3 & S4
The heart of the poster.

- **S3:** the prompt (retrieved docs + question → grounded answer); why we tell the model to
  admit when the docs don't cover something; how citations get attached.
- **S4:** the interface — streaming answers, chat history, the sources expander; one design
  decision you made and why.
- **Figures:** 5 the RAG loop diagram · 6 **the same question with and without retrieval** ·
  7 the hero screenshot.

> **Figure 6 is the most persuasive image on the poster.** It's the entire argument for the
> project in one picture. Pick a question where the difference is obvious.

> **Figure 7 is the most-looked-at image.** Crop it tight, pick a good question, make sure
> the citations are visible.

### Deploying on the NRP — S5
- The request path in plain words: browser → Ingress → Service → Pod → NRP LLM → back.
- Why the vector database lives on a PVC and survives a pod restart.
- Why the token is a Secret and never baked into the image.
- **Figures:** 8 the architecture diagram (**draw it with PowerPoint shapes — not a
  screenshot of ASCII art**) · 9 `kubectl get pods` showing `Running` · 10 QR code + live URL.

### Evaluation: Does It Work? — S6
- 20 real NRP questions, graded by hand, answered twice: with retrieval and without.
- **The headline number of the whole poster is the gap between those two scores.**
- Every miss classified as a retrieval miss or a model miss.
- Honest limitations: 20 questions is a small set and we wrote it ourselves.
- **Figures:** 11 the accuracy bar chart · 12 the failure breakdown. Both come straight out
  of the Wednesday notebook.

### Title, Introduction, Abstract, Conclusions — S7
- **Header:** everyone's name with matching superscripts, school affiliations, logos.
- **Introduction** (~110 words): what NRP is, who uses it, why searching docs is slow, why
  you can't just ask ChatGPT. End on the gap this project fills.
- **Abstract** (~110 words, five sentences, **written last**): problem → what we built → how
  it works → the result *with a number* → what it means.
- **Conclusions & Future Work:** 3 bullets each.
- **Assemble the file.** Paste everyone's text, place their images, keep every font size as
  the template set it, and read the whole thing twice for typos.

---

## Deadlines

| When | What |
|---|---|
| **Mon Jul 20, on the call** | Owners assigned |
| **Wed Jul 22, 9pm** | Your text + figures → sent to S7 |
| **Thu Jul 23, noon** | S7 has a complete draft in the shared folder |
| **Thu Jul 23, evening** | Mentor reviews and approves |
| **Fri Jul 24** | S7 exports the PDF and submits. **Hard REHS deadline.** |

After Friday the poster is frozen and goes to print — SDSC prints it, you don't. **Nothing
can change after submission**, so read it twice before it goes.

**Showcase: Friday July 31, 3:00 PM.** We rehearse Thursday July 30.

---

## Common ways posters go wrong

- **Too many words.** The most common failure by far. Nobody at a poster session reads
  paragraphs. Cut until it hurts, then cut again.
- **Screenshots with tiny text.** If you can't read your terminal comfortably on your own
  laptop, it will be illegible printed. **Increase your font size, then re-take the shot.**
- **No numbers.** "It works well" means nothing. "17/20 with retrieval vs. 6/20 without" is
  a result.
- **Blurry images.** Never screenshot a screenshot. Never scale an image up.
- **Only showing what worked.** Where it fails is genuinely interesting, and visiting
  scientists respect it. Put the failures in — that's what Figure 12 is for.
