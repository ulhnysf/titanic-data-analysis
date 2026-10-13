"""Titanic SQL analiz paneli; eğitim ayrı model.py komutuyla çalıştırılır."""
from hashlib import sha256
import json
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from analysis import GROUP_TITLES, summarize
from data_access import CSV_PATH, ROOT, DataValidationError, load_database


def make_figure(summary, title, axis_label):
    figure = go.Figure(go.Bar(
        x=summary['label'].tolist(), y=summary['rate'].tolist(),
        customdata=summary[['passengers', 'survivors']].values.tolist(),
        marker_color='#2563eb',
        hovertemplate='%{x}<br>Hayatta kalma: %{y:.1f}%<br>Yolcu: %{customdata[0]}<br>Hayatta kalan: %{customdata[1]}<extra></extra>',
    ))
    if summary.empty:
        figure.add_annotation(text='Bu filtrelerde veri bulunamadı.', showarrow=False)
    figure.update_layout(template='plotly_white', title=title, xaxis_title=axis_label,
                         yaxis_title='Hayatta kalma (%)', yaxis_range=[0, 100],
                         margin={'l': 55, 'r': 15, 't': 60, 'b': 80}, height=370,
                         font={'family': 'Arial', 'size': 12})
    figure.update_xaxes(type='category', automargin=True)
    return figure


def filter_data(df, pclass, sex):
    if pclass not in ['all', 1, 2, 3] or sex not in ['all', 'female', 'male']:
        raise ValueError('Geçersiz filtre.')
    result = df
    if pclass != 'all':
        result = result[result.Pclass == pclass]
    if sex != 'all':
        result = result[result.Sex == sex]
    return result


def dashboard_outputs(df, pclass='all', sex='all'):
    selected = filter_data(df, pclass, sex)
    count = len(selected)
    survivors = int(selected.Survived.sum())
    rate = f'{survivors / count * 100:.1f}%' if count else '—'
    cards = [html.Div([html.Span(label), html.Strong(str(value))], className='stat')
             for label, value in [('Yolcu', count), ('Hayatta kalan', survivors),
                                  ('Hayatta kalma', rate), ('Eksik yaş', int(selected.Age.isna().sum()))]]
    figures = [make_figure(summarize(selected, key), title, label)
               for key, (label, title) in GROUP_TITLES.items()]
    return cards, *figures


def model_panel():
    path = ROOT / 'reports' / 'model_metrics.json'
    try:
        metrics = json.loads(path.read_text(encoding='utf-8'))
        if (metrics['source_sha256'] != sha256(CSV_PATH.read_bytes()).hexdigest()
                or metrics['model_code_sha256'] != sha256((ROOT / 'model.py').read_bytes()).hexdigest()):
            raise ValueError('Eski metrikler')
        rows = [html.Tr([html.Th(label), html.Td(f"{metrics[key]*100:.2f}%")])
                for label, key in [('Doğruluk', 'accuracy'), ('Precision', 'precision'),
                                   ('Recall', 'recall'), ('F1', 'f1'),
                                   ('ROC AUC', 'roc_auc'), ('Çoğunluk tabanı', 'baseline_accuracy')]]
        return html.Div([
            html.H2('Random Forest değerlendirmesi'),
            html.P(f"{metrics['train_rows']} eğitim / {metrics['test_rows']} test kaydı · sabit ayrım, random_state=42"),
            html.Table(html.Tbody(rows)),
            html.P('Metrikler tüm veri kümesindeki sabit test ayrımına aittir; panel filtreleriyle değişmez. '
                   'Bu sonuç Kaggle yarışma skoru veya bağımsız dış doğrulama değildir.'),
        ], className='panel')
    except (OSError, ValueError, KeyError, TypeError):
        return html.Div('Güncel model sonuçları bulunamadı. python model.py komutunu çalıştırın.', className='note')


def create_app(db_path=None):
    df = load_database() if db_path is None else load_database(db_path)
    app = Dash(__name__, assets_folder=str(ROOT / 'assets'))
    app.title = 'Titanic | Veri Analizi'
    initial = dashboard_outputs(df)
    app.layout = html.Main([
        html.Header([html.P('SQL / PYTHON / VERİ ANALİZİ', className='eyebrow'),
                     html.H1('Titanic Veri Analizi'),
                     html.P('891 yolcu üzerinden keşifsel analiz ve model değerlendirmesi.')]),
        html.Div([
            html.Div([html.Label('Yolcu sınıfı', htmlFor='class-filter'),
                      dcc.Dropdown(id='class-filter', options=[{'label': 'Tüm sınıflar', 'value': 'all'}]
                                   + [{'label': f'{i}. sınıf', 'value': i} for i in [1, 2, 3]], value='all', clearable=False)]),
            html.Div([html.Label('Cinsiyet', htmlFor='sex-filter'),
                      dcc.Dropdown(id='sex-filter', options=[{'label': 'Tümü', 'value': 'all'},
                                   {'label': 'Kadın', 'value': 'female'}, {'label': 'Erkek', 'value': 'male'}], value='all', clearable=False)]),
        ], className='filters'),
        html.Div(initial[0], id='stats', className='stats', **{'aria-live': 'polite'}),
        html.P('Grafikler seçili yolcular içindeki oranları gösterir. Eksik yaş ve biniş limanı ayrı gruptadır. '
               'Grup farkları nedensellik veya randomize A/B testi sonucu değildir.', className='note'),
        html.Div([dcc.Graph(id=f'chart-{key}', figure=figure, config={'displaylogo': False}, responsive=True)
                  for key, figure in zip(GROUP_TITLES, initial[1:])], className='charts'),
        model_panel(),
        html.Footer([html.A('Veri kaynağı: Kaggle / Yasser H', href='https://www.kaggle.com/datasets/yasserh/titanic-dataset'),
                     html.P('Veri: CC0 · Oranlar bu 891 kaydın özetidir; gemideki tüm yolcuları temsil etmez.')]),
    ], className='container')

    @app.callback(Output('stats', 'children'),
                  *[Output(f'chart-{key}', 'figure') for key in GROUP_TITLES],
                  Input('class-filter', 'value'), Input('sex-filter', 'value'))
    def update(pclass, sex):
        return dashboard_outputs(df, pclass, sex)

    return app


if __name__ == '__main__':
    try:
        create_app().run(debug=False, host='127.0.0.1', port=8050)
    except DataValidationError as exc:
        raise SystemExit(str(exc)) from exc
