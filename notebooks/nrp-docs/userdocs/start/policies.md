# Cluster Policies

Source: https://nrp.ai/documentation/userdocs/start/policies

# Cluster Policies

### Acceptable Use Policy

Read the NRP Acceptable Use Policy (AUP) .

### Resource allocation

- Set the resource (particularly CPU, memory and ephemeral-storage) limits properly. Your resource limits must be within 20% of the resource requests .

Set the resource (particularly CPU, memory and ephemeral-storage) limits properly. Your resource limits must be within 20% of the resource requests .

- While running a large number (> ~100) of pods or jobs, you must choose your resource limit = request .

While running a large number (> ~100) of pods or jobs, you must choose your resource limit = request .

- If a pod goes over its memory limit, it will be killed (OOM - Out of Memory).

If a pod goes over its memory limit, it will be killed (OOM - Out of Memory).

- If a pod exceeds the CPU limit, it puts pressure on the node. It can affect the whole node and other use’s work.

If a pod exceeds the CPU limit, it puts pressure on the node. It can affect the whole node and other use’s work.

- Do not waste resources. Namespaces with consistently underutilized requests risk being banned.

Do not waste resources. Namespaces with consistently underutilized requests risk being banned.

### Resource usage violations

- A user can not submit more than 4 pods , violating the following conditions: GPU utilization is more than 40% of the requested GPUs. CPU usage is within 20-200% of the requested CPUs. Memory (RAM) usage is within 20-150% of the requested memory.

- GPU utilization is more than 40% of the requested GPUs.

- CPU usage is within 20-200% of the requested CPUs.

- Memory (RAM) usage is within 20-150% of the requested memory.

- These restrictions do not apply to pods requesting 1 CPU core and 2GB memory .

- Keep checking the Violations page on the Nautilus portal to see if your pods are violating the usage policies.

### Interactive use (6 hours max runtime)

- Pods do not stop on their own under normal conditions and won’t recover if a node fails. Because of this, we assume any pod running without a controller is interactive , meaning it’s used temporarily for development or debugging.

- Time limit: such pods will be destroyed in 6 hours unless you request an exception for your namespace (in case you run JupyterHub or some other application controlling the pods for you).

- Resource limits: interactive pods are limited to 2 GPUs, 32 GB RAM, and 16 CPU cores.

- It is okay to run sleep in an interactive pod.

### Batch jobs

- Use Job to run batch jobs and set resources carefully. You can use Guaranteed QoS for those.

- You can use Guaranteed QoS for those.

- While running a large number (> ~100) of jobs, you must choose your resource limit = request .

- Using sleep infinity in Jobs is not allowed. Users running a Job with sleep infinity command or equivalent (script ending with “sleep”) will be banned from using the cluster.

### Long-running idle pods

If you need some pods to run idle for a long time, you can use the Deployment controller .

- Use Deployment if you need a long-running pod .

- Make sure you set minimal requests and proper limits for those to get the Burstable QoS .

- Such a deployment can not request a GPU.

- Deployments are automatically deleted after 2 weeks (unless the namespace is added to the exceptions list and runs a permanent service).

### Workloads purging (2 weeks max runtime)

- A periodic process removes workloads (deployments) older than 2 weeks to free up resources and maintain system efficiency.

- If you need to run some permanent services beyond two weeks, contact admins in Nautilus Support and ask for an exception. Please provide an estimated period of service functioning and a brief description of what the service does.

- Long idle pods can’t be added to the exceptions list, since those are considered temporary and we need to be sure those are cleaned when not needed.

- You will receive 3 notifications if your workload is not on the exception list. After that, your workload will be deleted. Any data in persistent volumes will remain.

### Requesting GPUs

- When you request GPUs for your pod , nobody else can use those until you stop your pod. You should only schedule GPUs that you can actually use.

- Check the GPU dashboard for your namespace to make sure the utilization is above 40%, and ideally is close to 100%.

- The only reason to request more than a single GPU is when your GPU utilization is close to 100% and you can leverage using more GPUs.

- GPUs are a limited resource shared by many users. If you plan on deploying large jobs (>50 GPUs) please present a plan in Nautilus Support .

### Data purging

- Please purge any data you do not need. You should clean up your storage at regular intervals.

- NRP resources should not be used as archival storage. You can only store the data actively used for computations.

- Any volume that was not accessed for 6 months can be purged without notification .
