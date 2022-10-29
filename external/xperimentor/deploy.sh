#!/bin/bash

gcloud container clusters get-credentials task-executor-cluster --zone southamerica-east1-a --project monografia-238917 && \

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
      - name: "xperimentor-container"
        image: "mpacheco95/task_executor:1.0.0"
        ports:
        - containerPort: 5050
EOF

kubectl apply -f xperimentor-deployment.yaml && \
kubectl get pods (e aguarda o status = running)
kubectl expose deployment task-executor-deployment --type=LoadBalancer --name=xperimentor-service
kubectl describe service xperimentor-service | grep IP (e pega o ip)