# Virtualization - Talos Linux

Source: https://nrp.ai/documentation/userdocs/running/virtualization-talos

# Virtualization - Talos Linux

## Intro

Running talos linux in kubevirt

## Deploying Talos cluster using LoadBalancer service

### Deploying the control plane

- Deploy the LoadBalancer service for control plane apiVersion : v1 kind : Service metadata : name : talos-cp spec : ports : - name : https port : 6443 protocol : TCP targetPort : 6443 - name : api port : 50000 protocol : TCP targetPort : 50000 selector : app : talos sessionAffinity : None type : LoadBalancer

Deploy the LoadBalancer service for control plane

```
apiVersion: v1
kind: Service
metadata:
  name: talos-cp
spec:
  ports:
  - name: https
    port: 6443
    protocol: TCP
    targetPort: 6443
  - name: api
    port: 50000
    protocol: TCP
    targetPort: 50000
  selector:
    app: talos
  sessionAffinity: None
  type: LoadBalancer
```

- Get the IP of the created LoadBalancer service Terminal window export LOADBALANCER_IP = ` kubectl get svc talos-cp -ojson | jq -r ' .status.loadBalancer.ingress[0].ip ' ` echo $LOADBALANCER_IP

Get the IP of the created LoadBalancer service

```
export LOADBALANCER_IP=`kubectl get svc talos-cp -ojson | jq -r '.status.loadBalancer.ingress[0].ip'`
echo $LOADBALANCER_IP
```

- Deploy the VM for the control plane apiVersion : kubevirt.io/v1 kind : VirtualMachine metadata : name : talos-cp01 labels : app : talos role : controlplane spec : runStrategy : Always template : metadata : labels : app : talos role : controlplane spec : dnsPolicy : None dnsConfig : nameservers : - 8.8.8.8 - 8.8.4.4 affinity : nodeAffinity : requiredDuringSchedulingIgnoredDuringExecution : nodeSelectorTerms : - matchExpressions : - key : topology.kubernetes.io/zone operator : In values : - ucsd - ucsd-sdsc - ucsd-nrp terminationGracePeriodSeconds : 0 domain : clock : timer : {} utc : {} cpu : model : host-passthrough threads : 4 machine : type : q35 resources : limits : devices.kubevirt.io/kvm : " 1 " memory : 4G cpu : 4 requests : devices.kubevirt.io/kvm : " 1 " memory : 2G cpu : 2 devices : rng : {} autoattachSerialConsole : true autoattachGraphicsDevice : true disks : - name : talos-cp01-disk-vda-root bootOrder : 1 disk : bus : virtio volumes : - name : talos-cp01-disk-vda-root dataVolume : name : talos-cp01-root dataVolumeTemplates : - metadata : name : talos-cp01-root spec : pvc : accessModes : - ReadWriteOnce storageClassName : linstor-igrok resources : requests : storage : 40G source : http : url : https://github.com/siderolabs/talos/releases/download/v1.12.2/metal-amd64.iso

Deploy the VM for the control plane

```
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: talos-cp01
  labels:
    app: talos
    role: controlplane
spec:
  runStrategy: Always
  template:
    metadata:
      labels:
        app: talos
        role: controlplane
    spec:
      dnsPolicy: None
      dnsConfig:
        nameservers:
          - 8.8.8.8
          - 8.8.4.4
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: topology.kubernetes.io/zone
                    operator: In
                    values:
                      - ucsd
                      - ucsd-sdsc
                      - ucsd-nrp
      terminationGracePeriodSeconds: 0
      domain:
        clock:
          timer: {}
          utc: {}
        cpu:
          model: host-passthrough
          threads: 4
        machine:
          type: q35
        resources:
          limits:
            devices.kubevirt.io/kvm: "1"
            memory: 4G
            cpu: 4
          requests:
            devices.kubevirt.io/kvm: "1"
            memory: 2G
            cpu: 2
        devices:
          rng: {}
          autoattachSerialConsole: true
          autoattachGraphicsDevice: true
          disks:
            - name: talos-cp01-disk-vda-root
              bootOrder: 1
              disk:
                bus: virtio
      volumes:
        - name: talos-cp01-disk-vda-root
          dataVolume:
            name: talos-cp01-root
  dataVolumeTemplates:
    - metadata:
        name: talos-cp01-root
      spec:
        pvc:
          accessModes:
            - ReadWriteOnce
          storageClassName: linstor-igrok
          resources:
            requests:
              storage: 40G
        source:
          http:
            url: https://github.com/siderolabs/talos/releases/download/v1.12.2/metal-amd64.iso
```

- Generate the talos configs With the patch.yaml file in the current folder: patch.yaml cluster : network : podSubnets : - 10.224.0.0/16 serviceSubnets : - 10.98.0.0/12 machine : features : hostDNS : enabled : true Run: Terminal window talosctl gen config talos-dev https:// $LOADBALANCER_IP :6443 --output-dir talos-config --config-patch patch.yaml --additional-sans talos-cp, $LOADBALANCER_IP --install-disk /dev/vda ; talosctl --talosconfig=talos-config/talosconfig config endpoints $LOADBALANCER_IP

Generate the talos configs

With the patch.yaml file in the current folder:

```
cluster:
  network:
    podSubnets:
      - 10.224.0.0/16
    serviceSubnets:
      - 10.98.0.0/12
machine:
  features:
    hostDNS:
      enabled: true
```

Run:

```
talosctl gen config talos-dev https://$LOADBALANCER_IP:6443 --output-dir talos-config --config-patch patch.yaml --additional-sans talos-cp,$LOADBALANCER_IP --install-disk /dev/vda;
talosctl --talosconfig=talos-config/talosconfig config endpoints $LOADBALANCER_IP
```

- When the VM is running (might take some time to pull the images), open VNC client to see the CP console Terminal window virtctl vnc talos-cp01

When the VM is running (might take some time to pull the images), open VNC client to see the CP console

```
virtctl vnc talos-cp01
```

- Wait for the head node to go into the maintenance mode . Run the talosctl apply-config Terminal window talosctl apply-config -n $LOADBALANCER_IP --insecure -f talos-config/controlplane.yaml

Wait for the head node to go into the maintenance mode . Run the talosctl apply-config

```
talosctl apply-config -n $LOADBALANCER_IP --insecure -f talos-config/controlplane.yaml
```

- The VM will reboot. Once it’s back up and healthy (look in VNC), run bootstrap. It will reboot again. Terminal window talosctl bootstrap -n $LOADBALANCER_IP --talosconfig talos-config/talosconfig

The VM will reboot. Once it’s back up and healthy (look in VNC), run bootstrap. It will reboot again.

```
talosctl bootstrap -n $LOADBALANCER_IP --talosconfig talos-config/talosconfig
```

- Talos cluster will initialize. Get the kubeconfig for the cluster. Terminal window talosctl kubeconfig kubeconfig -n $LOADBALANCER_IP --talosconfig=talos-config/talosconfig

Talos cluster will initialize. Get the kubeconfig for the cluster.

```
talosctl kubeconfig kubeconfig -n $LOADBALANCER_IP --talosconfig=talos-config/talosconfig
```

- Try if you can get node for the control plane. Terminal window KUBECONFIG = ./kubeconfig kubectl get nodes

Try if you can get node for the control plane.

```
KUBECONFIG=./kubeconfig kubectl get nodes
```

### Deploying the workers

- Deploy the workers VMPool apiVersion : pool.kubevirt.io/v1beta1 kind : VirtualMachinePool metadata : name : talos-worker spec : replicas : 3 selector : matchLabels : kubevirt.io/vmpool : talos-worker virtualMachineTemplate : metadata : labels : kubevirt.io/vmpool : talos-worker spec : runStrategy : Always template : metadata : labels : kubevirt.io/vmpool : talos-worker spec : dnsPolicy : None dnsConfig : nameservers : - 8.8.8.8 - 8.8.4.4 affinity : nodeAffinity : requiredDuringSchedulingIgnoredDuringExecution : nodeSelectorTerms : - matchExpressions : - key : topology.kubernetes.io/zone operator : In values : - ucsd - ucsd-sdsc - ucsd-nrp terminationGracePeriodSeconds : 0 domain : clock : timer : {} utc : {} cpu : model : host-passthrough threads : 4 machine : type : q35 resources : limits : devices.kubevirt.io/kvm : " 1 " memory : 8G cpu : 4 requests : devices.kubevirt.io/kvm : " 1 " memory : 4G cpu : 2 devices : rng : {} autoattachSerialConsole : true autoattachGraphicsDevice : true disks : - name : talos-worker01-disk-vda-root bootOrder : 1 disk : bus : virtio volumes : - name : talos-worker01-disk-vda-root dataVolume : name : talos-worker01-root dataVolumeTemplates : - metadata : name : talos-worker01-root spec : pvc : accessModes : - ReadWriteOnce storageClassName : linstor-igrok resources : requests : storage : 10G source : http : url : https://github.com/siderolabs/talos/releases/download/v1.12.2/metal-amd64.iso

Deploy the workers VMPool

```
apiVersion: pool.kubevirt.io/v1beta1
kind: VirtualMachinePool
metadata:
  name: talos-worker
spec:
  replicas: 3
  selector:
    matchLabels:
      kubevirt.io/vmpool: talos-worker
  virtualMachineTemplate:
    metadata:
      labels:
        kubevirt.io/vmpool: talos-worker
    spec:
      runStrategy: Always
      template:
        metadata:
          labels:
            kubevirt.io/vmpool: talos-worker
        spec:
          dnsPolicy: None
          dnsConfig:
            nameservers:
              - 8.8.8.8
              - 8.8.4.4
          affinity:
            nodeAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
                nodeSelectorTerms:
                  - matchExpressions:
                      - key: topology.kubernetes.io/zone
                        operator: In
                        values:
                          - ucsd
                          - ucsd-sdsc
                          - ucsd-nrp
          terminationGracePeriodSeconds: 0
          domain:
            clock:
              timer: {}
              utc: {}
            cpu:
              model: host-passthrough
              threads: 4
            machine:
              type: q35
            resources:
              limits:
                devices.kubevirt.io/kvm: "1"
                memory: 8G
                cpu: 4
              requests:
                devices.kubevirt.io/kvm: "1"
                memory: 4G
                cpu: 2
            devices:
              rng: {}
              autoattachSerialConsole: true
              autoattachGraphicsDevice: true
              disks:
                - name: talos-worker01-disk-vda-root
                  bootOrder: 1
                  disk:
                    bus: virtio
          volumes:
            - name: talos-worker01-disk-vda-root
              dataVolume:
                name: talos-worker01-root
      dataVolumeTemplates:
        - metadata:
            name: talos-worker01-root
          spec:
            pvc:
              accessModes:
                - ReadWriteOnce
              storageClassName: linstor-igrok
              resources:
                requests:
                  storage: 10G
            source:
              http:
                url: https://github.com/siderolabs/talos/releases/download/v1.12.2/metal-amd64.iso
```

- Deploy the Headless service for workers apiVersion : v1 kind : Service metadata : name : talos-workers spec : clusterIP : None ports : - name : https port : 6443 protocol : TCP targetPort : 6443 - name : api port : 50000 protocol : TCP targetPort : 50000 selector : kubevirt.io/vmpool : talos-worker sessionAffinity : None type : ClusterIP

Deploy the Headless service for workers

```
apiVersion: v1
kind: Service
metadata:
  name: talos-workers
spec:
  clusterIP: None
  ports:
  - name: https
    port: 6443
    protocol: TCP
    targetPort: 6443
  - name: api
    port: 50000
    protocol: TCP
    targetPort: 50000
  selector:
    kubevirt.io/vmpool: talos-worker
  sessionAffinity: None
  type: ClusterIP
```

- Upload generated configs to the NRP cluster Terminal window kubectl create secret generic talos-secrets --from-file=talos-config

Upload generated configs to the NRP cluster

```
kubectl create secret generic talos-secrets --from-file=talos-config
```

- Run the talosctl deployment to get access to workers apiVersion : apps/v1 kind : Deployment metadata : name : talosctl labels : app : talosctl spec : replicas : 1 selector : matchLabels : app : talosctl template : metadata : labels : app : talosctl spec : containers : - name : deploy image : alpine resources : requests : cpu : 100m memory : 100Mi limits : cpu : 1 memory : 1Gi command : - sh - -c - | apk add curl openssl bind-tools; curl -sL https://talos.dev/install | sh; sleep infinity; imagePullPolicy : IfNotPresent volumeMounts : - mountPath : " /talos-config " name : config volumes : - name : config secret : secretName : talos-secrets

Run the talosctl deployment to get access to workers

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: talosctl
  labels:
    app: talosctl
spec:
  replicas: 1
  selector:
    matchLabels:
      app: talosctl
  template:
    metadata:
      labels:
        app: talosctl
    spec:
      containers:
        - name: deploy
          image: alpine
          resources:
            requests:
              cpu: 100m
              memory: 100Mi
            limits:
              cpu: 1
              memory: 1Gi
          command:
            - sh
            - -c
            - |
              apk add curl openssl bind-tools;
              curl -sL https://talos.dev/install | sh;
              sleep infinity;
          imagePullPolicy: IfNotPresent
          volumeMounts:
            - mountPath: "/talos-config"
              name: config
      volumes:
      - name: config
        secret:
          secretName: talos-secrets
```

- Once all worker VMs are running, exec to the talosctl deployment and bootstrap the workers from it Terminal window kubectl exec -it deploy/talosctl -- sh dig talos-workers.<your_namespace>.svc.cluster.local +short | xargs -I {} talosctl apply-config -n {}:50000 --insecure -f /talos-config/worker.yaml

Once all worker VMs are running, exec to the talosctl deployment and bootstrap the workers from it

```
kubectl exec -it deploy/talosctl -- sh
dig talos-workers.<your_namespace>.svc.cluster.local +short | xargs -I{} talosctl apply-config -n {}:50000 --insecure -f /talos-config/worker.yaml
```

- You should see the workers nodes appear in the cluster.

You should see the workers nodes appear in the cluster.

## Deploying Talos cluster using Ingress (WIP)

Coming soon…
