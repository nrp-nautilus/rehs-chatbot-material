# Local Scratch

Source: https://nrp.ai/documentation/userdocs/storage/local

# Local Scratch

Most nodes in the cluster have local NVMe drives, which provide faster I/O than shared filesystems. These can be used for workloads that require very intensive I/O operations ( see recommendations and an example for running these ).

You can request an ephemeral volume to be attached to your pod as a fast scratch space. Note that any information stored in it will be destroyed after pod shutdown.

```
apiVersion: batch/v1
kind: Job
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: demo
        image: gitlab-registry.nrp-nautilus.io/prp/jupyter-stack/prp
        command:
        - "python"
        args:
        - "/home/my_script.py"
        - "--data=/mnt/data/..."
        volumeMounts:
        - name: data
          mountPath: /mnt/data
        resources:
          limits:
            memory: 8Gi
            cpu: "6"
            nvidia.com/gpu: "1"
            ephemeral-storage: 100Gi
          requests:
            memory: 4Gi
            cpu: "1"
            nvidia.com/gpu: "1"
            ephemeral-storage: 100Gi
      volumes:
      - name: data
        emptyDir: {}
      restartPolicy: Never
  backoffLimit: 5
```

Please note that in case a node starves on disk, ALL pods will be evicted from the node. If you set the request to be 50G, and limit is 100G, and you use 100G, it’s likely this will destroy the node, as scheduler will put your workload on a 50G node. So make sure your request is close to the limit you set.

Important: On Nautilus, pods that write more than 50Gi of ephemeral scratch data per container (for example, to an emptyDir local scratch volume) can be evicted. When you mount an emptyDir scratch volume and plan to use more than 50Gi, explicitly set resources.requests.ephemeral-storage (and optionally resources.limits.ephemeral-storage ) in the container spec to the scratch size you need, as shown in the examples above.
