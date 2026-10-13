# Kaynak incelemesi ve düzeltmeler

İnceleme tarihi: 2026-10-13. Kapsam: Drive'daki üç Python dosyası, SQL dosyası, SQLite veritabanı, CSV, altı Word belgesi ve beş grafik; proje isterleri ve sertifika PDF'leri; GitHub'daki ilk yayımlanan sürüm.

| Bulgu | Yapılan düzeltme |
| --- | --- |
| Eski CSV'deki 418 etiket cinsiyete birebir eşitti | Raporda belirtilen Kaggle kaynağından 891 kayıtlı sürüm indirildi; kaynak, sürüm, lisans bildirimi ve SHA-256 kaydedildi |
| Önceki GitHub README'sinde kaynak URL'sinin bulunmadığı yazıyordu | Kaynak proje özeti ve test raporunda bulundu; önceki ifade düzeltildi |
| Drive veritabanında yaş boşlukları doldurulmuştu; CSV'de 86 boşluk vardı | Güncel veritabanı doğrulanmış ham CSV'den yeniden üretilebilir; EDA eksikleri korur |
| İlk kodda kişisel Windows yolları vardı | Yollar proje köküne göre çözülür |
| CSV doğrulama eksikti | Tam şema, eksikler, tipler, kategori değerleri, kimlik benzersizliği, negatif/sonsuz değer ve sağlama toplamı kontrolleri eklendi |
| İlk aktarım tablo kısıtlarını to_sql ile kaybediyordu | PRIMARY KEY ve CHECK kısıtlı, transaction içinde aktarım eklendi |
| sqlite3 context manager bağlantıyı kendiliğinden kapatmıyordu | Bağlantılar açıkça kapatılıyor |
| Eski veritabanı güncel veri sanılabilirdi | Kaynak/sürüm kontrolü ve satır karşılaştırması eklendi |
| SQL ve Python'da yaş/ücret sınırları farklıydı; sıfır ücret dışarıda kalabiliyordu | Panel ve raporlar aynı SQL gruplamasını kullanıyor; sınır testleri eklendi |
| Cinsiyet pasta grafiği oranları yanlış temsil ediyordu | Grup sayılarıyla birlikte çubuk grafikler kullanılıyor |
| Grup ortalaması “A/B testi” diye sunuluyordu | Nedensellik ve A/B testi iddiası kaldırıldı; betimsel analiz olarak açıklandı |
| Tüm veride ön işleme yapılıp sonra test ayrılıyordu | Bölme ön işlemden önce yapılıyor; Pipeline sadece eğitimde fit ediliyor |
| Rapordaki yaklaşık %80 başarının dayanağı gösterilmiyordu | Sabit ayrım, gerçek metrikler, test kimlikleri, taban model ve karışıklık matrisi kaydedildi |
| Dokümanlarda depoda olmayan pandas_eda.py, pythondash.py, ml_model.py isimleri vardı | README gerçek dosya adları ve komutlarıyla yeniden yazıldı |
| Kullanılmayan Tableau/PySpark/Excel, lojistik regresyon ve görselleştirme yöntemleri ima ediliyordu | Güncel belge sadece mevcut kodun yaptığı işleri anlatıyor |
| Dash'in eski run_server çağrısı ve eksik bağımlılık listesi vardı | Güncel run API'si ve test edilen sabit bağımlılıklar kullanılıyor |
| İlk GitHub yüklemesinde eski hatalı kodlar çalıştırılabilir arşivde kalmıştı | Güncel ağaçtan kaldırıldı; geçmiş Git commit'leri ve özgün Drive dosyaları korunuyor |

Güncel doğrulamanın sonuçları `validation.md` içindedir. Bu inceleme Drive'daki teslim belgelerinin içeriğini değiştirmez; GitHub'daki yeni belgeler güncel çalışmayı anlatır. İlk sürümle yeni sonuçlar farklı veri kullanıldığı için doğrudan karşılaştırılmaz.

## İsterlerle eşleştirme

- SQL sorguları: `sql/analysis.sql`
- Görselleştirmeler: `app.py` ve panelden PNG dışa aktarma
- Veri kümesi: `data/titanic.csv`, kaynak bildirimi: `data/source.json`
- Proje özeti/teknikleri: ana `README.md`
- Analiz sonuçları: `reports/analysis.md` ve özet CSV dosyaları
- Model test verisi kimlikleri ve sonuçları: `reports/model_metrics.json`
- Çalıştırma talimatları: ana `README.md`
- Sunum videosu: incelenen klasörde bulunmadı; bu kod incelemesi video teslimini doğrulamaz.

Sertifikalar eğitim alındığını gösterir; her teknolojinin bu projede kullanıldığının kanıtı değildir. Sertifika ve öğrenci numarası içeren belgeler herkese açık depoya kopyalanmadı.
