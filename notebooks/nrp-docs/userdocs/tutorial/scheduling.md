# Scheduling Workloads in Nautilus

Source: https://nrp.ai/documentation/userdocs/tutorial/scheduling

# Scheduling Workloads in Nautilus

# Scheduling

In Kubernetes, scheduling refers to the process of assigning pods to nodes in a cluster based on various factors such as resource requirements, node capacity, and other constraints. The Kubernetes scheduler is responsible for determining where and how to run pods within the cluster.

❗ While you can run jobs without any special node selectors, understanding this section will allow you to better optimize the placement of your workloads and significantly increase computational performance. You can request more performant CPUs, GPUs with more memory, faster network links, and even select nodes in a specific geographical region to optimize latency to your storage.

## Prerequisites

This section builds on skills from both the Quickstart and the tutorial on Basic Kubernetes .

## Learning Objectives

- You will learn how to query the cluster to view high-level node availability in real time.

- You will understand how node capabilities (e.g. GPU type, network speed, geography) are exposed through labels.

- You will learn how to target specific node features without requiring direct access to individual nodes.

- You will be able to enforce or prefer node types and resource requirements within a pod yaml file.

## Explore the system

Let’s start by looking at what’s available in the system. You have already seen the list of all nodes:

```
kubectl get nodes
```

This is a very long list — and growing. While you can see basic node information, Nautilus intentionally limits direct access to detailed node configuration.

⚠️ Note on permissions

Nautilus users have list-only access to nodes.

- ✅ kubectl get nodes

- ✅ kubectl get nodes -L

- ✅ kubectl get node -l

- ❌ kubectl get node

- ❌ kubectl describe node

- ❌ kubectl get nodes -o yaml

All user-relevant scheduling information is exposed through node labels, which are safe to query and can be used directly in pod scheduling.

### Viewing node capabilities with labels

You may view the full labels of a node through the following (change <NODE_HOST> to the hostname of the node you are concerned with, e.g., node-1-1.sdsc.optiputer.net ):

```
kubectl get nodes --field-selector 'metadata.name=<NODE_HOST>' -o go-template='{{range $k, $v := (index .items 0).metadata.labels}}{{$k}}={{$v}}{{println}}{{end}}'
```

Examples of commonly usable labels (not exhaustive and variable):

```
cpu-feature.node.kubevirt.io/adx=true
cpu-feature.node.kubevirt.io/aes=true
cpu-feature.node.kubevirt.io/avx=true
cpu-feature.node.kubevirt.io/avx2=true
cpu-feature.node.kubevirt.io/fma=true
cpu-feature.node.kubevirt.io/sse=true
cpu-feature.node.kubevirt.io/sse2=true
cpu-feature.node.kubevirt.io/sse4.1=true
cpu-feature.node.kubevirt.io/sse4.2=true
cpu-feature.node.kubevirt.io/ssse3=true
cpu-model.node.kubevirt.io/Broadwell=true
cpu-model.node.kubevirt.io/Haswell=true
cpu-vendor.node.kubevirt.io/Intel=true
kubernetes.io/arch=amd64
kubernetes.io/hostname=dtn-gpu2.kreonet.net
kubernetes.io/os=linux
mtu=9000
nautilus.io/network=40000
netbox.io/site=kreonet
nvidia.com/cuda.driver-version.full=580.126.09
nvidia.com/cuda.driver-version.major=580
nvidia.com/cuda.driver-version.minor=126
nvidia.com/cuda.driver-version.revision=09
nvidia.com/cuda.driver.major=580
nvidia.com/cuda.driver.minor=126
nvidia.com/cuda.driver.rev=09
nvidia.com/cuda.runtime-version.full=13.0
nvidia.com/cuda.runtime-version.major=13
nvidia.com/cuda.runtime-version.minor=0
nvidia.com/cuda.runtime.major=13
nvidia.com/cuda.runtime.minor=0
nvidia.com/gpu.compute.major=6
nvidia.com/gpu.compute.minor=1
nvidia.com/gpu.count=5
nvidia.com/gpu.family=pascal
nvidia.com/gpu.memory=12288
nvidia.com/gpu.present=true
nvidia.com/gpu.product=NVIDIA-TITAN-Xp
topology.kubernetes.io/region=pacific
topology.kubernetes.io/zone=korea
```

Below, you can list nodes that have a certain type of node capabilities.

For example, you can see which nodes provide which GPU types:

```
kubectl get nodes -L nvidia.com/gpu.product
```

This shows a cluster-wide view of GPU availability without inspecting any individual node.

You can also view other commonly useful labels, such as network speed:

```
kubectl get node -l 'nautilus.io/network=100000'
```

Or combine selectors and label output:

```
kubectl get node -l 'nvidia.com/gpu.product!=NVIDIA-GeForce-GTX-1080' -L nvidia.com/gpu.product
```

❗ Many of these queries are also available through the Nautilus portal. You can visit the Resources page to view a live table of nodes and their features.

## Validating requirements

Before adding scheduling constraints to your pod yaml , it’s good practice to verify that the requested resources exist somewhere in the cluster.

For example, to check whether a specific GPU type is available:

```
kubectl get node -l 'nvidia.com/gpu.product=NVIDIA-GeForce-RTX-3090'
```

❓ Did you get any results?

Here we check for nodes with 100 Gbps networking:

```
kubectl get node -l 'nautilus.io/network=100000'
```

❓ Did you get any results?

💡 Even though you cannot inspect nodes directly, the scheduler has full visibility and will match your pod requirements against all eligible nodes automatically.

## Requirements in pods

You have already used resource requirements in pods. Here is a simple example:

```
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
  - name: mypod
    image: rocker/cuda
    resources:
      limits:
        memory: 100Mi
        cpu: 100m
      requests:
        memory: 100Mi
        cpu: 100m
    command: ["sh", "-c", "sleep infinity"]
```

The resource requests and limits are intentionally small, making it very likely that the pod will start.

### Requesting a GPU

Now let’s add a GPU requirement.

❗ Note: You cannot request a fraction of a GPU. Requests and limits must match.

```
apiVersion: v1
kind: Pod
metadata:
  name: test-gpupod
spec:
  containers:
  - name: mypod
    image: rocker/cuda
    resources:
      limits:
        memory: 100Mi
        cpu: 100m
        nvidia.com/gpu: 1
      requests:
        memory: 100Mi
        cpu: 100m
        nvidia.com/gpu: 1
    command: ["sh", "-c", "sleep infinity"]
```

Once the pod starts, log into it and verify the GPU:

```
kubectl exec test-gpupod -it -- /bin/bash
```

Inside the container, run:

```
nvidia-smi
```

❗ Remember to delete old pods when you are done.

## Requesting a specific GPU type

To require a specific GPU model, use nodeAffinity:

```
apiVersion: v1
kind: Pod
metadata:
  name: test-gpupod
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: nvidia.com/gpu.product
            operator: In
            values:
            - NVIDIA-GeForce-RTX-3090
  containers:
  - name: mypod
    image: rocker/cuda
    resources:
      limits:
        memory: 100Mi
        cpu: 100m
        nvidia.com/gpu: 1
      requests:
        memory: 100Mi
        cpu: 100m
        nvidia.com/gpu: 1
    command: ["sh", "-c", "sleep infinity"]
```

If the pod starts successfully, confirm the GPU type using nvidia-smi.

## Preferences in pods

Sometimes you would prefer a resource but do not want to require it. This can be expressed using preferredDuringSchedulingIgnoredDuringExecution:

```
apiVersion: v1
kind: Pod
metadata:
  name: test-gpupod
spec:
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: nvidia.com/gpu.product
            operator: In
            values:
            - NVIDIA-GeForce-RTX-2080-Ti
            - Tesla-V100-SXM2-32GB
  containers:
  - name: mypod
    image: rocker/cuda
    resources:
      limits:
        memory: 100Mi
        cpu: 100m
        nvidia.com/gpu: 1
      requests:
        memory: 100Mi
        cpu: 100m
        nvidia.com/gpu: 1
    command: ["sh", "-c", "sleep infinity"]
```

Check where the pod landed and which GPU you received.

## Using geographical topology

Nautilus nodes are distributed globally. You can select nodes closer to your data or collaborators using topology labels.

View available regions and zones:

```
kubectl get nodes -L topology.kubernetes.io/zone,topology.kubernetes.io/region
```

Run a pod in Korea:

```
apiVersion: v1
kind: Pod
metadata:
  name: test-geo
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: topology.kubernetes.io/zone
            operator: In
            values:
            - korea
  containers:
  - name: mypod
    image: alpine
    resources:
      limits:
        memory: 100Mi
        cpu: 100m
      requests:
        memory: 100Mi
        cpu: 100m
    command:
    - sh
    - -c
    - |
      apk add curl;
      curl ipinfo.io
```

Check the logs:

```
kubectl logs test-geo
```

## Optional: Reserved nodes and taints

Some nodes are restricted and require explicit tolerations. You can view node taints at: https://nrp.ai/viz/resources/ .

If a pod cannot be scheduled, inspect events:

```
kubectl get events --sort-by=.metadata.creationTimestamp
```

You may see a NoSchedule taint. To tolerate it:

```
tolerations:
- key: nautilus.io/reservations
  operator: Equals
  value: "name"
  effect: NoSchedule
```
