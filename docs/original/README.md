# İlk sürüm arşivi

Bu klasör, projenin ilk Python ve SQL kodlarını gelişim geçmişini göstermek amacıyla saklar. Bilgisayara özel mutlak dosya yolları göreli örnek yollarla değiştirilmiştir. Güncel çalışma talimatları deponun ana README dosyasındadır; bu klasör güncel uygulama değildir.

İlk sürümdeki sınırlılıklar:

- `Survived` etiketleri cinsiyetle tamamen eşleşir; Random Forest doğruluğu gerçek hayatta kalma başarısını ölçmez.
- Ön işleme eğitim/test ayrımından önce yapılmıştır.
- “A/B testi” olarak adlandırılan işlem yalnızca grup ortalamalarının karşılaştırmasıdır.
- SQL yorumlarındaki kurs adları, PySpark veya Excel'in gerçekten kullanıldığı anlamına gelmez; sorgular SQLite sorgularıdır.
- `run_server` eski Dash API'sidir; güncel uygulama `run` kullanır.
- SQL dosyasında yaş değerlerini değiştiren UPDATE vardır. Güncel `sql/analysis.sql` salt okunurdur.
- Eski pasta grafiği cinsiyet bazlı hayatta kalma oranlarını doğru karşılaştırmaz; güncel uygulama grup ortalamalarını çubuk grafikle gösterir.

Özgün rapor ve sertifika PDF'leri çalışma zamanı için gerekli olmadığından bu depoya eklenmemiştir.
