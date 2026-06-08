# Troubleshooting Guide

"It broke. Now what?" When something doesn't work, find your symptom below.

---

## The debugging mindset

Before grabbing this guide, do these in order:

1. **Read the actual error message.** Out loud if needed. The message almost always says what's wrong.
2. **Reproduce it.** Can you make it happen again? If it only happened once, write down what you typed.
3. **Bisect.** What's the *smallest* change that makes it stop working? `git diff` is your friend.
4. **Google the exact error.** Copy the last line of the stack trace verbatim, paste into Google in quotes.
5. **Ask the AI.** Cursor/Claude Code/ChatGPT are great at parsing stack traces. Paste the error + the relevant code.
6. **Ask the team.** Matrix `#rehs-2026`. Half the time another pair has seen it.
7. **Ask the mentor.** When you do, include: (a) what you tried, (b) the exact error, (c) what you expected.

The skill is *systematic* debugging, not lucky guessing. Build the habit now.

---

## Python errors

### `ModuleNotFoundError: No module named 'X'`
You forgot to `pip install` or installed in the wrong env. Check: `which python3` and `which pip3` — do they match?
```bash
pip3 install X
# or, if in a venv:
source .venv/bin/activate && pip install X
```

### `ImportError: cannot import name 'X' from 'Y'`
Version mismatch. Check the docs for the version you installed. `pip show <package>` to see your version.

### `KeyError: 'NRP_LLM_TOKEN'`
`.env` file missing, wrong name, or not loaded.
```python
from dotenv import load_dotenv
load_dotenv()    # must run BEFORE os.environ[...]
print(os.environ.get("NRP_LLM_TOKEN", "MISSING"))
```

### `FileNotFoundError: [Errno 2] No such file or directory: 'foo.txt'`
You're in the wrong working directory. `print(os.getcwd())` to see where Python actually is.

### `IndentationError`
You mixed tabs and spaces. Use spaces only. In VS Code: "Convert Indentation to Spaces".

### `UnicodeDecodeError`
Reading a non-UTF-8 file as UTF-8. Specify encoding:
```python
open("file.txt", encoding="utf-8")
# or
open("file.txt", encoding="latin-1")   # for old text files
```

---

## NRP LLM API errors

### `401 Unauthorized`
Wrong token. Regenerate at [nrp.ai/llmtoken](https://nrp.ai/llmtoken).

### `404 Not Found`
Wrong base URL or wrong model name. Verify:
```bash
curl -H "Authorization: Bearer $NRP_LLM_TOKEN" https://ellm.nrp-nautilus.io/v1/models
```

### `429 Too Many Requests` or rate limit
You hit the fair-use cap. Slow down. Implement exponential backoff:
```python
import time
for attempt in range(5):
    try:
        return client.chat.completions.create(...)
    except RateLimitError:
        time.sleep(2 ** attempt)
```

### `500 Internal Server Error` from NRP
NRP server-side issue. Check the [LLM status page](https://nrp.ai/documentation/userdocs/ai/llm-managed/). If it's down, ping `#general:matrix.nrp-nautilus.io` in Matrix.

### Streaming chunks come through garbled
Make sure you're handling `delta.content` (not `message.content`) and that it can be `None`:
```python
delta = chunk.choices[0].delta.content or ""
```

### Bot ignores the system prompt
The model is small. Either use a bigger model (`qwen3` instead of `gpt-oss`), repeat the instruction in the user message, or make the system prompt shorter & more direct.

---

## Git errors

### `error: failed to push some refs to 'origin'`
Someone else pushed first. Pull and retry:
```bash
git pull --rebase origin main
git push origin <your-branch>
```

### `CONFLICT (content): Merge conflict in foo.py`
Two pairs edited the same lines. Open the file, look for `<<<<<<<`, `=======`, `>>>>>>>` markers. Pick which version to keep. Delete the markers. `git add` and continue.
- See [Oh Shit, Git!?!](https://ohshitgit.com/)

### "I accidentally committed `.env`"
Rotate the token immediately at nrp.ai/llmtoken (assume it's compromised). Then:
```bash
git rm --cached .env
echo ".env" >> .gitignore
git commit -am "Stop tracking .env"
git push
```
Note: the secret is still in git history. For real prod, use `git filter-repo` to remove it. Ask mentor.

### "I want to undo my last commit (but keep my changes)"
```bash
git reset --soft HEAD~1
```

### "I'm on the wrong branch and made changes"
```bash
git stash
git checkout right-branch
git stash pop
```

### `fatal: not a git repository`
You're outside the repo. `cd` to the right folder.

---

## Streamlit issues

### App opens but is blank
Check the terminal where you ran `streamlit run`. There's an error there.

### Chat input doesn't trigger anything
You forgot the walrus: `if prompt := st.chat_input(...):` — the `:=` matters.

### State resets between messages
You're using a regular variable instead of `st.session_state`. Use `st.session_state.messages`, not `messages = []`.

### "RuntimeError: Tried to use SessionInfo before it was initialized"
You're using Streamlit APIs outside `streamlit run`. Don't `python app.py` — use `streamlit run app.py`.

### Streaming response appears all at once
You're rendering to `st.write` instead of using `placeholder = st.empty()` + `placeholder.markdown(text)`.

---

## Docker issues

### `docker: command not found`
Install Docker Desktop and **start it** (the app must be running for the CLI to work).

### `Cannot connect to the Docker daemon`
Docker Desktop isn't running. Open the app.

### `permission denied` on Linux
Add yourself to the docker group: `sudo usermod -aG docker $USER`, then log out and back in.

### Build is slow on every change
Order your Dockerfile: copy `requirements.txt` and `pip install` *before* copying source code. That way Docker caches the deps layer.

### Image is huge (multi-GB)
- Use `python:3.12-slim` not `python:3.12`
- Add a `.dockerignore` excluding `.venv/`, `.git/`, `__pycache__/`, `*.pyc`, `data/raw/`
- Use multi-stage builds

### "Cannot connect" from outside the container
Streamlit defaults to `localhost`. Inside Docker, you need `--server.address=0.0.0.0`.

---

## Kubernetes issues

### `error: You must be logged in to the server`
OIDC token expired. Just run any kubectl command — it'll trigger browser login.

### Pod stuck in `Pending`
```bash
kubectl describe pod <name> -n $NS | tail -30
```
Look at Events. Common: `Insufficient nvidia.com/gpu` (no GPU available), `Insufficient memory`, or PVC not bound.

### Pod in `ImagePullBackOff`
- Image name typo
- Image is private and no pull secret
- Make GHCR image public via repo settings

### Pod in `CrashLoopBackOff`
```bash
kubectl logs <name> -n $NS --previous
```
That shows the logs from the most recent crash.

### Service has 0 endpoints
```bash
kubectl get endpoints <svc> -n $NS
```
If empty: your Service `selector` doesn't match any Pod `labels`. Compare them.

### Ingress works on port-forward but not via URL
- Wrong `ingressClassName` (check `kubectl get ingressclass`)
- TLS not issued: `kubectl describe ingress <name>` — look at events from cert-manager
- DNS not propagated yet (wait 5 min)
- NRP doesn't expose that hostname (confirm with mentor)

### Vector DB empty after pod restart
- You wrote to wrong path (not the PVC mount)
- `kubectl exec <pod> -n $NS -- ls -la /app/chroma_db`
- PVC was recreated (a delete-recreate of the PVC wipes data!)

---

## "Everything is broken and I want to give up"

Real talk: this happens to every engineer. Including the mentor. Including the people at NRP. The difference between giving up and not isn't IQ — it's habits:

1. **Take a 10-min break.** Walk. Get water. Come back.
2. **Explain the problem out loud to your pair partner** — even if they have no idea. Rubber-duck debugging works.
3. **Reduce.** Strip the problem down to the smallest reproducible thing. Often the bug becomes obvious.
4. **Sleep on it.** Bugs that are impossible at 6pm dissolve at 9am. We're not joking.
5. **Ask for help.** Helping each other is a *feature* of the program, not a fallback.

You're going to ship something real this summer. Frustration is part of the price. Keep going. 💪
