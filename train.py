import pickle

import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import make_pipeline
from xgboost import XGBClassifier


def load_data():
    df = pd.read_csv('dataset.csv')

    df.columns = df.columns.str.lower().str.replace(' ', '_')

    # Remove unnecessary match id and redundant red-first-* flags
    del df['matchid']
    del df['redfirstblood']
    del df['redfirstturret']
    del df['redfirstdragon']

    return df


def train_model(df):
    # Target
    y_train = df['bluewins']

    # All input features except the target
    feature_cols = [c for c in df.columns if c != 'bluewins']

    # Convert to list-of-dicts
    train_dict = df[feature_cols].to_dict(orient='records')

    # Build pipeline: DictVectorizer → XGBoost
    pipeline = make_pipeline(
        DictVectorizer(sparse=False),
        XGBClassifier(
            eta=0.05,
            max_depth=5,
            min_child_weight=0.1,
            subsample=0.5,
            colsample_bytree=0.8,
            reg_lambda=20,
            reg_alpha=10,
            objective='binary:logistic',
            eval_metric='auc',
            nthread=8,
            seed=1,
            verbosity=1,
        )
    )

    pipeline.fit(train_dict, y_train)

    return pipeline


def save_model(filename, model):
    with open(filename, 'wb') as f_out:
        pickle.dump(model, f_out)

    print(f'Model saved to {filename}')


df = load_data()
pipeline = train_model(df)
save_model('model.bin', pipeline)
