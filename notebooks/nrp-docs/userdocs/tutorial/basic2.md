# Scheduling and Exposing

Source: https://nrp.ai/documentation/userdocs/tutorial/basic2

# Scheduling and Exposing

# Horizontal scaling

In a Kubernetes cluster, orchestration refers to the automated coordination, deployment, scaling, and management of containerized applications and their associated workloads.

Horizontal scaling is crucial for services hosted on a Kubernetes cluster for several reasons, and it aligns with the fundamental principles of container orchestration and cloud-native architectures.

Horizontal scaling in Nautilus allows you increase the overall workload of your jobs, improve reliability and availability, use resources more efficiently, load balance across replicas, and it increases fault tolerance (no single instance failing disrupts your work). Horizontal scaling is common practice for cloud-native applications.

## Prerequisites

This section builds on skills from both the Quickstart and the tutorial on Basic Kubernetes .

## Learning Objectives

- You will learn how to deploy a basic Apache service across multiple replicas.

- You will learn how to load balance between replicas.

- You understand how to expose services running inside of your pods to the public internet.

## Let’s launch multiple web servers

In this exercise, we will launch multiple Web servers.

To make distinguishing the two servers easier, we will force the nodename into their homepages. Using stock images, we achieve this by using an init container .

You can copy-and-paste the lines below into a new file called http2.yaml (using the cat command to redirect the standard input).

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-http
  labels:
    k8s-app: test-http
spec:
  replicas: 2
  selector:
    matchLabels:
      k8s-app: test-http
  template:
    metadata:
      labels:
        k8s-app: test-http
    spec:
      initContainers:
      - name: myinit
        image: busybox
        command: ["sh", "-c", "echo '<html><body><h1>I am ' `hostname` '</h1></body></html>' > /usr/local/apache2/htdocs/index.html"]
        volumeMounts:
        - name: dataroot
          mountPath: /usr/local/apache2/htdocs
      containers:
      - name: mypod
        image: httpd:alpine
        resources:
           limits:
             memory: 200Mi
             cpu: 1
           requests:
             memory: 50Mi
             cpu: 50m
        volumeMounts:
        - name: dataroot
          mountPath: /usr/local/apache2/htdocs
      volumes:
      - name: dataroot
        emptyDir: {}
```

Examine the above text and try to identify what makes this different than the other YAML files we’ve encountered so far. Some new fields can be found under the initContainers tag.

What happens if you want to scale beyond just two replicas? Feel free to change the number of replicas (within reason) and the text it is shown in home page of each server, if so desired.

### Launch the deployment:

Now that you have created this new YAML file, and you understand what makes this file different, let’s try it by executing the following command.

```
kubectl create -f http2.yaml
```

In order for us to examine what’s happening in our deployment, we’ll need to access it via another pod running within our namespace.

#### Let’s build a pod to examine our deployment

It’s an important skill to be able to iterate by modifying your existing YAML files. This is how most people develop new versions: they modify existing versions.

In this mini-exercise, we are going to copy pod1.yaml , make some modifications using our favorite CLI text editor (e.g. vi, nano or vim), and use our modified version to peer into our pods from http2.yaml .

Let’s recall what the pod1.yaml file looked like:

```
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
  - name: mypod
    image: ubuntu
    resources:
      limits:
        memory: 100Mi
        cpu: 100m
      requests:
        memory: 100Mi
        cpu: 100m
    command: ["sh", "-c", "echo 'Im a new pod' && sleep infinity"]
```

In Kubernetes, the base unit for describing memory resources is the byte . However, to make it more convenient and human-readable, memory values are commonly expressed in multiples of bytes using the International System of Units (SI) prefixes.

- Kilobyte (Ki): 1 Ki is equivalent to 1024 bytes.

- Megabyte (Mi): 1 Mi is equivalent to 1024 KiB or 1,048,576 bytes.

- Gigabyte (Gi): 1 Gi is equivalent to 1024 MiB or 1,073,741,824 bytes.

- …and so on

In Kubernetes, the base unit for describing CPU resources is the “millicore” which represents one thousandth of a CPU core. The term “millicore” is often abbreviated as “mCPU” or simply “m” (as above). For example, a CPU value of “100m” means 100 millicores, which is equivalent to 0.1 CPU core. Similarly, “500m” represents 500 millicores or 0.5 CPU core.

### A Container that has curl

In order for us to use another pod to peer into our load-balanced web servers, we need a container that has curl as a preinstalled package. It’s important for us to realize that a customized container that automates what we need is much preferred for repeatability and scale (and they are often available prebuilt in places like Docker Hub ).

In this case, we’re providing you with an image that has ‘curl’ preinstalled. Create a YAML file with the name pod-curl.yaml by coping the code below.

```
apiVersion: v1
kind: Pod
metadata:
  name: test-curl-pod
spec:
  containers:
  - name: mycurlpod
    image: curlimages/curl:latest
    resources:
      limits:
        memory: 200Mi
        cpu: 200m
      requests:
        memory: 200Mi
        cpu: 200m
    command: ["sh", "-c", "echo 'Im a new curl pod' && sleep infinity"]
```

Notice that we’ve increased our resources and requests for memory and CPU.

When using a shared Kubernetes cluster (or any shared cluster for that matter), it is wise to balance your need for resources with their availability. Asking for too many resources will decrease the chances the cluster can provide them in a reasonable timeframe. Asking for too few resources will negatively impact your ability to compute.

Once this new pod is launched, you can continue with the tutorial.

#### Check your web servers are running and get their IP addresses

Check the pods you have, alongside the IPs they were assigned to:

```
kubectl get pods -o wide
```

Log into pod1

```
kubectl exec -it test-curl-pod -- /bin/sh
```

Now, from inside your curl -capable pod, try to pull the home pages from the two Web servers; use the IPs you obtained above:

```
curl http:// < IPofPod >
```

Each pod should say something like, "<html><body><h1>I am test-http-76f7d84c67-j5ff4 </h1></body></html>" where the hash of numbers and characters is unique to each pod you are querying.

## Load balancing

Having to manually switch between the two Pods is obviously tedious. What we really want is to have a single logical address that will automatically load-balance between them.

You can copy-and-paste the lines below.

```
apiVersion: v1
kind: Service
metadata:
  labels:
    k8s-app: test-svc
  name: test-svc
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    k8s-app: test-http
  type: ClusterIP
```

Let’s now start the service:

```
kubectl create -f svc2.yaml
```

Look up your service, and write down the IP it is reporting under:

```
kubectl get services
```

Log into pod1

```
kubectl exec -it test-curl-pod -- /bin/sh
```

Now try to pull the home page from the service IP:

curl http://*IPofService*

Try it a few times…by repeating the command (hint: the ↑ on your keyboard will toggle through previous commands). Which Web server is serving you? Does it matter? How could you imagine using a service like this to balance the load across multiple pods or deployments?

Note that you can also use the local DNS name for this (from pod1)

curl http://test-svc.<namespace>.svc.cluster.local

## Exposing public services

Sometimes you have the opposite problem; you want to export resources of a single node to the public internet.

The above Web services only serve traffic on the private IP network LAN. If you try curl from your laptops, you will never reach those Pods!

What we need, is set up an Ingress instance for our service.

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: test-ingress
spec:
  ingressClassName: haproxy
  rules:
  - host: test-service.nrp-nautilus.io
    http:
      paths:
      - backend:
          service:
            name: test-svc
            port:
              number: 80
        path: /
        pathType: ImplementationSpecific
  tls:
  - hosts:
    - test-service.nrp-nautilus.io
```

Launch the new ingress

```
kubectl create -f ingress.yaml
```

You should now be able to fetch the Web pages from your browser by opening https://test-service.nrp-nautilus.io .

You can now delete the deployment:

```
kubectl delete -f http2.yaml
kubectl delete -f svc2.yaml
kubectl delete -f ingress.yaml
kubectl delete -f pod-curl.yaml
```
