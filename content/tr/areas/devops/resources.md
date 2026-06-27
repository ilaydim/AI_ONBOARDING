# DevOps Kaynaklar

## İç Repolar

- `technova/infra` — Terraform modülleri ve değişken dosyaları
- `technova/k8s-manifests` — Kubernetes deployment ve service tanımları
- `technova/runbooks` — Operasyonel playbook'lar ve incident rehberleri
- `technova/helm-charts` — Ortak Helm chart'ları

## Araç Dokümantasyonu

- **Kubernetes**: [kubernetes.io/docs](https://kubernetes.io/docs)
- **Terraform**: [developer.hashicorp.com/terraform](https://developer.hashicorp.com/terraform)
- **ArgoCD**: [argo-cd.readthedocs.io](https://argo-cd.readthedocs.io)
- **GitHub Actions**: [docs.github.com/actions](https://docs.github.com/actions)
- **Datadog**: [docs.datadoghq.com](https://docs.datadoghq.com)

## Sık Kullanılan Komutlar

```bash
# Cluster durumu
kubectl get nodes
kubectl get pods -n technova

# ArgoCD uygulama durumu
argocd app list
argocd app sync technova-backend

# Terraform
terraform plan -var-file=staging.tfvars
terraform apply -var-file=prod.tfvars

# Log stream (Datadog Agent)
kubectl logs -f deployment/technova-backend -n technova
```

## Datadog Dashboardları

- **API Latency**: `datadog.internal/d/api-latency` — istek sürelerini izle
- **Cluster Health**: `datadog.internal/d/k8s-health` — pod ve node sağlığı
- **Error Rate**: `datadog.internal/d/error-rate` — 5xx oranları

## Yeni Üye Checklist

- [ ] AWS Console erişimi (IT'den talep et)
- [ ] `technova/infra` reposuna push yetkisi
- [ ] Datadog hesabı aktif
- [ ] PagerDuty rotasyona eklendi
- [ ] Vault token alındı
