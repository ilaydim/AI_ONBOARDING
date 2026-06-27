# DevOps / Infrastructure Ekibi

TechNova'nın altyapısını ve CI/CD süreçlerini yöneten 5 kişilik ekip.

## Teknoloji Stack

| Kategori | Araç |
|---|---|
| Orkestrasyon | Kubernetes (AWS EKS) |
| IaC | Terraform |
| GitOps | ArgoCD |
| CI/CD | GitHub Actions |
| Gözlemlenebilirlik | Datadog, PagerDuty |
| Secret Yönetimi | HashiCorp Vault |
| CDN | AWS CloudFront |

## Ortamlar

| Ortam | Amaç | URL |
|---|---|---|
| dev | Geliştirici testleri | dev.technova.internal |
| staging | QA ve UAT | staging.technova.internal |
| prod | Canlı sistem | app.technova.com |

## GitOps Akışı

1. PR merge → GitHub Actions tetiklenir
2. Docker image build ve push (ECR)
3. ArgoCD yeni image'ı algılar
4. staging'e otomatik deploy
5. Onay sonrası prod'a deploy

## Sorumluluklar

- Kubernetes cluster operasyonu ve kapasitesi
- CI/CD pipeline bakımı ve iyileştirme
- Güvenlik, sertifika ve secret yönetimi
- Maliyet optimizasyonu ve kaynak takibi
- Incident müdahalesi ve post-mortem

## On-Call

- Rotasyon: Haftalık, her DevOps mühendisi sırayla
- Uyarılar: Datadog → PagerDuty → Slack #alerts
- SLA: Kritik olaylar için 15 dakika ilk müdahale
