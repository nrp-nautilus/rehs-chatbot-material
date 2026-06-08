# kubectl Cheatsheet

The commands you'll actually run all summer. Set `NS=<namespace>` once and stop typing it.

```bash
export NS=rehs-2026          # the cohort's ONE shared namespace (mentor posts the real name)
```

(Or permanently: `kubectl config set-context --current --namespace=$NS`)

---

## Looking at stuff (read-only — safe to run)

```bash
kubectl get pods -n $NS                                  # all pods
kubectl get pods -n $NS -o wide                          # + node, IP
kubectl get pods -n $NS --watch                          # live updates
kubectl get all -n $NS                                   # everything
kubectl get deploy,svc,ingress,pvc,secret,cm -n $NS      # the chatbot stack

kubectl describe pod <pod-name> -n $NS                   # detailed status + events
kubectl describe deployment chatbot -n $NS

kubectl logs <pod-name> -n $NS                           # last container logs
kubectl logs <pod-name> -n $NS -f                        # follow (tail -f)
kubectl logs <pod-name> -n $NS --previous                # logs from before crash
kubectl logs deploy/chatbot -n $NS                       # any pod from this deployment

kubectl get events -n $NS --sort-by=.lastTimestamp       # what just happened?

kubectl top pods -n $NS                                  # CPU/memory (if metrics-server)
```

---

## Inside a pod

```bash
kubectl exec -it <pod-name> -n $NS -- bash               # shell into it
kubectl exec <pod-name> -n $NS -- ls /app                # one-shot command
kubectl exec <pod-name> -n $NS -- env                    # see its env vars
kubectl exec <pod-name> -n $NS -- cat /app/chroma_db/...
```

---

## Port forwarding (test locally before public)

```bash
kubectl port-forward pod/<pod-name> 8501:8501 -n $NS         # pod
kubectl port-forward svc/chatbot 8501:80 -n $NS              # service
kubectl port-forward deploy/chatbot 8501:8501 -n $NS         # any pod from deploy
# Then visit http://localhost:8501
# Ctrl+C to stop
```

---

## Applying manifests

```bash
kubectl apply -f deploy/                                 # all files in deploy/
kubectl apply -f deploy/deployment.yaml                  # one file
kubectl apply -f deploy/ --dry-run=client                # validate without applying
kubectl diff -f deploy/                                  # what would change?
```

---

## Updating & rolling

```bash
kubectl rollout status deploy/chatbot -n $NS             # is the rollout done?
kubectl rollout restart deploy/chatbot -n $NS            # cycle the pod (re-read secrets)
kubectl rollout history deploy/chatbot -n $NS            # past releases
kubectl rollout undo deploy/chatbot -n $NS               # roll back one
kubectl rollout undo deploy/chatbot --to-revision=3 -n $NS
```

---

## Deleting (be careful — this is destructive)

```bash
kubectl delete pod <pod-name> -n $NS                     # K8s spawns a new one
kubectl delete -f deploy/deployment.yaml                 # remove deployment (+ all its pods)
kubectl delete -f deploy/                                # remove everything in deploy/
kubectl delete deploy chatbot -n $NS                     # remove a deployment by name
```

**Never** `kubectl delete namespace $NS` unless you mean it. That nukes everything.

---

## Secrets & configmaps

```bash
# Create a secret from a literal
kubectl create secret generic chatbot-llm-token \
  --from-literal=NRP_LLM_TOKEN=sk-xxxxx -n $NS

# Update a secret (delete + recreate)
kubectl delete secret chatbot-llm-token -n $NS
kubectl create secret generic chatbot-llm-token --from-literal=... -n $NS
kubectl rollout restart deploy/chatbot -n $NS        # so pod picks it up

# View secret (base64-encoded)
kubectl get secret chatbot-llm-token -n $NS -o yaml

# Decode a secret value
kubectl get secret chatbot-llm-token -n $NS -o jsonpath='{.data.NRP_LLM_TOKEN}' | base64 -d

# ConfigMap from a file
kubectl create configmap chatbot-config --from-env-file=.env.prod -n $NS
```

---

## Debugging recipes

### "My pod is stuck Pending"

```bash
kubectl describe pod <name> -n $NS | tail -30
# Look at Events. Common: "Insufficient cpu/memory/nvidia.com/gpu"
```

### "My pod is CrashLoopBackOff"

```bash
kubectl logs <name> -n $NS                        # current crash
kubectl logs <name> -n $NS --previous             # previous crash (usually what you want)
kubectl describe pod <name> -n $NS                # exit codes, restart count
```

### "My image won't pull"

```bash
kubectl describe pod <name> -n $NS
# Look for "ImagePullBackOff" → check image name spelling, registry auth
```

### "My pod is Running but the app doesn't respond"

```bash
kubectl logs <name> -n $NS -f                     # is the app even starting?
kubectl exec <name> -n $NS -- curl localhost:8501 # works from inside?
kubectl describe pod <name> -n $NS                # are probes failing?
```

### "The service has no endpoints"

```bash
kubectl get endpoints chatbot -n $NS              # if empty: selector doesn't match pod labels
kubectl get pods -n $NS --show-labels             # check pod labels
kubectl describe svc chatbot -n $NS               # check selector
```

### "Ingress doesn't work but port-forward does"

- Wrong `ingressClassName`? Check NRP docs.
- TLS cert pending? `kubectl describe ingress chatbot -n $NS` and look at events.
- Hostname not in DNS yet? Try again in 5 minutes.

---

## Watching the world

```bash
# Live pod status (top-style)
kubectl get pods -n $NS -w

# Multi-resource live
watch -n 2 'kubectl get pods,svc,ingress -n $NS'

# Recent events live
kubectl get events -n $NS --watch
```

---

## Useful aliases (add to your shell)

```bash
alias k='kubectl'
alias kn='kubectl -n $NS'
alias kp='kubectl get pods -n $NS'
alias kl='kubectl logs -n $NS -f'
alias kd='kubectl describe -n $NS'
alias kctx='kubectl config get-contexts'
```

---

## Common gotchas

| Gotcha | Fix |
|---|---|
| Forgot `-n $NS`, got "no resources found" | Add `-n $NS` or set default namespace |
| `kubectl apply -f X.yaml` errors but the apply succeeded | The "error" is often a warning — read carefully |
| `kubectl logs <name>` empty after pod restart | Use `--previous` for last run's logs |
| Edits to a Pod don't stick | Pods are immutable; edit the Deployment (which makes new pods) |
| `kubectl edit` opens vi and you can't escape | `:q!` to quit without saving; `Esc` then `:wq` to save |
| OIDC token expired mid-day | Just run any kubectl command — it triggers re-auth in browser |

---

## What `kubectl` actually does

Mental model: every kubectl command is just **HTTP to the Kubernetes API**. `kubectl get pods` is GET, `kubectl apply -f` is PUT, `kubectl delete` is DELETE. If you ever want to see the raw call: `kubectl get pods -v=8` prints the HTTP request.

That's it. kubectl is just a friendly curl.

---

## Read more

- [kubectl official cheatsheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [`k9s`](https://k9scli.io/) — TUI replacement for half of these commands
- [`stern`](https://github.com/stern/stern) — better multi-pod log tailing
