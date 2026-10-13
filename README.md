# Titanic Veri Analizi

Titanic yolcu verilerinin **SQLite ile analiz edilmesi** ve **Python, Dash ve Plotly** kullanılarak etkileşimli bir gösterge panelinde görselleştirilmesi.

Proje; CSV'den veritabanına aktarım, veri kalitesi kontrolü, SQL ile gruplama ve görsel raporlama adımlarını bir araya getirir.

## Özellikler

- CSV verisini tek komutla SQLite'a aktarma.
- Yolcu sınıfı, cinsiyet, yaş ve bilet ücretine göre karşılaştırmalar.
- Grafiklerde değer inceleme, yakınlaştırma ve PNG indirme.
- Eksik değerlerin ayrı grupta gösterilmesi.
- Tekrar çalıştırılabilir, salt okunur SQL analiz sorguları.

## Veri hakkında önemli not

Depodaki `data/tested.csv` **418 yolcu** içerir. `Survived` sütunu, **418 satırın tamamında kadınlar için 1, erkekler için 0** değerindedir. Bu nedenle etiketler doğrulanmış tarihsel sonuçlar olarak kabul edilmez. Grafikler yalnızca bu dosyanın dağılımını gösterir; gerçek hayatta kalma oranlarını veya nedensel etkileri kanıtlamaz.

İlk sürümdeki Random Forest modeli bu etiketlerle eğitildiği için yüksek doğruluk, gerçek sonuçları tahmin etme başarısı şeklinde yorumlanamaz. Ana uygulama bu yanıltıcı başarı göstergesini içermez. Cinsiyete göre ortalama karşılaştırması da randomize bir A/B testi değildir.

Veri, proje arşivindeki `tested.csv` dosyasından alınmıştır. İlk proje dokümanı kaynak olarak Kaggle'ı belirtir; belirli veri sayfasının URL'si ve lisansı arşivde doğrulanamamıştır. Bu sınırlılık özellikle belirtilmiştir; veri için bir lisans iddiasında bulunulmaz.

## Kurulum

Python 3.11 veya üzeri kullanın. Aşağıdaki komutları proje klasöründe çalıştırın.

```bash
git clone https://github.com/ulhnysf/titanic-data-analysis.git
cd titanic-data-analysis
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Ardından:

```bash
python -m pip install -r requirements.txt
python import_csv_to_db.py
python app.py
```

Tarayıcıda **http://127.0.0.1:8050** adresini açın. Uygulamayı kapatmak için terminalde `Ctrl+C` kullanın. Aktivasyon engellenirse Windows'ta komutlardaki `python` yerine `.\.venv\Scripts\python.exe` kullanabilirsiniz.

SQLite, Python standart kütüphanesine dahildir; ayrıca `pip install sqlite3` çalıştırmayın. Veritabanı `data/titanic.db` olarak oluşturulur ve Git'e eklenmez. Aktarım komutunu tekrar çalıştırmak `tested` tablosunu CSV'den yeniden oluşturur.

## Proje yapısı

| Dosya / klasör | İçerik |
| --- | --- |
| `app.py` | Türkçe Dash gösterge paneli |
| `import_csv_to_db.py` | Veri doğrulama ve SQLite aktarımı |
| `data/tested.csv` | Analizde kullanılan veri |
| `sql/analysis.sql` | Veri kalitesi ve grup karşılaştırması sorguları |
| `requirements.txt` | Uygulamanın bağımlılıkları |
| `docs/validation.md` | Kontroller ve veri bulguları |
| `docs/original/` | İlk sürüm kodları ve yöntem notu |

SQL sorgularını bir SQLite istemcisinde `data/titanic.db` üzerinde çalıştırabilirsiniz. Grafikler mevcut etiketleri özetler; model eğitimi veya hipotez testi çalıştırmaz.

## Veri özeti

| Kontrol | Sonuç |
| --- | ---: |
| Yolcu sayısı | 418 |
| Eksik yaş | 86 |
| Eksik bilet ücreti | 1 |
| Eksik kabin | 327 |
| Cinsiyet kuralıyla eşleşen etiket | 418 / 418 |

Yaş grupları: 18 yaş altı, 18–39, 40 ve üzeri. Bilet ücreti grupları: 10 altı, 10–50 arası, 50–100 arası, 100 ve üzeri; üst sınırlar bir sonraki gruba dahildir. Eksik değerler `Bilinmiyor` olarak ayrı tutulur.

## Teknolojiler

Python · pandas · SQLite · Dash · Plotly

İlk sürümün makine öğrenmesi denemesi scikit-learn kullanır; güncel gösterge panelinin bağımlılığı değildir. Eğitim sertifikaları, kullanılan teknolojilerin kanıtı olarak uygulama bağımlılıklarına eklenmemiştir.

## Geliştirme alanları

- Kaynağı ve lisansı doğrulanmış, gerçek sonuç etiketli veriyle analizi tekrarlamak.
- Bu veri sağlandıktan sonra eğitim/test ayrımından sonra ön işleme yapan bir model hattı kurmak.
- Panel için sınıf ve yaş filtreleri eklemek.

## Yazar

Uluhan Yusuf Dokay
