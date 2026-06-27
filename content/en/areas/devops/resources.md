# DevOps — Technologies, Links & Standards

## Internal Resources
- **Confluence**: `DevOps Runbooks` space — incident playbooks, deployment guides
- **Linear**: `DEVOPS` project
- **GitHub**: `technova/infra` (Terraform), `technova/k8s-manifests` (ArgoCD)
- **Datadog**: All `nova-infra-*` dashboards
- **ArgoCD**: Internal URL provided by team lead
- **Vault**: Secret management (access via team lead)

## Tech Documentation

### Kubernetes
- Cluster: EKS on AWS (us-east-1 primary, eu-west-1 DR)
- Namespaces: `nova-staging`, `nova-prod`, `nova-monitoring`
- Resource requests/limits required on all pods
- HPA configured for API and worker deployments

### Terraform
- State in S3 + DynamoDB locking
- Module structure: `modules/` for reusable components
- All changes via PR, never `terraform apply` locally on prod
- `terraform plan` output added to PR description

### GitHub Actions
- Workflows in `.github/workflows/`
- Required checks: lint, test, security scan, build
- Secrets stored in GitHub Secrets, accessed via `${{ secrets.X }}`
- Matrix builds for multi-arch Docker images (amd64 + arm64)

### ArgoCD
- GitOps: K8s manifests in `technova/k8s-manifests` repo
- App-of-apps pattern for managing multiple services
- Auto-sync enabled for staging, manual for production

### Datadog
```
# Key dashboards
nova-backend-api      # API latency, error rates
nova-infra-overview   # Cluster health, node utilization
nova-db-postgres      # Database performance
nova-kafka-consumer   # Kafka consumer lag
```

## Standards & Policies
- All infra changes via PR (no console clicking)
- Minimum 2 AZs for all production workloads
- Backups: daily snapshots, 30-day retention for prod RDS
- Secrets rotation: every 90 days via Vault
- Container images: non-root user, read-only filesystem where possible

## Useful Commands
```bash
# Check pod logs
kubectl logs -n nova-prod deployment/api-gateway --tail=100

# Port-forward to staging service
kubectl port-forward -n nova-staging svc/user-service 8080:80

# Terraform plan
cd infra/aws && terraform plan -var-file=staging.tfvars

# Check ArgoCD app status
argocd app list
argocd app sync nova-staging
```

## Key Contacts
- **Senior DevOps Engineer**: Architecture, Terraform ownership
- **#devops** Slack: infrastructure discussions
- **#incidents** Slack: active incidents (auto-created by PagerDuty)
