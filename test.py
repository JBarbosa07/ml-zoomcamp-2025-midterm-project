import requests

url = 'http://localhost:9696/predict'

match = {
    "bluefirstblood": 1,
    "bluefirstturret": 1,
    "bluefirstdragon": 0,

    "bluewardsplaced": 41,
    "bluecontrolwardsplaced": 9,
    "bluewardsdestroyed": 11,
    "bluecontrolwardsdestroyed": 4,

    "bluekills": 7,
    "bluedeaths": 8,
    "blueassists": 7,

    "bluedragons": 0,
    "blueheralds": 0,
    "bluevoidgrubs": 6,

    "bluetowersdestroyed": 3,
    "blueplatesdestroyed": 7,
    "blueinhibitorsdestroyed": 0,

    "bluetotalgold": 24827,
    "bluetotalexperience": 28943,
    "bluetotalminionskilled": 347,
    "bluetotaljungleminionskilled": 83,


    "redwardsplaced": 33,
    "redcontrolwardsplaced": 9,
    "redwardsdestroyed": 11,
    "redcontrolwardsdestroyed": 2,

    "redkills": 8,
    "reddeaths": 7,
    "redassists": 14,

    "reddragons": 2,
    "redheralds": 0,
    "redvoidgrubs": 0,

    "redtowersdestroyed": 0,
    "redplatesdestroyed": 0,
    "redinhibitorsdestroyed": 2,

    "redtotalgold": 25332,
    "redtotalexperience": 31039,
    "redtotalminionskilled": 394,
    "redtotaljungleminionskilled": 108,

    "gameduration": 1409.276
}

response = requests.post(url, json=match)
pred = response.json()

print("Prediction:", pred)

if pred["win"]:
    print("Blue team likely wins")
else:
    print("Blue team likely loses")
