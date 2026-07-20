# Ray Cluster

Source: https://nrp.ai/documentation/userdocs/running/ray-cluster

# Ray Cluster

Ray is an open-source unified framework for scaling AI and Python applications like machine learning. It provides the compute layer for parallel processing so that you don’t need to be a distributed systems expert. To run Ray applications on multiple nodes, you must first deploy a Ray cluster. This document is adapted from the official guide of RayCluster Quickstart for deploying and using a Ray Cluster on Nautilus in your namespace.

:::caution Namespace All commands below use -n <namespace> . Replace <namespace> with your actual namespace (e.g. mfsada ). If you omit the namespace, kubectl may use your default. :::

- Prerequisites: add Helm repo and prepare values Add the KubeRay Helm repo and ensure you have a values file that sets required rayStartParams (the RayCluster CRD rejects empty values): Terminal window helm repo add kuberay https://ray-project.github.io/kuberay-helm/ helm repo update Create a values.yaml in your working directory with at least: head : rayStartParams : block : " true " dashboard-host : " 0.0.0.0 " worker : rayStartParams : block : " true "

Prerequisites: add Helm repo and prepare values

Add the KubeRay Helm repo and ensure you have a values file that sets required rayStartParams (the RayCluster CRD rejects empty values):

```
helm repo add kuberay https://ray-project.github.io/kuberay-helm/
helm repo update
```

Create a values.yaml in your working directory with at least:

```
head:
  rayStartParams:
    block: "true"
    dashboard-host: "0.0.0.0"
worker:
  rayStartParams:
    block: "true"
```

- Deploy a RayCluster custom resource Once the KubeRay operator is running, create a RayCluster Custom Resource (CR). You must pass the values file so head and worker have non-empty rayStartParams : Terminal window helm install raycluster kuberay/ray-cluster -n <namespace> -f values.yaml View the RayCluster CR (use the same namespace as the install): Terminal window kubectl get rayclusters -n <namespace> # NAME                 DESIRED WORKERS   AVAILABLE WORKERS   CPUS   MEMORY   GPUS   STATUS   AGE # raycluster-kuberay   1                                     2      3G       0               39s The KubeRay operator will detect the RayCluster object, then start your Ray cluster by creating head and worker pods. To view Ray cluster’s pods, run: Terminal window kubectl get pods --selector=ray.io/cluster=raycluster-kuberay -n <namespace> A raycluster-kuberay-head-... pod and a raycluster-kuberay-worker-... pod should be listed in the output: Terminal window # NAME                                          READY   STATUS    RESTARTS   AGE # raycluster-kuberay-head-txb7l                 1/1     Running   0          124m # raycluster-kuberay-worker-workergroup-w74gh   1/1     Running   0          124m

Deploy a RayCluster custom resource

Once the KubeRay operator is running, create a RayCluster Custom Resource (CR). You must pass the values file so head and worker have non-empty rayStartParams :

```
helm install raycluster kuberay/ray-cluster -n <namespace> -f values.yaml
```

View the RayCluster CR (use the same namespace as the install):

```
kubectl get rayclusters -n <namespace>
# NAME                 DESIRED WORKERS   AVAILABLE WORKERS   CPUS   MEMORY   GPUS   STATUS   AGE
# raycluster-kuberay   1                                     2      3G       0               39s
```

The KubeRay operator will detect the RayCluster object, then start your Ray cluster by creating head and worker pods. To view Ray cluster’s pods, run:

```
kubectl get pods --selector=ray.io/cluster=raycluster-kuberay -n <namespace>
```

A raycluster-kuberay-head-... pod and a raycluster-kuberay-worker-... pod should be listed in the output:

```
# NAME                                          READY   STATUS    RESTARTS   AGE
# raycluster-kuberay-head-txb7l                 1/1     Running   0          124m
# raycluster-kuberay-worker-workergroup-w74gh   1/1     Running   0          124m
```

- Run an application on a RayCluster Once the RayCluster has been deployed, users in the namespace can run Ray jobs. The most straightforward way is to exec directly into the head pod. Identify the RayCluster’s head pod (include -n <namespace> or the selector returns nothing): Terminal window export HEAD_POD = $( kubectl get pods --selector=ray.io/node-type=head -o custom-columns=POD:metadata.name --no-headers -n <namespace> ) echo $HEAD_POD # raycluster-kuberay-head-txb7l Execute a Ray job to print the cluster resources. Use -n <namespace> before -- ; putting the namespace after -- can cause “pod not found”: Terminal window kubectl exec -it $HEAD_POD -n <namespace> -- python -c " import ray; ray.init(); print(ray.cluster_resources()) " # 2026-03-07 19:33:00,053 INFO worker.py:1554 -- Using address 127.0.0.1:6379 set in the environment variable RAY_ADDRESS # 2026-03-07 19:33:00,053 INFO worker.py:1694 -- Connecting to existing Ray cluster at address: 10.244.118.7:6379... # 2026-03-07 19:33:00,072 INFO worker.py:1879 -- Connected to Ray cluster. View the dashboard at 10.244.118.7:8265 # {'CPU': 2.0, 'memory': 3000000000.0, 'object_store_memory': 469440921.0, 'node:10.244.118.2': 1.0, 'node:10.244.118.7': 1.0, 'node:__internal_head__': 1.0} You may also submit a Ray job to the RayCluster via ray job submission SDK. For more information, please refer to https://docs.ray.io/en/latest/cluster/kubernetes/getting-started/raycluster-quick-start.html#method-2-submit-a-ray-job-to-the-raycluster-via-ray-job-submission-sdk

Run an application on a RayCluster

Once the RayCluster has been deployed, users in the namespace can run Ray jobs. The most straightforward way is to exec directly into the head pod.

Identify the RayCluster’s head pod (include -n <namespace> or the selector returns nothing):

```
export HEAD_POD=$(kubectl get pods --selector=ray.io/node-type=head -o custom-columns=POD:metadata.name --no-headers -n <namespace>)
echo $HEAD_POD
# raycluster-kuberay-head-txb7l
```

Execute a Ray job to print the cluster resources. Use -n <namespace> before -- ; putting the namespace after -- can cause “pod not found”:

```
kubectl exec -it $HEAD_POD -n <namespace> -- python -c "import ray; ray.init(); print(ray.cluster_resources())"
# 2026-03-07 19:33:00,053 INFO worker.py:1554 -- Using address 127.0.0.1:6379 set in the environment variable RAY_ADDRESS
# 2026-03-07 19:33:00,053 INFO worker.py:1694 -- Connecting to existing Ray cluster at address: 10.244.118.7:6379...
# 2026-03-07 19:33:00,072 INFO worker.py:1879 -- Connected to Ray cluster. View the dashboard at 10.244.118.7:8265
# {'CPU': 2.0, 'memory': 3000000000.0, 'object_store_memory': 469440921.0, 'node:10.244.118.2': 1.0, 'node:10.244.118.7': 1.0, 'node:__internal_head__': 1.0}
```

You may also submit a Ray job to the RayCluster via ray job submission SDK. For more information, please refer to https://docs.ray.io/en/latest/cluster/kubernetes/getting-started/raycluster-quick-start.html#method-2-submit-a-ray-job-to-the-raycluster-via-ray-job-submission-sdk

- Access the Ray Dashboard Execute this command to create a tunnel (include -n <namespace> ): Terminal window kubectl port-forward service/raycluster-kuberay-head-svc 8265:8265 -n <namespace> Visit http://127.0.0.1:8265 in your browser for the Dashboard.

Access the Ray Dashboard

Execute this command to create a tunnel (include -n <namespace> ):

```
kubectl port-forward service/raycluster-kuberay-head-svc 8265:8265 -n <namespace>
```

Visit http://127.0.0.1:8265 in your browser for the Dashboard.

- Cleanup When the RayCluster is not needed anymore, uninstall the Helm release in the same namespace: Terminal window helm uninstall raycluster -n <namespace> # release "raycluster" uninstalled It might take several seconds for the RayCluster’s pods to terminate. Confirm that the pods are gone by running: Terminal window kubectl get pods -n <namespace>

Cleanup

When the RayCluster is not needed anymore, uninstall the Helm release in the same namespace:

```
helm uninstall raycluster -n <namespace>
# release "raycluster" uninstalled
```

It might take several seconds for the RayCluster’s pods to terminate. Confirm that the pods are gone by running:

```
kubectl get pods -n <namespace>
```
