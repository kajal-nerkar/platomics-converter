# Platomics Number Converter

## A lightweight HTTP API that converts numbers between **decimal**, **binary**, and **hexadecimal** formats — containerised with Docker, deployed on Kubernetes, and fully automated via GitHub Actions CI/CD.
---

## 📋 Table of Contents

- [Overview](#overview)
- [Live Demo](#live-demo)
- [Prerequisites](#prerequisites)
- [Folder Structure](#folder-structure)
- [Part 1 — The Application](#part-1--the-application)
- [Part 2 — Infrastructure Design](#part-2--infrastructure-design)
- [CI/CD Pipeline](#cicd-pipeline)
- [Local Kubernetes Deployment](#local-kubernetes-deployment)
- [Bonus — Implementation Evidence](#bonus--implementation-evidence)
- [Technology Choices](#technology-choices)

---

## Overview

This project solves two tasks:

| Part | Task | Status |
|------|------|--------|
| Part 1 | HTTP API for number base conversion | ✅ Complete |
| Part 1 Bonus | `/health` endpoint | ✅ Complete |
| Part 1 Bonus | Web UI served from `/` | ✅ Complete |
| Part 2 | Production architecture design | ✅ Complete |
| Part 2 Bonus | Implemented with working CI/CD + K8s | ✅ Complete |

---

## Live Demo

The app exposes three endpoints:

```
GET /convert/<value>/<input-format>/<output-format>   ← converter API
GET /health                                           ← health check
GET /                                                 ← web UI
```

### Example API calls

```bash
curl http://localhost:8080/convert/255/dec/hex     # → ff
curl http://localhost:8080/convert/ff/hex/bin      # → 11111111
curl http://localhost:8080/convert/1010/bin/dec    # → 10
curl http://localhost:8080/health                  # → OK
```

### Supported formats

| Format | Description | Example |
|--------|-------------|---------|
| `dec` | Decimal (base-10) | 255 |
| `bin` | Binary (base-2) | 11111111 |
| `hex` | Hexadecimal (base-16) | ff |

---

## Prerequisites

Make sure you have the following installed before getting started:

| Tool | Purpose | Download |
|------|---------|----------|
| Python 3.10+ | Run the app locally | [python.org](https://python.org) |
| Docker Desktop | Build and run containers + local Kubernetes | [docker.com](https://docker.com/products/docker-desktop) |
| kubectl | Interact with Kubernetes cluster | [kubernetes.io](https://kubernetes.io/docs/tasks/tools/) |
| Git | Version control | [git-scm.com](https://git-scm.com) |
| GitHub account | CI/CD pipeline + container registry | [github.com](https://github.com) |

### Enable Kubernetes in Docker Desktop

```
Docker Desktop → Settings → Kubernetes → Enable Kubernetes → Apply & Restart
```

Verify:
```bash
kubectl get nodes
# NAME             STATUS   ROLES           AGE
# docker-desktop   Ready    control-plane   5m
```

---

## Folder Structure

```
platomics-converter/
│
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions CI/CD pipeline
│                                   # Job 1: Test | Job 2: Build+Push | Job 3: Deploy
│
├── app/
│   └── app.py                      # Python HTTP server — converter API + Web UI
│                                   # No external dependencies — stdlib only
│
├── k8s/
│   ├── deployment.yaml             # Production deployment (ghcr.io image, 2 replicas)
│   ├── deployment-local.yaml       # Local deployment (Docker Desktop)
│   ├── service.yaml                # ClusterIP service (production)
│   ├── service-local.yaml          # NodePort service — exposes localhost:30080
│   └── ingress.yaml                # nginx Ingress — routes converter.local → app
│
├── terraform/
│   └── main.tf                     # Provisions Kubernetes namespace via Terraform
│
├── screenshots/                    # Evidence for bonus task implementation
│
├── Dockerfile                      # Container image — python:3.11-slim base
├── architecture-diagram.md         # Part 2 architecture design with diagrams
└── README.md                       # This file
```

---

## Part 1 — The Application

### Run Locally with Python

No dependencies to install — uses Python standard library only.

```bash
# Clone the repo
git clone https://github.com/kajal-nerkar/platomics-converter.git
cd platomics-converter

# Run the app
python app/app.py
```

Open your browser at `http://localhost:8080` — the Web UI loads automatically.

### Run with Docker

```bash
# Build the image
docker build -t platomics-converter:latest .

# Run the container
docker run -p 8080:8080 platomics-converter:latest
```

Open your browser at `http://localhost:8080`

### Test all endpoints

```bash
# Health check
curl http://localhost:8080/health
# → OK

# Decimal to Hexadecimal
curl http://localhost:8080/convert/255/dec/hex
# → ff

# Hexadecimal to Binary
curl http://localhost:8080/convert/ff/hex/bin
# → 11111111

# Binary to Decimal
curl http://localhost:8080/convert/1010/bin/dec
# → 10

# Invalid input → returns 400 with clear error
curl http://localhost:8080/convert/xyz/bin/hex
# → Value 'xyz' is not valid bin format.

# Usage guide
curl http://localhost:8080/
# → shows full usage guide
```

---

## CI/CD Pipeline

The pipeline has **3 jobs** that run automatically on every push to `main`:

```
Push to main
     │
     ▼
┌──────────┐     ┌─────────────────────┐     ┌──────────────────────┐
│  Test    │────▶│  Build & Push       │────▶│  Deploy              │
│          │     │                     │     │                      │
│ Python   │     │ docker build        │     │ kubectl apply        │
│ curl     │     │ push to ghcr.io     │     │ deployment-local     │
│ /health  │     │                     │     │ service-local        │
│ /convert │     │ image tagged with   │     │ ingress              │
│          │     │ commit SHA + latest │     │                      │
│ ~12s     │     │ ~23s                │     │ ~30s                 │
└──────────┘     └─────────────────────┘     └──────────────────────┘
  GitHub            GitHub                     Self-hosted runner
  servers           servers                    (your machine)
```

### Setting Up the Self-Hosted Runner

The deploy job runs on a self-hosted runner so it can reach your local Kubernetes cluster:

```powershell
# 1. Create runner directory
cd C:\
mkdir actions-runner
cd actions-runner

# 2. Download runner (get fresh token from GitHub Settings → Actions → Runners)
Invoke-WebRequest -Uri https://github.com/actions/runner/releases/download/v2.334.0/actions-runner-win-x64-2.334.0.zip -OutFile actions-runner-win-x64-2.334.0.zip

# 3. Extract
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory("$PWD/actions-runner-win-x64-2.334.0.zip", "$PWD")

# 4. Configure (get fresh token from GitHub repo → Settings → Actions → Runners → New runner)
./config.cmd --url https://github.com/kajal-nerkar/platomics-converter --token YOUR_TOKEN

# 5. Start runner interactively (keeps running while you work)
./run.cmd
```

---

## Local Kubernetes Deployment

### Deploy via CI/CD Pipeline (Recommended)

Just push to main — the pipeline deploys automatically:

```bash
git push origin main
# → pipeline triggers → all 3 jobs run → app deployed to Kubernetes
```

### Deploy Manually (without pipeline)

```powershell
# 1. Build image
docker build -t platomics-converter:latest .

# 2. Create namespace
kubectl create namespace converter

# 3. Install nginx ingress controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/cloud/deploy.yaml

# 4. Apply manifests
kubectl apply -f k8s/deployment-local.yaml
kubectl apply -f k8s/service-local.yaml
kubectl apply -f k8s/ingress.yaml

# 5. Watch pods come up
kubectl get pods -n converter -w
```

### Access the App

**Option 1 — NodePort (works immediately):**
```
http://localhost:30080
<img width="1952" height="1624" alt="image" src="https://github.com/user-attachments/assets/15de673c-8d77-4f15-b8ae-8a84333a6a7c" />

```

**Option 2 — Ingress via hostname:**

First add to your hosts file (run PowerShell as Administrator):
```powershell
Add-Content -Path "C:\Windows\System32\drivers\etc\hosts" -Value "127.0.0.1 converter.local"
```

Then access:
```
http://converter.local
```

### Verify Everything is Running

```powershell
# Check nodes
kubectl get nodes

# Check pods (should show 2 Running)
kubectl get pods -n converter

# Check services
kubectl get service -n converter

# Check ingress
kubectl get ingress -n converter

# Check full deployment status
kubectl rollout status deployment/converter-app -n converter
```

### Provision Namespace with Terraform

```powershell
cd terraform

# Download providers
terraform init

# Preview what will be created
terraform plan

# Create the namespace
terraform apply
```
<img width="2588" height="998" alt="image" src="https://github.com/user-attachments/assets/c32e08ed-19b9-4549-a227-4d2b4892c9d5" />

<img width="1960" height="1634" alt="image" src="https://github.com/user-attachments/assets/fe994906-82c2-4475-960d-9d9c9a0b5e84" />


```
---
## Part 2 — Infrastructure Design

# Please check architecture-diagram.png

## Technology Choices

| Technology | Why chosen |
|------------|-----------|
| **Python** | No external dependencies — stdlib `http.server` only. Clean, readable, easy to containerise |
| **Docker** | Portable — runs identically on any machine or cluster |
| **Kubernetes** | Matches Platomics stack exactly. Auto-healing, rolling updates, 2-replica redundancy |
| **GitHub Actions** | Native to the repo — no extra CI tool needed. Free 2000 min/month |
| **ghcr.io** | Built into GitHub — no separate registry account. Free for public repos |
| **nginx Ingress** | Industry standard K8s ingress controller. Host-based routing, SSL-ready |
| **Terraform** | IaC for namespace provisioning — matches Platomics stack. Repeatable across environments |
| **Prometheus + Grafana** | Matches Platomics stack. Scrapes `/health` endpoint for uptime monitoring |

---

## Author

**Kajal Nerkar**
GitHub: [@kajal-nerkar](https://github.com/kajal-nerkar)
