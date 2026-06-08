# NRP Cheatsheet

A quick reference for the NRP-specific things you'll do all summer. Bookmark this.

---

## URLs you'll use constantly

| What | URL |
|---|---|
| LLM token generation | https://nrp.ai/llmtoken |
| LLM Open WebUI (browser chat) | https://nrp-openwebui.nrp-nautilus.io |
| LLM API base URL | https://ellm.nrp-nautilus.io/v1 |
| LLM status dashboard | https://nrp.ai/documentation/userdocs/ai/llm-managed/ |
| Matrix (chat) | https://element.nrp-nautilus.io |
| Documentation site | https://nrp.ai/documentation/ |
| Source repo for docs | https://github.com/nrp-nautilus/documentation |

---

## Models you'll use

| Model | Size | Good for | Notes |
|---|---|---|---|
| `gpt-oss` | 120B | General chat, fast, LTS | Default for our chatbot |
| `qwen3-small` | 27B | Latency-sensitive multimodal | Faster than qwen3, smaller |
| `qwen3` | 397B | Frontier reasoning, hard questions | Big, slow, very smart |
| `gemma` | 31B | Multimodal (image+text+video) | Reasoning off by default |
| `qwen3-embedding` | 8B | **Embeddings only** — not chat | Use for RAG vectors |

> Context lengths differ per model and change as NRP updates them — check the live [models page](https://nrp.ai/documentation/userdocs/ai/llm-managed/models/).

Status & live load: https://nrp.ai/documentation/userdocs/ai/llm-managed/

---

## Minimal Python call

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["NRP_LLM_TOKEN"],
    base_url="https://ellm.nrp-nautilus.io/v1",
)

response = client.chat.completions.create(
    model="gpt-oss",
    messages=[{"role": "user", "content": "Hello"}],
)
print(response.choices[0].message.content)
```

## Minimal curl call

```bash
curl -H "Authorization: Bearer $NRP_LLM_TOKEN" \
     -H "Content-Type: application/json" \
     -X POST https://ellm.nrp-nautilus.io/v1/chat/completions \
     -d '{"model":"gpt-oss","messages":[{"role":"user","content":"hi"}]}'
```

## Minimal embedding call

```python
resp = client.embeddings.create(model="qwen3-embedding", input=["text to embed"])
vector = resp.data[0].embedding   # list[float] — run len(vector) to see the dimension
```

---

## Streaming responses

```python
stream = client.chat.completions.create(
    model="gpt-oss",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content or ""
    print(delta, end="", flush=True)
```

---

## `cache_salt` (for our chatbot)

Add a per-tenant salt so prompt caching doesn't leak across users:

```python
import secrets, base64
salt = base64.b64encode(secrets.token_bytes(32)).decode()

response = client.chat.completions.create(
    model="gpt-oss",
    messages=[...],
    extra_body={"cache_salt": salt},
)
```

---

## Fair use — be a good citizen

- There are concurrency limits per model. SDDC/Internet2 affiliates get higher limits.
- Don't loop without backoff. Don't fan out 100 parallel requests.
- If you get rate-limited, slow down and ask in Matrix `#general:matrix.nrp-nautilus.io` before assuming it's broken.
- Read the [Fair Use Policy](https://nrp.ai/documentation/userdocs/ai/llm-managed/) before doing anything weird.

---

## Common kubectl commands for our chatbot's namespace

```bash
NS=<namespace>

kubectl get pods -n $NS                    # what's running
kubectl get deploy,svc,ingress,pvc -n $NS  # all the chatbot resources
kubectl logs deploy/chatbot -n $NS -f      # tail the bot's logs
kubectl describe pod <pod-name> -n $NS     # why is this pod broken?
kubectl exec -it <pod-name> -n $NS -- bash # shell into the pod
kubectl port-forward svc/chatbot 8501:80 -n $NS   # local test
kubectl rollout restart deploy/chatbot -n $NS     # cycle the pod
kubectl rollout undo deploy/chatbot -n $NS        # rollback last deploy
```

---

## Matrix rooms to join (and why)

| Room | Purpose |
|---|---|
| `#rehs-2026` | Our private team room — primary daily chatter |
| `#general:matrix.nrp-nautilus.io` | The main NRP community room — for help & announcements |
| `#news:matrix.nrp-nautilus.io` | Cluster news, downtime notices, releases |
| `#llm-managed` | LLM service-specific discussion (if it exists) |

**Don't DM admins.** They reject private messages. Ask in the public room.

---

## Things you'll wish someone told you on Day 1

- **Always pass `-n <namespace>`** with kubectl. Or set it as default: `kubectl config set-context --current --namespace=<namespace>`.
- **Never commit `.env`.** Add it to `.gitignore` *before* you put anything in it.
- **`cache_salt` is mandatory for multi-tenant apps.** Our chatbot is multi-tenant once it's public.
- **NRP doesn't auto-restart pods on token rotation.** When you rotate, `kubectl rollout restart deploy/chatbot`.
- **Storage classes & ingress classes are cluster-specific.** Ask. Don't guess.
- **The `qwen3-embedding` model is for embeddings only.** It won't chat with you.
