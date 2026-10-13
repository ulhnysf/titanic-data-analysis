-- Salt okunur sorgular; kaynak tablo: passengers.
-- Yaş ve ücret sınırları alt sınır dahil, üst sınır hariçtir.
-- name: quality
SELECT COUNT(*) AS passengers, SUM(Survived) AS survivors,
       SUM(Age IS NULL) AS missing_age, SUM(Fare IS NULL) AS missing_fare,
       SUM(Cabin IS NULL) AS missing_cabin, SUM(Embarked IS NULL) AS missing_port
FROM passengers;
-- name: class
SELECT CAST(Pclass AS TEXT) AS label, COUNT(*) AS passengers,
       SUM(Survived) AS survivors, AVG(Survived)*100 AS rate
FROM passengers GROUP BY Pclass ORDER BY Pclass;
-- name: sex
SELECT CASE Sex WHEN 'female' THEN 'Kadın' ELSE 'Erkek' END AS label,
       COUNT(*) AS passengers, SUM(Survived) AS survivors, AVG(Survived)*100 AS rate
FROM passengers GROUP BY Sex ORDER BY Sex;
-- name: age
WITH grouped AS (
 SELECT *, CASE WHEN Age IS NULL THEN 3 WHEN Age < 18 THEN 0 WHEN Age < 40 THEN 1 ELSE 2 END AS bucket
 FROM passengers
)
SELECT CASE bucket WHEN 0 THEN '0 ≤ yaş < 18' WHEN 1 THEN '18 ≤ yaş < 40'
       WHEN 2 THEN '40 ≤ yaş' ELSE 'Bilinmiyor' END AS label,
       COUNT(*) AS passengers, SUM(Survived) AS survivors, AVG(Survived)*100 AS rate
FROM grouped GROUP BY bucket ORDER BY bucket;
-- name: fare
WITH grouped AS (
 SELECT *, CASE WHEN Fare IS NULL THEN 4 WHEN Fare < 10 THEN 0 WHEN Fare < 50 THEN 1
               WHEN Fare < 100 THEN 2 ELSE 3 END AS bucket FROM passengers
)
SELECT CASE bucket WHEN 0 THEN '0 ≤ ücret < 10' WHEN 1 THEN '10 ≤ ücret < 50'
       WHEN 2 THEN '50 ≤ ücret < 100' WHEN 3 THEN '100 ≤ ücret' ELSE 'Bilinmiyor' END AS label,
       COUNT(*) AS passengers, SUM(Survived) AS survivors, AVG(Survived)*100 AS rate
FROM grouped GROUP BY bucket ORDER BY bucket;
-- name: port
SELECT CASE Embarked WHEN 'C' THEN 'Cherbourg' WHEN 'Q' THEN 'Queenstown'
       WHEN 'S' THEN 'Southampton' ELSE 'Bilinmiyor' END AS label,
       COUNT(*) AS passengers, SUM(Survived) AS survivors, AVG(Survived)*100 AS rate
FROM passengers GROUP BY Embarked ORDER BY Embarked IS NULL, Embarked;
-- name: class_sex
SELECT Pclass, Sex, COUNT(*) AS passengers, SUM(Survived) AS survivors,
       AVG(Survived)*100 AS rate FROM passengers GROUP BY Pclass,Sex ORDER BY Pclass,Sex;
