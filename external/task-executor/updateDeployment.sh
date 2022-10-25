#!/bin/bash

kubectl scale --replicas=0 deployment task-executor-deployment
sleep 5
kubectl scale --replicas=3 deployment task-executor-deployment
sleep 5
kubectl describe deployment task-executor-deployment