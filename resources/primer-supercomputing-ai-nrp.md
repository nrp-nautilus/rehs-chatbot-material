# Primer: Supercomputing, AI, and Why NRP Exists

> This is the readable companion to **Week 1, Call 2 ("The Big Picture")**. Skim it before the
> call, read it properly after. By the end you should be able to explain — to a friend who knows
> nothing — what SDSC is, why supercomputers matter, why AI made them matter *more*, and what the
> National Research Platform (NRP) and Kubernetes have to do with the chatbot you're about to build.

---

## 1. SDSC — the San Diego Supercomputer Center

SDSC opened in **1985** as one of the original U.S. national supercomputer centers, funded by the
National Science Foundation (NSF). It lives at UC San Diego. Its job, then and now: **run big
computers so that scientists everywhere can do research they couldn't do on their own machines.**

Over the decades SDSC has run a series of famous supercomputers (Comet, Expanse, Voyager, and
others). But SDSC isn't just "a room full of computers." It's a center for **cyberinfrastructure** —
the people, software, networks, and storage that make large-scale computing actually usable. (More
on that word in section 4.)

**The one-liner:** SDSC's mission is to make serious computing power available to researchers who
need it — and that mission is exactly why you have free access to a 120-billion-parameter language
model this summer.

---

## 2. What "supercomputing" (HPC) actually means

Your laptop has maybe 8–16 CPU cores and one modest GPU. A **supercomputer** (the field is called
**HPC — High-Performance Computing**) is what you get when you wire **thousands of computers
together** with a very fast network and treat them as one giant machine.

Why bother? Because some problems are simply too big for one computer:

- Simulating a hurricane, a galaxy, or how a protein folds
- Training or running a modern AI model
- Searching genomes, modeling earthquakes, designing new materials

These problems are solved by **splitting the work across many machines at once** (parallelism). A
job that would take your laptop 40 years can finish overnight on thousands of cores. That's the
whole point of HPC: **scale you can't get any other way.**

---

## 3. The AI compute crunch — why this all got urgent

Here's the shift that makes 2026 different from 2015.

Modern AI — the large language models (LLMs) you'll use this summer — are **enormous**. Training one
can take thousands of specialized **GPUs** (graphics processors, which turn out to be fantastic at
the math AI needs) running for weeks. Even just *running* a trained model to answer your questions
("inference") needs serious GPU power.

The result is a worldwide **scramble for compute**:

- GPUs are expensive and in short supply.
- A single researcher or a high school can't buy a cluster of them.
- Demand for AI compute is growing faster than anyone can build data centers.

This is the **AI compute crunch**. And it's exactly the kind of problem cyberinfrastructure exists
to solve: instead of everyone buying their own GPUs (most of which would sit idle), **pool them and
share them.** That idea — shared, pooled, research-grade computing — is what NRP is built on.

---

## 4. Cyberinfrastructure — the unglamorous thing that makes it all work

"**Cyberinfrastructure**" (often shortened to **CI**) is the boring-sounding word for the glue:
the compute, the storage, the high-speed networks, the software, and the people that, together, let
researchers actually *do* computing at scale.

Think of it like roads and power grids, but for science. You don't think about the electrical grid
when you charge your phone — you just plug in. Cyberinfrastructure aims to make computing feel the
same way: a researcher should be able to "plug in" to compute and storage without personally owning
or babysitting a data center.

**Why it matters to you:** the reason eight high schoolers can deploy a chatbot onto a real cluster
is that the cyberinfrastructure already exists. You're plugging into the grid, not building it.

---

## 5. The National Research Platform (NRP) and Nautilus

The **National Research Platform (NRP)** is a shared, nationwide cyberinfrastructure for research.
Its compute cluster is called **Nautilus**, and it's *distributed*: instead of one giant machine in
one building, Nautilus is **hundreds of machines and GPUs spread across many universities**, wired
together into one big shared pool.

A few things that make NRP special — and perfect for this program:

- **Distributed and shared.** Resources at many institutions, usable as one cluster. Idle GPUs at
  one university can serve a researcher at another.
- **Open to research and education.** It's not locked behind a corporate paywall. Students and
  researchers can get access.
- **It hosts LLMs for free** (within fair-use limits) at `ellm.nrp-nautilus.io` — the models you'll
  call all summer.
- **It runs on Kubernetes** (next section), which is how you'll deploy your own chatbot *onto* it.

**The story you'll tell at your final presentation:** your chatbot helps people use NRP — and it
*runs on* NRP. The thing that answers questions about the cluster lives on the cluster.

---

## 6. Kubernetes — how a thousand computers pretend to be one

If Nautilus is hundreds of machines, *something* has to decide where your program runs, restart it
if it crashes, and give it storage and a network address. That something is **Kubernetes** (often
written **K8s** — "K", then 8 letters, then "s").

### A little history (it's actually a good story)
Google spent years running everything — Search, Gmail, YouTube — on an internal system called
**Borg** that packed huge numbers of programs onto huge numbers of machines efficiently. In **2014**
Google released an open-source version of those ideas called **Kubernetes**. It became the
industry-standard way to run software across many machines, everywhere from startups to
supercomputers. NRP uses it to manage Nautilus.

### The mental model
You hand Kubernetes a **container** (your app, packaged with everything it needs to run — you'll
build one with Docker), and you describe *what you want*:

> "Run one copy of this chatbot, give it some storage that survives restarts, and put it at this web
> address."

Kubernetes figures out the *how*: which machine to run it on, restarting it if it dies, reconnecting
its storage, routing traffic to it. You declare the goal; it keeps reality matching the goal.

The vocabulary you'll meet (don't memorize now — you'll learn each by doing):

- **Pod** — the smallest unit; basically "your running container(s)"
- **Deployment** — "keep N copies of this pod alive"
- **Service** — a stable internal address for your pods
- **Ingress** — exposes your service to the public internet (your chatbot's URL)
- **PVC (PersistentVolumeClaim)** — storage that survives a pod restart (where your vector database
  will live)
- **Namespace** — your own walled-off area inside the shared cluster
- **`kubectl`** — the command-line tool you use to talk to Kubernetes

---

## 7. Putting it together — the summer in one picture

```
   SDSC's mission: make serious compute usable for research
                 │
                 ▼
   HPC / supercomputing: thousands of machines as one
                 │
        AI made compute scarce and precious (the "crunch")
                 │
                 ▼
   Cyberinfrastructure: pool + share compute, storage, network
                 │
                 ▼
   NRP / Nautilus: a national, distributed, shared research cluster
                 │   (and it hosts free LLMs + runs on Kubernetes)
                 ▼
   Kubernetes: schedules & heals your app across the cluster
                 │
                 ▼
   YOU: build a RAG chatbot, containerize it, deploy it onto NRP,
        and contribute it back to the community.
```

Every concept above is something you'll *touch with your hands* over the next 8 weeks. You're not
just learning what a supercomputer is — you're going to put a program on one and tell strangers the
URL.

---

## Go deeper (optional)

- [NRP documentation](https://nrp.ai/documentation/) — your real reference all summer
- [NRP available LLMs](https://nrp.ai/documentation/userdocs/ai/llm-managed/models/)
- [Kubernetes "what is Kubernetes"](https://kubernetes.io/docs/concepts/overview/) — official, surprisingly readable
- [Docker in 100 seconds (Fireship)](https://www.youtube.com/watch?v=Gjnup-PuquQ)
- [Kubernetes in 100 seconds (Fireship)](https://www.youtube.com/watch?v=PziYflu8cB8)
- [SDSC](https://www.sdsc.edu/) — who's behind all this
