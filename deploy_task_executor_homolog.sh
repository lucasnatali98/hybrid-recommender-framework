#!/bin/bash

gcloud container clusters get-credentials autopilot-cluster-1 --zone us-central1 --project thematic-mapper-364320 && \

cat <<EOF > task-executor-deployment.yaml
---
apiVersion: "apps/v1"
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
      - name: "task-executor-homolog-container"
        image: "lucasnatali98/task-executor:task-executor-homolog-1.0.0"
        ports:
        - containerPort: 5050
EOF

kubectl apply -f task-executor-deployment.yaml && \
kubectl get pods
kubectl expose deployment task-executor-deployment --type=LoadBalancer --name=task-executor-service-homolog
kubectl describe service task-executor-service-homolog | grep IP