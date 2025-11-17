import pickle

import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def load_data():
    df = pd.read_csv("dataset.csv")

    # Start with lowercase column names
    df.columns = df.columns.str.lower()

    # Columns to drop completely
    drop_cols = [
        'matchid',
        'gameduration',

        # jungle minions
        'bluetotaljungleminionskilled',
        'redtotaljungleminionskilled',

        # red vision stats
        'redwardsplaced',
        'redcontrolwardsplaced',
        'redwardsdestroyed',
        'redcontrolwardsdestroyed',

        # red first events (keeping only blue)
        'redfirstblood',
        'redfirstturret',
        'redfirstdragon',

        # experience is not visible in-game (optional)
        'bluetotalexperience',
        'redtotalexperience'
    ]

    df = df.drop(columns=drop_cols, errors='ignore')

    # Create diffs
    df['kills_diff'] = df['bluekills'] - df['redkills']
    df['deaths_diff'] = df['bluedeaths'] - df['reddeaths']
    df['assists_diff'] = df['blueassists'] - df['redassists']
    df['dragons_diff'] = df['bluedragons'] - df['reddragons']
    df['heralds_diff'] = df['blueheralds'] - df['redheralds']
    df['voidgrubs_diff'] = df['bluevoidgrubs'] - df['redvoidgrubs']
    df['towers_diff'] = df['bluetowersdestroyed'] - df['redtowersdestroyed']
    df['plates_diff'] = df['blueplatesdestroyed'] - df['redplatesdestroyed']
    df['gold_diff'] = df['bluetotalgold'] - df['redtotalgold']
    df['cs_diff'] = df['bluetotalminionskilled'] - df['redtotalminionskilled']

    # Drop the original left/right stat columns
    original_stats = [
        'bluekills', 'redkills',
        'bluedeaths', 'reddeaths',
        'blueassists', 'redassists',
        'bluedragons', 'reddragons',
        'blueheralds', 'redheralds',
        'bluevoidgrubs', 'redvoidgrubs',
        'bluetowersdestroyed', 'redtowersdestroyed',
        'blueplatesdestroyed', 'redplatesdestroyed',
        'bluetotalgold', 'redtotalgold',
        'bluetotalminionskilled', 'redtotalminionskilled'
    ]

    df = df.drop(columns=original_stats, errors='ignore')

    # Rename blue-side labels to generic names
    df = df.rename(columns={
        'bluewins': 'win',
        'bluefirstblood': 'first_blood',
        'bluefirstturret': 'first_turret',
        'bluefirstdragon': 'first_dragon',
        'bluewardsplaced': 'wards_placed',
        'bluewardsdestroyed': 'wards_destroyed'
    })

    # Final ordering
    df = df[
        [
            'win',
            'first_blood',
            'first_turret',
            'first_dragon',
            'wards_placed',
            'wards_destroyed',
            'kills_diff',
            'deaths_diff',
            'assists_diff',
            'dragons_diff',
            'heralds_diff',
            'voidgrubs_diff',
            'towers_diff',
            'plates_diff',
            'gold_diff',
            'cs_diff'
        ]
    ]

    return df


def train_model(df):
    # Target
    y_train = df['win']

    # All input features except the target
    features = [c for c in df.columns if c != 'win']

    # Convert to list-of-dicts
    train_dict = df[features].to_dict(orient='records')

    # Build pipeline: DictVectorizer → XGBoost
    pipeline = make_pipeline(
        DictVectorizer(sparse=False),
        StandardScaler(),
        LogisticRegression(solver='liblinear', max_iter=1000, C=0.1)
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
