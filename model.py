"""Sabit test ayrımıyla, ön işlemeyi yalnızca eğitim verisinde öğrenen model."""
import json
from hashlib import sha256
from pathlib import Path
import platform
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from data_access import CSV_PATH, ROOT, DataValidationError, load_csv

FEATURES = ['Pclass', 'Sex', 'Age', 'Fare', 'SibSp', 'Parch', 'Embarked']
NUMERIC = ['Age', 'Fare', 'SibSp', 'Parch']
CATEGORICAL = ['Pclass', 'Sex', 'Embarked']


def make_pipeline():
    preprocessing = ColumnTransformer([
        ('numeric', SimpleImputer(strategy='median'), NUMERIC),
        ('categorical', Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder(handle_unknown='ignore')),
        ]), CATEGORICAL),
    ])
    return Pipeline([
        ('preprocessing', preprocessing),
        ('classifier', RandomForestClassifier(n_estimators=200, min_samples_leaf=2,
                                              random_state=42, n_jobs=1)),
    ])


def evaluate_model(df):
    if (df.Survived == (df.Sex == 'female').astype(int)).all():
        raise DataValidationError('Cinsiyet kuralıyla birebir eşleşen etiketler model değerlendirmesi için reddedildi.')
    train, test = train_test_split(df, test_size=0.2, random_state=42, stratify=df.Survived)
    model = make_pipeline()
    model.fit(train[FEATURES], train.Survived)
    prediction = model.predict(test[FEATURES])
    probability = model.predict_proba(test[FEATURES])[:, 1]
    dummy = DummyClassifier(strategy='most_frequent').fit(train[FEATURES], train.Survived)
    result = {
        'train_rows': len(train), 'test_rows': len(test), 'random_state': 42,
        'test_fraction': 0.2, 'features': FEATURES,
        'accuracy': float(accuracy_score(test.Survived, prediction)),
        'precision': float(precision_score(test.Survived, prediction, zero_division=0)),
        'recall': float(recall_score(test.Survived, prediction, zero_division=0)),
        'f1': float(f1_score(test.Survived, prediction, zero_division=0)),
        'roc_auc': float(roc_auc_score(test.Survived, probability)),
        'baseline_accuracy': float(accuracy_score(test.Survived, dummy.predict(test[FEATURES]))),
        'confusion_matrix': confusion_matrix(test.Survived, prediction, labels=[0, 1]).tolist(),
        'train_ids': train.PassengerId.astype(int).tolist(),
        'test_ids': test.PassengerId.astype(int).tolist(),
        'python': platform.python_version(), 'scikit_learn': sklearn.__version__,
    }
    return result, model


def write_results():
    result, _ = evaluate_model(load_csv())
    result['source_sha256'] = sha256(CSV_PATH.read_bytes()).hexdigest()
    result['model_code_sha256'] = sha256(Path(__file__).read_bytes()).hexdigest()
    output = ROOT / 'reports' / 'model_metrics.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"Accuracy: {result['accuracy']:.4f}; baseline: {result['baseline_accuracy']:.4f}; test: {result['test_rows']}")
    return result


if __name__ == '__main__':
    write_results()
