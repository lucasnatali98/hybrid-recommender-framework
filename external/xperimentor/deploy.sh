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
      - name: "xperimentor-container"
        image: "mpacheco95/xperimentor:latest"
        ports:
        - containerPort: 3000
      - name: "task-executor-container"
        image: "mpacheco95/task_executor:latest"
        ports:
        - containerPort: 5050

EOF

kubectl apply -f xperimentor-deployment.yaml && \
kubectl get pods
kubectl expose deployment xperimentor-deployment --type=LoadBalancer --name=xperimentor-service
kubectl describe service xperimentor-service | grep IP