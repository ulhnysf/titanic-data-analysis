# Titanic: keşifsel analiz raporu

Kaynak: 891 kayıt; 342 hayatta kalan; oran %38.38.

Bu rapor `python generate_report.py` ile doğrulanmış CSV üzerinde SQL sorgularından üretilir.

## Veri kalitesi

| Sütun | Eksik kayıt |
| --- | ---: |
| Age | 177 |
| Fare | 0 |
| Cabin | 687 |
| Embarked | 2 |

## Sınıfa göre hayatta kalma

| Grup | Yolcu | Hayatta kalan | Oran (%) |
| --- | ---: | ---: | ---: |
| 1 | 216 | 136 | 62.96 |
| 2 | 184 | 87 | 47.28 |
| 3 | 491 | 119 | 24.24 |

## Cinsiyete göre hayatta kalma

| Grup | Yolcu | Hayatta kalan | Oran (%) |
| --- | ---: | ---: | ---: |
| Kadın | 314 | 233 | 74.20 |
| Erkek | 577 | 109 | 18.89 |

## Yaş grubuna göre hayatta kalma

| Grup | Yolcu | Hayatta kalan | Oran (%) |
| --- | ---: | ---: | ---: |
| 0 ≤ yaş < 18 | 113 | 61 | 53.98 |
| 18 ≤ yaş < 40 | 438 | 168 | 38.36 |
| 40 ≤ yaş | 163 | 61 | 37.42 |
| Bilinmiyor | 177 | 52 | 29.38 |

## Bilet ücretine göre hayatta kalma

| Grup | Yolcu | Hayatta kalan | Oran (%) |
| --- | ---: | ---: | ---: |
| 0 ≤ ücret < 10 | 336 | 67 | 19.94 |
| 10 ≤ ücret < 50 | 394 | 166 | 42.13 |
| 50 ≤ ücret < 100 | 108 | 70 | 64.81 |
| 100 ≤ ücret | 53 | 39 | 73.58 |

## Biniş limanına göre hayatta kalma

| Grup | Yolcu | Hayatta kalan | Oran (%) |
| --- | ---: | ---: | ---: |
| Cherbourg | 168 | 93 | 55.36 |
| Queenstown | 77 | 30 | 38.96 |
| Southampton | 644 | 217 | 33.70 |
| Bilinmiyor | 2 | 2 | 100.00 |

## Yorum sınırları

- Grup farkları betimseldir. Nedensel etki, istatistiksel anlamlılık veya A/B testi iddia edilmez.
- Eksik yaş ve biniş limanı değerleri ayrı gruptadır; analizde değer uydurulmaz.
- Az gözlem içeren grupların oranları kararsız olabilir; oranlarla birlikte sayılar verilmiştir.
- Sonuçlar bu veri kümesine aittir; gemideki tüm yolculara doğrudan genellenmez.
- Model değerlendirmesi ayrı `model_metrics.json` dosyasındadır; EDA verisiyle model test ayrımı karıştırılmamalıdır.
