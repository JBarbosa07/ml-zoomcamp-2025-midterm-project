import requests

# url = 'http://localhost:8080/predict'
url = 'https://predict-lol-match-win-565690770584.us-west1.run.app/predict'

match = {
  "first_blood": 1,
  "first_turret": 1,
  "first_dragon": 1,
  "wards_placed": 20,
  "wards_destroyed": 2,
  "kills_diff": 2,
  "deaths_diff": -2,
  "assists_diff": 6,
  "dragons_diff": 0,
  "heralds_diff": 0,
  "voidgrubs_diff": -3,
  "towers_diff": 0,
  "plates_diff": 1,
  "gold_diff": 2020,
  "cs_diff": 62
}

response = requests.post(url, json=match)
pred = response.json()

print("Prediction:", pred)

if pred["win"]:
    print("Blue team likely wins")
else:
    print("Blue team likely loses")
