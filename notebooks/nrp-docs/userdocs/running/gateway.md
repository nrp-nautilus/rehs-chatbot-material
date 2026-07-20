# Gateway API

Source: https://nrp.ai/documentation/userdocs/running/gateway

# Gateway API

Gateway API is a Kubernetes API for defining and managing network gateways and their associated routing rules. It provides a declarative way to define how traffic should be routed to services within a Kubernetes cluster, making it easier to manage complex network topologies and improve the scalability and reliability of applications. It obsoletes Ingress .

# Exposing HTTP services

Create HTTPRoute to expose HTTP services.

```
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-service-route
spec:
  hostnames:
  - my-service-name.nrp-nautilus.io
  parentRefs:
  - group: gateway.networking.k8s.io
    kind: Gateway
    name: ingress
    namespace: haproxy
    sectionName: https
  rules:
  - backendRefs:
    - group: ""
      kind: Service
      name: service-name
      port: 8443
      weight: 1
    matches:
    - path:
        type: PathPrefix
        value: /
```

Replace:

- .metadata.name - any name unique within the namespace

- .spec.hostnames[0] - the hostname for the HTTP service. Choose any unique one within .nrp-nautilus.io .

- .spec.rules[0].backendRefs[0].name - the name of the service in the namespace where it is deployed.

- .spec.rules[0].backendRefs[0].port - the port of the service in the namespace where it is deployed.

Use the official docs / reference spec for other fields.

# Exposing GRPC services

Create GRPCRoute to expose GRPC services.

```
apiVersion: gateway.networking.k8s.io/v1
kind: GRPCRoute
metadata:
  name: my-service-route
spec:
  hostnames:
  - my-service-name.nrp-nautilus.io
  parentRefs:
  - group: gateway.networking.k8s.io
    kind: Gateway
    name: ingress
    namespace: haproxy
    sectionName: grpc
  rules:
  - backendRefs:
    - kind: Service
      name: service-name
      port: 50051
      weight: 1
```

Replace:

- .metadata.name - any name unique within the namespace

- .spec.hostnames[0] - the hostname for the GRPC service. Choose any unique one within .nrp-nautilus.io .

- .spec.rules[0].backendRefs[0].name - the name of the service in the namespace where it is deployed.

- .spec.rules[0].backendRefs[0].port - the port of the service in the namespace where it is deployed.

Use the official docs / reference spec for other fields.

# Testing

## Testing GRPC

(Taken from envoy gateway docs )

Deploy the test app:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: yages
    example: grpc-routing
  name: yages
spec:
  selector:
    matchLabels:
      app: yages
  replicas: 1
  template:
    metadata:
      labels:
        app: yages
    spec:
      containers:
        - name: grpcsrv
          image: ghcr.io/projectcontour/yages:v0.1.0
          resources:
            limits:
              cpu: 100m
              memory: 100Mi
            requests:
              cpu: 50m
              memory: 50Mi
          ports:
            - containerPort: 9000
              protocol: TCP
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: yages
    example: grpc-routing
  name: yages
spec:
  type: ClusterIP
  ports:
    - name: http
      port: 9000
      protocol: TCP
      targetPort: 9000
  selector:
    app: yages
---
apiVersion: gateway.networking.k8s.io/v1
kind: GRPCRoute
metadata:
  name: yages
  labels:
    example: grpc-routing
spec:
  hostnames:
  - test-service.nrp-nautilus.io
  parentRefs:
  - group: gateway.networking.k8s.io
    kind: Gateway
    name: ingress
    namespace: haproxy
    sectionName: grpc
  rules:
  - backendRefs:
    - kind: Service
      name: yages
      port: 9000
      weight: 1
```

Check the status of GRPCRoute:

```
kubectl get grpcroutes --selector=example=grpc-routing -o yaml
```

The status for the GRPCRoute should surface “Accepted=True” and a parentRef that references the example Gateway. The yages route matches any traffic for “test-service.nrp-nautilus.io” and forwards it to the “yages” Service.

Test GRPC routing to the yages backend using the grpcurl command.

```
grpcurl test-service.nrp-nautilus.io:50051 yages.Echo/Ping
```

You should see the below response

```
{
  "text": "pong"
}
```

Envoy Gateway also supports gRPC-Web requests for this configuration. The below curl command can be used to send a grpc-Web request with over HTTP/2. You should receive the same response seen in the previous command.

The data in the body AAAAAAA= is a base64 encoded representation of an empty message (data length 0) that the Ping RPC accepts.

```
curl -s https://test-service.nrp-nautilus.io:50051/yages.Echo/Ping -H 'Content-Type: application/grpc-web-text' -H 'Accept: application/grpc-web-text' -XPOST -d'AAAAAAA=' | base64 -d
```
