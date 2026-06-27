# QA Kaynaklar

## Test Araçları

- **Playwright** — E2E browser otomasyonu
- **pytest** — Backend ve entegrasyon testleri
- **k6** — Yük ve performans testleri
- **Jira** — Bug tracker (QA board)

## Test Ortamı

- URL: `staging.technova.internal`
- Test kullanıcıları: `test_user_1 / TestPass123` (staging-only)
- Test veritabanı: staging DB (gerçek veriden izole)

## Sık Kullanılan Komutlar

```bash
# E2E testleri çalıştır
npx playwright test
npx playwright test --headed       # browser görünür şekilde
npx playwright test tests/login.spec.ts  # tek dosya

# Backend testleri
pytest tests/ -v
pytest tests/test_api.py::test_login -v  # tek test
pytest --cov=app tests/            # coverage raporu

# Yük testi (k6)
k6 run scripts/load-test.js
k6 run --vus 50 --duration 60s scripts/load-test.js
```

## Coverage Standartları

| Alan | Minimum Coverage |
|---|---|
| Backend (Python) | %80 |
| Frontend (React) | %70 |
| API entegrasyon | %90 (kritik endpoint'ler) |

## Bug Rapor Şablonu

```
BAŞLIK: [Kısa, etkili açıklama]
SEVERITY: P0 / P1 / P2 / P3
ORTAM: local / staging / prod
TARAYICI: Chrome 124 / Firefox / Safari
ADIMLAR:
  1. /login adresine git
  2. emp1 / emp1 ile giriş yap
  3. "Tasks" sekmesine tıkla
BEKLENEN: Görev listesi görünür
GERÇEKLEŞEN: Sayfa boş kalıyor
LOG / EKRAN GÖRÜNTÜSÜ: [ekle]
```

## Faydalı Linkler

- Playwright dokümantasyonu: [playwright.dev](https://playwright.dev)
- pytest dokümantasyonu: [docs.pytest.org](https://docs.pytest.org)
- k6 dokümantasyonu: [k6.io/docs](https://k6.io/docs)
- Jira QA Board: `jira.technova.internal/projects/QA`
