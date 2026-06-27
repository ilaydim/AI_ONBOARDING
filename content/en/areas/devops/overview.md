# DevOps & Platform Team

The team responsible for infrastructure, CI/CD, reliability, and platform tooling at TechNova.

## Team Structure
- 5 DevOps/Platform engineers (1 junior, 2 mid, 2 senior)
- 1 Engineering Manager (shared with Backend)

## Tech Stack
- **Container Orchestration**: Kubernetes (EKS on AWS)
- **CI/CD**: GitHub Actions + ArgoCD (GitOps)
- **IaC**: Terraform
- **Monitoring**: Datadog (metrics, logs, APM, alerts)
- **Secrets**: HashiCorp Vault
- **Registry**: AWS ECR

## Responsibilities
- Infrastructure provisioning and maintenance
- CI/CD pipeline development and optimization
- Kubernetes cluster management
- Security patching and compliance
- On-call for infrastructure incidents
- Cost optimization (FinOps)

## Infrastructure Overview

### AWS Services Used
- **EKS**: Kubernetes worker nodes
- **RDS**: PostgreSQL (Multi-AZ, automated backups)
- **ElastiCache**: Redis cluster
- **MSK**: Managed Kafka
- **S3**: Object storage, Terraform state
- **CloudFront**: CDN for frontend assets
- **Route53**: DNS management

### Environments
| Environment | Purpose | Auto-deploy |
|---|---|---|
| local | Developer machines | No |
| staging | QA and testing | Yes (on merge to main) |
| production | Live traffic | Manual (release tag) |

## GitOps Flow
1. Developer merges PR → GitHub Actions tests pass
2. GitHub Actions builds Docker image, pushes to ECR
3. ArgoCD detects new image tag in K8s manifests
4. ArgoCD syncs staging cluster automatically
5. Production deploy: tag release → manual ArgoCD sync

## On-Call
- DevOps engineers rotate 1-week on-call
- PagerDuty alerts for: high error rates, latency spikes, pod crashes, disk alerts
- Runbooks in Confluence `DevOps Runbooks` space
- Post-mortems required for P0 and P1 incidents
