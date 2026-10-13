# Titanic Veri Analizi

Titanic yolcu verilerinin **SQL ile incelenmesi**, **Dash ve Plotly ile görselleştirilmesi** ve **Random Forest ile değerlendirilmesi**.

Python · pandas · SQLite · Dash · Plotly · scikit-learn

## Projenin kapsamı

- Kaynağı belirtilmiş 891 yolcu kaydı üzerinde keşifsel analiz.
- Yolcu sınıfı ve cinsiyet filtreleriyle güncellenen beş grafik.
- Sınıf, cinsiyet, yaş, bilet ücreti ve biniş limanına göre SQL özetleri.
- Eksik veri, geçersiz değer, tekrar eden kimlik ve kaynak bütünlüğü kontrolleri.
- Eğitim verisinde öğrenilen ön işleme ve ayrı test kümesiyle model değerlendirmesi.
- Yeniden üretilebilir CSV/Markdown raporları ve otomatik regresyon testleri.

## Hızlı başlangıç

Doğrulanan ortam **Python 3.12**'dir. Windows PowerShell'de:

```powershell
git clone https://github.com/ulhnysf/titanic-data-analysis.git
cd titanic-data-analysis
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe import_csv_to_db.py
.\.venv\Scripts\python.exe app.py
```

Sanal ortamı etkinleştirmek zorunlu değildir; yukarıdaki komutlar doğrudan o ortamın Python'unu kullanır.

macOS / Linux (Python 3.12 kurulu olmalı):

```bash
git clone https://github.com/ulhnysf/titanic-data-analysis.git
cd titanic-data-analysis
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python import_csv_to_db.py
.venv/bin/python app.py
```

Tarayıcıda **http://127.0.0.1:8050** adresini açın. Kapatmak için terminalde `Ctrl+C` kullanın. Sunucu yalnızca yerel bilgisayarı dinler. Bu geliştirme sunucusu internete açık üretim dağıtımı için tasarlanmamıştır.

SQLite Python ile birlikte gelir; ayrıca kurulmaz. Veritabanı `data/titanic.db` olarak üretilir. Aktarım komutu `passengers` tablosunu yeniden oluşturur; farklı adlı tabloları korur. Önceki sürümden kalan veritabanını bu komutla yenileyin.

## Veri kaynağı ve değişiklik

Veri, özgün proje raporunda verilen [Kaggle / Yasser H — Titanic Dataset](https://www.kaggle.com/datasets/yasserh/titanic-dataset) kaynağının **1. sürümünden** 13 Ekim 2026 tarihinde indirildi. Yayıncı lisansı **CC0: Public Domain** olarak listeler. Kaynak dosya `Titanic-Dataset.csv`, depoda içeriği değiştirilmeden `data/titanic.csv` adıyla saklanır. Kaynak adresleri ve SHA-256 özeti [data/source.json](data/source.json) içindedir.

İlk teslimdeki `tested.csv`, 418 kayıt içeriyordu ve `Survived` değeri bütün satırlarda cinsiyet kuralıyla eşleşiyordu. Bu etiketler gerçek sonuç kabul edilerek model başarısı raporlanamaz. **Güncel sürüm 891 kayıtlı kaynak veriyi kullanır; eski sonuçlarla doğrudan karşılaştırılmamalıdır.** Eski dosyalar Git geçmişinde ve özgün Drive klasöründe korunur. [İnceleme ve düzeltme raporu](docs/audit.md).

## Veri ve analiz

| Ölçüm | Değer |
| --- | ---: |
| Yolcu | 891 |
| Hayatta kalan | 342 |
| Hayatta kalma oranı | %38,38 |
| Eksik yaş | 177 |
| Eksik kabin | 687 |
| Eksik biniş limanı | 2 |
| Eksik bilet ücreti | 0 |

Grafiklerde eksik veriler ayrı tutulur. Yaş sınırları **[0,18), [18,40), [40,∞)**; ücret sınırları **[0,10), [10,50), [50,100), [100,∞)** şeklindedir. 40 yaş üstü gruba “yaşlı” anlamı yüklenmez. Gruplama kuralları ve panel hesapları aynı [SQL dosyasından](sql/analysis.sql) gelir.

[Analiz raporu ve grup tabloları](reports/analysis.md) · [Veri sözlüğü](docs/data_dictionary.md)

## Model değerlendirmesi

712 eğitim ve 179 test kaydı kullanılır. Bölme, `stratify=Survived` ve `random_state=42` ile bir kez belirlenir. Ön işlemede sayısal eksikler medyanla, kategorik eksikler en sık değerle doldurulur; bu değerler **yalnızca eğitim kümesinden öğrenilir**. Kategoriler one-hot encoding ile dönüştürülür. Random Forest: 200 ağaç, `min_samples_leaf=2`.

| Ölçüt | Sabit test ayrımı sonucu |
| --- | ---: |
| Accuracy | %79,33 |
| Precision | %78,57 |
| Recall | %63,77 |
| F1 | %70,40 |
| ROC AUC | 0,8385 |
| Çoğunluk sınıfı tabanı — accuracy | %61,45 |

Pozitif sınıf `Survived=1`'dir. Karışıklık matrisi **[[98,12],[25,44]]**; satırlar gerçek [0,1], sütunlar tahmin [0,1] sırasındadır. Değerler [model_metrics.json](reports/model_metrics.json) dosyasından alınmıştır. Model paneli bu genel test sonuçlarını gösterir; grafik filtreleri model sonuçlarını değiştirmez.

Bu sonuçlar Kaggle yarışma skoru veya bağımsız dış doğrulama değildir. Tek ayrım sonuçları farklı bölmelerde değişebilir. Yolcular arasındaki aile/bilet ilişkileri nedeniyle satır bazlı ayrım tam bağımsızlık sağlamayabilir. Model bir üretim tahmin servisi olarak sunulmaz. Gruplar arası farklılıklar nedensellik veya A/B testi kanıtı değildir.

## Sonuçları ve testleri yeniden üretme

Windows:

```powershell
.\.venv\Scripts\python.exe generate_report.py
.\.venv\Scripts\python.exe model.py
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q -W error
```

macOS / Linux'ta aynı komutlarda Python yolu `.venv/bin/python` olur. Testler geçici veritabanları kullanır. [Doğrulama kapsamı](docs/validation.md).

## Dosyalar

| Yol | Görev |
| --- | --- |
| `app.py`, `assets/style.css` | Filtrelenebilir Türkçe panel |
| `data_access.py` | CSV doğrulama, güvenli aktarım ve kaynak kontrolü |
| `import_csv_to_db.py` | Veritabanı oluşturma komutu |
| `analysis.py`, `sql/analysis.sql` | Ortak SQL analizleri |
| `model.py` | Ön işleme, eğitim, taban model ve test metrikleri |
| `generate_report.py`, `reports/` | Yeniden üretilebilir analiz ve model sonuçları |
| `data/titanic.csv`, `data/source.json` | Veri ve kaynak kaydı |
| `tests/` | Regresyon testleri |
| `docs/` | İnceleme, veri sözlüğü ve doğrulama belgeleri |

**Yazar:** Uluhan Yusuf Dokay
