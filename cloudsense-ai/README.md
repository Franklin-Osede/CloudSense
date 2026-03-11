# CloudSense AI ☁️🤖

> Multi-account AWS cost monitoring platform with AI anomaly detection and GitOps.

## Architecture

```text
+-------------------+        +----------------+       +------------------+
|                   |        |                |       |                  |
|  AWS Cost Data    +------->+  Python Engine +------>+  AWS Bedrock     |
|  (Simulated)      |        |  (DDD + TDD)   |       |  (Claude/AI)     |
|                   |        |                |       |                  |
+-------------------+        +-------+--------+       +------------------+
                                     |
                                     v
+------------------------------------------------------------------------+
|                      Amazon EKS (Kubernetes)                           |
|                                                                        |
|  +-------------+    +-----------------------------------------------+  |
|  |             |    |               Observability                   |  |
|  |   ArgoCD    |--->|  +------------+ +------------+ +-----------+  |  |
|  |  (GitOps)   |    |  | Prometheus | |   Loki     | |  Grafana  |  |  |
|  +-------------+    |  +------------+ +------------+ +-----------+  |  |
|          |          +-----------------------------------------------+  |
|          |          +-----------------------------------------------+  |
|          +--------->|               Application                     |  |
|                     |  +---------------------------------------+    |  |
|                     |  |  CloudSense AI Docker (K8s CronJob)   |    |  |
|                     |  +---------------------------------------+    |  |
|                     +-----------------------------------------------+  |
+------------------------------------------------------------------------+
```

## Description

This is a portfolio demonstration project built by a Senior Cloud/DevOps Engineer. It solves a real FinOps problem: understanding unexpected AWS billing spikes using Generative AI (AWS Bedrock).

It showcases:

- **Infrastructure as Code**: Terraform (VPC, EKS, IAM, Helm).
- **GitOps**: ArgoCD driving the Kubernetes deployments (App of Apps pattern).
- **Software Engineering**: Python logic strictly adhering to Domain-Driven Design (DDD) and Test-Driven Development (TDD).
- **Containerization**: Dockerized application deployed as a Kubernetes CronJob.
- **Operations Make**: Abstracted operational commands via `Makefile`.
- **Observability**: Prometheus, Loki, and Grafana.
- **CI/CD**: GitHub Actions pipeline.

## Demo Instructions (For Hiring Managers)

**WARNING:** This project provisions an EKS cluster and other AWS resources. To avoid charges, you **MUST** destroy the infrastructure immediately after your demo.

### 1. Run the Tests (TDD Proof)

```bash
make test
```

### 2. Deploy Infrastructure & GitOps

This command initializes Terraform, provisions EKS and ArgoCD, and then automatically applies the ArgoCD App of Apps manifests.

```bash
make deploy
```

### 3. Run the AI Simulation in K8s

Since the Python engine is now a Dockerized CronJob managed by ArgoCD, you can trigger it manually to see the logs immediately:

```bash
kubectl create job --from=cronjob/cloudsense-ai-job manual-run-1 -n cloudsense-app
kubectl logs -f job/manual-run-1 -n cloudsense-app
```

### 4. CLEANUP (CRITICAL)

```bash
make destroy
```

Wait for completion and verify in the AWS Console.
