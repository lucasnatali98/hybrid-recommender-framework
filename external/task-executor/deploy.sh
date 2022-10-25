#!/bin/bash

gcloud container clusters get-credentials task-executor-cluster --zone southamerica-east1-a --project monografia-238917 && \

cat <<EOF > task-executor-deployment.yaml
---
apiVersion: "extensions/v1beta1"
kind: "Deployment"
metadata:
  name: "task-executor-deployment"
  namespace: "default"
  labels:
    app: "task-executor-deployment"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: "task-executor-deployment"
  template:
    metadata:
      labels:
        app: "task-executor-deployment"
    spec:
      containers:
      - name: "task-executor-container"
        image: "mpacheco95/task_executor:1.0.0"
        ports:
        - containerPort: 5050
EOF

kubectl apply -f task-executor-deployment.yaml && \
kubectl get pods (e aguarda o status = running)
kubectl expose deployment task-executor-deployment --type=LoadBalancer --name=task-executor-service
kubectl describe service task-executor-service | grep IP (e pega o ip)