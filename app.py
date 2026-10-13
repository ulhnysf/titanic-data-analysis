"""Titanic verisi için SQL tabanlı keşif ve Plotly görselleştirmeleri."""
import sqlite3
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from import_csv_to_db import DB_PATH


def load_data():
    if not DB_PATH.exists():
        raise FileNotFoundError('Önce python import_csv_to_db.py komutunu çalıştırın.')
    with sqlite3.connect(DB_PATH) as connection:
        return pd.read_sql_query('SELECT Pclass, Sex, Age, Fare, Survived FROM tested', connection)


def create_app():
    df = load_data()
    df['Sex'] = df['Sex'].map({'female': 'Kadın', 'male': 'Erkek'})
    df['Age_Group'] = pd.cut(df['Age'], [-float('inf'), 18, 40, float('inf')],
                              labels=['18 yaş altı', '18–39 yaş', '40 yaş ve üzeri'], right=False)
    df['Fare_Group'] = pd.cut(df['Fare'], [-float('inf'), 10, 50, 100, float('inf')],
                               labels=['10 altı', '10–49,99', '50–99,99', '100 ve üzeri'], right=False)
    for column in ['Age_Group', 'Fare_Group']:
        df[column] = df[column].cat.add_categories(['Bilinmiyor']).fillna('Bilinmiyor')
    charts = []
    for column, title, label in [
        ('Pclass', 'Yolcu sınıfına göre etiket oranı', 'Yolcu sınıfı'),
        ('Sex', 'Cinsiyete göre etiket oranı', 'Cinsiyet'),
        ('Age_Group', 'Yaş grubuna göre etiket oranı', 'Yaş grubu'),
        ('Fare_Group', 'Bilet ücretine göre etiket oranı', 'Bilet ücreti grubu'),
    ]:
        summary = df.groupby(column, observed=True)['Survived'].agg(['mean', 'count']).reset_index()
        summary['mean'] *= 100
        figure = px.bar(summary, x=column, y='mean', title=title,
                        hover_data={'count': True}, color_discrete_sequence=['#2563eb'],
                        labels={column: label, 'mean': 'Survived = 1 (%)', 'count': 'Yolcu sayısı'})
        figure.update_layout(template='plotly_white', yaxis_range=[0, 105])
        charts.append(dcc.Graph(figure=figure, id=f'chart-{column}'))
    app = Dash(__name__)
    app.title = 'Titanic | Veri Analizi'
    app.layout = html.Main([
        html.P('SQL • PYTHON • VERİ GÖRSELLEŞTİRME', style={'color': '#2563eb'}),
        html.H1('Titanic Veri Analizi'),
        html.P('Yolcu özelliklerinin SQLite sorguları ve etkileşimli grafiklerle incelenmesi.'),
        html.Div(f"{len(df)} yolcu · Eksik yaş: {df.Age.isna().sum()} · Eksik ücret: {df.Fare.isna().sum()}"),
        html.P('Veri notu: Bu dosyada Survived etiketi tüm satırlarda cinsiyetle birebir eşleşir. '
               'Grafikler dosyadaki etiketleri özetler; doğrulanmış tarihsel hayatta kalma oranları '
               'veya nedensel etkiler olarak yorumlanmamalıdır.',
               style={'background': '#fff7ed', 'padding': '18px', 'borderRadius': '8px'}),
        *charts,
        html.P('Grafiklerin üzerine gelerek değerleri görebilir, araç çubuğundan yakınlaştırabilir veya PNG indirebilirsiniz.'),
    ], style={'maxWidth': '1050px', 'margin': '40px auto', 'padding': '0 24px',
              'fontFamily': 'Arial, sans-serif', 'color': '#172033'})
    return app


if __name__ == '__main__':
    create_app().run(debug=False)
