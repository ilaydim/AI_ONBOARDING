# Backend Kaynaklar ve Standartlar

## Kod Standartları
- PEP 8 + Black formatter (zorunlu)
- Tip anotasyonu zorunlu (mypy strict)
- Docstring: Google style
- Test coverage: minimum %80

## Önemli Repolar
- `technova/core-api` — Ana API (FastAPI)
- `technova/data-pipeline` — ETL süreçleri
- `technova/auth-service` — Kimlik doğrulama servisi

## Geliştirme Ortamı Kurulumu
```bash
git clone git@github.com:technova/core-api.git
cd core-api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker-compose up -d  # DB + Redis
uvicorn app.main:app --reload
```

## PR Süreci
1. Feature branch: `feat/JIRA-123-kısa-açıklama`
2. En az 2 reviewer onayı gerekli
3. CI yeşil olmadan merge yok
4. Squash merge zorunlu
