# Infrastructure folder

In this repository we'll find the infrastructure k8s folder.

## Setup 
### Install Helm
```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh

### Publish the charts:
```
helm install fastapi-app ./helm-chart
```

