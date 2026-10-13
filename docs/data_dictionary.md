# Veri sözlüğü

| Sütun | Anlam | Kabul edilen değer |
| --- | --- | --- |
| PassengerId | Yolcu kimliği | Pozitif, benzersiz tam sayı |
| Survived | Kaynak veri kümesindeki hayatta kalma sonucu | 0: hayır, 1: evet |
| Pclass | Bilet sınıfı | 1, 2, 3 |
| Name | Yolcu adı | Boş olmayan metin |
| Sex | Kaynaktaki cinsiyet kategorisi | female, male |
| Age | Yaş; bebeklerde kesirli olabilir | Sıfır veya pozitif sayı, boş olabilir |
| SibSp | Gemideki kardeş/eş sayısı | Sıfır veya pozitif tam sayı |
| Parch | Gemideki ebeveyn/çocuk sayısı | Sıfır veya pozitif tam sayı |
| Ticket | Bilet kodu | Boş olmayan metin |
| Fare | Kaynakta kayıtlı bilet ücreti, GBP | Sıfır veya pozitif sayı, boş olabilir |
| Cabin | Kabin kodu | Metin veya boş |
| Embarked | Biniş limanı | C: Cherbourg, Q: Queenstown, S: Southampton veya boş |

Fare paylaşılan biletlerle ilişkili olabilir; kişi başına düşen ücret olduğu varsayılmaz. Name, Ticket, Cabin ve PassengerId model girdisi değildir. Boş değerler analizde korunur, modeldeki doldurma işlemi yalnızca eğitim verisinde öğrenilir.
