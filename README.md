# CloudSense AI ☁️🤖

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/AWS-Bedrock-orange.svg" alt="AWS Bedrock">
  <img src="https://img.shields.io/badge/Kubernetes-EKS-326CE5.svg" alt="Kubernetes EKS">
  <img src="https://img.shields.io/badge/GitOps-ArgoCD-ef7b4d.svg" alt="ArgoCD">
  <img src="https://img.shields.io/badge/IaC-Terraform-844FBA.svg" alt="Terraform">
</div>

<br />

> **A Multi-Account AWS FinOps Platform with AI Anomaly Detection and GitOps CI/CD.**

CloudSense AI is a professional DevOps/Cloud engineering project built to solve a crucial FinOps challenge: automatically identifying, analyzing, and explaining unexpected AWS billing spikes using **Generative AI** (AWS Bedrock / Claude).

---

## 🎯 Project Overview

This architecture leverages bleeding-edge Cloud Native and Machine Learning technologies to provide intelligent cost oversight. The system collects cost data from AWS, feeds it into an advanced AI model capable of financial reasoning, and emits highly detailed anomalies and actionable recommendations.

### Key Capabilities:
- **Intelligent FinOps**: Replaces manual cost analysis with automated AI evaluations.
- **GitOps Methodology**: Entire workload lifecycle is managed declaratively via ArgoCD on EKS.
- **Robust Software Engineering**: Python application strictly built using Domain-Driven Design (DDD) and Test-Driven Development (TDD). 
- **Full Observability Stack**: Prometheus, Promtail, Loki, and Grafana integrated for metrics and logs.
- **Infrastructure as Code**: End-to-end AWS provisioning with Terraform.

---

## 🏛️ Architecture & Workflow

### 1. High-Level Infrastructure (AWS & K8s)

```mermaid
graph TD
    subgraph AWS Cloud
        CostData[AWS Cost Explorer API]
        Bedrock[AWS Bedrock - Claude AI]
    end

    subgraph AWS EKS Cluster
        Argo[ArgoCD GitOps Controller]
        
        subgraph Namespace: cloudsense-app
            Cron[CronJob: cloudsense-ai-job]
            PythonApp[/Python DDD Engine/]
            Cron -->|Instantiates| PythonApp
        end
        
        subgraph Namespace: observability
            Prometheus[Prometheus]
            Loki[Loki Log Aggregation]
            Grafana[Grafana Dashboards]
        end
        
        Argo -->|Declarative Sync| Cron
        Argo -->|Declarative Sync| Prometheus
    end

    PythonApp -->|1. Fetch Billing Data| CostData
    PythonApp -->|2. Analyze via Prompt Engineering| Bedrock
    PythonApp -->|3. Output JSON Metrics & Logs| Loki
    Loki -->|Visualize| Grafana
```

### 2. Application Domain Flow (Python Engine)

The core logic operates as a scheduled Kubernetes Job, separating infrastructure from the business domain.

```mermaid
sequenceDiagram
    participant K8s as EKS CronJob
    participant Main as Python Core (main.py)
    participant CE as AWS Cost Explorer
    participant Claude as AWS Bedrock
    participant Loki as K8s stdout (Loki)
    
    K8s->>Main: Trigger scheduled cycle
    activate Main
    Main->>CE: fetch_costs_uc.execute(date_range)
    CE-->>Main: Cost Data (JSON)
    Main->>Claude: detect_anomaly_uc.execute(CostData, baseline)
    Claude-->>Main: AI Analysis Result & Recommendations (JSON)
    Main->>Loki: Emit Structured Logs (Anomalies & AI Summary)
    deactivate Main
```

---

## 🚀 Technology Stack

| Domain | Technologies Used |
| :--- | :--- |
| **Cloud & FinOps** | AWS Services (EKS, IAM, VPC, Bedrock, Cost Explorer) |
| **Infrastructure as Code** | Terraform, Helm |
| **GitOps & Orchestration**| Kubernetes, ArgoCD, App of Apps Pattern |
| **Application Layer** | Python, Pydantic, Boto3, Domain-Driven Design (DDD) |
| **Testing & CI/CD** | Pytest (TDD), GitHub Actions, Makefiles |
| **Observability** | Prometheus, Loki, Grafana, Promtail |

---

## 💻 Repository Structure

```text
.
├── cloudsense-ai/
│   ├── src/                 # Python Engine (DDD Architecture)
│   │   ├── analysis/        # AI Anomaly Detection Domain
│   │   └── billing/         # AWS Cost Fetching Domain
│   ├── tests/               # Pytest TDD Suite
│   ├── terraform/           # IaC for VPC, EKS, IAM, and ArgoCD
│   ├── k8s/                 # Kubernetes Manifests & ArgoCD Apps
│   ├── dashboards/          # Grafana JSON Dashboards
│   ├── Makefile             # Abstracted Developer Operations
│   └── Dockerfile           # K8s Workload Image
└── README.md                # Project Documentation
```

---

## ⚙️ Execution & Demo Instructions

> **⚠️ WARNING:** This project provisions real AWS EKS infrastructure. To avoid unexpected charges, strictly follow the cleanup step after testing.

### Prerequisites
- AWS CLI configured with administrator credentials.
- `terraform`, `kubectl`, `docker`, and `make` installed.
- Python 3.11+ for local unit testing.

### 1. Verification (TDD Proof)
Validate the application's domain logic using the `Makefile` test wrapper:
```bash
cd cloudsense-ai
make test
```

### 2. Infrastructure Deployment
Automatically initialize Terraform, provision the EKS cluster, configure IAM OIDC, and bootstrap ArgoCD.
```bash
cd cloudsense-ai
make deploy
```
*Note: ArgoCD will automatically detect the Kubernetes manifests in the Git repository and sync the `cloudsense-ai-job` and observability stack.*

### 3. Run the AI Simulation
The Python engine runs natively as a managed Docker container in K8s. Perform a manual run to observe the AI analyzing an anomaly in real logs:
```bash
kubectl create job --from=cronjob/cloudsense-ai-job manual-run-1 -n cloudsense-app
kubectl logs -f job/manual-run-1 -n cloudsense-app
```

### 4. Cleanup (CRITICAL)
Destroy all K8s workloads and AWS resources gracefully to preserve cloud hygiene:
```bash
cd cloudsense-ai
make destroy
```

---

<div align="center">
  <p>Built as a demonstrator for modern Cloud Engineering, GitOps, and AI integrations.</p>
</div>
