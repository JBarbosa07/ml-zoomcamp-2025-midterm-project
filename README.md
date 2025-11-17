# Predicting Victory in League of Legends from Early-Game Statistics

## Project Overview
In competitive *League of Legends* matches, early-game performance often determines which team gains momentum toward victory. Key milestones, especially the **15-minute laning phase**, reflects critical indicators like gold, kills, and objective control, which can significantly influence the outcome of a match. The 15-minute mark is also crucially the first opportunity for players to forfeit a match, so a means to accurately assess whether it is worth cutting losses early is valuable.

This project aims to **predict a team’s probability of winning** using early-game statistics. The model considers:

- Numerical performance indicators for each role (`gold_14`, `xp_14`, `kda_14`)  
- Team objectives (`dragons_14`, `towers_14`, `plates_14`)  
- Champion selection per role (`top`, `jungle`, `mid`, `adc`, `support`)  

The aggregated dataset represents **team-level and match-level data**, where each row contains both teams’ compositions, early-game stats, and objectives.

The goal is to help both casual or competitive players, coaches, or automated systems quickly assess whether a team is on track to win, providing insights for **real-time evaluation, esports analytics, or player training dashboards**.

---

## Dataset
URL: https://www.kaggle.com/datasets/thanhquc/league-of-legends-pre-15-minutes-stats

The dataset contains ranked solo queue matches from Korean servers in *League of Legends*, collected via Riot’s official API. It contains data for both the blue team and red team, showing stats for both teams including wards placed/destroyed, kills, deaths, assists, objectives, etc.

### **Simplification/Feature Engineering**
The original dataset contains lots of information that cannot be gleaned directly during a match- Only postgame directly from the client or entirely hidden outside of the Riot API. While this information is quite salient for training a model, I want this project to be entirely focussed on informaton that a player can directly get from a real-time match.

As such, several features from the dataset were removed, leaving only stats that are directly visible in the in-game scoreboard, or through manually keeping track of team objectives. 1-to-1 stats between blue and red team such as Kills/Deaths/Assists were also consolidated into features that took only the differences, in order to remove redundancies and simplify the inputs for the API.

(provide a list here)

### **Target Variable**
- `win` — binary variable indicating whether the **blue team won** (`1`) or lost (`0`).

---

## Problem Framing
This is a **binary classification problem**:  

> Predict whether the blue team wins (`1`) or loses (`0`) based on early-game statistics and champion selections.

**Primary evaluation metric:** ROC-AUC  

**Justification:** Early-game analysis is critical in competitive strategy. A model predicting outcomes from mid-game snapshots can support:

- Tactical evaluation for esports teams or casual players 
- AI commentary and highlight generation  
- Game balance and design research  
- Educational dashboards for player improvement  

---

## Intended Usage
- **Training phase:** Learn patterns from historical matches linking team composition, early-game stats, and outcomes.  
- **Prediction phase (API):** Submit early-game data from a new match (15-minute snapshot) and receive a **win probability** for the team.

---

## Example API Request & Response

**Input JSON:**
```json
{
  "blue_team": {
    "top": "garen",
    "jungle": "leesin",
    "mid": "ahri",
    "adc": "jinx",
    "support": "thresh",
    "gold_14": 9252,
    "xp_14": 10317,
    "kda_14": 3.2,
    "towers_14": 2,
    "dragons_14": 1,
    "plates_14": 5
  },
  "red_team": {
    "top": "darius",
    "jungle": "amumu",
    "mid": "zed",
    "adc": "caitlyn",
    "support": "lux",
    "gold_14": 9780,
    "xp_14": 6599,
    "kda_14": 2.5,
    "towers_14": 1,
    "dragons_14": 0,
    "plates_14": 3
  }
}
```
**Output JSON:**
```json
{
  "blue_win_probability": 0.73
}
```
