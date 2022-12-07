#!/bin/bash

gcloud container clusters get-credentials autopilot-cluster-1 --zone us-central1 --project thematic-mapper-364320 && \

cat <<EOF > xperimentor-deployment.yaml
---
apiVersion: "apps/v1"
kind: "Deployment"
metadata:
  name: "xperimentor-deployment"
  namespace: "default"
  labels:
    app: "xperimentor-deployment"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: "xperimentor-deployment"
  template:
    metadata:
      labels:
        app: "xperimentor-deployment"
    spec:
      containers:
      - name: "xperimentor-homolog-container"
        image: "lucasnatali98/xperimentor:xperimentor-homolog-1.0.1"
        ports:
        - containerPort: 3000
EOF

kubectl apply -f xperimentor-deployment.yaml && \
kubectl get pods
kubectl expose deployment xperimentor-deployment --type=LoadBalancer --name=xperimentor-service-homolog
kubectl describe service xperimentor-service-homolog | grep IP