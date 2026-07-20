# ClickHouse Cluster

Source: https://nrp.ai/documentation/userdocs/running/clickhouse

# ClickHouse Cluster

### Using the Altinity ClickHouse Operator in Kubernetes

This guide explains how to deploy a ClickHouse cluster on NRP using the Altinity ClickHouse Operator . A single cluster-wide operator reconciles ClickHouseInstallation resources in every namespace — you don’t deploy your own.

### 1. Deploying a ClickHouse Cluster

Create a ClickHouseInstallation (CHI) custom resource. The simplest case is a single-replica cluster:

#### Example: clickhouse-cluster.yaml

```
apiVersion: "clickhouse.altinity.com/v1"
kind: "ClickHouseInstallation"
metadata:
  name: "my-clickhouse"
spec:
  configuration:
    users:
      # Use a sha256 of your password. Generate with:
      #   echo -n 'mypassword' | sha256sum
      myapp/password_sha256_hex: "REPLACE_ME"
      myapp/networks/ip:
        - "::/0"
      myapp/profile: "default"
      myapp/quota: "default"
    clusters:
      - name: "main"
        layout:
          shardsCount: 1
          replicasCount: 1
  defaults:
    templates:
      dataVolumeClaimTemplate: data-volume
  templates:
    volumeClaimTemplates:
      - name: data-volume
        spec:
          accessModes: [ReadWriteOnce]
          resources:
            requests:
              storage: 20Gi
          storageClassName: linstor-ha
```

Apply it:

```
kubectl apply -n default -f clickhouse-cluster.yaml
```

Replace default with your namespace. Any namespace works — the operator watches the whole cluster.

The operator creates a StatefulSet, ConfigMaps, Services, and a PersistentVolumeClaim. The CHI status field moves from InProgress to Completed :

```
kubectl get chi
NAME            STATUS      CLUSTERS   HOSTS   AGE
my-clickhouse   Completed   1          1       2m
```

### 2. Accessing the ClickHouse Cluster

Two services are created automatically:

- Cluster Service : clickhouse-my-clickhouse.default.svc.cluster.local (load-balanced across replicas)

- Per-pod Service : chi-my-clickhouse-main-0-0.default.svc.cluster.local

ClickHouse listens on:

- 9000/TCP — native protocol (use with clickhouse-client )

- 8123/TCP — HTTP protocol (use with curl , JDBC, drivers)

Quick test:

```
kubectl run -i --tty --rm ch-client --image=clickhouse/clickhouse-server:25.5.6 -- \
  clickhouse-client --host=clickhouse-my-clickhouse --user=myapp --password='REPLACE_ME' \
  --query "SELECT version()"
```

### 3. Scaling and Sharding

To add a replica, increase replicasCount :

```
clusters:
  - name: "main"
    layout:
      shardsCount: 1
      replicasCount: 2
```

For sharded analytics across multiple nodes, use multiple shards. You must also deploy ClickHouse Keeper or ZooKeeper (the CHI spec needs a configuration.zookeeper block); replicated tables require coordination. See the Altinity sharding docs for the full pattern.

```
clusters:
  - name: "main"
    layout:
      shardsCount: 3
      replicasCount: 2
```

Apply the changes; the operator will reconcile in place.

### 4. Choosing the storage class

Your data PVC’s storage class determines which nodes can mount it. Pick based on whether your CHI spans regions or zones:

Refer to the linstor storage docs for details.

### 5. Backups

Two patterns are in production use on NRP:

Sidecar with HTTP API (preferred for ongoing scheduled backups):

```
spec:
  templates:
    podTemplates:
      - name: pod-template
        spec:
          containers:
            - name: clickhouse
              # main CH container — operator manages
            - name: clickhouse-backup
              image: altinity/clickhouse-backup:2.6.10
              ports:
                - containerPort: 7171
              volumeMounts:
                - { name: clickhouse-data, mountPath: /var/lib/clickhouse }
                - { name: backups, mountPath: /backups }
          volumes:
            - name: backups
              persistentVolumeClaim:
                claimName: clickhouse-backups
```

Then trigger backups via the HTTP API (a CronJob is the usual driver):

```
curl -X POST http://chi-my-clickhouse-main-0-0:7171/backup/create?name=backup-$(date -u +%Y%m%d)
```

Logical SQL dump (good for one-off, portable backups):

Use a Job that runs clickhouse-client --query 'SELECT * FROM <db>.<table> FORMAT Native' per table, gzips, and writes to a separate clickhouse-backup PVC. See kubectl get cronjob backup-clickhouse -n clickhouse for a working example.

### 6. Monitoring

Operator-aggregated metrics ( chi_clickhouse_* series, per-CHI) are scraped automatically by the shared NRP Prometheus and visible in Grafana under the ClickHouse Operator and ClickHouse Server dashboards. No tenant-side ServiceMonitor needed.

If you want CH-server-internal metrics ( ClickHouseAsyncMetrics_* , ClickHouseMetrics_* ), enable the Prometheus endpoint in your CHI spec:

```
spec:
  configuration:
    settings:
      prometheus/endpoint: "/metrics"
      prometheus/port: 9363
```

CHI status:

```
kubectl get chi my-clickhouse -o jsonpath='{.status.status}'
```

### 7. Common pitfalls

- distributed_ddl_task_timeout setting : this is a profile setting (must go under spec.configuration.profiles ), not a server-wide one ( spec.configuration.settings ). ClickHouse 24.x will refuse to start with Code: 137 UNKNOWN_ELEMENT_IN_CONFIG if placed wrong.

- Multi-region shards : each per-region pod template needs topology.kubernetes.io/zone -level affinity, not just region — otherwise pods land in zones their PVC can’t reach.

- ZooKeeper / Keeper PVCs : small (10 GiB is fine) but they also need a multi-zone storage class. Don’t put them on rook-ceph-block without zone pinning.

For more advanced configurations, see the Altinity operator docs .
