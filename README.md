
# Predicting Victory in League of Legends from Early-Game Statistics

## Project Overview

In competitive League of Legends, early-game performance often dictates which team gains momentum toward victory. The 15-minute mark represents a critical inflection point: it captures early kills, gold disparities, and objective control, and it is also the earliest moment when players are able to surrender.

This project predicts a team’s probability of winning using early-game statistics that are directly visible in the in-game scoreboard or easily tracked manually during live play.

Unlike many datasets that rely heavily on API-only data (e.g., jungle CS, champion IDs, XP totals), this project intentionally limits itself to inputs a player could realistically gather in real-time.

The model uses:

- **Binary early objectives** (first blood, first turret, first dragon)

- **Team vision stats** (wards placed, wards cleared)

- **Performance differences between teams** (kills, gold, cs, objectives, etc.)


These features form a lightweight but effective predictor suitable for:

- Player improvement tools

- Esports analytics

- Real-time win-chance dashboards

- Surrender decision evaluation



## Dataset

### Source
https://www.kaggle.com/datasets/thanhquc/league-of-legends-pre-15-minutes-stats

The dataset consists of ranked solo queue matches from Korean servers, containing early-game team statistics for both blue and red teams. This model uses blue team as the player's team for determining win/lose rate.

### Feature Engineering

Since the goal is real-time predictability without API access, the following transformations were applied:

#### Removed because they are NOT visible in-game

- Total experience

- Jungle minions killed

- Hidden or post-match values

- Red-team-only redundant fields

- Match ID and game duration (not needed for prediction)

#### Removed redundant features

Stats that exist for both blue and red teams (e.g., kills, gold, towers) were converted into diff features, such as:

- ``kills_diff``

- ``gold_diff``

- ``cs_diff``

- ``towers_diff``, etc.

This reduces input redundancy and better reflects the relative state of the match, which is stronger for prediction.

#### Renamed or consolidated features:

- ``bluewins`` → ``win``

- ``bluefirstblood`` → ``first_blood``

- ``bluefirstturret`` → ``first_turret``

- ``bluefirstdragon`` → ``first_dragon``

#### Final Input Features:

After processing, the model trains on:
```
first_blood
first_turret
first_dragon
wards_placed
wards_destroyed
kills_diff
deaths_diff
assists_diff
dragons_diff
heralds_diff
voidgrubs_diff
towers_diff
plates_diff
gold_diff
cs_diff
```
#### Target Variable:
- ``win`` - ``1`` if the team wins, ``0`` if it loses.
## Exploratory Data Analysis

#### Key findings from EDA

- Gold difference, tower difference, and first turret have the strongest correlations with winning.

- Dragon and herald advantages also strongly correlate with win probability.

- Vision stats correlate positively but with lower weight.

- Most diff features have intuitive positive or negative distributions toward the win outcome.

- Objective “firsts” (blood/turret/dragon) show strong win-rate advantages individually and cumulatively.

This can all be examined in full detail in the notebook.
## Modeling Approach & Metrics

### Problem Statement

This is a **binary classification** task:

- Predict whether the team will win or lose the match based on early-game visible statistics.

### Primary Metric

- **ROC-AUC** — chosen because it evaluates probabilistic ranking quality, not just accuracy.

### Training the Model

Multiple models were tested (Logistic Regression, Decision Tree, Random Forest, XGBoost) with an 80/20/20 split ratio and a set random seed for reproducibility.

After parameter tuning these were the results:

- **Logistic Regression**: 0.8655

- **Decision Tree**: 0.8618

- **Random Forest**: 0.8643

- **XGBoost**: 0.8652

### Conclusion

Surprisingly, **Logistic Regression** performed the best under this simplified, all-numeric dataset, likely because:

- No categorical champion data

- Many features are already normalized as differences

- Logistic Regression handles linear feature relationships cleanly

- Data is high-dimensional but not expressive enough for tree models to shine

Full details on the analysis and parameter tuning can be found in the notebook.
## How to Run
### Local

#### Dependencies
Recommended to use uv for dependencies.

```
uv sync
```

Otherwise run:

```
pip install -r requirements.txt
```

#### Training

There is a `model.bin` file already present with the trained model, but if you want to train the model yourself you may run:

```
uv run python train.py
```

#### Deployment

Now you can run:

```
uv run uvicorn predict:app --reload --host 0.0.0.0 --port 8080
```

On a new terminal, you can send a request with the following structure:

```
curl -X POST "http://localhost:8080/predict" \
  -H "Content-Type: application/json" \
  -d '{
      "first_blood": 1,
      "first_turret": 0,
      "first_dragon": 1,
      "wards_placed": 12,
      "wards_destroyed": 1,
      "kills_diff": 3,
      "deaths_diff": -1,
      "assists_diff": 2,
      "dragons_diff": 0,
       "heralds_diff": 1,
       "voidgrubs_diff": 0,
       "towers_diff": 1,
       "plates_diff": 5,
       "gold_diff": 3500,
       "cs_diff": 40
      }'
```

Simply tune the features to your liking. There are input limitations you can view in the 'predict.py' file itself.

You may also run

```
uv run python service.py
```

for a script that sends a request itself with inputs you can also modify. Just ensure that the `url` variable is set to `"http://localhost:8080/predict"` before running.

### Docker

#### Build Container

The Dockerfile provided allows you to build an image with this command:

```
docker build -t lol-match-predictor
```

#### Run Container

Simply run the following command:

```
docker run -it --rm -p 8080:8080 lol-match-predictor
```

Like with the local deploymeny, use

```
curl -X POST "http://localhost:8080/predict" \
  -H "Content-Type: application/json" \
  -d '{
      "first_blood": 1,
      "first_turret": 0,
      "first_dragon": 1,
      "wards_placed": 12,
      "wards_destroyed": 1,
      "kills_diff": 3,
      "deaths_diff": -1,
      "assists_diff": 2,
      "dragons_diff": 0,
       "heralds_diff": 1,
       "voidgrubs_diff": 0,
       "towers_diff": 1,
       "plates_diff": 5,
       "gold_diff": 3500,
       "cs_diff": 40
      }'
```

OR

```
uv run python service.py
```

to use the predict app.

### Cloud API

The application has also been deployed to Google Cloud Run at:

https://predict-lol-match-win-565690770584.us-west1.run.app/

The API is active and can be used at anytime. Similar to the local way, run the following with the above url:

```
curl -X POST "https://predict-lol-match-win-565690770584.us-west1.run.app/predict" \
  -H "Content-Type: application/json" \
  -d '{
      "first_blood": 1,
      "first_turret": 0,
      "first_dragon": 1,
      "wards_placed": 12,
      "wards_destroyed": 1,
      "kills_diff": 3,
      "deaths_diff": -1,
      "assists_diff": 2,
      "dragons_diff": 0,
       "heralds_diff": 1,
       "voidgrubs_diff": 0,
       "towers_diff": 1,
       "plates_diff": 5,
       "gold_diff": 3500,
       "cs_diff": 40
      }'
```

```
uv run python service.py
```

You can also access the direct interactive interface with:

```
https://predict-lol-match-win-565690770584.us-west1.run.app/docs
```
## Known Limitations / Next Steps
### Limitations:

- No champion data → limits meta/role interactions with no categorical feature contributions

- No lane-level data → cannot evaluate mismatches or power spikes

- No jungle CS / XP due to in-game visibility constraints

- Logistic regression assumes linear influence, which may oversimplify complex game dynamics

### Potential Future Improvements

- Add champion embeddings (if API access allowed)

- Add lane-differentiated CS, damage, or gold

- Try time-series modeling (LSTM, transformers)

- Build a real-time overlay or web dashboard

- Add uncertainty estimation (e.g., calibration curves)
