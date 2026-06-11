# Week 2 — Python Fundamentals & Git Basics

> **Goal:** By Friday, you can write a Python program that talks to the NRP LLM in a loop — and you've used git like a real engineer (branches, PRs, code review).

**The vibe:** training arc. Every good origin story has the "learning to control your powers" episode. This is yours. The reason your Week 5 self can ship a RAG pipeline at 2x speed with AI tools is that your Week 2 self learned to type Python by hand. **You're not behind anyone. You're earning the speed.**

This week we slow down and learn the language. Reminder: **no AI assistants this week.** Write every character of code yourself. It will feel slow. That's the point. Muscle memory matters.

---

## 📅 Live sessions this week (remote)

~3 sync hours; the other ~17 are pair work with your partner. Times are pinned in `#rehs-2026`.

| Session | Required? | What happens |
|---|---|---|
| **Weekly call** (1 hr) | ✅ Yes | Demo last week (5 min/pair) → this week's goals → **live-code: Python idioms + a guided `git` branch → PR → review walkthrough** → unblock |
| **Office hours #1** (1 hr) | Optional, encouraged | Drop-in: bring a blocker or a screen to share |
| **Office hours #2** (1 hr) | Optional, encouraged | Drop-in: last push before this week's milestone |

**Before the call:** read this week's file with your pair. **After the call:** post your pair's plan (who does what) in `#rehs-2026`.

> Your **weekly milestone** is the deadline; you'll **demo it in next week's call**. New to the remote rhythm? See [the README](../README.md#how-the-program-runs).

---

## This week's milestone

You and your pair build and demo **`chat.py`**: a command-line chatbot that:

- Reads your API token from `.env`
- Asks the user for input in a loop (`while True:`)
- Sends each message to the NRP LLM
- Prints the response
- Exits cleanly when you type `quit` or hit Ctrl+C
- Has **at least one custom feature** you and your pair add (saves history to a file? counts tokens? supports `/model qwen3` to switch models?)

And the team milestone: every pair has merged a PR with `chat.py` into the team repo on a branch named `week02/<pair-name>-chat`.

---

## Concepts you'll meet this week

**Python:**
- Variables, types (`str`, `int`, `float`, `bool`, `list`, `dict`)
- `if`/`elif`/`else` and `while`/`for` loops
- Functions (`def`) and arguments
- Imports (`import`, `from ... import`)
- Reading user input (`input()`)
- Exception handling (`try`/`except`)
- Reading & writing files
- Virtual environments (`venv`)

**Git:**
- `git clone`, `git status`, `git add`, `git commit`, `git push`, `git pull`
- Branches (`git checkout -b`, `git switch`)
- Pull Requests on GitHub
- Code review (you'll review your pair partner's PR)
- `.gitignore`

---

## 📓 Interactive notebook — start here

Open [**`notebooks/week-02-python-and-git.ipynb`**](../notebooks/week-02-python-and-git.ipynb) in VS Code (install the *Jupyter* extension if it prompts you). It's this whole week as **runnable cells** — every Python concept below has a live example and a **🔧 Your turn** cell. Type, run, break, fix. Most of it needs **no NRP token**, so you can start today. Work through it with your pair, then build `chat.py` for real.

---

## Suggested daily flow

### Monday — Python basics, hand-written

Don't peek at AI. Write these in `practice/` (gitignored). Goal: build muscle memory.

- [ ] **Variables & math** — write a script that asks for your name and age, prints how old you'll be in 10 years.
- [ ] **Lists & loops** — print the first 20 numbers in the Fibonacci sequence.
- [ ] **Dictionaries** — make a dict mapping NRP model names → their context length (from [models page](https://nrp.ai/documentation/userdocs/ai/llm-managed/models/)). Print them in a nice table.
- [ ] **Functions** — write `def is_prime(n): ...` and use it to print primes under 100.

Watch: [Python in 100 Seconds](https://www.youtube.com/watch?v=x7X9w_GIm1s) (one of those is-it-100-seconds-or-7-minutes videos)
Reference: [official Python tutorial, sections 3-4](https://docs.python.org/3/tutorial/introduction.html)

### Tuesday — Reading docs, calling APIs, handling errors

- [ ] Read [the NRP API access page](https://nrp.ai/documentation/userdocs/ai/llm-managed/api-access/) carefully. What is `cache_salt`? What's `max_tokens`? Discuss with your pair.
- [ ] Take last week's `hello_llm.py` and **add error handling**. What happens if the network is down? If your token is wrong? Use `try`/`except`.
  ```python
  try:
      response = client.chat.completions.create(...)
  except Exception as e:
      print(f"Oops, something broke: {e}")
  ```
- [ ] Make the model name a variable at the top of the file. Try 3 different models with the same prompt. Diff the answers.

### Wednesday — Build `chat.py` v1

Now the real thing. **Write every line.**

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.environ["NRP_LLM_TOKEN"],
    base_url=os.environ["NRP_LLM_BASE_URL"],
)

print("NRP Chat. Type 'quit' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() in ("quit", "exit"):
        break
    response = client.chat.completions.create(
        model="gpt-oss",
        messages=[{"role": "user", "content": user_input}],
    )
    print("Bot:", response.choices[0].message.content)
    print()
```

- [ ] Get this working in your pair.
- [ ] Try chatting with it. Notice the bot **doesn't remember** previous messages. Why? (Hint: look at `messages=[...]`. It's only ever one message.)
- [ ] **Fix the memory problem**: keep a `history = []` list, append each user message and each bot reply, and pass `history` as `messages`. Now it remembers.
- [ ] Commit your progress on a branch.

### Thursday — Git deep-dive + custom feature

- [ ] Watch: [Git in 100 Seconds](https://www.youtube.com/watch?v=hwP7WQkmECE) (this one actually is fast).
- [ ] Read: [GitHub's "About Pull Requests"](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
- [ ] **Each pair picks a custom feature** for `chat.py`. Pick one that excites you:
  - 💾 Save conversations to `history.json` on quit
  - 🎯 Add `/model qwen3` slash commands to switch models mid-chat
  - 🧮 Show token count after each response (`response.usage.total_tokens`)
  - 🌊 Stream the response word-by-word using `stream=True`
  - 🎭 Load a system prompt from `system.txt` to give the bot a persona
  - 🌈 Color the output (try [`rich`](https://rich.readthedocs.io/))
- [ ] Implement it.
- [ ] **Push a PR**: each pair creates `week02/<pair-name>-chat` branch. One person opens the PR, the *other person* reviews it on GitHub (leave comments, request changes if needed).
- [ ] The mentor will merge once both pair members + mentor have approved.

### Friday — Demo + cross-pair code review + retro

- [ ] **5-min demo per pair** — show your custom feature.
- [ ] **Cross-pair code review** — each pair reviews another pair's PR. Leave at least 3 comments (anything: questions, praise, suggestions, typos).
- [ ] **Retro**: what was confusing this week? What clicked? What feature do you wish your chatbot had?

---

## Pair check-ins

- Can both of you explain what `while True:` does? What happens without the `break`?
- Why does the bot need a `history` list? What goes in it?
- Both of you should be able to `git push` from your own laptops by Friday. If only one of you has, fix it.
- Did your `.env` file accidentally get committed? (Check `git log -p .env`. If you see your token in git history, regenerate it immediately at [nrp.ai/llmtoken](https://nrp.ai/llmtoken).)

---

## Stretch goals

- 🥚 **Easter egg:** if the user types `/joke`, send a special prompt asking for a programmer joke.
- 🎨 **Personas:** support `--persona pirate` (CLI arg) that loads `personas/pirate.txt` as the system prompt.
- 📊 **Stats:** after every 5 messages, print total tokens used and estimated cost (NRP is free, but pretend each token = $0.0001).
- 🐍 **Type hints:** add `def chat(messages: list[dict]) -> str: ...` style type hints everywhere.
- 🧪 **Tests:** write a `test_chat.py` using `pytest`. (Mock the OpenAI client — Google "pytest mock openai".)

---

## Resources

**Python:**
- [Python official tutorial](https://docs.python.org/3/tutorial/) — the canonical one
- [Real Python beginner path](https://realpython.com/learning-paths/python-basics/) — gentle ramp
- [Fluent Python (free chapters)](https://www.fluentpython.com/lingo/) — if you want to go deep

**Git:**
- [Git in 100 Seconds (Fireship)](https://www.youtube.com/watch?v=hwP7WQkmECE)
- [Pro Git book (free)](https://git-scm.com/book/en/v2) — sections 1.1–2.5 cover everything you need this summer
- [Oh Shit, Git!?!](https://ohshitgit.com/) — how to un-break things (bookmark it now, you'll need it)

**OpenAI SDK (which NRP is compatible with):**
- [OpenAI Python SDK docs](https://github.com/openai/openai-python#readme)
- [Chat completions reference](https://platform.openai.com/docs/api-reference/chat)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `KeyError: 'NRP_LLM_TOKEN'` | `.env` not loaded or missing key | Check `.env` exists, has the key, and `load_dotenv()` runs before `os.environ[...]` |
| Bot replies but doesn't remember context | Not appending to `messages` list | Build a list and pass the *whole list* on each call |
| `pip install` says "permission denied" | Installing globally instead of in venv | Create a venv: `python3 -m venv .venv && source .venv/bin/activate`, then `pip install` |
| Can't push: "remote: Permission denied" | Not added to org / using HTTPS without token | Ask mentor in Matrix; set up SSH key or GitHub CLI (`gh auth login`) |
| Merge conflict on PR | Two pairs edited the same file | Pull main, resolve manually, push again. See [oh shit, git](https://ohshitgit.com/) |

---

**Next:** [Week 3 — Kubernetes Crash Course (and AI tools unlock!)](week-03-kubernetes.md)
