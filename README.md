# OnboardAI

AI destekli çalışan onboarding sistemi — ICERI2026 PoC (SRS Faz 1).

Yeni çalışanın deneyim seviyesine ve alanına göre kişiselleştirilmiş, görev bazlı bir öğrenme yolu sunar.
Şirket bilgisi Markdown dosyalarından gelir ve bir LLM ile konuşarak öğrenilir. İlerleme ve bilgi boşlukları takip edilir.

Yapılacaklar ve SRS'e göre durum: [TODO.md](TODO.md)

## Kurulum

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # GROQ_API_KEY veya ANTHROPIC_API_KEY ekle
python seed_admin.py   # ilk admin: admin / admin123 (demo için, değiştir)
uvicorn app.main:app --reload
```
API dokümantasyonu (Swagger): `http://localhost:8000/docs`

### Frontend
```bash
cd frontend
npm install
npm start
```

### Testler
Gerçek API anahtarı gerekmez; LLM `MockAdapter` ile taklit edilir.
```bash
cd backend
pytest
```

## LLM sağlayıcısı

Sağlayıcı `backend/config.yaml` içindeki `llm.provider` ile seçilir (`groq` veya `claude`), kod değişikliği gerekmez.
SRS varsayılanı Claude'dur; repodaki config şu an `groq` ile gelir. Yeni bir sağlayıcı eklemek için
`LLMAdapter` arayüzünü implemente eden bir adapter yazıp `llm/factory.py`'ye kaydetmek yeterlidir.

## Proje yapısı
```
├── backend/
│   ├── config.yaml          # LLM sağlayıcısı, chunk boyutu, boşluk eşikleri, CORS
│   ├── app/
│   │   ├── api/             # auth, chat, tasks, proficiency, progress, content
│   │   ├── content/         # md okuma, chunking, tasks.md parser, ilerleme (JSON)
│   │   ├── core/            # auth, sanitize, rate limit, JSON log, ayarlar
│   │   ├── llm/             # adapter arayüzü, Claude/Groq/Mock, prompt'lar, geçmiş kısaltma
│   │   └── models/
│   ├── tests/
│   └── data/                # çalışma verisi (users.json, ilerleme, log) — git'e girmez
├── frontend/                # React (giriş, sohbet + görevler, ilerleme, yönetici paneli)
└── content/
    ├── tr/                  # Türkçe içerik
    └── en/                  # İngilizce içerik
        ├── company/         # overview, culture, processes
        └── areas/<alan>/    # overview.md, tasks.md, resources.md
```

## Yeni alan / içerik ekleme
`content/<dil>/areas/<yeni-alan>/` altına `overview.md`, `tasks.md` ve `resources.md` koymak yeterlidir.
Görev şeması için mevcut bir `tasks.md`'ye bakın (ID, Seviye, Bağımlılık, Beklenen Çıktı, Tamamlanma Kriteri,
Tahmini Süre, Atlanabilir). Eksik/hatalı dosyalar uygulamayı çökertmez; ilgili alan devre dışı kalır.
Yönetici olarak `GET /content/health` içerik sorunlarını listeler.

## API özeti

| Uç nokta | Açıklama |
|---|---|
| `POST /auth/login` | Kullanıcı adı + şifre ile giriş (JWT) |
| `POST /auth/users`, `GET /auth/users`, `DELETE /auth/users/{id}` | Yönetici: kullanıcı yönetimi |
| `POST /chat`, `GET/DELETE /chat/history` | Konuşma tabanlı etkileşim |
| `GET /tasks/learning-path` | Kişiselleştirilmiş, bağımlılık sıralı görev listesi |
| `POST /tasks/complete`, `/tasks/{id}/skip`, `/tasks/{id}/resume`, `GET /tasks/stats` | Görev akışı |
| `POST /proficiency/generate`, `/proficiency/submit` | Yeterlilik testi |
| `GET /progress/me`, `/progress/me/gaps`, `POST /progress/me/session-summary` | Çalışan ilerleme özeti |
| `GET /progress/admin/{user_id}` | Yönetici: çalışan ilerleme raporu |
| `GET /content/areas`, `GET /content/health` | Alan listesi / içerik sağlığı (admin) |

## Dağıtım notları
- **HTTPS:** Uygulama sunucusu HTTP konuşur. Üretimde/demoda bir ters vekil (Nginx, Caddy vb.) ile TLS sonlandırılmalıdır (NFR-2.2).
- **CORS:** Frontend adresi `config.yaml` → `server.cors_origins`.
- **Sırlar:** API anahtarları ve `SECRET_KEY` yalnızca `.env` içinde tutulur; `.env` ve `backend/data/` git'e girmez.
- **Kimlik doğrulama:** Faz 1'de kullanıcı adı + bcrypt; oturum 30 dk hareketsizlikte kapanır.

## Faz 1 sınırlılıkları (SRS §8.3)
Gerçek şirket verisi yok (kurgusal "TechNova"), görev doğrulaması LLM değerlendirmesine dayanır, vektör veritabanı yok
(chunk seçimi anahtar kelime eşleştirmesiyle), tek şirket / multi-tenant yok, mobil arayüz yok, ilerleme ve kullanıcılar
JSON dosyalarında tutulur.
