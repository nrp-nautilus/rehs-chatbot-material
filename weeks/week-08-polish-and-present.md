# Week 8 — Polish, Ship & Present

> **Goal:** By Friday: your **one team repo** is polished and public, the **chatbot is running live on NRP**, you've announced it to the NRP community, and you've delivered a 30-min presentation to SDSC staff with a 1-page report — and 8 students who can put this on their college apps.

**The vibe:** **DEMO WEEK + VICTORY LAP.** You shipped last week. This week is about making it *legible to the world*. Great README. Sharp slides. Honest demo. A public repo with your eight names on it and a live URL anyone can hit. Future-you applying to college will reference this week. Future-you on a job application will reference this week. Make it shine, then show it off, then celebrate. *You earned this.* 🚀

You've shipped a working chatbot. This week we **make it shareable**: a great README on the team repo, the bot running live on NRP, an announcement to the community, and a public demo. This is the week your work goes from "we built it" to "the world can see it."

---

## 📅 Live sessions this week (remote)

Demo week has a different shape — more live time, because we're presenting. Times pinned in `#rehs-2026`.

| Session | Required? | What happens |
|---|---|---|
| **Weekly call** (1 hr) | ✅ Yes | Final-week plan → **repo polish + community announcement walkthrough** → assign presentation roles |
| **Rehearsal #1** (1 hr) | Encouraged | Polish + a full run-through of your demo |
| **Rehearsal #2** (1 hr) | Encouraged | Dress rehearsal — timing, slides, handoffs |
| **🎤 Final presentation** (30 min) | ✅ Yes | Live demo + talk to SDSC staff and a guest researcher |

**Before the call:** make sure your bot is live and your README is presentable. **After the presentation:** post the announcement and pin the repo. New to the remote rhythm? See [the README](../README.md#how-the-program-runs).

---

## This week's milestone

- ✅ Your **one team repo** is public and polished: README with screenshots, MIT license, contributing guide
- ✅ The **chatbot is running live on NRP** at its public URL (from Week 7) — and stays up
- ✅ A Matrix announcement in `#general:matrix.nrp-nautilus.io` with the URL + a clear ask for feedback
- ✅ A 30-min presentation delivered to SDSC staff with live demo
- ✅ A 1-page written project report submitted to the mentor
- ✅ All pairs have written a "what I learned this summer" paragraph

---

## The week's arc

```
   Mon          Tue           Wed          Thu          Fri
   ──────────   ──────────    ──────────   ──────────   ──────────
   Polish      README +       Publish +    Practice     Present
   the         license +      announce     the          + report
   product     screenshots    to community demo         + retro
```

---

## Suggested daily flow

### Monday — Polish the product

Today: make the deployed chatbot look like something a stranger would actually use.

- [ ] **All pairs review the live URL together (1 hour).** Make a list of every UX paper cut. Common ones:
  - First-load UX (does it tell you what it is?)
  - Empty state ("no chat yet")
  - Error states (what if NRP LLM is down?)
  - Mobile rendering
  - Footer attribution
  - Favicon
  - Page title
  - Loading spinners
- [ ] Each pair picks 3 fixes from the list. Implement, PR, merge, redeploy.
- [ ] **Add a `/about` section in the sidebar:**
  - What this bot does
  - Who built it (link to each student's GitHub)
  - Link to repo
  - "How does it work?" — 2-sentence RAG explanation
  - "Found a problem?" → link to GitHub issues
- [ ] **Add an `examples` section:** 3-5 starter questions a new user can click to try. (Streamlit makes this easy with `st.button`.)

### Tuesday — README + license + repo polish

Your README is your storefront. Make it good.

- [ ] **Write the README** (`README.md`) with these sections:
  1. **One-line tagline** at the top
  2. **Hero screenshot or GIF** (use [LICEcap](https://www.cockos.com/licecap/) for the GIF)
  3. **What is this?** — 2 paragraphs
  4. **Live demo link**
  5. **How it works** — paste the architecture diagram from Week 7
  6. **Tech stack** — Streamlit, Chroma, NRP LLM, Kubernetes
  7. **Local setup** — exact `git clone` → `pip install` → `streamlit run` instructions
  8. **Repo layout** — 5-line tree
  9. **Built by** — eight names, each linked to their GitHub
  10. **License** — MIT
  11. **Acknowledgments** — REHS program, SDSC, mentor, NRP team
- [ ] Add a `LICENSE` file (MIT is fine; ask mentor if SDSC has a different default).
- [ ] Add `.github/CONTRIBUTING.md` with how someone else could submit a PR.
- [ ] Add a `CITATION.cff` so people can cite your work academically. ([How](https://citation-file-format.github.io/))
- [ ] Add GitHub repo metadata: description, website, topics (`rag`, `llm`, `kubernetes`, `nrp`, `chatbot`).
- [ ] Pin the repo on each of your personal GitHub profiles. (This is your portfolio piece — show it off!)

### Wednesday — Publish the repo + announce to the community

Your **public repo + the live bot** are the deliverable. Today you make them findable and tell the world.

- [ ] **Make the team repo public and polished** (`github.com/<<GH_ORG>>/rehs-nrp-chatbot`): great README (from Tuesday), MIT license, `CONTRIBUTING.md`, repo description + topics (`rag`, `llm`, `kubernetes`, `nrp`, `chatbot`).
- [ ] **Confirm the bot is live and stable** at its public URL — hit it from a phone, off the network.
- [ ] **Each student pins the repo** on their GitHub profile. This is your portfolio piece.
- [ ] **Matrix announcement** in `#general:matrix.nrp-nautilus.io`:
  ```
  Hi NRP community! 👋

  We're eight high schoolers in the SDSC REHS summer program, and over the
  past 8 weeks we built an AI chatbot to help researchers use NRP. It runs
  *on* the Nautilus cluster and uses NRP's hosted LLMs.

  Try it here: https://<<INGRESS_HOST>>
  Source code: https://github.com/<<GH_ORG>>/rehs-nrp-chatbot

  We'd love your feedback — especially: what kinds of questions does it get
  wrong? Reply here or open an issue on the repo.

  Thank you to <mentor> and the NRP team for hosting our project! 🙏
  ```
- [ ] **Email your families** so they can try it. Bragging rights matter.

### Thursday — Presentation prep

Final demo day is Friday. Prep today.

- [ ] **Slide deck (12 slides max):**
  1. Title — Chatbot name, REHS 2026, your eight names
  2. The problem — "Researchers spend X hours hunting through docs..."
  3. The solution — "A chatbot that grounds its answers in real NRP docs"
  4. Live demo *placeholder* (no slide content — you'll demo here)
  5. Architecture diagram
  6. What is RAG? (2-sentence explanation + picture)
  7. The team & how we worked (pairs, the bake-off, the merge)
  8. Eval results (real numbers)
  9. What surprised us
  10. What we'd do with more time
  11. Acknowledgments
  12. Q&A / try it yourself QR code + URL
- [ ] **Each pair presents part of the story** for 2 minutes — your bake-off bot and what of yours made it into the merged product. 4 pairs × 2 min = 8 min, plus intro/demo/Q&A = 30 min.
- [ ] **Run-through (full dress rehearsal).** Time it. Fix what's clunky.
- [ ] **Backup plans:** what if Wi-Fi dies? what if the bot is rate-limited mid-demo? what if the URL is broken? Have screenshots and a recorded video as backup.
- [ ] **Practice the hard questions.** Mentor asks: "What's the accuracy?" / "What if a user pastes their password?" / "How much does it cost to run?" / "Why didn't you fine-tune a model?"

### Friday — Present + report + retro + celebrate

- [ ] **Morning:** final repo polish, last commits, freeze main branch.
- [ ] **Presentation (30 min)** to SDSC staff + invited researchers. Each pair owns their slide. Mentor moderates Q&A.
- [ ] **Live demo** mid-presentation. Pre-load 2 backup questions in case nothing comes from the audience.
- [ ] **1-page written report.** Sections:
  - Project name & team
  - Problem statement (3 sentences)
  - Approach (3 sentences) — "We built a RAG chatbot that..."
  - Results (3 sentences) — "On a 20-question eval, we scored... Deployed at..."
  - What we learned (1 paragraph)
  - Future work (3 bullets)
- [ ] **"What I learned this summer" paragraph** — each student writes their own. These become the testimonial section for next year's REHS recruitment. Keep them honest.
- [ ] **Retro (1 hour, last thing):**
  - Best part of the summer?
  - Hardest part?
  - What would you tell next year's REHS students?
- [ ] **Celebrate.** You shipped a real AI system. Take the win.

---

## Optional but recommended after Week 8

You're not required to do these, but the project lives on if you want it to:

- 🎓 **Submit to a high-school research showcase / science fair** — REHS often has one, and this project is competitive.
- 📝 **Blog post** — write up the project on Medium or your personal site. Recruiters love a build story.
- 🎥 **YouTube demo video (3 min)** — link from the README.
- 🤝 **Maintain it** — if a few students want to keep contributing through the school year, the mentor can stay on as an advisor. The bot becomes *yours*.
- 🏅 **List the project on your college apps** — "I built and deployed an AI system used by researchers at the San Diego Supercomputer Center." That sentence is true now.

---

## Pair check-ins

- Is the live URL working *right now*? (Check it.)
- Does the README explain the project in 30 seconds to someone who's never heard of NRP?
- Is the team repo **public** (not 404 for a stranger), and did you announce the URL in `#general:matrix.nrp-nautilus.io`?
- Does every student have the repo pinned on their GitHub profile?

---

## 🤖 Bonus: put your bot in Matrix (+ tool calling)

Your bot has a web UI — but the NRP community already lives in **Matrix**. This bonus puts your bot *where the users are*: a Matrix account that answers NRP questions in a room, using the **exact same RAG core** (`answer_question()`) behind your web app. It's the most "real integration" thing you can ship this summer.

> **Mentor sets this up:** it needs a dedicated **Matrix bot account** on `matrix.nrp-nautilus.io` and its **access token** (treat it like the LLM token — secret, in a `.env`/Secret). The mentor creates it ahead of time and picks which room the bot joins (`#rehs-2026` first; wider NRP rooms only with NRP's OK).

**How it works** (Python, [`matrix-nio`](https://github.com/matrix-nio/matrix-nio)) — it reuses your RAG core, so it's a new *front door*, not new bot logic:
```python
pip install matrix-nio

from nio import AsyncClient, RoomMessageText
from src.ui.chat import answer_question      # the SAME core your web app calls

client = AsyncClient("https://matrix.nrp-nautilus.io", "@rehs-bot:matrix.nrp-nautilus.io")

async def on_message(room, event):
    if event.body.startswith("!nrp "):        # e.g. "!nrp how do I request a GPU?"
        result = answer_question(event.body[5:])
        sources = "\n".join(f"- {c['title']}: {c['source_url']}" for c in result["chunks"])
        await client.room_send(room.room_id, "m.room.message",
            {"msgtype": "m.text", "body": f"{result['answer']}\n\nSources:\n{sources}"})

client.add_event_callback(on_message, RoomMessageText)
# log in with the bot's access token, then await client.sync_forever(timeout=30000)
```
- Run it as a second process/pod next to the web app (it's a long-lived client, not a web server).
- Bonus polish: reply in a thread, render citations nicely, add a 👍/👎 reaction.

### Extra bonus: give the bot *tools* (let it act, not just answer)

Plain RAG answers from docs. **Tool calling** (function calling) lets the LLM decide to *run code* for live answers — turning your bot agentic. Use the OpenAI-compatible `tools` parameter:
```python
tools = [{
  "type": "function",
  "function": {
    "name": "get_pod_status",
    "description": "Get the live status of a Kubernetes pod in the user's namespace",
    "parameters": {"type": "object", "properties": {"pod": {"type": "string"}}, "required": ["pod"]},
  },
}]
# Pass tools=tools to chat.completions.create. If the model returns a tool_call, YOU run
# get_pod_status() (e.g. `kubectl get pod <pod>`), send the result back, and the model writes
# the final answer. Now "is my pod running?" gets a *real* answer.
```
- Start with **one read-only tool** (`get_pod_status`, `list_my_pods`). Read-only keeps it safe.
- ⚠️ **Never** give the bot a tool that deletes or changes cluster state without a human confirm. Talk safety through with the mentor first.
- This is genuinely how real AI agents work — landing even one tool is a standout demo and a great résumé line.

---

## Stretch goals (week-8-only ideas)

- 🤖 **Matrix bot + tool calling** — see the bonus section just above; the headline stretch this week.
- 🌐 **Multilingual:** test the bot in Spanish, Mandarin, or another language. Most LLMs handle this with zero changes.
- 🎙️ **Voice mode:** use Streamlit's audio input + Whisper. (Whisper hosted on NRP? Ask mentor.)
- 📱 **Mobile app shell:** wrap the URL in a PWA so it installs to a phone home screen.

---

## Resources

- [How to write a great README (Make a README)](https://www.makeareadme.com/)
- [Choose a license (MIT, etc.)](https://choosealicense.com/)
- [How to write a good PR description (GitHub blog)](https://github.blog/2022-06-22-write-better-commits-build-better-projects/) (applies to PRs too)
- [Anthropic's tips for live demos](https://www.anthropic.com/engineering/built-multi-agent-research-system) (great article on what real engineers do)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| URL is slow during demo | Cold-start of pod after low traffic | Hit the URL 30 min before the demo to warm it up |
| Bot rate-limited mid-demo | Hit NRP fair-use cap | Use cached responses for canned demo questions; ask mentor about quota |
| Repo is a 404 for visitors | It's still private | GitHub → repo **Settings** → **Change visibility** → Public |
| Slides hard to read when screen-shared | Low contrast / small text | Use a dark theme, 24pt+ text, plenty of whitespace |
| Audience asks something you don't know | This is fine | "Great question — I don't know offhand. Can I follow up after?" is a 100% acceptable answer |

---

## You did it.

8 weeks ago you may not have written a line of Python. Today you've shipped a real AI system, contributed to open source, and presented to research scientists. That's a real accomplishment. Take a victory lap.

**Welcome to engineering. Now go build the next thing.** 🚀
