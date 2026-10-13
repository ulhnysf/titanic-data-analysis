"""Veri kaybı, yanlış gruplama, eski kaynak ve model sızıntısı için regresyon testleri."""
import json
import sqlite3
from contextlib import closing
from hashlib import sha256
import numpy as np
import pandas as pd
import pytest

from data_access import (CSV_PATH, MANIFEST_PATH, DataValidationError,
                         build_database, load_csv, load_database, validate_frame)
from analysis import GROUP_TITLES, read_queries, summarize
from app import create_app, dashboard_outputs, filter_data
from model import FEATURES, NUMERIC, evaluate_model, make_pipeline


@pytest.fixture
def frame():
    return load_csv()


@pytest.fixture
def database(tmp_path):
    path = tmp_path / 'titanic.db'
    build_database(db_path=path)
    return path


def test_source_manifest_and_labels(frame):
    manifest = json.loads(MANIFEST_PATH.read_text())
    assert sha256(CSV_PATH.read_bytes()).hexdigest() == manifest['sha256']
    assert len(frame) == 891
    assert frame.Survived.sum() == 342
    assert frame.Age.isna().sum() == 177
    assert not (frame.Survived == (frame.Sex == 'female').astype(int)).all()


@pytest.mark.parametrize('column,value', [
    ('PassengerId', None), ('PassengerId', 1.5), ('PassengerId', -1),
    ('Survived', 2), ('Survived', None), ('Pclass', 4),
    ('Sex', 'unknown'), ('Sex', None), ('Embarked', 'X'),
    ('Age', -1), ('Age', float('inf')), ('Fare', -1), ('Fare', 'bad'),
    ('SibSp', 1.2), ('Parch', -1), ('Name', '  '), ('Ticket', None),
])
def test_invalid_values_rejected(frame, column, value):
    frame[column] = frame[column].astype(object)
    frame.loc[0, column] = value
    with pytest.raises(DataValidationError):
        validate_frame(frame)


def test_empty_duplicate_and_missing_columns(frame):
    for bad in [frame.iloc[:0], pd.concat([frame, frame.iloc[:1]]), frame.drop(columns='Embarked')]:
        with pytest.raises(DataValidationError):
            validate_frame(bad)


def test_changed_source_rejected(tmp_path):
    path = tmp_path / 'changed.csv'
    path.write_bytes(CSV_PATH.read_bytes() + b'\n')
    with pytest.raises(DataValidationError, match='sağlama'):
        load_csv(path)


def test_repeat_import_and_preserve_other_table(database):
    with closing(sqlite3.connect(database)) as c:
        c.execute('CREATE TABLE unrelated (value TEXT)')
        c.execute("INSERT INTO unrelated VALUES ('keep')")
        c.commit()
    build_database(db_path=database)
    assert len(load_database(database)) == 891
    with closing(sqlite3.connect(database)) as c:
        assert c.execute('SELECT * FROM unrelated').fetchall() == [('keep',)]
        with pytest.raises(sqlite3.IntegrityError):
            c.execute('UPDATE passengers SET Survived=3 WHERE PassengerId=1')


def test_invalid_import_preserves_database(database, frame, tmp_path):
    before = database.read_bytes()
    frame.loc[0, 'Survived'] = 3
    path = tmp_path / 'invalid.csv'
    frame.to_csv(path, index=False)
    with pytest.raises(DataValidationError):
        build_database(path, database, verify_source=False)
    assert database.read_bytes() == before


def test_transaction_rolls_back_on_sql_failure(database, monkeypatch):
    # SQLite authorizer permits DROP but refuses CREATE; original table must survive.
    original = sqlite3.connect
    def connect(*args, **kwargs):
        c = original(*args, **kwargs)
        c.set_authorizer(lambda action, *rest: sqlite3.SQLITE_DENY
                         if action == sqlite3.SQLITE_CREATE_TABLE else sqlite3.SQLITE_OK)
        return c
    monkeypatch.setattr('data_access.sqlite3.connect', connect)
    with pytest.raises(sqlite3.DatabaseError):
        build_database(db_path=database)
    monkeypatch.setattr('data_access.sqlite3.connect', original)
    assert len(load_database(database)) == 891


def test_missing_database_not_created(tmp_path):
    path = tmp_path / 'absent.db'
    with pytest.raises(DataValidationError, match='bulunamadı'):
        load_database(path)
    assert not path.exists()


def test_old_database_rejected(tmp_path):
    path = tmp_path / 'old.db'
    with closing(sqlite3.connect(path)) as c:
        c.execute('CREATE TABLE tested (Age REAL)')
    with pytest.raises(DataValidationError):
        load_database(path)


def test_tampered_database_rejected(database):
    with closing(sqlite3.connect(database)) as c:
        c.execute('UPDATE passengers SET Age=99 WHERE PassengerId=1')
        c.commit()
    with pytest.raises(DataValidationError, match='uyuşmuyor'):
        load_database(database)


@pytest.mark.parametrize('group', list(GROUP_TITLES))
def test_summary_conserves_counts_and_survivors(frame, group):
    result = summarize(frame, group)
    assert result.passengers.sum() == 891
    assert result.survivors.sum() == 342
    np.testing.assert_allclose(result.rate, result.survivors / result.passengers * 100)
    assert result.rate.between(0, 100).all()


def test_boundary_values_are_not_dropped(frame):
    sample = frame.iloc[:6].copy()
    sample['Age'] = [0, 17.999, 18, 39.999, 40, np.nan]
    sample['Fare'] = [0, 10, 49.999, 50, 100, np.nan]
    assert summarize(sample, 'age').passengers.tolist() == [2, 2, 1, 1]
    assert summarize(sample, 'fare').passengers.tolist() == [1, 2, 1, 1, 1]


def test_sql_queries_read_only(database):
    with closing(sqlite3.connect(database.resolve().as_uri()+'?mode=ro', uri=True)) as c:
        for query in read_queries().values():
            assert c.execute(query).fetchall()


def test_filters_and_empty_state(frame):
    selected = filter_data(frame, 1, 'female')
    assert len(selected) == 94
    outputs = dashboard_outputs(frame, 1, 'female')
    assert len(outputs) == 6
    empty = dashboard_outputs(frame.iloc[:0])
    assert all(len(figure.data[0].x) == 0 for figure in empty[1:])
    with pytest.raises(ValueError):
        filter_data(frame, 5, 'all')


def test_http_and_filter_callback(database):
    app = create_app(database)
    client = app.server.test_client()
    for url in ['/', '/_dash-layout', '/_dash-dependencies', '/assets/style.css']:
        with client.get(url) as response:
            assert response.status_code == 200
    key = next(iter(app.callback_map))
    outputs = [{'id': 'stats', 'property': 'children'}] + [
        {'id': f'chart-{group}', 'property': 'figure'} for group in GROUP_TITLES]
    r = client.post('/_dash-update-component', json={
        'output': key, 'outputs': outputs, 'changedPropIds': ['class-filter.value'],
        'inputs': [{'id': 'class-filter', 'property': 'value', 'value': 1},
                   {'id': 'sex-filter', 'property': 'value', 'value': 'female'}], 'state': []})
    assert r.status_code == 200
    bars = r.json['response']['chart-class']['figure']['data'][0]
    assert bars['customdata'][0] == [94, 91]


def test_preprocessing_fits_only_training_data(frame):
    train = frame.iloc[:100].copy()
    model = make_pipeline().fit(train[FEATURES], train.Survived)
    medians = model.named_steps['preprocessing'].named_transformers_['numeric'].statistics_.copy()
    np.testing.assert_allclose(medians, train[NUMERIC].median().to_numpy())
    external = frame.iloc[100:105].copy()
    external['Age'] = 999
    external['Embarked'] = 'unseen'
    assert len(model.predict(external[FEATURES])) == 5
    np.testing.assert_array_equal(medians, model.named_steps['preprocessing'].named_transformers_['numeric'].statistics_)


def test_model_split_and_metrics(frame):
    result, _ = evaluate_model(frame)
    assert result['train_rows'] == 712 and result['test_rows'] == 179
    assert set(result['train_ids']).isdisjoint(result['test_ids'])
    assert set(result['train_ids']) | set(result['test_ids']) == set(frame.PassengerId)
    assert np.array(result['confusion_matrix']).sum() == 179
    for key in ['accuracy','precision','recall','f1','roc_auc','baseline_accuracy']:
        assert 0 <= result[key] <= 1
    matrix = np.array(result['confusion_matrix'])
    assert result['accuracy'] == matrix.trace()/matrix.sum()


def test_rule_based_labels_rejected(frame):
    frame.Survived = (frame.Sex == 'female').astype(int)
    with pytest.raises(DataValidationError):
        evaluate_model(frame)
