import pickle

import pandas as pd
import numpy as np
import sklearn

from xgboost import XGBClassifier


def load_data():
    df = pd.read_csv('dataset.csv')

    df.columns = df.columns.str.lower().str.replace(' ', '_')

    return df


def train_model(df):
    numerical = [col for col in df.columns if df[col].dtype != 'object' and col not in ['bluewins']]

    X_train = df[numerical]
    y_train = df['bluewins']

    model = XGBClassifier(
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

    model.fit(X_train, y_train)

    return model


def save_model(filename, model):
    with open(filename, 'wb') as f_out:
        pickle.dump(model, f_out)

    print(f'Model saved to {filename}')


df = load_data()
model = train_model(df)
save_model('model.bin', model)