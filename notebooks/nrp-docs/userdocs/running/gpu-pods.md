# GPU Pods

Source: https://nrp.ai/documentation/userdocs/running/gpu-pods

# GPU Pods

## Running GPU pods

Use this definition to create your own pod and deploy it to kubernetes:

```
apiVersion: v1
kind: Pod
metadata:
  name: gpu-pod-example
spec:
  containers:
  - name: gpu-container
    image: tensorflow/tensorflow:latest-gpu
    command: ["sleep", "infinity"]
    resources:
      limits:
        nvidia.com/gpu: 1
      requests:
        nvidia.com/gpu: 1
```

This example requests 1 GPU device. You can have up to 8 per node if you’re using jobs , and up to 2 for pods. If you request GPU devices in your pod, kubernetes will auto schedule your pod to the appropriate node. There’s no need to specify the location manually.

## Requesting special GPUs

Certain kinds of GPUs are advertised on nodes as a special resource, f.e. “nvidia.com/rtx-8000”. You have to request that resource instead of the “nvidia.com/gpu” one.

The current list is:

Note: NVIDIA RTX PRO 6000 Blackwell nodes are reserved for exclusive use and are not generally available at this time.

For example, modifying the above example for one of these GPUs, the new yaml would be:

```
apiVersion: v1
kind: Pod
metadata:
  name: gpu-pod-example
spec:
  containers:
  - name: gpu-container
    image: tensorflow/tensorflow:latest-gpu
    command: ["sleep", "infinity"]
    resources:
      limits:
        nvidia.com/a100: 1
      requests:
        nvidia.com/a100: 1
```

For Grace Hopper node make sure you’re also using the image with arm support ( nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04 is a good one) and tolerating the arm64 architecture :

```
tolerations:
- key: "nautilus.io/arm64"
  operator: "Exists"
  effect: "NoSchedule"
```

For RTX PRO 6000 Blackwell nodes, request the dedicated resource:

```
resources:
  limits:
    nvidia.com/rtx6000bw: 1
  requests:
    nvidia.com/rtx6000bw: 1
```

## Requesting many GPUs

Since 1 and 2 GPU jobs are blocking nodes from getting 4 and 8-GPU jobs, there are some nodes reserved for those. Once you submit a job with 4 or 8 GPUs request, a controller will automatically add toleration which will allow you to use the node reserved for more GPUs. You don’t need to do anything manually for that.

## Choosing GPU type

See requesting special GPUs for special types of GPU

We have a variety of GPU flavors attached to Nautilus. This table describes the types of GPUs available for use, but is not up to date - it’s better to use the actual cluster information (f.e. kubectl get nodes -L nvidia.com/gpu.product ).

Credit: GPU types by NRP Nautilus

If you need more graphical memory, use this table or official specs to choose the type:

To use a specific type of GPU , add the affinity definition to you pod yaml file. The example below specifies 1080Ti GPU:

```
spec:
 affinity:
   nodeAffinity:
     requiredDuringSchedulingIgnoredDuringExecution:
       nodeSelectorTerms:
       - matchExpressions:
         - key: nvidia.com/gpu.product
           operator: In
           values:
           - NVIDIA-GeForce-GTX-1080-Ti
```

To make sure you did everything correctly after you’ve submited the job, look at the corresponding pod yaml ( kubectl get pod ... -o yaml ) and check that resulting nodeAffinity is as expected.

## Selecting CUDA version

In general the higher CUDA versions support the lower and same driver version. The nodes are labelled with the major and minor CUDA and driver versions. You can check those at the resources page or list with this command (it will also choose only GPU nodes):

```
kubectl get nodes -L nvidia.com/cuda.driver.major,nvidia.com/cuda.driver.minor,nvidia.com/cuda.runtime.major,nvidia.com/cuda.runtime.minor -l nvidia.com/gpu.product
```

If you’re using the container image with higher CUDA version, you have to pick the nodes supporting it. Example:

```
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: nvidia.com/cuda.runtime.major
            operator: In
            values:
            - "12"
          - key: nvidia.com/cuda.runtime.minor
            operator: In
            values:
            - "2"
```

Also you can choose the driver above something if you know which one you need (this will pick drivers above 535):

```
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: nvidia.com/cuda.driver.major
            operator: Gt
            values:
            - "535"
```

## Adding Shared Memory (shm)
