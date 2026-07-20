# Using Nautilus

Source: https://nrp.ai/documentation/userdocs/start/using-nautilus

# Using Nautilus

NRP Nautilus is a Kubernetes cluster distributed all over the US and there are a few sites in Asia and Europe. Currently there are over 75 sites as part of the NRP. See all the sites on the NRP dashboard .

## How to use the cluster

There are three main ways to use the computing resources on the NRP Nautilus cluster.

- NRP-hosted JupyterHub platform

- NRP-hoster Coder platform

- Interfacing with Kubernetes using the kubectl tool

- Using the managed cluster services

We will discuss these options below.

### JupyterHub Platform

JupyterHub is arguably the most user-friendly way to interact with the NRP Nautilus cluster. It allows you to run Jupyter notebooks in a web browser, without having to worry about the underlying infrastructure. You can access the NRP-hosted JupyterHub platform by visiting the JupyterHub link and logging in with your institutional credentials. Once authenticated, you can choose the hardware specs to spawn your instance and run Jupyter notebooks as usual.

### Coder Platform

Coder provides an easy-to-use, JupyterHub-like experience, and you can use the NRP Nautilus cluster without Kubernetes knowledge. Coder also runs on the web browser. You can run your code without worrying about the underlying infrastructure. You can access the NRP-hosted Coder platform by visiting the Coder link and logging in with your institutional credentials using OpenID Connect (once the cluster admins approve your account).

### Kubernetes

This method provides greater control over your computing resources but requires basic Kubernetes knowledge. You can create pods, jobs, and deployments while specifying the required CPU, GPU, memory, and other resources. This is particularly useful for running custom software stacks or jobs with specific resource requirements.

## Kubernetes concepts

This section highlights some of the Kubernetes concepts that are essential to start using the Nautilus cluster. You can learn more about these components in the tutorial sections . If you are new to Kubernetes and like to learn about the Kubernetes concepts in detail, please follow the Concepts page from Kubernetes Documentation .

### Namespace

One of the main concepts of running workloads in Kubernetes is a namespace. A namespace creates an isolated environment in which you can run your pods. It is possible to invite other users to your namespace and it is possible to have access to multiple namespaces. Each namespace has at least one namespace admin (usually researchers, engineers, or faculties). If you are new to the cluster, please follow the instructions on the Getting Started page.

### Container images

A container image is a lightweight, standalone, and executable software package containing everything needed to run a piece of software: the code, runtime, libraries, dependencies, and default values for any essential settings. Images are typically stored in container registries (e.g., Docker Hub, GitLab Container Registry) and can be pulled by Kubernetes nodes when running your code.

### Pod, Job and Deployment

A Kubernetes pod is the smallest and most basic deployable unit in Kubernetes, representing a single instance of a running process. A pod can contain one or more tightly coupled containers that share the same network and storage. If you frequently deploy single-container pods, you can generally replace the word “pod” with “container.”

A Kubernetes job is a resource used to run short-lived, batch, or parallel processing tasks to completion. It creates one or more pods and retries execution until the specified number of successful completions is reached. It tracks completed pods and terminates once the specified number of successes is achieved. Deleting a job will clean up all the jobs it created.

A Kubernetes deployment manages the lifecycle of application workloads by ensuring the desired number of pod replicas are running and up to date. It supports rolling updates, rollbacks, and scaling to maintain application availability. Deployments automatically replace failed or outdated pods, making them ideal for managing stateless applications in a cluster.

### Resource allocation

For all the abovementioned Kubernetes objects (pods, jobs, deployments, etc) you need to ask for computing resources like (CPU, GPU, memory) before creating the objects.

- A request is the minimum amount of CPU, GPU, or memory that Kubernetes guarantees to a container. Kubernetes scheduler reserves this amount of resources to schedule a pod.

- A limit is the maximum amount of CPU or memory that a container is allowed to use.

### Storage

A Kubernetes storage provides a way to persist and manage data for containerized applications. It supports various storage options, including temporary storage (emptyDir), and persistent storage (PersistentVolumes). On Nautilus, you will be using both temporary ( ephemeral-storage ) and persistent storage for your work.

A pod can access the requested ephemeral-storage from the local disks of the node. Users need to create their own PersistentVolumeClaim (PVC) under their namespace.

Important: On Nautilus, pods that write more than 50Gi of ephemeral scratch data per container (for example, to an emptyDir ) can be evicted. If you attach an emptyDir scratch volume and expect to write more than 50Gi, set resources.requests.ephemeral-storage (and optionally resources.limits.ephemeral-storage ) in your pod spec to the size you need. See the Storage tutorial and Local Scratch pages for complete YAML examples that show both emptyDir and ephemeral-storage configured together.

### System load

While you are welcome to use as many resources as needed, using those inefficiently causes problems for others. The CPU load of the system consists of user load, system load, and several others. If you run top , you’ll see something like:

```
%Cpu(s): 26.9 us,  1.5 sy,  0.0 ni, 71.5 id,  0.0 wa,  0.0 hi,  0.1 si,  0.0 st
```

This means 26.9% of all system CPU time is spent on user tasks (computing), 1.5% on system stuff (kernel tasks), 71.5 idle, and so on. If the system (kernel) load is more than ~15%, it indicates a problem with the user’s code. Usually, it is caused by too many threads (the system is spending too much time just switching between those), inefficient file I/O (lots of small files processed by too many workers), or something similar. In this case, the system time is wasted not on processing.

If you were told your pod is causing too much load, look at your code and try to figure out why it is spending too much kernel time instead of computations.
