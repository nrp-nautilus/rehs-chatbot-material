# Week 3 — Kubernetes Crash Course (AI tools unlock 🎉)

> **Goal:** By Friday, every pair has deployed a "hello world" web server as a Kubernetes pod in their NRP namespace and reached it from their laptop.

**The vibe:** the level-up week. Two big unlocks at once: (1) **you get the cluster** — the actual Nautilus supercomputer that powers researchers across dozens of universities, your code runs there now, and (2) **AI tools unlock** — Cursor, Claude Code, Copilot. The training wheels come off. You can move 3x faster *if* you still understand what you're doing. Don't let the AI ship code you can't defend in a code review.

This week we step away from chatbots and learn the **infrastructure** that runs them. By the end you'll know what a pod is, what a deployment is, why namespaces exist, and how `kubectl` is just a friendly wrapper around the Kubernetes API. This makes you a better engineer *and* prepares you to deploy your bot in Week 7.

**🎉 AI tools unlock today.** You may now use Cursor, Claude Code, GitHub Copilot, or ChatGPT for code generation. **Rule:** if you can't explain a line, you don't get to commit it. Your pair partner gets to grill you on every PR.

---

## 📅 Live sessions this week (remote)

~3 sync hours; the other ~17 are pair work with your partner. Times are pinned in `#rehs-2026`.

| Session | Required? | What happens |
|---|---|---|
| **Weekly call** (1 hr) | ✅ Yes | Demo last week (5 min/pair) → this week's goals → **live `kubectl` demo: deploy a pod to NRP together — and AI tools officially unlock** → unblock |
| **Office hours #1** (1 hr) | Optional, encouraged | Drop-in: bring a blocker or a screen to share |
| **Office hours #2** (1 hr) | Optional, encouraged | Drop-in: last push before this week's milestone |

**Before the call:** read this week's file with your pair. **After the call:** post your pair's plan (who does what) in `#rehs-2026`.

> Your **weekly milestone** is the deadline; you'll **demo it in next week's call**. New to the remote rhythm? See [the README](../README.md#how-the-program-runs).

---

## This week's milestone

A live demo where:

1. You run `kubectl get pods -n <namespace>` and a `hello-nginx` pod is `Running`
2. You `kubectl port-forward` to it and curl/visit `http://localhost:8080` and see the nginx welcome page
3. You can **explain your `deployment.yaml`** line by line to the cohort — including: what's a `kind`? what's `replicas`? what's the difference between a `Pod` and a `Deployment`?

---

## Concepts you'll meet this week

- **Container** — a packaged-up app (think: a frozen-meal version of software)
- **Image** — the recipe for a container (lives in a "registry" like Docker Hub)
- **Pod** — Kubernetes' smallest unit, usually 1 container
- **Deployment** — a controller that keeps N copies of a pod alive
- **Service** — a stable network address for pods (which keep dying and getting replaced)
- **Namespace** — a folder for your stuff (you're working in `rehs-2026-<yourname>`)
- **YAML** — the config language Kubernetes reads (Python-like indentation, like JSON's calmer cousin)
- **`kubectl`** — the CLI command for talking to the cluster

Mental model:
```
   Your laptop  ──kubectl──>  Kubernetes API server  ──schedules──>  Nodes  ──run──>  Containers
                                                                      (GPUs!)         (your code)
```

---

## Suggested daily flow

### Monday — Install kubectl, get your kubeconfig

- [ ] **Install `kubectl`** on your laptop:
  - Mac: `brew install kubectl`
  - Linux: [official guide](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
  - Windows (WSL2): inside WSL, use the Linux instructions
- [ ] **Get your NRP kubeconfig** — follow [NRP's "Get a cluster config" guide](https://nrp.ai/documentation/userdocs/start/getting-started/). Save it as `~/.kube/config`.
- [ ] **Heads-up: the whole cohort shares ONE namespace** — the mentor posts its name in `#rehs-2026`. Wherever you see `<namespace>` in commands and manifests, use that one shared name.
- [ ] **Verify access:**
  ```bash
  kubectl config get-contexts          # should show "nautilus"
  kubectl get pods -n <namespace> # should work, even if empty
  kubectl auth can-i create pods -n <namespace>   # should say "yes"
  ```
- [ ] Watch: [Kubernetes in 100 Seconds (Fireship)](https://www.youtube.com/watch?v=PziYflu8cB8) — actually closer to 2 min, still worth it.
- [ ] Watch: [Containers vs VMs (IBM, 8 min)](https://www.youtube.com/watch?v=cjXI-yxqGTI) — important context.

### Tuesday — Pods, the smallest thing

A pod is just "a running container or two." Let's run one.

- [ ] **Run a pod imperatively** (no YAML yet):
  ```bash
  kubectl run hello --image=nginx -n <namespace>
  kubectl get pods -n <namespace>      # wait until STATUS=Running
  kubectl describe pod hello -n <namespace>
  kubectl logs hello -n <namespace>
  ```
- [ ] **Port-forward to talk to it:**
  ```bash
  kubectl port-forward pod/hello 8080:80 -n <namespace>
  # leave this running. In another terminal:
  curl http://localhost:8080
  # OR open http://localhost:8080 in your browser
  ```
  You should see the nginx welcome page.
- [ ] **Delete it:**
  ```bash
  kubectl delete pod hello -n <namespace>
  ```
- [ ] Discuss with your pair: what *is* a "container"? Why is it not a VM? Why is `nginx` so common?

### Wednesday — YAML, the declarative way

Imperative commands are quick to type but you can't save them. YAML files are checked into git.

- [ ] Create `deploy/hello-deployment.yaml`:
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: hello-nginx
    namespace: <namespace>   # ← change this
  spec:
    replicas: 2                   # two copies for redundancy
    selector:
      matchLabels:
        app: hello-nginx
    template:
      metadata:
        labels:
          app: hello-nginx
      spec:
        containers:
        - name: nginx
          image: nginx:1.27
          ports:
          - containerPort: 80
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 256Mi
  ```
- [ ] Apply it:
  ```bash
  kubectl apply -f deploy/hello-deployment.yaml
  kubectl get deployments -n <namespace>
  kubectl get pods -n <namespace>     # should see TWO pods now
  ```
- [ ] **Kill a pod and watch K8s heal:**
  ```bash
  kubectl delete pod <one-of-the-pod-names> -n <namespace>
  kubectl get pods -n <namespace>     # K8s spawns a new one
  ```
  Discuss with your pair: who told K8s to make a new pod? (Answer: the Deployment controller.)
- [ ] **AI-assisted exercise:** open Cursor/Claude Code and ask it to "add a livenessProbe and readinessProbe to my deployment.yaml". Apply the result, then **explain to your pair what each probe does and why**.

### Thursday — Services + Ingress (so others can reach you)

A pod's IP changes every time it restarts. A **Service** gives you a stable address.

- [ ] Create `deploy/hello-service.yaml`:
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: hello-nginx
    namespace: <namespace>
  spec:
    selector:
      app: hello-nginx
    ports:
    - port: 80
      targetPort: 80
    type: ClusterIP
  ```
- [ ] Apply it. Port-forward:
  ```bash
  kubectl apply -f deploy/hello-service.yaml
  kubectl port-forward service/hello-nginx 8080:80 -n <namespace>
  curl http://localhost:8080
  ```
- [ ] **Bonus** (do with mentor — needs cluster permissions): create an `Ingress` so it gets a public URL like `https://hello-<yourname>.nrp-nautilus.io`. See [NRP ingress docs](https://nrp.ai/documentation/userdocs/tutorial/basic2/) for examples.
- [ ] Read: [Kubernetes Comic from Google](https://cloud.google.com/kubernetes-engine/kubernetes-comic) — yes, a literal comic. It's amazing.

### Friday — Demo, retro, cleanup

- [ ] **Pair demo (5 min):** port-forward to your service, hit it in the browser, talk through your YAML.
- [ ] **The grilling:** another pair asks 3 K8s questions. Examples:
  - "Why does your deployment have 2 replicas?"
  - "What happens if I delete the deployment?"
  - "What's the difference between `port`, `targetPort`, and `containerPort`?"
- [ ] **Clean up** (NRP is shared — be a good citizen):
  ```bash
  kubectl delete -f deploy/hello-deployment.yaml
  kubectl delete -f deploy/hello-service.yaml
  ```
- [ ] **Commit** your YAMLs to the team repo on a branch `week03/<pair-name>-k8s-hello`.
- [ ] **Retro:** rate the week 1–5, what was the hardest concept.

---

## Pair check-ins

- Can you both explain what happens when you run `kubectl apply -f deployment.yaml`? (Hint: kubectl reads the YAML, sends it to the API server, the API server stores it in etcd, the deployment controller notices, the scheduler picks a node, kubelet pulls the image and starts the container.)
- Why does `kubectl get pods` show pods with weird suffixes like `hello-nginx-7d6c8f9b4-xk2lp`? (Hint: ReplicaSet name + random hash.)
- What namespace are you using? Have you ever accidentally deployed to the wrong namespace? (You will. It's fine. Just be careful with `-n`.)

---

## Stretch goals

- 🔧 **Lens or k9s:** install [Lens Desktop](https://k8slens.dev/) or [k9s](https://k9scli.io/) — beautiful Kubernetes dashboards. Lens has a learning curve; k9s is a TUI.
- 📈 **Resource requests:** read [Pod resource requests/limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/). Why did we set 100m CPU?
- 🔄 **Rolling updates:** change `image: nginx:1.27` → `image: nginx:1.28`, `kubectl apply`, watch the rollout: `kubectl rollout status deployment/hello-nginx -n <namespace>`.
- 🛡️ **kubectl get events:** when things break, `kubectl get events -n <namespace> --sort-by=.lastTimestamp` is your friend.
- 🧠 **AI literacy:** use Claude Code to ask "explain the YAML I just wrote like I'm 12". Compare its explanation to your own.

---

## Resources

- [NRP getting started](https://nrp.ai/documentation/userdocs/start/getting-started/) — read this fully
- [NRP namespace docs](https://nrp.ai/documentation/userdocs/start/policies/)
- [Kubernetes Comic (Google)](https://cloud.google.com/kubernetes-engine/kubernetes-comic) — surprisingly the best intro
- [Kubernetes Basics tutorial (k8s.io)](https://kubernetes.io/docs/tutorials/kubernetes-basics/) — interactive, 6 modules
- [`kubectl` cheatsheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/) — keep this open
- See [resources/kubectl-cheatsheet.md](../resources/kubectl-cheatsheet.md) for the commands we use most

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `error: You must be logged in` | OIDC token expired | Re-run `kubectl get pods` — it'll trigger browser login |
| `forbidden: User ... cannot create pods` | Wrong namespace | Add `-n <namespace>` to every command |
| Pod stuck in `Pending` | No nodes have capacity | `kubectl describe pod <name>` and look at Events |
| Pod in `ImagePullBackOff` | Image name typo or registry needs auth | Check spelling; try `kubectl describe pod` for details |
| Pod in `CrashLoopBackOff` | App crashes immediately | `kubectl logs <pod>` to see why |
| `port-forward` exits immediately | Pod isn't `Running` yet | Wait for `STATUS=Running`, then retry |

---

**Next:** [Week 4 — HPC Concepts + LLM API Deep Dive](week-04-hpc-and-llm-api.md)
