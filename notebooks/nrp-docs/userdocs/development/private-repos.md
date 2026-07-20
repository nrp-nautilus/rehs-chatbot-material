# Private Repos

Source: https://nrp.ai/documentation/userdocs/development/private-repos

# Private Repos

Follow these steps to provide access to container images stored in the private Nautilus GitLab repository.

- Go to your repository Settings->Repository->Deploy Tokens , and create a deploy token with read_registry flag enabled.

Go to your repository Settings->Repository->Deploy Tokens , and create a deploy token with read_registry flag enabled.

- Follow the instructions for pulling image from private registry . Your registry server your-registry-server will be NRP’s default docker images registry FQDN, identifies as one of gitlab-registry.nrp-nautilus.io gitlab-registry.nrp-nautilus.io/USERNAME/REPONAME where USERNAME is your Gitlab user name and REPONAME is your repository. Terminal window kubectl create -n somenamespace secret docker-registry regcred --docker-server=gitlab-registry.nrp-nautilus.io/somegroup/somerepo --docker-username=gitlab+deploy-token-XXX --docker-password=XXXXXXXXXXXX

Follow the instructions for pulling image from private registry . Your registry server your-registry-server will be NRP’s default docker images registry FQDN, identifies as one of

- gitlab-registry.nrp-nautilus.io

- gitlab-registry.nrp-nautilus.io/USERNAME/REPONAME

where USERNAME is your Gitlab user name and REPONAME is your repository.

```
kubectl create -n somenamespace secret docker-registry regcred --docker-server=gitlab-registry.nrp-nautilus.io/somegroup/somerepo --docker-username=gitlab+deploy-token-XXX --docker-password=XXXXXXXXXXXX
```
