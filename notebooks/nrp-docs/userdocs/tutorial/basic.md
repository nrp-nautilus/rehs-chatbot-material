# Basic Kubernetes (k8s) Tutorial

Source: https://nrp.ai/documentation/userdocs/tutorial/basic

# Basic Kubernetes (k8s) Tutorial

In this tutorial, you will be introduced to basic k8s commands, how to launch simple pods and deployments, as well as interact with the cluster to query its status and the status of your processes running in the cluster. You will also see your first example of a YAML file.

## Prerequisites

This section assumes you’ve completed the quickstart section.

## Learning Objectives

- You will understand the basic format of k8s commands.

- You will be able to use k8s commands to interact with the cluster.

- You will have a basic understanding of YAML and you will be able to use that to create a simple pod.

- You will have an understanding of the difference between an pod and a deployment.

- You will have a basic understanding of the “stateless” nature of a pod and how deployments can be used to specify an ideal state for your pods or software containers (running inside your pods).

## Explore the system

Now that you understand how to set your namespace, let’s begin to explore the system.

### List cluster nodes

The Nautilus Cluster is widely geographically distributed and highly heterogenous. You can get a sense of the types of nodes in the system by typing:

```
kubectl get nodes
```

Please note : You likely won’t have access to all the nodes listed, as some are reserved.

### List processes running in your namespace

There are three categories of processes we will examine:

- pods

- deployments

- services

Listing the categories running in k8s follows a similar format.

```
kubectl get <category>
```

Right now you probably don’t have anything running in the namespace, and these commands will return No resources found in ... <namespace>. but you will revisit these commands as we step through the tutorials as a way of checking on status.

#### List pods

List all the pods in your namespace

```
kubectl get pods
```

#### List deployments

List all the deployments in your namespace

```
kubectl get deployments
```

#### List services

List all the services in your namespace

```
kubectl get services
```

## Setup your first pod with YAML

Let’s create a simple generic pod, and then login into it.

### A simple YAML file

Create the pod1.yaml file with the following contents by copy-pasting:

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
        memory: 200Mi
        cpu: 200m
      requests:
        memory: 200Mi
        cpu: 200m
    command: ["sh", "-c", "echo 'Im a new pod' && sleep infinity"]
```

Reminder : Indentation is important in YAML, just like in Python

### Creating YAML files dynamically

Alternatively, if you don’t want to create a file and are using Unix-like system, you can create YAML files dynamically like this:

```
kubectl create -f - << EOF
<contents you want to deploy>
EOF
```

### Launch a simple pod

Making sure you are in the same file directory as your pod1.yaml file, type the following command:

```
kubectl create -f pod1.yaml
```

After a few moments (as the pod is creating itself), see if you can find it:

```
kubectl get pods
```

Please Note : You may see the other pods too.

If it is not yet in Running state, you can check what is going on with a list of the events in your namespace:

```
kubectl get events --sort-by=.metadata.creationTimestamp
```

Events and other useful information about the pod can be seen in describe :

```
kubectl describe pod test-pod
```

:question: Where did the name test-pod come from? Examine the pod1.yaml file to find the answer.

If the pod is in Running state, we can check it’s logs

```
kubectl logs test-pod
```

Let’s log into it

```
kubectl exec -it test-pod -- /bin/bash
```

Try to create some directories and some files with content (using the cat command, if you like). “Hello world” will do, but feel free to be creative.

### Let’s examine the pod’s networking

Networking inside a Kubernetes pod is crucial for facilitating communication between containers within the same pod and enabling connectivity with other pods, as well as external services. Understanding how networking works inside a pod is essential for building and deploying applications effectively in a Kubernetes environment. So, let’s examine how the network is configured inside our simple pod by logging into it.

Remember that pods running inside k8s are “stateless” and since we didn’t specify any software packages to be included in our simple pod example when we launched it, we have some work to do before we can look at the network.

The package ifconfig is not included in our initial pod; so let’s install it.

First, let’s make sure our installation tools are updated.

```
apt update
```

Now, we can use apt to install the necessary network tools.

```
apt install net-tools
```

Now check the networking:

```
ifconfig -a
```

Finally, let’s exit out of the pod and move on by entering the exit command in the command line interface of the pod, or using the keyboard shortcut ‘Control-D’.

### Testing statelessness

To demonstrate that pods really are stateless, we are going to shutdown our simple pod, and repeat the creation of our simple pod, then take a look at it again.

### Shutdown the originall

Let’s manually shut down the pod using kubectl

```
kubectl delete -f pod1.yaml
```

This may take a moment, as the system will remove the pod gracefully. After a few moments, check that it is actually gone:

```
kubectl get pods
```

### Looking at Pod1.yaml (again)

Give the system a moment to create the new pod.

Now, let’s look for the files you created with the cat command. Are they where you left them? What is the status of the files your created?

### Cleaning up

Since Nautilus is a shared platform and a community resource, it’s very important that we don’t leave any stray processes running. So, everytime we’re finished using a pod, we should make sure to clean up after ourselves.

So, let’s delete explicitly the pod, using the following command:

```
kubectl delete pod test-pod
```

## Let’s transform our pod into a deployment

You saw that when a pod was terminated, it was gone. While above we did it by ourselves, the result would have been the same if a node died or was restarted. This is normal and expected in a k8s cluster, and is actually a great feature of Kubernetes: it is highly resilient. Kubernetes constantly monitors the health of pods and containers. In the event of a failure or unresponsiveness, Kubernetes automatically restarts containers or entire pods to maintain the desired state specified by the user.

In order to specify to the cluster your “desired state”, the use of Deployments is recommended.

You can copy-and-paste the lines below into a new file on your local system (using the cat command, if you like).

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-dep
  labels:
    k8s-app: test-dep
spec:
  replicas: 1
  selector:
    matchLabels:
      k8s-app: test-dep
  template:
    metadata:
      labels:
        k8s-app: test-dep
    spec:
      containers:
      - name: mypod
        image: ubuntu
        resources:
           limits:
             memory: 500Mi
             cpu: 500m
           requests:
             memory: 100Mi
             cpu: 50m
        command: ["sh", "-c", "sleep infinity"]
```

Now let’s start the deployment:

```
kubectl create -f dep1.yaml
```

See if you can find it:

```
kubectl get deployments
```

See if you can find the associated pod:

```
kubectl get pods
```

Once you have found the name assigned to it by the cluster, let’s log into it.

```
kubectl get pod -o wide test-dep-<hash>
kubectl exec -it test-dep-<hash> -- /bin/bash
```

You are now inside the (container in the) pod!

### Testing statelessness with deployments

Create directories and files as before.

Try various commands as before.

Let’s now delete the pod!

```
kubectl delete pod test-dep-<hash>
```

Is it really gone?

```
kubectl get pods
```

What happened to the deployment?

```
kubectl get deployments
```

Get into the new pod

```
kubectl get pod -o wide test-dep-<hash>
kubectl exec -it test-dep-<hash> -- /bin/bash
```

Let’s now delete the deployment:

```
kubectl delete -f dep1.yaml
```

Verify everything is gone:

```
kubectl get deployments
kubectl get pods
```

## Next steps

In the next tutorial , we will explore how to run a simple web server in a pod, and how to expose it to the outside world and scale it.
