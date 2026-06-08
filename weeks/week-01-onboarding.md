# Week 1 — Onboarding & Your First API Call

> **Goal:** By the end of the week, every student can run a single command that makes a real Large Language Model on the National Research Platform answer a question of their choice — *and* has made their first contribution to a repo with a branch and a pull request.

**The vibe:** Day 1 of a startup. You're the eight founding engineers. The CEO (you, collectively) just signed up for a frontier-LLM platform that costs other companies thousands of dollars per month, and you got it for free because you're shipping something useful with it. This week you set up your tools, learn the lay of the land, and talk to a 120-billion-parameter model from your own laptop. **Show up. Set up. Talk to a giant brain.**

It feels slow — it's the "set up your tools and your head" week. Skipping it costs you for the whole summer, so take the time now.

---

## 📅 Live sessions this week (remote)

Week 1 is front-loaded with live time so we all start grounded and set up. Zoom links are pinned in Matrix `#rehs-2026`. The work below happens around the calls, with your pair.

| Session | What we'll do together |
|---|---|
| **Kickoff** | Welcome, introductions, what we're building, how the summer works |
| **The Big Picture** | Why this exists: SDSC, supercomputing, the AI compute crunch, NRP, and Kubernetes |
| **Get Running on NRP** | Live: join NRP, get your token, make your first API call, set up your repos |

New here? Read [the README](../README.md#how-the-program-runs) for how the whole program runs (schedule, expectations, repos).

---

## This week's milestone

By the end of the week, be ready to show:

1. A **`curl` or Python call** to the NRP LLM API, with **your own** token, answering a question *you* wrote
2. Your **personal practice repo** on GitHub, with an `about-me.md` you added **on a branch and merged via a pull request**
3. At least **3 commits** total in your repo

If you can do those three things, you nailed Week 1. Everything else is bonus.

---

## Concepts you'll meet this week

- **SDSC, HPC, NRP, Kubernetes** — the *why* behind the program (covered live + in [the primer](../resources/primer-supercomputing-ai-nrp.md))
- **Matrix / Element** — the chat system NRP uses (like Discord/Slack, but federated)
- **NRP namespace** — the cohort's shared "folder" inside the giant NRP Kubernetes cluster (all 8 of you work in one)
- **API token** — a secret string that proves you're you when you call NRP's LLM
- **The terminal** — the black-text-on-white window where real engineers live
- **git & GitHub** — branches, commits, and pull requests: how the world ships code
- **Pair programming** — two engineers, one keyboard

---

## 📖 Read this before the Big-Picture session

Skim [**the primer: Supercomputing, AI, and Why NRP Exists**](../resources/primer-supercomputing-ai-nrp.md) before the call, and read it properly after. By the end you should be able to explain — to a friend who knows nothing — what SDSC is, why supercomputers matter, what NRP is, and what Kubernetes does. Don't memorize it; you'll touch every one of these with your hands over the summer.

---

## Hands-on this week

Do these with your pair. The exact order is up to you; this is a sane default.

### 1. Get on the team chat (right after the kickoff call)
- [ ] **Install [Element](https://element.io/download)** on your laptop *and* phone.
- [ ] **Make a Matrix account on NRP's server:** open [element.nrp-nautilus.io](https://element.nrp-nautilus.io) → Create Account → username, password, real email. Your handle becomes `@yourname:matrix.nrp-nautilus.io`. **Back up your encryption keys** when prompted.
- [ ] Join `#general:matrix.nrp-nautilus.io`, `#news:matrix.nrp-nautilus.io`, and `#rehs-2026` (mentor will invite you to the last).
- [ ] Post a "hello" in `#rehs-2026` with your name and what you're most excited to learn.

### 2. Install your tools
- [ ] **Mac:** open **Terminal**, install [Homebrew](https://brew.sh/), then `brew install git python3 curl`.
- [ ] **Windows:** install **WSL2 + Ubuntu** ([guide](https://learn.microsoft.com/en-us/windows/wsl/install)), then inside Ubuntu: `sudo apt update && sudo apt install -y git python3 python3-pip curl`.
- [ ] **Linux:** `apt`/`dnf`/`pacman`, your call.
- [ ] **Install [VS Code](https://code.visualstudio.com/)**.
- [ ] **Make a [GitHub account](https://github.com)** with your real name — it's going on your college apps. Post your username in `#rehs-2026`.
- [ ] **Configure git:**
  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "your_email@example.com"
  ```

### 3. Get your NRP token (we do this together in the "Get Running" session)
- [ ] Confirm our shared **namespace** name in `#rehs-2026` (the mentor posts it — the whole cohort uses one).
- [ ] At [nrp.ai/llmtoken](https://nrp.ai/llmtoken) → log in → **Generate Token** → **copy it immediately** (shown once).
- [ ] Put it in a `.env` file (git will ignore this — your secret never leaves your machine):
  ```
  NRP_LLM_TOKEN=sk-xxxxxxxxxxxxxxxxxxxxxxx
  NRP_LLM_BASE_URL=https://ellm.nrp-nautilus.io/v1
  ```
- [ ] ⚠️ **NEVER** paste your token in Matrix, a screenshot, or a commit. Treat it like your Instagram password. Leak it? Regenerate it immediately.

### 4. Make your first API call — the moment it gets real
- [ ] **First with curl** (raw HTTP):
  ```bash
  curl -H "Authorization: Bearer $NRP_LLM_TOKEN" \
       -H "Content-Type: application/json" \
       -X POST https://ellm.nrp-nautilus.io/v1/chat/completions \
       -d '{
         "model": "gpt-oss",
         "messages": [{"role": "user", "content": "Tell me a joke about supercomputers."}]
       }'
  ```
  You should get a JSON blob with a joke. `401 Unauthorized` = token wrong. `404` = check the URL.
- [ ] **Then in Python**, in your personal repo (see homework below):
  ```bash
  pip3 install openai python-dotenv
  ```
  ```python
  # hello_llm.py
  import os
  from dotenv import load_dotenv
  from openai import OpenAI

  load_dotenv()
  client = OpenAI(
      api_key=os.environ["NRP_LLM_TOKEN"],
      base_url=os.environ["NRP_LLM_BASE_URL"],
  )
  response = client.chat.completions.create(
      model="gpt-oss",
      messages=[{"role": "user", "content": "What is the National Research Platform?"}],
  )
  print(response.choices[0].message.content)
  ```
  Run it: `python3 hello_llm.py`
- [ ] Try **5 different questions** and **3 different models** (`gpt-oss`, `qwen3-small`, `gemma`). Notice how the answers differ.

---

## 📝 Homework — after our first (kickoff) call

This is your **first real git workflow** — the exact loop you'll use to contribute code all summer. Don't worry if it's new; that's the point. Take it one step at a time.

**Goal:** create your own repo, add a file about yourself on a branch, and open a pull request.

1. **Create your personal practice repo on GitHub.** Click **New repository** → name it `rehs-2026-yourname` → check **"Add a README"** → Create. (This is *your* repo — your sandbox for the summer.)
2. **Clone it to your laptop:**
   ```bash
   git clone https://github.com/yourname/rehs-2026-yourname.git
   cd rehs-2026-yourname
   ```
3. **Make a branch** (never work directly on `main`):
   ```bash
   git checkout -b about-me
   ```
4. **Add a file called `about-me.md`** with:
   - Your name, school, and grade
   - Why you joined this program
   - **3 things you hope to learn this summer**
   - One fun fact about you (emoji encouraged 🎉)
5. **Commit it** with a real message:
   ```bash
   git add about-me.md
   git commit -m "Add about-me: who I am and what I want to learn"
   ```
6. **Push your branch:**
   ```bash
   git push origin about-me
   ```
7. **Open a Pull Request** on GitHub (it'll prompt you after the push). Title it `About me: yourname`, write a one-line description, and **Create pull request**.
8. **Post the PR link in `#rehs-2026`** so we can all read them.
9. **Merge your PR** (green "Merge pull request" button) — congrats, that's your first merge.

**Bonus (do it if you can):** open a teammate's PR and leave **one kind comment**. Reviewing each other's work is half of how real teams ship.

> Why this matters: by Week 5 you'll be opening PRs to add real features to the chatbot. Learning the branch → commit → push → PR loop *now*, on something low-stakes and fun, means it's muscle memory when the stakes are real.

---

## Pair check-ins (talk to your pair about these)

- Can you both run `hello_llm.py` on your own laptops?
- Did you both keep your `.env` out of git? (Check: `cat .gitignore` should contain `.env`.)
- Did you both get your `about-me` PR merged? If one of you is stuck on git, the other helps — that's the job.
- After the primer: can each of you explain, in one sentence, what NRP is and what Kubernetes does?

---

## Stretch goals

- Try the `qwen3` model (huge — frontier reasoning, multimodal). Ask it about an image (the OpenAI SDK supports image_url content).
- Try the `gpt-oss` reasoning capability (set `extra_body={"reasoning_effort": "high"}`).
- Write a tiny `chat_loop.py` that asks for input in a `while` loop and sends each message to the LLM. (Don't worry about memory yet — that's Week 4.)
- Read the [NRP LLM Fair Use Policy](https://nrp.ai/documentation/userdocs/ai/llm-managed/). Be a good citizen.

---

## Resources

- [Primer: Supercomputing, AI, and Why NRP Exists](../resources/primer-supercomputing-ai-nrp.md) — read this for the Big-Picture session
- [the README](../README.md#how-the-program-runs) — schedule, expectations, how the repos work
- [GitHub Hello World tutorial](https://docs.github.com/en/get-started/quickstart/hello-world) — branches + PRs, beginner-friendly (great for the homework)
- [NRP LLM API docs](https://nrp.ai/documentation/userdocs/ai/llm-managed/api-access/)
- [NRP available models](https://nrp.ai/documentation/userdocs/ai/llm-managed/models/)
- [VS Code intro video](https://code.visualstudio.com/docs/introvideos/basics) (7 min)
- [Bash terminal in 100 seconds](https://www.youtube.com/watch?v=I4EWvMFj37g)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `curl: command not found` | curl not installed | Mac: `brew install curl`. Ubuntu: `sudo apt install curl`. |
| `401 Unauthorized` | Token wrong/expired/missing | Regenerate at [nrp.ai/llmtoken](https://nrp.ai/llmtoken) |
| `command not found: python3` | Python not installed or not in PATH | Reinstall via Homebrew (Mac) or apt (Linux) |
| `ModuleNotFoundError: openai` | Didn't `pip install` | `pip3 install openai python-dotenv` |
| `.env` shows up in `git status` | Not gitignored | Add `.env` on its own line in a `.gitignore` file |
| `git push` rejected / asks for password | Not authenticated to GitHub | Set up a [Personal Access Token](https://docs.github.com/en/authentication) or `gh auth login` |
| Can't open a PR — "nothing to compare" | You pushed to `main`, not a branch | Make a branch (`git checkout -b about-me`), commit there, push that |
| Matrix won't let me make an account | Wrong server URL | Use **matrix.nrp-nautilus.io**, not matrix.org |

See [resources/troubleshooting.md](../resources/troubleshooting.md) for more.

---

**Next:** [Week 2 — Python Fundamentals & Git Basics](week-02-python-and-git.md)
