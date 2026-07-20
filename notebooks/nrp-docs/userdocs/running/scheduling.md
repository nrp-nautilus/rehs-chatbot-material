# Scheduling

Source: https://nrp.ai/documentation/userdocs/running/scheduling

# Scheduling

## Introduction

Armada multi-Kubernetes cluster batch job meta-scheduler designed to handle massive-scale workloads. Built on top of Kubernetes, Armada enables organizations to distribute millions of batch jobs per day across tens of thousands of nodes spanning multiple clusters, making it an ideal solution for high-throughput computational workloads.

## Installation

To start using Armada download the client application armadactl .

Download Armadactl for MacOS/arm

Put it in your PATH folder (f.e. ~/bin/ ) and make runnable ( chmod +x ~/bin/armadactl )

Save the .armadactl.yaml config file in your home folder:

Download .armadactl.yaml config file

You’re ready to use armada.

## Usage

Start from listing the queues:

```
armadactl get queues
```

It will list all queues matching the list of all namespaces in the cluster. You can submit to the ones you normally access in the cluster.

Submit a job:

```
queue: <your_namespace>
jobSetId: job-set
jobs:
  - namespace: <your_namespace>
    priorityClassName: armada-default
    podSpec:
      terminationGracePeriodSeconds: 0
      restartPolicy: Never
      containers:
        - name: tester
          image: alpine:latest
          command:
            - sh
          args:
            - -c
            - echo $(( (RANDOM % 60) + 10 ))
          resources:
            limits:
              memory: 128Mi
              cpu: 2
            requests:
              memory: 128Mi
              cpu: 2
```

```
armadactl submit test-job.yaml
```

Login to the lookout page and see the status of your job. Also you should see the pod running in your namespace.

### Priorities

Allowed priorities in armada:

## Python client

To use python client, you can get the OIDC token from the lookout page in web browser. After logging in, check the site storage developer tab. There will be the id_token stored for authentik. It’s good for 30 minutes.

Example of the python client:

```
pip install armada-client
```

```
import os
import uuid

import grpc

from armada_client.client import ArmadaClient
from armada_client.k8s.io.api.core.v1 import generated_pb2 as core_v1
from armada_client.k8s.io.apimachinery.pkg.api.resource import (
    generated_pb2 as api_resource,
)

def create_dummy_job(client: ArmadaClient):
    """
    Create a dummy job with a single container.
    """

    pod = core_v1.PodSpec(
        containers=[
            core_v1.Container(
                name="container1",
                image="index.docker.io/library/ubuntu:latest",
                args=["sleep", "10s"],
                securityContext=core_v1.SecurityContext(runAsUser=1000),
                resources=core_v1.ResourceRequirements(
                    requests={
                        "cpu": api_resource.Quantity(string="120m"),
                        "memory": api_resource.Quantity(string="510Mi"),
                    },
                    limits={
                        "cpu": api_resource.Quantity(string="120m"),
                        "memory": api_resource.Quantity(string="510Mi"),
                    },
                ),
            )
        ],
    )

    return [client.create_job_request_item(priority=0, pod_spec=pod, namespace="your_namespace")]

token = "your_id_token"

HOST = "armada.nrp-nautilus.io"
PORT = "50051"

queue = f"your_namespace"
job_set_id = f"simple-jobset-{uuid.uuid1()}"

class BearerAuth(grpc.AuthMetadataPlugin):
    def __call__(self, context, callback):
        callback((("authorization", f"Bearer {token}"),), None)

channel = grpc.secure_channel(f"{HOST}:{PORT}",
    grpc.composite_channel_credentials(
        grpc.ssl_channel_credentials(),
        grpc.metadata_call_credentials(BearerAuth())
    )
)

client = ArmadaClient(channel)

job_request_items = create_dummy_job(client)

client.submit_jobs(
    queue=queue, job_set_id=job_set_id, job_request_items=job_request_items
)

print("Completed Workflow")
```
