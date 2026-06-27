# QA / Test Ekibi

Test stratejisi, otomasyon ve hata yönetiminden sorumlu 4 kişilik ekip.

## Test Piramidi

| Seviye | Oran | Araç | Yazan |
|---|---|---|---|
| Unit | %60 | pytest, Jest | Geliştiriciler |
| Integration | %25 | pytest, Supertest | QA + Dev |
| E2E | %15 | Playwright | QA |
| Yük / Performans | Ayrıca | k6 | QA |

## Test Ortamları

- **local**: Geliştirici makinesi, birim testler
- **staging**: `staging.technova.internal` — entegrasyon ve E2E
- **prod (shadow)**: Yalnızca smoke testler, canlı veri okunmaz

## Bug Severity SLA

| Severity | Tanım | Çözüm Süresi |
|---|---|---|
| P0 - Critical | Canlıda servis tamamen çökmüş | 2 saat |
| P1 - High | Kritik kullanıcı akışı bozuk | 24 saat |
| P2 - Medium | Özellik eksik ama workaround var | Sprint içi |
| P3 - Low | Kozmetik, ufak davranış | Backlog |

## Definition of Done

Bir feature "done" sayılmadan önce:
- [ ] Unit testler yazıldı ve geçti
- [ ] Integration testler geçti
- [ ] E2E happy path testi yazıldı
- [ ] Staging'de QA onayı alındı
- [ ] PR review yapıldı
- [ ] Dokümantasyon güncellendi

## Hata Raporlama

Bug'lar Jira'da raporlanır. Şablon:
```
Başlık: [Kısa, etkili açıklama]
Severity: P0/P1/P2/P3
Ortam: staging / prod
Adımlar: 1. ... 2. ... 3. ...
Beklenen: ...
Gerçekleşen: ...
Ekran görüntüsü / log: ...
```
