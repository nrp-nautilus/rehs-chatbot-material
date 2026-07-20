# K8s Gitlab Integration

Source: https://nrp.ai/documentation/userdocs/development/k8s-integration

# K8s Gitlab Integration

This page covers integrating GitLab with the Nautilus cluster to automatically deploy from GitLab to Kubernetes via CI/CD jobs.

- In your project, go to Operate -> Kubernetes clusters , click the dropdown in the top right and select Connect a cluster (certificate - deprecated)

In your project, go to Operate -> Kubernetes clusters , click the dropdown in the top right and select Connect a cluster (certificate - deprecated)

- In the namespace create a GitLab service account: kubectl create sa gitlab -n <your_namespace>

In the namespace create a GitLab service account: kubectl create sa gitlab -n <your_namespace>

- Create the rolebinding for the service account: kubectl create -f - << EOF apiVersion: rbac.authorization.k8s.io/v1 kind: RoleBinding metadata: name: gitlab namespace: <your_namespace> roleRef: apiGroup: rbac.authorization.k8s.io kind: ClusterRole name: admin subjects: - kind: ServiceAccount name: gitlab namespace: <your_namespace> EOF

Create the rolebinding for the service account:

```
 kubectl create -f - << EOF
 apiVersion: rbac.authorization.k8s.io/v1
 kind: RoleBinding
 metadata:
   name: gitlab
   namespace: <your_namespace>
 roleRef:
   apiGroup: rbac.authorization.k8s.io
   kind: ClusterRole
   name: admin
 subjects:
 - kind: ServiceAccount
   name: gitlab
   namespace: <your_namespace>
 EOF
```

- Create a secret for the service account: kubectl -n <your_namespace> apply -f - << EOF apiVersion: v1 kind: Secret metadata: name: gitlab-secret annotations: kubernetes.io/service-account.name: gitlab type: kubernetes.io/service-account-token EOF

Create a secret for the service account:

```
 kubectl -n <your_namespace> apply -f - << EOF
 apiVersion: v1
 kind: Secret
 metadata:
   name: gitlab-secret
   annotations:
     kubernetes.io/service-account.name: gitlab
 type: kubernetes.io/service-account-token
 EOF
```

- Get the secret and Certificate Authority (CA) for the service account: kubectl get secret -n your_namespace | grep gitlab kubectl get secret -n your_namespace <gitlab-secret-...> -o yaml echo <the token value> | base64 -d - this will give you the service token field value echo <the CA value> | base64 -d - CA API URL - get from your cluster config file ( https://67.58.53.148:443 )

Get the secret and Certificate Authority (CA) for the service account:

kubectl get secret -n your_namespace | grep gitlab

kubectl get secret -n your_namespace <gitlab-secret-...> -o yaml

echo <the token value> | base64 -d - this will give you the service token field value

echo <the CA value> | base64 -d - CA

API URL - get from your cluster config file ( https://67.58.53.148:443 )

- Uncheck GitLab-managed cluster , enter the namespace into Project namespace prefix (optional, unique)

Uncheck GitLab-managed cluster , enter the namespace into Project namespace prefix (optional, unique)

- Click Add kubernetes cluster

Click Add kubernetes cluster

Now your cluster config will be available to tools like kubectl and helm to access your namespace. You can use this project as an example of how to automatically deploy a Helm application to your namespace and this one to automatically update the deployment image.
