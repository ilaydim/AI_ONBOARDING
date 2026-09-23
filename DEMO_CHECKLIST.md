# Demo ve Doğrulama Kontrol Listesi (SRS Faz 1)

Otomatik testler (`cd backend && pytest`) sahte LLM kullanır. Bu liste, **gerçek LLM ve arayüzle** elle yapılması gereken doğrulamalardır.

## 0. Hazırlık
- [ ] `backend/.env` içinde `config.yaml`'daki sağlayıcının anahtarı var (`groq` → `GROQ_API_KEY`, `claude` → `ANTHROPIC_API_KEY`)
- [ ] Backend: `cd backend && source .venv/bin/activate && uvicorn app.main:app --reload`
- [ ] Frontend: `cd frontend && npm start` → http://localhost:3000
- [ ] `backend/data/users.json` içinde `ayse` kullanıcısı zaten var. Temiz demo için yeni bir kullanıcı adı kullan (ör. `ayse.demo`) veya eski kullanıcının `progress_<id>.json` dosyasını sil
- [ ] Admin: `admin` / `admin123` (yoksa `python seed_admin.py`)

## 1. Demo senaryosu (SRS 8.4) — çıktıyı not et / ekran görüntüsü al

| # | Adım | Beklenen | Sonuç | Not |
|---|---|---|---|---|
| 1 | Yönetici girişi | Admin paneli açılır | ☐ | |
| 2 | Çalışan oluştur: Ayşe Kaya, Backend, Junior, notlar: `Python`=biliyor, `Docker`=bilmiyor | Kullanıcı listede görünür | ☐ | |
| 3 | Çıkış yap, Ayşe ile giriş | "Ayşe" adıyla karşılanır, backend alanına yönlenir | ☐ | |
| 4 | Sol kenar çubuğunda "Docker" notunun yanındaki itiraz butonuna tıkla | Yeterlilik testi penceresi açılır | ☐ | |
| 5 | Docker testini başlat | LLM 3–5 soru üretir | ☐ | |
| 6 | Testi geçecek şekilde çöz (≥ %70) | Not doğrulanır, **"Servisi Docker ile Konteynerleştir" görevi listeden kalkar** | ☐ | |
| 7 | Görev listesinde ilerle, ilk göreve soru sor | Yanıt gelir; ikinci görev 🔒 kilitli | ☐ | |
| 8 | Şirketle ilgili bir soru sor (ör. "Mimari nasıl?") | md içeriğine dayalı yanıt, kaynak notu **yok** | ☐ | |
| 9 | Alanla ilgili ama md'de olmayan soru (ör. "Kubernetes nedir?") | Yanıt + "genel teknik bilgimden geliyor" notu | ☐ | |
| 9b | Tamamen konu dışı soru (ör. "Bugün hava nasıl?") | Kibarca reddeder | ☐ | |
| 10 | Bir görevi tamamla (çıktıyı yaz) | LLM değerlendirir, geçerse görev tamamlanır, sıradaki açılır | ☐ | |
| 11 | İlerleme ekranı | Tamamlanan görev ve yüzde güncellenir | ☐ | |
| 12 | Oturum özeti al | LLM 3 noktalı özet üretir | ☐ | |
| 13 | Yönetici olarak Ayşe'nin raporuna bak | Yüzde, boşluklar (9. adımdaki soru dahil), test sonucu görünür | ☐ | |

Ek kontroller:
- [ ] Aynı göreve 5+ soru sor → boşluk uyarısı çıkar, raporda `question_count` boşluğu görünür
- [ ] Aynı görevi 2 kez başarısız tamamla → yardım önerisi çıkar
- [ ] Atlanamaz görevde (backend-001) "Atla" butonu görünmez; atlanabilir görevlerde görünür
- [ ] Atlanabilir görevi atla → listede "atlandı", geri dönebilir
- [ ] TR ↔ EN dil değişimi: arayüz **ve** LLM yanıtları değişir
- [ ] Backend'i kapat, mesaj gönder → anlaşılır hata mesajı, oturum kaybolmaz, teknik detay yok
- [ ] 30 dk hareketsizlik sonrası otomatik çıkış (test için `useInactivityLogout.js` içindeki `TIMEOUT_MS` geçici kısaltılabilir)

## 2. Performans ölçümü (NFR-1) — Faz 1 hedefleri

Tarayıcı DevTools → Network sekmesi ile `POST /chat` süresine bak (5 farklı soru, ortalama al).

| Ölçüt | Hedef | Ölçülen |
|---|---|---|
| Sayfa yüklenme (NFR-1.2) | ≤ 3 sn | |
| Tam yanıt süresi (NFR-1.1b, streaming yok) | ≤ 10 sn | |
| md yükleme + chunking (NFR-1.3) | ≤ 5 sn | |

`md yükleme + chunking` için (bu makinede ~0.002 sn ölçüldü): `cd backend && python -c "import time;from app.content.loader import build_context;t=time.time();build_context('backend','test','tr');print(time.time()-t)"`

Not: Uygulama streaming kullanmıyor; SRS'e göre bu durumda tam yanıt süresi (NFR-1.1b) esas alınır.

## 3. Kullanılabilirlik testi (NFR-3.1) — 2–3 kişi

Katılımcıya yalnızca kullanıcı adı/şifre ver, yönlendirme yapma. Süre tut.

| Katılımcı | İlk göreve ulaşma süresi (hedef ≤ 2 dk) | Görevi tamamladı mı? | Takıldığı yer | Yorum |
|---|---|---|---|---|
| 1 | | ☐ | | |
| 2 | | ☐ | | |
| 3 | | ☐ | | |

Başarı ölçütü: görev tamamlama oranı ≥ %80.
