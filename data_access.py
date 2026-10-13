"""Doğrulanmış CSV, işlemsel SQLite aktarımı ve salt okunur veri erişimi."""
from contextlib import closing
from hashlib import sha256
from pathlib import Path
import csv
import json
import sqlite3

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / 'data' / 'titanic.csv'
DB_PATH = ROOT / 'data' / 'titanic.db'
MANIFEST_PATH = ROOT / 'data' / 'source.json'
COLUMNS = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age',
           'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
SCHEMA_VERSION = '2'


class DataValidationError(ValueError):
    """Veri sözleşmesi ihlali; kullanıcıya gösterilebilir hata."""


def validate_frame(df):
    if list(df.columns) != COLUMNS:
        raise DataValidationError('CSV sütunları ve sırası beklenen Titanic şemasıyla eşleşmiyor.')
    if df.empty:
        raise DataValidationError('Veri kümesi boş olamaz.')
    df = df.copy()
    numeric = ['PassengerId', 'Survived', 'Pclass', 'Age', 'SibSp', 'Parch', 'Fare']
    for column in numeric:
        try:
            df[column] = pd.to_numeric(df[column], errors='raise')
        except (ValueError, TypeError) as exc:
            raise DataValidationError(f'{column} sayısal olmalıdır.') from exc
        if np.isinf(df[column].dropna().to_numpy(dtype=float)).any():
            raise DataValidationError(f'{column} sonsuz değer içeremez.')
    for column in ['PassengerId', 'Survived', 'Pclass', 'SibSp', 'Parch']:
        if df[column].isna().any() or (df[column] % 1 != 0).any():
            raise DataValidationError(f'{column} eksiksiz tam sayılardan oluşmalıdır.')
        df[column] = df[column].astype('int64')
    if (df.PassengerId <= 0).any() or df.PassengerId.duplicated().any():
        raise DataValidationError('PassengerId pozitif ve benzersiz olmalıdır.')
    if not df.Survived.isin([0, 1]).all() or not df.Pclass.isin([1, 2, 3]).all():
        raise DataValidationError('Survived 0/1; Pclass 1/2/3 olmalıdır.')
    if not df.Sex.isin(['female', 'male']).all():
        raise DataValidationError('Sex yalnızca female/male içerebilir.')
    if not df.Embarked.dropna().isin(['C', 'Q', 'S']).all():
        raise DataValidationError('Embarked C/Q/S veya boş olmalıdır.')
    for column in ['Age', 'Fare', 'SibSp', 'Parch']:
        if (df[column].dropna() < 0).any():
            raise DataValidationError(f'{column} negatif olamaz.')
    for column in ['Name', 'Ticket']:
        if df[column].isna().any() or df[column].astype(str).str.strip().eq('').any():
            raise DataValidationError(f'{column} boş olamaz.')
    return df


def load_csv(path=CSV_PATH, verify_source=True):
    path = Path(path)
    if not path.is_file():
        raise DataValidationError(f'CSV bulunamadı: {path.name}')
    # Pandas'ın yinelenen başlıkları sessizce yeniden adlandırmasını önler.
    with path.open(encoding='utf-8-sig', newline='') as stream:
        if next(csv.reader(stream), []) != COLUMNS:
            raise DataValidationError('CSV başlıkları beklenen şemayla eşleşmiyor.')
    if verify_source:
        metadata = json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))
        if sha256(path.read_bytes()).hexdigest() != metadata['sha256']:
            raise DataValidationError('CSV kaynak sağlama toplamı uyuşmuyor; özgün data/titanic.csv dosyasını geri yükleyin.')
    try:
        df = pd.read_csv(path, dtype={'Name': str, 'Ticket': str, 'Cabin': str})
    except (ValueError, pd.errors.ParserError) as exc:
        raise DataValidationError('CSV okunamadı.') from exc
    df = validate_frame(df)
    if verify_source and len(df) != metadata['rows']:
        raise DataValidationError('CSV kayıt sayısı kaynak bildirimiyle uyuşmuyor.')
    return df


def build_database(csv_path=CSV_PATH, db_path=DB_PATH, verify_source=True):
    """Doğrulamadan sonra tek transaction ile tabloyu yeniler; diğer tabloları korur."""
    df = load_csv(csv_path, verify_source=verify_source)
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    records = [tuple(None if pd.isna(v) else v for v in row)
               for row in df.itertuples(index=False, name=None)]
    with closing(sqlite3.connect(db_path)) as connection:
        with connection:
            connection.execute('BEGIN')
            connection.execute('DROP TABLE IF EXISTS passengers')
            connection.execute('''CREATE TABLE passengers (
                PassengerId INTEGER PRIMARY KEY CHECK(PassengerId > 0),
                Survived INTEGER NOT NULL CHECK(Survived IN (0,1)),
                Pclass INTEGER NOT NULL CHECK(Pclass IN (1,2,3)),
                Name TEXT NOT NULL, Sex TEXT NOT NULL CHECK(Sex IN ('female','male')),
                Age REAL CHECK(Age >= 0), SibSp INTEGER NOT NULL CHECK(SibSp >= 0),
                Parch INTEGER NOT NULL CHECK(Parch >= 0), Ticket TEXT NOT NULL,
                Fare REAL CHECK(Fare >= 0), Cabin TEXT,
                Embarked TEXT CHECK(Embarked IN ('C','Q','S')))''')
            connection.executemany('INSERT INTO passengers VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', records)
            connection.execute('CREATE TABLE IF NOT EXISTS dataset_metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
            connection.executemany('INSERT OR REPLACE INTO dataset_metadata VALUES (?,?)', [
                ('schema_version', SCHEMA_VERSION),
                ('csv_sha256', sha256(Path(csv_path).read_bytes()).hexdigest())])
    return len(df)


def load_database(db_path=DB_PATH):
    path = Path(db_path)
    if not path.is_file():
        raise DataValidationError('Veritabanı bulunamadı. Önce python import_csv_to_db.py çalıştırın.')
    try:
        with closing(sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True)) as connection:
            metadata = dict(connection.execute('SELECT key,value FROM dataset_metadata'))
            expected = json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))['sha256']
            if metadata.get('schema_version') != SCHEMA_VERSION or metadata.get('csv_sha256') != expected:
                raise DataValidationError('Veritabanı eski bir kaynağa ait. python import_csv_to_db.py ile yenileyin.')
            df = validate_frame(pd.read_sql_query('SELECT * FROM passengers ORDER BY PassengerId', connection))
        # Sonradan elle düzenlenmiş veritabanının eski metriklerle kullanılmasını önler.
        source = load_csv().sort_values('PassengerId').reset_index(drop=True)
        pd.testing.assert_frame_equal(df.fillna(np.nan), source.fillna(np.nan), check_dtype=False)
        return df
    except DataValidationError:
        raise
    except (sqlite3.Error, pd.errors.DatabaseError, AssertionError) as exc:
        raise DataValidationError('Veritabanı kaynakla uyuşmuyor veya bozuk. python import_csv_to_db.py ile yenileyin.') from exc
