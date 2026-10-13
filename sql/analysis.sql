-- Salt okunur keşif sorguları. Önce import_csv_to_db.py çalıştırılmalıdır.
-- Survived sütunu doğrulanmış sonuç değil, mevcut dosyanın etiketi olarak yorumlanır.
SELECT COUNT(*) AS passenger_count FROM tested;

SELECT SUM(Age IS NULL) AS missing_age, SUM(Fare IS NULL) AS missing_fare,
       SUM(Cabin IS NULL) AS missing_cabin FROM tested;

SELECT Pclass, COUNT(*) AS passengers, ROUND(AVG(Survived) * 100, 2) AS label_rate_pct
FROM tested GROUP BY Pclass ORDER BY Pclass;

SELECT Sex, COUNT(*) AS passengers, ROUND(AVG(Survived) * 100, 2) AS label_rate_pct
FROM tested GROUP BY Sex;

SELECT CASE WHEN Age IS NULL THEN 'Bilinmiyor' WHEN Age < 18 THEN '18 yaş altı'
            WHEN Age < 40 THEN '18–39 yaş' ELSE '40 yaş ve üzeri' END AS age_group,
       COUNT(*) AS passengers, ROUND(AVG(Survived) * 100, 2) AS label_rate_pct
FROM tested GROUP BY age_group;

SELECT CASE WHEN Fare IS NULL THEN 'Bilinmiyor' WHEN Fare < 10 THEN '10 altı'
            WHEN Fare < 50 THEN '10–49,99' WHEN Fare < 100 THEN '50–99,99'
            ELSE '100 ve üzeri' END AS fare_group,
       COUNT(*) AS passengers, ROUND(AVG(Survived) * 100, 2) AS label_rate_pct
FROM tested GROUP BY fare_group;

SELECT Embarked, Pclass, COUNT(*) AS passengers,
       ROUND(AVG(Survived) * 100, 2) AS label_rate_pct
FROM tested GROUP BY Embarked, Pclass ORDER BY Embarked, Pclass;

SELECT COUNT(*) AS rows_matching_sex_rule FROM tested
WHERE Survived = CASE WHEN Sex = 'female' THEN 1 ELSE 0 END;
