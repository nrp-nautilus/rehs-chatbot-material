# Week 7 — Merge & Deploy to NRP

> **Goal:** By Friday, the **single merged team bot** — assembled from the best pieces of all four bake-off bots — is live at a public URL on the NRP cluster. Real people can use it. The bot that answers questions about NRP runs on NRP.

**The vibe:** **LAUNCH WEEK.** This is the week. Everything before this was a rehearsal — Friday afternoon a URL exists on the internet and anyone who clicks it talks to your code running on a real supercomputer. Your mom can text the URL to her friends. You can put it in your bio. You can refresh it from your phone in line at Starbucks and know that the request is hitting a pod *you wrote* on the Nautilus cluster. **This is shipping.** Take it seriously, then take a screenshot.

This is the **shipping week**, and it has two halves. **First (Mon–Tue): the merge.** You take the bake-off winners — the best ingest, retrieval, prompt, and UI from across all four bots — and assemble them into one team repo. Because every bot honored the same interfaces, the pieces snap together. **Then (Wed–Fri): deploy.** Everything you've built has lived on a laptop; this week it goes to production, together. By Friday, when someone in a different city visits your URL, they hit a pod on the Nautilus cluster running the bot your whole cohort built.

---

## 📅 Live sessions this week (remote)

~3 sync hours; the other ~17 are pair work with your partner. Times are pinned in `#rehs-2026`.

| Session | Required? | What happens |
|---|---|---|
| **Weekly call** (1 hr) | ✅ Yes | Demo last week (5 min/pair) → this week's goals → **deployment walkthrough: manifests, `kubectl apply`, and debugging a live rollout** → unblock |
| **Office hours #1** (1 hr) | Optional, encouraged | Drop-in: bring a blocker or a screen to share |
| **Office hours #2** (1 hr) | Optional, encouraged | Drop-in: last push before launch |

**Before the call:** read this week's file with your pair. **After the call:** post your pair's plan (who does what) in `#rehs-2026`.

> Your **weekly milestone** is the deadline; you'll **demo it in next week's call**. New to the remote rhythm? See [the README](../README.md#how-the-program-runs).

---

## This week's milestone

First, the **merged team bot** is assembled in the shared repo from the bake-off winners. Then, a live demo where:

1. The URL `https://rehs-chatbot.nrp-nautilus.io` (or your assigned hostname) loads in a stranger's browser
2. They ask a question — the bot answers with retrieved context and citations
3. You can show `kubectl get pods -n <namespace>` with your `chatbot-*` pod `Running`
4. You can show `kubectl logs <pod>` displaying the request that just happened
5. The vector DB **persists** across pod restarts (kill the pod, it comes back, still works)

---

## Concepts you'll meet this week

- **Container registry** — where Docker images live (we'll use NRP's harbor or GHCR)
- **Image tags & versioning** — `v0.1`, `latest`, immutable tags
- **PersistentVolumeClaim (PVC)** — pod-attached storage that survives restarts
- **Secrets** — how to give your pod the LLM token without baking it into the image
- **ConfigMap** — non-secret config (model name, base URL, etc.)
- **Ingress + TLS** — how your pod gets a public HTTPS URL
- **Probes** — liveness (am I alive?) and readiness (can I serve traffic?)
- **Resource requests/limits** — being a polite cluster citizen
- **Rolling updates & rollbacks** — deploying without downtime

---

## Architecture you'll have by Friday

```
                  Internet
                     │
                     ▼
   ┌────────────────────────────────────┐
   │ Ingress (HTTPS, hostname)          │
   │ rehs-chatbot.nrp-nautilus.io       │
   └────────────────┬───────────────────┘
                    │
                    ▼
   ┌────────────────────────────────────┐
   │ Service                            │
   │ chatbot-svc (ClusterIP, port 80)   │
   └────────────────┬───────────────────┘
                    │
                    ▼
   ┌────────────────────────────────────┐
   │ Deployment: chatbot                │
   │ ├── replicas: 1                    │
   │ └── pod                            │
   │     ├── container: streamlit       │
   │     ├── env: NRP_LLM_TOKEN ◄── Secret
   │     ├── env: model, base_url ◄── ConfigMap
   │     └── mount: /app/chroma_db ◄── PVC (10Gi)
   └────────────────┬───────────────────┘
                    │
                    ▼ (HTTPS calls)
   ┌────────────────────────────────────┐
   │ NRP LLM API                        │
   │ https://ellm.nrp-nautilus.io/v1    │
   └────────────────────────────────────┘
```

---

## Part 1 — The Merge (Mon–Tue)

Assemble the **one team bot** from the bake-off winners, following the `MERGE-PLAN.md` you wrote in Week 6.

- [ ] **Use the shared team repo** (`rehs-nrp-chatbot`) — the starter scaffold is the skeleton; you fill it with the *winning* implementations.
- [ ] **Drop in each chosen component** from the pair that won it: the winning ingest, the winning `search()`, the winning prompt / `answer_question()`, the winning UI. Because every bot honored `docs/INTERFACES.md`, the pieces fit together.
- [ ] **Re-run `scripts/eval.py` on the merged bot** — it should score at least as well as the best single bot. If it's worse, something didn't merge cleanly; debug it.
- [ ] From here, **everyone works in the team repo** via branches + PRs. No more separate pair bots.

## Part 2 — Deploy together (Wed–Fri)

Nobody is "the deploy pair." **Everyone deploys** — rotate the keyboard so each of you runs `kubectl apply` at least once.

- [ ] **Step 1 — registry & image** — push the team Docker image to a registry NRP can pull from.
  - Option A: **GitHub Container Registry (GHCR)** — public, easy.
    ```bash
    docker tag rehs-chatbot:v0.7 ghcr.io/<<GH_ORG>>/rehs-chatbot:v0.7   # this ref is <<IMAGE>>
    docker login ghcr.io -u <gh-username>   # use a GitHub PAT with package:write
    docker push ghcr.io/<<GH_ORG>>/rehs-chatbot:v0.7
    ```
  - Option B: **NRP-hosted registry** (if mentor sets up) — ask in Matrix.
- [ ] **Step 2 — K8s manifests.** These live in `deploy/k8s/` (the starter repo already has the
  scaffold — fill in the cluster values). The six files are `configmap.yaml`, `secret.example.yaml`,
  `pvc.yaml`, `deployment.yaml`, `service.yaml`, `ingress.yaml`.

  > **No `namespace.yaml`.** The whole cohort shares **one namespace**, pre-assigned by the mentor —
  > you do **not** create or apply it yourself, so there's no namespace manifest to hunt for. Put that
  > one shared `<namespace>` in every manifest's `metadata.namespace`.

  `deploy/k8s/secret.yaml` (create with `kubectl create secret` — never commit secrets!):
  ```bash
  kubectl create secret generic chatbot-llm-token \
    --from-literal=NRP_LLM_TOKEN=sk-yourtoken \
    -n <namespace>
  ```

  `deploy/k8s/configmap.yaml`:
  ```yaml
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: chatbot-config
    namespace: <namespace>
  data:
    NRP_LLM_BASE_URL: "https://ellm.nrp-nautilus.io/v1"
    LLM_MODEL: "gpt-oss"
    EMBEDDING_MODEL: "qwen3-embedding"
  ```

  `deploy/k8s/pvc.yaml`:
  ```yaml
  apiVersion: v1
  kind: PersistentVolumeClaim
  metadata:
    name: chroma-data
    namespace: <namespace>
  spec:
    accessModes: [ReadWriteOnce]
    resources:
      requests:
        storage: 10Gi
    storageClassName: rook-ceph-block   # confirm with NRP docs / mentor
  ```

  `deploy/k8s/deployment.yaml`:
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: chatbot
    namespace: <namespace>
  spec:
    replicas: 1
    selector:
      matchLabels: {app: chatbot}
    template:
      metadata:
        labels: {app: chatbot}
      spec:
        containers:
        - name: streamlit
          image: <<IMAGE>>   # e.g. ghcr.io/<<GH_ORG>>/rehs-chatbot:v0.7
          ports:
          - containerPort: 8501
          envFrom:
          - configMapRef: {name: chatbot-config}
          - secretRef: {name: chatbot-llm-token}
          volumeMounts:
          - name: chroma
            mountPath: /app/chroma_db
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 2
              memory: 4Gi
          livenessProbe:
            httpGet: {path: /_stcore/health, port: 8501}
            initialDelaySeconds: 30
          readinessProbe:
            httpGet: {path: /_stcore/health, port: 8501}
            initialDelaySeconds: 5
        volumes:
        - name: chroma
          persistentVolumeClaim:
            claimName: chroma-data
  ```

  `deploy/k8s/service.yaml`:
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: chatbot
    namespace: <namespace>
  spec:
    selector: {app: chatbot}
    ports:
    - port: 80
      targetPort: 8501
    type: ClusterIP
  ```

  `deploy/k8s/ingress.yaml`:
  ```yaml
  apiVersion: networking.k8s.io/v1
  kind: Ingress
  metadata:
    name: chatbot
    namespace: <namespace>
    annotations:
      cert-manager.io/cluster-issuer: letsencrypt-prod   # confirm with NRP docs
  spec:
    ingressClassName: haproxy
    tls:
    - hosts: [rehs-chatbot.nrp-nautilus.io]
      secretName: rehs-chatbot-tls
    rules:
    - host: rehs-chatbot.nrp-nautilus.io
      http:
        paths:
        - path: /
          pathType: Prefix
          backend:
            service:
              name: chatbot
              port: {number: 80}
  ```

  **Note:** ingress class, cert issuer, storage class — get the right names from NRP docs or ask the mentor. They differ per cluster.

- [ ] **Step 3 — apply!**
  ```bash
  kubectl apply -f deploy/k8s/configmap.yaml
  kubectl apply -f deploy/k8s/pvc.yaml
  kubectl apply -f deploy/k8s/deployment.yaml
  kubectl apply -f deploy/k8s/service.yaml
  kubectl apply -f deploy/k8s/ingress.yaml
  kubectl get pods -n <namespace> -w   # watch it come up
  ```
- [ ] **First test:** `kubectl port-forward` to your service and confirm it works locally. Then visit the public hostname in your browser.
- [ ] **Step 4 — seed the vector DB.** The PVC is empty when the pod first starts! You need to seed it. Options:
  - **One-shot Job:** write a `Job` that runs `python scripts/ingest.py` then `python scripts/index.py` mounting the same PVC. Run once.
  - **Init container:** add an `initContainer` to your Deployment that runs the ingest+index on first start (skip if data already there).
  - **Bake into image (lazy):** check the chunks + a pre-built `chroma_db/` into the Docker image. Easiest but image gets large.
  Pick one. Discuss with mentor.
- [ ] **Step 5 — smoke test + demo.** Hit the URL from a friend's laptop. Walk through the demo. Celebrate.

## Hardening tasks (claim what you want — spread across pairs)

The team bot is one codebase now. Divvy these up so no two people step on each other; each is a branch + PR:

- [ ] **Re-ingest Job** — a `Job` manifest (`deploy/k8s/ingest-job.yaml`) the team can `kubectl apply -f` to refresh docs into the PVC. Add `{"ingested_at": ...}` freshness metadata to chunks.
- [ ] **Storage correctness** — confirm `chroma_db/` is written to `/app/chroma_db` (the PVC mount), and `search()` returns `[]` (with a friendly UI message) when the collection is empty, instead of crashing.
- [ ] **Graceful errors** — what does the UI show if the NRP LLM is down or retrieval is empty? Add `st.error(...)` states. No raw stack traces.
- [ ] **Footer + version** — "Built by REHS 2026 — view source on GitHub", plus the build version from an `APP_VERSION` env var in the ConfigMap.
- [ ] **Feedback button** — a "Report this answer" button that logs the conversation to a file on the PVC.
- [ ] **Mobile check** — open the deployed URL on your phone. Does it hold up?

---

## Suggested daily flow (whole cohort)

### Mon–Tue — Merge, then plan the cutover
- Merge the bake-off winners into the team repo (Part 1); get the merged bot passing eval from a clean clone.
- All-cohort: walk through the architecture diagram above. Identify unknowns (storage class? ingress class? hostname?).
- Mentor gets answers from the NRP team via Matrix.
- Together, draft the manifests; everyone reads them.

### Wed — First deploy attempt
- It will not work the first time. That's normal.
- Use `kubectl describe pod <name>`, `kubectl logs <pod>`, `kubectl get events --sort-by=.lastTimestamp -n <ns>` to debug.
- Common first-day issues: image pull errors, missing secret, wrong namespace, PVC pending.

### Wed–Thu — Get it serving traffic
- Port-forward should work.
- Public URL should work.
- TLS cert should be issued (cert-manager takes a few minutes).

### Thu — Seed data + harden
- Vector DB populated and persistent.
- Kill the pod, watch it come back, vector DB still works.
- Add monitoring/logging where useful.

### Fri — Demo + announce + retro
- 10-min demo to mentor + a guest researcher (mentor invites one).
- Post in Matrix `#general:matrix.nrp-nautilus.io`: "Hi NRP! We're some high schoolers and we built `[url]` — please try it and tell us where it's wrong."
- Retro: what was the scariest moment? When did you feel like it was actually going to work?

---

## Pair check-ins

- Does anyone *not* know the bot's public URL? Fix that.
- Has **every student** run `kubectl apply` at least once? (Everyone deploys this week — no spectators.)
- Did anyone commit the secret to git? *Check now.* If yes, rotate the token immediately at `nrp.ai/llmtoken`.

---

## Stretch goals

- 📈 **Metrics:** expose `/metrics` endpoint with request count, latency, error rate. Wire up to NRP's Prometheus.
- 🔄 **Auto-redeploy on push:** GitHub Action that builds + pushes the image on every merge to `main`, then `kubectl rollout restart`.
- 🛡️ **Rate-limit by IP:** so a single user can't burn through your fair-use quota.
- 🌍 **Custom domain (only if approved):** request a friendlier hostname.
- 🔍 **Honest "I don't know":** if retrieval returns nothing or scores are below a threshold, the bot explicitly says "I couldn't find this in the NRP docs" instead of guessing.
- 💬 **Feedback collection:** thumbs-up/thumbs-down on each answer, logged to PVC. Read in Week 8 to see what to improve.

---

## Resources

- [NRP storage docs (PVCs)](https://nrp.ai/documentation/userdocs/storage/intro/)
- [NRP ingress / public hostnames](https://nrp.ai/documentation/userdocs/tutorial/basic2/) — search for "ingress"
- [Kubernetes Secrets best practices](https://kubernetes.io/docs/concepts/configuration/secret/) — read the warnings
- [cert-manager docs](https://cert-manager.io/docs/) — how TLS certs auto-issue
- [Streamlit deployment notes](https://docs.streamlit.io/deploy/concepts) — minor but useful

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Pod `ImagePullBackOff` | Image is private and no pull secret | Make GHCR image public, or create `imagePullSecret` |
| Pod `CrashLoopBackOff` | App crashes on start | `kubectl logs <pod> --previous` to see why |
| PVC stuck `Pending` | Storage class wrong | Check NRP's available storage classes: `kubectl get storageclass` |
| Ingress works but no TLS / browser warning | cert-manager annotation wrong | Check `kubectl describe ingress` for cert events |
| Public URL gives 502 / 504 | Service can't reach pod | Check pod is `Ready`, check Service `selector` matches Pod `labels` |
| Bot works on port-forward but URL returns nothing | Ingress class wrong | Confirm ingressClassName with mentor |
| Pod restarts every 30s | Liveness probe failing | Increase `initialDelaySeconds`, confirm health endpoint exists |
| Vector DB empty after pod restart | Writing to wrong dir, not the PVC mount | `kubectl exec` into the pod, `ls /app/chroma_db` — is data there? |

---

**Next:** [Week 8 — Polish, Open-Source PR, Present](week-08-polish-and-present.md)
