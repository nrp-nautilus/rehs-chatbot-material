# Title

Source: https://nrp.ai/documentation/userdocs/storage/fuse

# Title

#### Mounting FUSE filesystem

Currently kubernetes requires elevated privileges to use FUSE mounts. The improvements are tracked in this issue . Normally we don’t allow users to run with privileged access in the cluster, and this methoud can only be used in exceptional cases.

Here we demonstrate connecting to nautilus western S3 pool, but it can be adjusted for any FUSE mount.

- Create the secret with your S3 credentials:

rclone.conf:

```
  [nautilus_s3]
  type = s3
  provider = Ceph
  access_key_id = <S3 key>
  secret_access_key = <S3 secret>
  endpoint = https://s3-west.nrp-nautilus.io
```

kubectl create secret generic s3 --from-file=rclone.conf

- Minimal pod example to mount S3: apiVersion: v1 kind: Pod metadata: name: fuse-pod spec: containers: - name: vol-container image: ubuntu command: - bash - -c - apt-get update && apt-get install -y vim fuse rclone curl && rclone mount nautilus_s3:<your_bucket_in_s3> /mnt securityContext: capabilities: add: - SYS_ADMIN resources: requests: memory: 1Gi cpu: "1" smarter-devices/fuse: "1" limits: memory: 1Gi cpu: "1" smarter-devices/fuse: "1" volumeMounts: - name: secret-volume mountPath: /root/.config/rclone volumes: - name: secret-volume secret: secretName: s3

Minimal pod example to mount S3:

```
 apiVersion: v1
 kind: Pod
 metadata:
   name: fuse-pod
 spec:
   containers:
   - name: vol-container
     image: ubuntu
     command:
     - bash
     - -c
     - apt-get update && apt-get install -y vim fuse rclone curl && rclone mount nautilus_s3:<your_bucket_in_s3> /mnt
     securityContext:
       capabilities:
         add:
         - SYS_ADMIN
     resources:
       requests:
         memory: 1Gi
         cpu: "1"
         smarter-devices/fuse: "1"
       limits:
         memory: 1Gi
         cpu: "1"
         smarter-devices/fuse: "1"
     volumeMounts:
     - name: secret-volume
       mountPath: /root/.config/rclone
   volumes:
   - name: secret-volume
     secret:
       secretName: s3
```

The fuse device will be provided by the special kubernetes plugin via the smarter-devices/fuse resource request, and SYS_ADMIN capability is needed to make the mount.
