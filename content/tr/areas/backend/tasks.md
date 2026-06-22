# Görevler — Backend Development

## Görev: Şirket Mimarisini Öğren
- **ID:** backend-001
- **Seviye:** junior, mid, senior
- **Bağımlılık:** Yok
- **Beklenen Çıktı:** Mimariyi kendi cümlelerinle özetle, 3 ana bileşeni açıkla
- **Tamamlanma Kriteri:** En az 3 bileşeni doğru tanımlama ve aralarındaki ilişkiyi açıklama
- **Tahmini Süre:** 1 saat
- **Atlanabilir:** Hayır

## Görev: Yerel Ortamı Kur
- **ID:** backend-002
- **Seviye:** junior, mid
- **Bağımlılık:** backend-001
- **Beklenen Çıktı:** Uygulamanın yerel makinede çalışır hale getirilmesi
- **Tamamlanma Kriteri:** `uvicorn` çalışıyor ve `/health` endpoint'i 200 dönüyor
- **Tahmini Süre:** 2 saat
- **Atlanabilir:** Evet

## Görev: İlk Servisi Ayağa Kaldır
- **ID:** backend-003
- **Seviye:** junior, mid
- **Bağımlılık:** backend-002
- **Beklenen Çıktı:** Auth servisi yerel ortamda çalışıyor
- **Tamamlanma Kriteri:** Login endpoint'i test isteğine doğru yanıt veriyor
- **Tahmini Süre:** 1.5 saat
- **Atlanabilir:** Evet

## Görev: CI/CD Pipeline'ını İncele
- **ID:** backend-004
- **Seviye:** junior, mid, senior
- **Bağımlılık:** backend-001
- **Beklenen Çıktı:** Pipeline adımlarını ve tetikleyicileri açıkla
- **Tamamlanma Kriteri:** GitHub Actions workflow dosyasını oku ve 5 adımı sırayla açıkla
- **Tahmini Süre:** 1 saat
- **Atlanabilir:** Hayır

## Görev: Kod Review Standartlarını Öğren
- **ID:** backend-005
- **Seviye:** junior, mid, senior
- **Bağımlılık:** backend-001
- **Beklenen Çıktı:** PR standartları ve reviewer beklentilerini özetle
- **Tamamlanma Kriteri:** PR kurallarından 4 maddeyi doğru aktarma
- **Tahmini Süre:** 0.5 saat
- **Atlanabilir:** Hayır

## Görev: İlk PR'ı Aç
- **ID:** backend-006
- **Seviye:** junior, mid, senior
- **Bağımlılık:** backend-005
- **Beklenen Çıktı:** Küçük bir iyileştirme veya typo fix ile PR açılması
- **Tamamlanma Kriteri:** PR açıldı ve en az 1 yorum alındı
- **Tahmini Süre:** 2 saat
- **Atlanabilir:** Hayır

## Görev: Mimari Karar Belgelerini (ADR) İncele
- **ID:** backend-007
- **Seviye:** mid, senior
- **Bağımlılık:** backend-001
- **Beklenen Çıktı:** Son 3 ADR'yi özetle ve kararların gerekçelerini açıkla
- **Tamamlanma Kriteri:** 3 ADR özetlendi ve "neden bu karar?" sorusu yanıtlandı
- **Tahmini Süre:** 2 saat
- **Atlanabilir:** Evet

## Görev: Teknik Borç Raporunu Değerlendir
- **ID:** backend-008
- **Seviye:** senior
- **Bağımlılık:** backend-007
- **Beklenen Çıktı:** Mevcut teknik borç alanlarını önceliklendirerek listele
- **Tamamlanma Kriteri:** En az 3 teknik borç alanı tespit edildi ve azaltma önerisi sunuldu
- **Tahmini Süre:** 3 saat
- **Atlanabilir:** Evet
