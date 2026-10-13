# Doğrulama kapsamı

Tarih: 2026-10-13. Ortam: Linux, Python 3.12.14. Testler temiz `.venv` içinde `requirements-dev.txt` kurulumu sonrasında çalıştırıldı. Doğrudan bağımlılıklar `requirements.txt`, test bağımlılığı `requirements-dev.txt`, kurulan tam ortam `requirements-lock.txt` dosyasında kaydedilmiştir. Tam ortamı tekrarlamak için Python 3.12 ile `python -m pip install -r requirements-lock.txt` kullanılabilir.

## Sonuç

**38 test geçti**, uyarılar hata kabul edildi (`python -m pytest -q -W error`). `python -m pip check`: bozuk bağımlılık bulunmadı.

Kontrol edilen davranışlar:

- Kaynak SHA-256, 891 kayıt, 342 pozitif etiket ve 177 eksik yaş.
- Eksik/tekrarlı/geçersiz kimlik; hatalı sınıf, cinsiyet, liman, hedef ve sayısal değerlerin reddi.
- Kaynak dosyası değişince sağlama toplamı kontrolünün başarısız olması.
- Tekrarlı aktarımın satır çoğaltmaması; diğer tabloların korunması.
- CSV doğrulama hatasında ve SQL işlem hatasında mevcut verinin korunması.
- Eksik, eski ve sonradan değiştirilmiş veritabanının reddi.
- Beş gruplamada tüm yolcu ve hayatta kalan sayılarının korunması.
- Yaş 0/18/40 ve ücret 0/10/50/100 sınırları ile eksik değerler.
- Yedi SQL sorgusunun salt okunur veritabanında çalışması.
- Boş filtre sonucu, geçersiz filtre, 1. sınıf kadın filtresinde 94 kayıt / 91 hayatta kalan.
- HTTP ana sayfa, Dash layout/dependencies, CSS ve gerçek callback POST yanıtları.
- Ön işleme istatistiklerinin yalnızca eğitim kümesinden öğrenilmesi; bilinmeyen kategori tahmininin çalışması.
- Eğitim/test yolcu kimliklerinin ayrıklığı; 712/179 bölme; metriklerin karışıklık matrisiyle tutarlılığı.
- Cinsiyetten birebir türetilmiş etiketlerin model değerlendirmesinde reddi.

## Yeniden üretim

```bash
python import_csv_to_db.py
python generate_report.py
python model.py
python -m pytest -q -W error
python -m pip check
```

İlk üç komut da temiz sanal ortamda çalıştırıldı. Model test doğruluğu 142/179 = %79,33; karışıklık matrisi [[98,12],[25,44]]. Ayrıntılar `reports/model_metrics.json` içindedir.

## Doğrulanamayanlar

- Windows üzerinde yerel çalıştırma yapılmadı; Windows komutları standart Python venv kullanımına göre yazıldı.
- Chromium indirmesi bu ortamda bozuk/eksik paket döndürdüğü için gerçek tarayıcıda görsel/JavaScript testi tamamlanamadı. HTTP ve callback testleri bunun yerine görsel test yapılmış sayılmaz.
- Kaggle yarışmasına gönderim ve bağımsız dış veri doğrulaması yapılmadı.

Bu testler belirli hata sınıflarını denetler; yazılımın her olası ortamda hatasız olacağını garanti etmez.
