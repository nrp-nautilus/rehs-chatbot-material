# Linstor

Source: https://nrp.ai/documentation/userdocs/storage/linstor

# Linstor

Linstor is currently the fastest distributed block storage in the cluster, and can be used for tasks requiring minimal latency, such as VM images, docker build space, databases, etc. Also it doesn’t lock the volumes like Ceph does, making it a good option for critical highly available storage volumes.

It uses the DRBD kernel module that handles the replication, and provides nearly native drive performance for I/O operations.

### Linstor storage pools data use

Credit: Linstor data use

Linstor Grafana dashboard

### Currently available Storage Classes:
