# OnboardAI

AI destekli çalışan onboarding sistemi — ICERI2026 PoC

## Kurulum

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # ANTHROPIC_API_KEY ekle
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Proje Yapısı
```
onboardai/
├── backend/          # FastAPI + LLM Adapter
├── frontend/         # React
└── content/          # Markdown içerik dosyaları
    ├── tr/           # Türkçe
    └── en/           # İngilizce
```
