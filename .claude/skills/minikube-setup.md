---
name: minikube-setup
description: Minikube setup and commands for Phase 4
priority: high
---

- minikube start --cpus 4 --memory 8192
- minikube addons enable ingress
- kubectl apply -f helm charts
- kubectl get pods -w