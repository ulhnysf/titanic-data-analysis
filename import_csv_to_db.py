"""CSV verisini, çalışma dizininden bağımsız olarak SQLite'a aktarır."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / 'data' / 'tested.csv'
DB_PATH = ROOT / 'data' / 'titanic.db'


def build_database():
    df = pd.read_csv(CSV_PATH)
    required = {'PassengerId', 'Pclass', 'Sex', 'Age', 'Fare', 'Survived'}
    if not required.issubset(df.columns):
        raise ValueError(f'Eksik sütunlar: {required - set(df.columns)}')
    if df.empty or df['PassengerId'].duplicated().any():
        raise ValueError('Veri boş veya PassengerId değerleri tekrarlanıyor.')
    if not df['Survived'].isin([0, 1]).all():
        raise ValueError('Survived yalnızca 0 veya 1 içermeli.')
    with sqlite3.connect(DB_PATH) as connection:
        df.to_sql('tested', connection, if_exists='replace', index=False)
    return len(df)


if __name__ == '__main__':
    print(f'{build_database()} kayıt aktarıldı: {DB_PATH}')
