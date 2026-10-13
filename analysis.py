"""Grafik ve SQL raporunda aynı sınırlarla kullanılan analiz sorguları."""
from contextlib import closing
from pathlib import Path
import sqlite3
import pandas as pd

QUERY_PATH = Path(__file__).resolve().parent / 'sql' / 'analysis.sql'
GROUP_TITLES = {
    'class': ('Yolcu sınıfı', 'Sınıfa göre hayatta kalma'),
    'sex': ('Cinsiyet', 'Cinsiyete göre hayatta kalma'),
    'age': ('Yaş grubu', 'Yaş grubuna göre hayatta kalma'),
    'fare': ('Bilet ücreti (GBP)', 'Bilet ücretine göre hayatta kalma'),
    'port': ('Biniş limanı', 'Biniş limanına göre hayatta kalma'),
}


def read_queries():
    result = {}
    for block in QUERY_PATH.read_text(encoding='utf-8').split('-- name: ')[1:]:
        name, sql = block.split('\n', 1)
        result[name.strip()] = sql.strip().rstrip(';')
    return result


def summarize(df, group):
    if group not in GROUP_TITLES:
        raise ValueError('Bilinmeyen analiz grubu.')
    with closing(sqlite3.connect(':memory:')) as connection:
        df.to_sql('passengers', connection, index=False)
        return pd.read_sql_query(read_queries()[group], connection)
