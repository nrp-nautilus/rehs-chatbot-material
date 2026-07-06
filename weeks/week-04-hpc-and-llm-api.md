# Week 4 — HPC Concepts + LLM API Deep Dive

> **Goal:** By Friday, you have a Streamlit web app on your laptop that streams responses from the NRP LLM with conversation memory and a custom system prompt — and you understand what a "GPU pod" is.

**The vibe:** the "we have a real product now" week. By Friday your bot has a UI a stranger could use. Tokens stream in real-time. It remembers what you said. It has a personality you wrote. Also: you'll briefly touch the GPUs that make all of this possible — the same hardware OpenAI and Google rent at $40k/month per node. **You're in the room with the actual machinery now.**

This is the **transition week**. First half: HPC concepts that make NRP special (GPUs, batch jobs, why your bot needs a real cluster). Second half: graduate from CLI to a real web UI with **Streamlit** + master the full LLM API surface area.

**This is the last "everyone learns the same thing" week.** Next week each pair builds its *own* complete RAG bot — the whole pipeline, not one slice.

---

## 📅 Live sessions this week (remote)

~3 sync hours; the other ~17 are pair work with your partner. Times are pinned in `#rehs-2026`.

| Session | Required? | What happens |
|---|---|---|
| **Weekly call** (1 hr) | ✅ Yes | Demo last week (5 min/pair) → this week's goals → **live demo: streaming LLM responses in Streamlit + prompt-design patterns** → unblock |
| **Office hours #1** (1 hr) | Optional, encouraged | Drop-in: bring a blocker or a screen to share |
| **Office hours #2** (1 hr) | Optional, encouraged | Drop-in: last push before this week's milestone |

**Before the call:** read this week's file with your pair. **After the call:** post your pair's plan (who does what) in `#rehs-2026`.

> Your **weekly milestone** is the deadline; you'll **demo it in next week's call**. New to the remote rhythm? See [the README](../README.md#how-the-program-runs).

---

## This week's milestone

A live demo where you:

1. Run `streamlit run app.py` and open a chat UI in your browser
2. Have a multi-turn conversation with the LLM (the bot **remembers** prior messages)
3. Show responses **streaming** in token-by-token (not waiting for full response)
4. Show a custom **system prompt** giving the bot a persona or specialty
5. **Bonus:** show a screenshot of a GPU pod you ran on NRP (or a Jupyter pod with GPU access)

---

## Concepts you'll meet this week

**HPC / NRP:**
- Why GPUs matter for AI (parallelism, matrix math, why your laptop can't run qwen3)
- Interactive vs batch jobs
- Persistent volumes (PVCs) — how data survives pod restarts
- GPU resource requests in K8s (`nvidia.com/gpu: 1`)
- Jupyter on Kubernetes
- The "shared cluster" mindset (fair use, concurrency limits)

**LLM API:**
- The chat messages format (`role: system | user | assistant`)
- System prompts (the bot's "personality")
- Streaming responses (`stream=True`)
- Token counting and context windows
- Temperature, top_p, and sampling
- `cache_salt` for NRP (privacy across tenants)
- Reasoning models and "thinking" tokens

**New library:**
- **Streamlit** — turn a Python script into a web app in 30 lines

---

## 📓 Interactive notebook — the Streamlit + tools build

Open [**`notebooks/week-04-streamlit-and-tools.ipynb`**](../notebooks/week-04-streamlit-and-tools.ipynb) in VS Code (install the *Jupyter* extension if it prompts). It's the Wednesday–Thursday material as runnable cells: the **LLM bits** (streaming, memory, system prompts — with the real NRP gotchas), then **Streamlit built up one `app.py` at a time**, then a **tools show-and-tell** ending in a read-only **`kubectl` tool** — a bot that can answer *"how many pods are running in our namespace?"* by inspecting the real cluster. It needs your NRP token (and `kubectl` set up from Week 3 for the last part).

---

## Suggested daily flow

### Monday — HPC concepts + GPUs on NRP

Today is mostly reading and watching. Take notes.

- [ ] Watch: [High Performance Computing (HPC) — Computerphile (~10 min)](https://www.youtube.com/watch?v=jBsc83_4RsQ)
- [ ] Watch: [MythBusters: GPU vs CPU — the NVIDIA paintball demo (~2 min)](https://www.youtube.com/watch?v=0udMBdo0Rac) — a famous, fun illustration of why GPUs win at parallel work
- [ ] Read: [NRP GPU pods guide](https://nrp.ai/documentation/userdocs/running/gpu-pods/)
- [ ] Read: [NRP storage guide](https://nrp.ai/documentation/userdocs/storage/intro/) — focus on **PVCs** (PersistentVolumeClaims). We'll need one for our vector DB.
- [ ] In your pair, sketch this picture on paper or a whiteboard:
  ```
  Your chatbot in Week 7 will need:
    - 1 pod running Streamlit (no GPU needed — it just calls the LLM API)
    - 1 PVC for the vector database
    - 1 Service so it has a stable network address
    - 1 Ingress so it has a public URL
  The LLM itself runs in someone *else's* pod on the cluster (already running, with a GPU).
  ```

### Tuesday — Launch a GPU pod (real one!)

- [ ] **With the mentor**, launch a GPU pod following [NRP's GPU pod guide](https://nrp.ai/documentation/userdocs/running/gpu-pods/). Example:
  ```yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: my-first-gpu-pod
    namespace: <namespace>
  spec:
    restartPolicy: Never
    containers:
    - name: gpu-test
      image: nvidia/cuda:12.4.0-base-ubuntu22.04
      command: ["sleep", "3600"]
      resources:
        limits:
          nvidia.com/gpu: 1
          memory: 8Gi
          cpu: 2
        requests:
          nvidia.com/gpu: 1
          memory: 8Gi
          cpu: 2
  ```
- [ ] `kubectl apply` it. Wait until `Running`. Then:
  ```bash
  kubectl exec -it my-first-gpu-pod -n <namespace> -- bash
  nvidia-smi   # shows the GPU. Take a screenshot.
  ```
- [ ] **Clean up immediately** when done: `kubectl delete pod my-first-gpu-pod -n <namespace>`. GPUs are scarce. Don't squat on one.
- [ ] **Optional:** spin up a Jupyter pod with GPU access (NRP has templates) and run a single Hugging Face inference. Skip if time's tight — the real goal this week is Streamlit.

### Wednesday — System prompts, conversation memory, streaming

Today you take the CLI chatbot from Week 2 and make it *much* better.

- [ ] **System prompts.** Add a system message to your chat:
  ```python
  history = [
      {"role": "system", "content": "You are an NRP support specialist. You are friendly, concise, and always answer with code examples when relevant. If you don't know something, say so."}
  ]
  ```
  Notice how the bot's tone changes.
- [ ] **Streaming.** Pass `stream=True`:
  ```python
  stream = client.chat.completions.create(
      model="gpt-oss",
      messages=history,
      stream=True,
  )
  full_response = ""
  for chunk in stream:
      delta = chunk.choices[0].delta.content or ""
      print(delta, end="", flush=True)
      full_response += delta
  print()
  history.append({"role": "assistant", "content": full_response})
  ```
- [ ] **Temperature.** Try the same prompt at `temperature=0.0` (deterministic) vs `temperature=1.2` (creative). Discuss with your pair: when would you want each?
- [ ] **Token budgets.** Print `response.usage.total_tokens` every turn. What's your conversation costing in tokens?
- [ ] **`cache_salt`** — read [the NRP API docs](https://nrp.ai/documentation/userdocs/ai/llm-managed/api-access/) on `cache_salt`. Add one to your requests:
  ```python
  import secrets, base64
  cache_salt = base64.b64encode(secrets.token_bytes(32)).decode()
  # pass as extra_body={"cache_salt": cache_salt}
  ```
  Why does this matter for a real chatbot? (Hint: privacy between users.)

### Thursday — Streamlit! Hello, web UI

Streamlit turns a Python script into a web app. No HTML, no JS. This is your bot's UI for the rest of the summer.

- [ ] Install: `pip install streamlit`
- [ ] Create `app.py`:
  ```python
  import os
  import streamlit as st
  from dotenv import load_dotenv
  from openai import OpenAI

  load_dotenv()
  client = OpenAI(
      api_key=os.environ["NRP_LLM_TOKEN"],
      base_url=os.environ["NRP_LLM_BASE_URL"],
  )

  st.title("🤖 NRP Helper")
  st.caption("Your friendly guide to the National Research Platform")

  if "messages" not in st.session_state:
      st.session_state.messages = [
          {"role": "system", "content": "You are a helpful NRP support assistant. Be concise."}
      ]

  # Show conversation so far
  for msg in st.session_state.messages:
      if msg["role"] != "system":
          st.chat_message(msg["role"]).write(msg["content"])

  # Get new user input
  if prompt := st.chat_input("Ask about NRP..."):
      st.session_state.messages.append({"role": "user", "content": prompt})
      st.chat_message("user").write(prompt)

      with st.chat_message("assistant"):
          placeholder = st.empty()
          full = ""
          stream = client.chat.completions.create(
              model="gpt-oss",
              messages=st.session_state.messages,
              stream=True,
          )
          for chunk in stream:
              delta = chunk.choices[0].delta.content or ""
              full += delta
              placeholder.markdown(full + "▌")
          placeholder.markdown(full)
      st.session_state.messages.append({"role": "assistant", "content": full})
  ```
- [ ] Run it: `streamlit run app.py`. Your browser should open `http://localhost:8501`.
- [ ] Chat with it. Streaming should work. Memory should work. **Take a screenshot — put it in your PR description on Friday.**
- [ ] Add a **sidebar** with a model dropdown (`st.sidebar.selectbox("Model", ["gpt-oss", "qwen3-small", "gemma"])`) and a temperature slider (`st.sidebar.slider("Temperature", 0.0, 1.5, 0.7)`).

### Friday — Demo, prep for the build sprint, retro

- [ ] **5-min Streamlit demo per pair** — chat with your bot live. Show streaming, memory, sidebar controls.
- [ ] **Look ahead to Week 5.** Next week your pair builds its *own* complete RAG bot — the full pipeline (scrape → embed → retrieve → prompt → UI). No one is "the frontend pair." Everyone does the AI core.
- [ ] **Preview the bake-off.** All four bots get compared on a shared eval set in Week 6, and the best pieces of all four get merged into one team product in Week 7. So build something you'd want in the ring. Skim [Week 5](week-05-rag-mvp.md) with your pair.
- [ ] **Make sure your pair has a repo ready** for next week (the mentor will share the starter scaffold to clone).
- [ ] **Retro:** rate the week, what excites you about building your own bot, what scares you.

---

## Pair check-ins

- Why does `stream=True` feel better than waiting for the full response? (UX!)
- What's a system prompt actually doing? (It's just another message in the list — but it sets the bot's voice.)
- Can you both explain the difference between **interactive** and **batch** jobs?
- Did you remember to clean up your GPU pod? (Go check now: `kubectl get pods -n <namespace>`.)

---

## Stretch goals

- 🧠 **Reasoning models.** Try `gpt-oss` with `extra_body={"reasoning_effort": "high"}`. The model "thinks" before answering. Compare answers on a hard question.
- 🎨 **UI polish.** Add `st.set_page_config(page_icon="🤖", page_title="NRP Helper")`. Add a "Clear chat" button. Add markdown rendering for code blocks (Streamlit does this automatically — try asking the bot for Python code).
- 📊 **Usage tracking.** Show a running token counter in the sidebar.
- 🎙️ **Voice input** (stretch stretch). Streamlit has `st.audio_input`. Transcribe with Whisper if you're feeling spicy. (Whisper on NRP? Ask mentor.)
- 🔥 **Multimodal.** `qwen3` supports images. Add `st.file_uploader` for an image and send it with the message.

---

## Resources

- [NRP GPU pods](https://nrp.ai/documentation/userdocs/running/gpu-pods/)
- [NRP storage / PVCs](https://nrp.ai/documentation/userdocs/storage/intro/)
- [NRP LLM API docs](https://nrp.ai/documentation/userdocs/ai/llm-managed/api-access/) — re-read with fresh eyes this week
- [Streamlit chat tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)
- [OpenAI streaming docs](https://platform.openai.com/docs/api-reference/streaming) (NRP is compatible)
- [3Blue1Brown: But what is a neural network?](https://www.youtube.com/watch?v=aircAruvnKk) — beautiful intuition
- [Andrej Karpathy: Intro to LLMs (1 hour, optional but excellent)](https://www.youtube.com/watch?v=zjkBMFhNj_g)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| GPU pod stuck `Pending` | No GPU available right now | `kubectl describe pod` — look for "Insufficient nvidia.com/gpu" in Events. Try later or request fewer GPUs. |
| Streamlit doesn't auto-reload | Browser cached | Hard refresh (Cmd+Shift+R / Ctrl+Shift+R) |
| Stream is super slow | Big model, high reasoning | Try `gpt-oss` or `qwen3-small` — they're faster than `qwen3` |
| `st.session_state` resets every message | You're calling `st.rerun()` somewhere | Don't call `rerun()` mid-stream |
| Got rate-limited by NRP | Hit fair-use cap | Slow down, check status page, ask in Matrix `#general:matrix.nrp-nautilus.io` |

---

**Next:** [Week 5 — Build Your Own RAG Bot](week-05-rag-mvp.md)
