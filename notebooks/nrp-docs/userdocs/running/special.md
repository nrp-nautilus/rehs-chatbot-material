# Special Use

Source: https://nrp.ai/documentation/userdocs/running/special

# Special Use

Our cluster combines various hardware resources from multiple universities and other organizations.

#### All Taints

Please use caution when applying tolerations and only tolerate taints for which you have explicit authorization from cluster administrators. Tolerating the wrong taints may cause your workloads to land on unintended or restricted nodes, leading to failures or policy violations.

Here is the taint system and their descriptions. To run on a node with a taint, you need to use the node toleration in your pod . Users may only tolerate values they are authorized for by cluster admins .

Observable notebook with taints summary

#### Reservations

Groups may request exclusive access to entire nodes if their workloads justify it. Such nodes can be reserved by setting the following taint and corresponding toleration :

```
spec:
  tolerations:
  - key: "nautilus.io/reservation"
    operator: "Equal"
    value: "group1"
    effect: "NoSchedule"
```

Please fill out the node reservation form if your group has a use case that would benefit from whole-node reservations.

In addition, our cluster contains several sets of nodes dedicated to certain groups.

Users can target ONLY THE GROUP NODES by using affinity , for example:

```
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: nautilus.io/reservation
            operator: In
            values:
            - group1
```

For large jobs, this helps avoid consuming all shared cluster resources. Optionally, a higher priority can be used (contact the admins before using one).

#### Other taints

Some nodes in the cluster don’t have access to public Internet, and can only access educational network. They still can pull images from Docker Hub using a proxy.

If your workload is not using the public Internet resources, you might tolerate the nautilus.io/science-dmz and get access to additional nodes.
