# Running Batch Jobs

Source: https://nrp.ai/documentation/userdocs/tutorial/jobs

# Running Batch Jobs

# Running batch jobs

The Nautilus Cluster is designed specifically to support high-throughput batch jobs.

In Kubernetes, a batch job is a type of workload designed to run a finite number of tasks to completion, as opposed to continuously running or long-lived services. Batch jobs are ideal for executing tasks such as data processing, data analysis, batch data updates, backups, or any other task that needs to be performed periodically or on-demand.

A batch job (or simply, a job) is a daemon which watches your pod and makes sure it exited with exit status 0. If it did not for any reason, it will be restarted up to backoffLimit number of times.

## Prerequisites

This section builds on skills from both the Quickstart and the tutorial on Basic Kubernetes .

## Learning Objectives

- You will learn how to create a simple job that will execute a command, then run to completion.

- You will have a preliminary understanding of job states, such as “Completed” or “Error”.

- You will understand how to set limits to jobs

Let’s run a simple job and get it’s result.

Create a a file called job.yaml file and submit ito the cluster:

```
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
    spec:
      containers:
      - name: pi
        image: perl
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
        resources:
           limits:
             memory: 200Mi
             cpu: 1
           requests:
             memory: 50Mi
             cpu: 50m
      restartPolicy: Never
  backoffLimit: 4
```

Explore what’s running:

```
kubectl get jobs
kubectl get pods
```

When job is finished, your pod will stay in Completed state, and Job will have COMPLETIONS field 1/1. For long jobs, the pods can have Error, Evicted, and other states until they finish properly or backoffLimit is exhausted.

Our job did not use any storage and output the result to STDOUT, which can be seen as our pod logs:

```
kubectl logs pi-<hash>
```

The pod and job will remain for you to come and look at for ttlSecondsAfterFinished=604800 seconds (1 week) by default, and you can adjust this value in your job definition if desired.

You can use the more advanced example when ready.

## The end

Please make sure you did not leave any pods and jobs behind.
