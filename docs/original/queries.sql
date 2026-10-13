-- SQLite
CREATE TABLE IF NOT EXISTS tested (
    PassengerId INTEGER PRIMARY KEY,
    Survived INTEGER,
    Pclass INTEGER,
    Name TEXT,
    Sex TEXT,
    Age REAL,
    SibSp INTEGER,
    Parch INTEGER,
    Ticket TEXT,
    Fare REAL,
    Cabin TEXT,
    Embarked TEXT
);

-- **1. Veri Keşfi ve Tanıma**

-- 1.1 Tablonun yapısını görmek
PRAGMA table_info(tested);

-- 1.2 Veri kümesindeki toplam yolcu sayısı
SELECT COUNT(*) AS Total_Passengers
FROM tested;

-- 1.3 Veri kümesindeki kolonlar ve örnek veriler
SELECT *
FROM tested
LIMIT 10;

-- **2. Veri Temizliği ve Hazırlığı**

-- 2.1 Eksik değerlerin kontrolü
SELECT
    SUM(CASE WHEN Age IS NULL THEN 1 ELSE 0 END) AS Missing_Age,
    SUM(CASE WHEN Cabin IS NULL THEN 1 ELSE 0 END) AS Missing_Cabin
FROM tested;

-- 2.2 Eksik yaş değerlerini ortalama yaşla doldurmak
UPDATE tested
SET Age = (SELECT AVG(Age) FROM tested)
WHERE Age IS NULL;

-- **3. Analitik Sorgular**

-- 3.1 Sınıfa göre hayatta kalma oranı
SELECT Pclass AS Passenger_Class,
       COUNT(*) AS Total_Passengers,
       SUM(CASE WHEN Survived = 1 THEN 1 ELSE 0 END) AS Survivors,
       ROUND(SUM(CASE WHEN Survived = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS Survival_Rate
FROM tested
GROUP BY Pclass;

-- 3.2 Cinsiyete göre hayatta kalma oranı
SELECT Sex,
       COUNT(*) AS Total_Passengers,
       SUM(CASE WHEN Survived = 1 THEN 1 ELSE 0 END) AS Survivors,
       ROUND(SUM(CASE WHEN Survived = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS Survival_Rate
FROM tested
GROUP BY Sex;

-- 3.3 Yaş gruplarına göre hayatta kalma oranı
SELECT CASE
           WHEN Age < 18 THEN 'Child'
           WHEN Age BETWEEN 18 AND 40 THEN 'Adult'
           ELSE 'Senior'
       END AS Age_Group,
       COUNT(*) AS Total_Passengers,
       SUM(CASE WHEN Survived = 1 THEN 1 ELSE 0 END) AS Survivors,
       ROUND(SUM(CASE WHEN Survived = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS Survival_Rate
FROM tested
GROUP BY Age_Group;

-- **4. İleri Düzey Analiz**

-- 4.1 Embarkation (biniş limanı) ve sınıfa göre hayatta kalma
SELECT Embarked,
       Pclass AS Passenger_Class,
       COUNT(*) AS Total_Passengers,
       SUM(CASE WHEN Survived = 1 THEN 1 ELSE 0 END) AS Survivors,
       ROUND(SUM(CASE WHEN Survived = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS Survival_Rate
FROM tested
WHERE Embarked IS NOT NULL
GROUP BY Embarked, Pclass;

-- 4.2 Bilet ücreti (Fare) ve hayatta kalma ilişkisi
SELECT CASE
           WHEN Fare < 10 THEN 'Low Fare'
           WHEN Fare BETWEEN 10 AND 50 THEN 'Medium Fare'
           ELSE 'High Fare'
       END AS Fare_Group,
       COUNT(*) AS Total_Passengers,
       SUM(CASE WHEN Survived = 1 THEN 1 ELSE 0 END) AS Survivors,
       ROUND(SUM(CASE WHEN Survived = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS Survival_Rate
FROM tested
GROUP BY Fare_Group;

-- **5. Raporlama için Özet Tablo**

-- 5.1 Sınıfa ve cinsiyete göre yolcu dağılımı
SELECT Pclass AS Passenger_Class,
       Sex,
       COUNT(*) AS Total_Passengers,
       SUM(CASE WHEN Survived = 1 THEN 1 ELSE 0 END) AS Survivors,
       ROUND(SUM(CASE WHEN Survived = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS Survival_Rate
FROM tested
GROUP BY Pclass, Sex
ORDER BY Passenger_Class, Survival_Rate DESC;

-- **6. Kurslara göre SQL Analizleri**

-- 6.1 İş gücü analizi (US Census Data) - Yaş ve cinsiyet dağılımı
SELECT Sex, 
       CASE
           WHEN Age < 18 THEN 'Child'
           WHEN Age BETWEEN 18 AND 40 THEN 'Adult'
           ELSE 'Senior'
       END AS Age_Group,
       COUNT(*) AS Total_Passengers
FROM tested
GROUP BY Sex, Age_Group;

-- 6.2 SQL'de gerçek dünya problemleri - Yüksek ücretle seyahat edenlerin hayatta kalma oranı
SELECT Pclass,
       COUNT(*) AS Total_Passengers,
       SUM(CASE WHEN Survived = 1 THEN 1 ELSE 0 END) AS Survivors,
       ROUND(SUM(CASE WHEN Survived = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS Survival_Rate
FROM tested
WHERE Fare > 50
GROUP BY Pclass;

-- 6.3 İş verisi analizi (Business Data Analysis) - Bilet ücreti ile hayatta kalma oranı
SELECT Fare,
       COUNT(*) AS Total_Passengers,
       SUM(CASE WHEN Survived = 1 THEN 1 ELSE 0 END) AS Survivors,
       ROUND(SUM(CASE WHEN Survived = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS Survival_Rate
FROM tested
GROUP BY Fare;

-- 6.4 PySpark ile büyük veri analizi - Sınıf bazında hayatta kalma oranları
SELECT Pclass, 
       COUNT(*) AS Total_Passengers,
       SUM(CASE WHEN Survived = 1 THEN 1 ELSE 0 END) AS Survivors,
       ROUND(SUM(CASE WHEN Survived = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS Survival_Rate
FROM tested
GROUP BY Pclass;

-- 6.5 Pazarlama kampanyası analizi (Marketing Campaign) - Cinsiyete göre kampanya başarısı
SELECT Sex,
       COUNT(*) AS Total_Passengers,
       SUM(CASE WHEN Survived = 1 THEN 1 ELSE 0 END) AS Survivors,
       ROUND(SUM(CASE WHEN Survived = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS Campaign_Success_Rate
FROM tested
GROUP BY Sex;

-- 6.6 A/B testi analizi (A/B Testing) - Farklı sınıflarda hayatta kalma oranları
SELECT Pclass, 
       COUNT(*) AS Total_Passengers,
       SUM(CASE WHEN Survived = 1 THEN 1 ELSE 0 END) AS Survivors,
       ROUND(SUM(CASE WHEN Survived = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS Survival_Rate
FROM tested
GROUP BY Pclass;

-- 6.7 Suç analizi (Police Activity) - Yaş ve cinsiyetle hayatta kalma oranı
SELECT Age,
       Sex,
       COUNT(*) AS Total_Passengers,
       SUM(CASE WHEN Survived = 1 THEN 1 ELSE 0 END) AS Survivors,
       ROUND(SUM(CASE WHEN Survived = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS Survival_Rate
FROM tested
GROUP BY Age, Sex;

-- 6.8 Excel fonksiyonları ve veri manipülasyonu - Yaş ve sınıfın etkisi
SELECT Pclass, 
       CASE
           WHEN Age < 18 THEN 'Child'
           WHEN Age BETWEEN 18 AND 40 THEN 'Adult'
           ELSE 'Senior'
       END AS Age_Group,
       COUNT(*) AS Total_Passengers,
       SUM(CASE WHEN Survived = 1 THEN 1 ELSE 0 END) AS Survivors
FROM tested
GROUP BY Pclass, Age_Group;
