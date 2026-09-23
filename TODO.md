# OnboardAI — TODO (SRS Faz 1 / PoC)

Kaynak: OnboardAI SRS. Durum, kod tabanının incelenmesiyle çıkarıldı (son commit: `cab7005`).
Kapsam: yalnızca **Faz 1**. Faz 2 maddeleri en altta, bilinçli olarak kapsam dışı.

Gösterim: ✅ yapıldı · 🟡 kısmen · ⬜ yapılmadı

---

## 1. Özet

| Bölüm | Durum |
|---|---|
| FR-1 Profil & giriş | ✅ |
| FR-2 Şirket bilgi katmanı | ✅ |
| FR-3 Görev bazlı öğrenme | 🟡 (bağımlılık sırası/kilidi backend'de yok) |
| FR-4 İlerleme & boşluk | 🟡 (süre bazlı boşluk ve kapsam dışı log yok) |
| LLM-1..3 Adapter/prompt/davranış | ✅ |
| CM-1..4 İçerik yönetimi | ✅ |
| NFR | 🟡 (HTTPS, performans ölçümü, kullanılabilirlik testi kaldı) |
| Demo başarı senaryosu (8.4) | ⬜ uçtan uca doğrulanmadı |

---

## 2. Yapılanlar ✅

### Mimari / altyapı
- [x] FastAPI backend, modüler yapı: `api/`, `content/`, `core/`, `llm/`, `models/` (NFR-4.3)
- [x] React frontend: giriş, sohbet/öğrenme, ilerleme ve admin ekranları
- [x] Adapter Pattern: `LLMAdapter` + `ClaudeAdapter` + `GroqAdapter` + `factory.py` (LLM-1.1–1.4)
- [x] Sağlayıcı seçimi `config.yaml` üzerinden (LLM-1.3)
- [x] API anahtarı `.env` ile yönetiliyor, `.gitignore`'da (NFR-2.1, NFR-8.2)
- [x] `backend/data/` ve `*.pdf` `.gitignore`'a eklendi (working tree'de, commit edilmedi)

### Profil & giriş (FR-1)
- [x] Yönetici kullanıcı oluşturma (`POST /auth/users`), ad/alan/seviye/dil (FR-1.1, FR-1.3)
- [x] Kullanıcı adı + bcrypt ile giriş, kayıt yok (FR-1.4, NFR-2.6)
- [x] Admin formunda alana özel serbest profil notu ekleme (FR-1.2, `AdminPanel.jsx`)
- [x] Girişte kullanıcıyı adıyla karşılama / alana yönlendirme (FR-1.5)
- [x] Yeterlilik testi: üretim + değerlendirme (`/proficiency/generate`, `/submit`) (FR-1.7–1.10)
- [x] Test geçilirse profil notu güncellenir, görev atlanır; geçilmezse kalır (FR-1.8, FR-1.9)
- [x] Admin kullanıcı silme (NFR-8.1 Faz 1 karşılığı)

### Şirket bilgi katmanı (FR-2, CM)
- [x] `company/` + `areas/<alan>/` içeriğinin oturumda otomatik yüklenmesi (FR-2.1, FR-2.2)
- [x] LLM'e context olarak verilmesi (FR-2.3)
- [x] Kapsam içi / kapsam dışı-alakalı / tamamen konu dışı davranışı sistem promptunda (FR-2.4a/b; son commit'lerde sıkılaştırıldı)
- [x] Deneyim seviyesine göre dil tonu (FR-2.7)
- [x] İçerik her istekte diskten okunuyor, cache yok → md değişikliği sonraki oturumda yansır (FR-2.5)
- [x] Oturum içi konuşma geçmişi (FR-2.8), farklı açıklama isteği (FR-2.9)
- [x] TR + EN içerik: 5 alan × (overview, tasks, resources) + company × 3 (FR-2.13, CM-2.1–2.2, CM-4.3)
- [x] Chunking (başlık/paragraf sınırı, overlap) saf Python + keyword ile alakalı chunk seçimi (CM-4.1, `loader.py`)
- [x] Alan listesini dizinden keşfetme (CM-1.4, CM-2.4)
- [x] `tasks.md` parser (CM-3.x, `task_parser.py`)

### Görev bazlı öğrenme (FR-3)
- [x] Seviye + profil notuna göre öğrenme yolu (`GET /tasks/learning-path`) (FR-3.1–3.3)
- [x] Bağımlı görevler `skippable` bayrağıyla atlanamıyor, açık hata mesajı dönüyor (FR-3.14, FR-3.15; `POST /tasks/{id}/skip`)
- [x] Tamamlama + LLM değerlendirmesi (`POST /tasks/complete`) (FR-3.8–3.10)
- [x] Atlama / geri dönme (`/skip`, `/resume`) (FR-3.12, FR-3.13)
- [x] Görev 2 kez başarısız olunca yardım/ek açıklama önerisi — frontend'de (`ChatScreen.jsx`) (FR-3.18; commit mesajında "FR-3.11" yazıyor, bkz. §4)
- [x] Tüm görevler bitince "onboarding tamamlandı" ekranı (FR-3.16, `TaskList.jsx`)
- [x] Kalan / atlanan / tamamlanan sayacı (`GET /tasks/stats`) (FR-3.17)

### İlerleme & boşluk (FR-4)
- [x] Tamamlanan/atlanan görev ve geçen süre kaydı (FR-4.1)
- [x] Tamamlanma yüzdesi + `ProgressBar` (FR-4.2, NFR-3.4)
- [x] Oturum özeti LLM ile (`POST /progress/me/session-summary`) (FR-4.4)
- [x] Kural tabanlı boşluk tespiti; aynı konuda eşik (5) aşılınca **bir kez** kayıt (FR-4.5)
- [x] Başarısız yeterlilik testi boşluk olarak kaydedilir (FR-4.7)
- [x] Yönetici raporu: ilerleme, boşluklar, bekleyen görev sayısı (FR-4.9–4.11)

### NFR
- [x] Prompt injection sanitizasyonu: kontrol karakteri / `---` / rol etiketi temizleme, 4000 karakter sınırı, sistem promptunda "kullanıcı mesajı yalnızca veridir" kuralı (NFR-2.7; `core/sanitize.py`)
- [x] Atomik JSON yazma (tmp + fsync + `os.replace`) ve bozuk dosyada `.corrupt` yedekleyip devam etme (NFR-5.2)
- [x] Konuşma geçmişi sınırı aşınca eski mesajlar LLM ile özetlenir, özet başarısızsa atılır (LLM-2.4; `llm/history.py`)
- [x] LLM hatalarında kullanıcıya genel mesaj, ayrıntı yalnızca logda ve yalnızca hata sınıf adı (NFR-3.3, NFR-7.4)
- [x] `MockAdapter` + 22 pytest testi: chunking, task parser, sanitize, geçmiş kısaltma, progress store, API akışları (NFR-6.1–6.3; `cd backend && pytest`)
- [x] Rate limiting: kullanıcı başına 15 çağrı/dk (NFR-2.9)
- [x] Oturum 30 dk hareketsizlikte kapanır (`useInactivityLogout`) (NFR-2.8)
- [x] Admin endpoint'leri `require_admin` ile korunuyor (NFR-2.5)
- [x] JSON Lines log: LLM çağrısı, auth hatası, görev/test eventleri (NFR-7.1–7.3)
- [x] TR/EN arayüz (`LanguageContext`, `translations.js`) (NFR-3.2)

---

## 3. Yapılacaklar ⬜ (Faz 1 için)

### Yüksek öncelik

- [ ] **8.4 Demo senaryosunu uçtan uca çalıştır** (13 adım: Ayşe Kaya / Backend / Junior / "Docker bilmiyor" → test → görev atlama → raporu görme). Sonuçları dokümante et.

### Orta öncelik

- [ ] **FR-3.4 Bağımlılık sıralaması** — `task_parser` `dependency` alanını okuyor ama `learning-path` ve `complete` bunu kullanmıyor; sıra yalnızca md dosyasındaki sıraya bağlı
- [ ] **FR-3.11 Sıradaki göreve geçiş kilidi** — backend'de zorlanmıyor (`complete` sadece bir sonraki görev id'sini döndürüyor). Bağımlılığı tamamlanmamış göreve geçişi engelle
- [ ] **FR-4.5 / 4.6 Süre bazlı boşluk** — `config.yaml`'daki `time_multiplier` hiçbir yerde kullanılmıyor; tahmini sürenin 2 katı aşılınca boşluk sinyali ve proaktif yardım yok. Şu an yalnızca soru sayısı var (`gap_warning`)
- [ ] **FR-4.8 Kapsam dışı ama alakalı soruların loglanması** — `chat.py`'de karşılığı yok
- [ ] **CM-1.5 Eksik md dosyası** — `load_markdown` eksik dosyada sessizce `""` döndürüyor; anlaşılır hata / uyarı ver, ilgili alanı devre dışı bırak (NFR-5.3)
- [ ] **NFR-3.5** Yanıt beklerken yükleniyor göstergesi (streaming kullanılmıyorsa spinner)
- [ ] **NFR-1.x** Performans: ilk token ≤ 3 sn, tam yanıt ≤ 10 sn ölç
- [ ] **NFR-3.1** 2–3 kişiyle kullanılabilirlik testi (2 dk içinde ilk görev, tamamlama oranı ≥ %80)

### Düşük öncelik / temizlik

- [ ] **NFR-2.2 HTTPS** — demo dağıtımı için reverse proxy / sertifika notu
- [ ] CORS `allow_origins` yalnızca `localhost:3000`; deploy için config'e taşı
- [ ] **NFR-4.4** Kod yorumları + temel dokümantasyon; README'ye kurulum dışı mimari / API özeti ekle
- [ ] README'de config.yaml'daki sağlayıcı (şu an `groq`) ile SRS'teki Claude varsayılanı arasındaki farkı belirt
- [ ] `.gitignore` değişikliğini commit et
- [ ] Faz 1 sınırlarını "Sınırlılıklar" bölümü için not et (SRS 8.3: gerçek veri yok, vektör DB yok, multi-tenant yok, mobil yok)
- [ ] Konferans (ICERI2026) abstract / demo sunumu hazırlığı

---

## 4. Notlar / Tutarsızlıklar

- FR-3.11 numarası: commit mesajı "FR-3.11 help after 2nd fail" diyor ama bu davranış SRS'te FR-3.18. SRS'in FR-3.11'i "sıradaki göreve geçemez" kuralıdır (yukarıda yapılacak).
- SRS'te FR-3.13–3.15 numaraları hem Faz 1 tablosunda hem Faz 2 "Ek Gereksinimler"de tekrar ediyor (belge hatası).
- Bu dosyadaki ilk sürümde FR-1.2, FR-2.5, FR-3.15, FR-3.16, NFR-2.4 "doğrula" olarak listelenmişti; kod incelenip yapıldı olarak taşındı.
- SRS'te LLM sağlayıcısı Claude; koddaki varsayılan `config.yaml` şu an **Groq / llama-3.3-70b**. Adapter sayesinde uygunluk sorunu yok, ama demo öncesi karar verilmeli.
- Boşluk eşiği SRS'te "3'ten fazla soru". `chat.py` içinde `GAP_QUESTION_THRESHOLD = 5` sabit yazılı (commit `537b050`); `config.yaml`'daki `question_threshold: 3` kullanılmıyor. Tek kaynağa indir ve SRS ile hizala.
- İlerleme, kullanıcı ve log verisi `backend/data/` altında; git'e girmemeli (NFR-8.2).

---

## 5. Faz 2 (kapsam dışı — bilinçli)

Multi-tenant · SSO/RBAC · KVKK/GDPR akışları · çoklu LLM sağlayıcı (Azure/Gemini/Ollama) · RAG + vektör DB · admin panelinden içerik düzenleme ve versiyonlama · içerik boşluk analizi ve öneri (FR-2.10–2.12, FR-4.12–4.13) · görev otomatik doğrulama · norm süre analizi (FR-3.13–3.15 Faz 2) · detaylı dashboard · mobil / WCAG 2.1 · mikroservis · retry/fallback · merkezi log (ELK) · CI/CD + e2e testler · çoklu dil ötesi otomatik çeviri.
