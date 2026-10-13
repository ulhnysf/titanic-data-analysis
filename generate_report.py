"""SQL özetlerini CSV ve Markdown olarak yeniden üretir; modeli ayrıca çalıştırın."""
from pathlib import Path
from analysis import GROUP_TITLES, summarize
from data_access import ROOT, load_csv


def generate_report():
    df = load_csv()
    folder = ROOT / 'reports'
    folder.mkdir(exist_ok=True)
    lines = ['# Titanic: keşifsel analiz raporu', '',
             f'Kaynak: 891 kayıt; {int(df.Survived.sum())} hayatta kalan; oran %{df.Survived.mean()*100:.2f}.', '',
             'Bu rapor `python generate_report.py` ile doğrulanmış CSV üzerinde SQL sorgularından üretilir.', '',
             '## Veri kalitesi', '', '| Sütun | Eksik kayıt |', '| --- | ---: |']
    for column in ['Age', 'Fare', 'Cabin', 'Embarked']:
        lines.append(f'| {column} | {df[column].isna().sum()} |')
    for key, (_, title) in GROUP_TITLES.items():
        result = summarize(df, key)
        result.to_csv(folder / f'{key}_summary.csv', index=False)
        lines += ['', f'## {title}', '', '| Grup | Yolcu | Hayatta kalan | Oran (%) |', '| --- | ---: | ---: | ---: |']
        for row in result.itertuples():
            lines.append(f'| {row.label} | {row.passengers} | {row.survivors} | {row.rate:.2f} |')
    lines += ['', '## Yorum sınırları', '',
              '- Grup farkları betimseldir. Nedensel etki, istatistiksel anlamlılık veya A/B testi iddia edilmez.',
              '- Eksik yaş ve biniş limanı değerleri ayrı gruptadır; analizde değer uydurulmaz.',
              '- Az gözlem içeren grupların oranları kararsız olabilir; oranlarla birlikte sayılar verilmiştir.',
              '- Sonuçlar bu veri kümesine aittir; gemideki tüm yolculara doğrudan genellenmez.',
              '- Model değerlendirmesi ayrı `model_metrics.json` dosyasındadır; EDA verisiyle model test ayrımı karıştırılmamalıdır.', '']
    (folder / 'analysis.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    generate_report()
