# Predicting Victory in League of Legends from Early-Game Statistics

## Project Overview
In competitive *League of Legends* matches, early-game performance often determines which team gains momentum toward victory. Key milestones, such as the **14-minute laning phase** and **20-minute mid-game transition**, reflect critical indicators like gold, experience, kills, and objective control, which can significantly influence the outcome of a match.

This project aims to **predict a team’s probability of winning** using early-game statistics and champion compositions. The model considers:

- Numerical performance indicators for each role (`gold_14`, `xp_14`, `kda_14`, `gold_20`, `xp_20`, `damage_20`)  
- Team objectives (`dragons_14`, `towers_14`, `plates_14`)  
- Champion selection per role (`top`, `jungle`, `mid`, `adc`, `support`)  

The aggregated dataset represents **team-level and match-level data**, where each row contains both teams’ compositions, early-game stats, and objectives.

The goal is to help analysts, coaches, or automated systems quickly assess whether a team is on track to win, providing insights for **real-time evaluation, AI commentary, esports analytics, or player training dashboards**.

---

## Dataset
URL: https://www.kaggle.com/datasets/keerthivasankannan/lol-dataset

The dataset contains ranked solo queue matches from *League of Legends*, collected via Riot’s official API.  

### **Aggregation**
- Original dataset is **player-level**.  
- For modeling, rows were **aggregated to team-level per match**:
  - **Blue team** and **Red team** stats are represented as separate columns in a single row per match.  
  - Each player’s role is preserved (`top`, `jungle`, `mid`, `adc`, `support`) to keep **role-specific stats and champions**.

### **Selected Features**
| Feature Type          | Examples | Notes |
|----------------------|----------|-------|
| **Per-role stats** | `top_gold_14`, `mid_kda_14`, `adc_xp_20`, `support_damage_20` | Includes 14- and 20-minute snapshots |
| **Team objectives** | `dragons_14`, `towers_14`, `plates_14` | `heralds_14` and `grubs_14` removed (all zeros) |
| **Champion selections** | `champion_top_blue`, `champion_mid_red` | One-hot encoded for ML models |

### **Target Variable**
- `target_win` — binary variable indicating whether the **blue team won** (`1`) or lost (`0`).

### **Handling Missing / Zero Values**
- Rows where all numeric features were zero were removed as likely **corrupted or incomplete matches**.  
- All other numeric and categorical features are complete after aggregation.

---

## Problem Framing
This is a **binary classification problem**:  

> Predict whether the blue team wins (`1`) or loses (`0`) based on early-game statistics and champion selections.

**Primary evaluation metric:** ROC-AUC  
**Secondary metrics:** Accuracy, F1-score

**Justification:** Early-game analysis is critical in competitive strategy. A model predicting outcomes from mid-game snapshots can support:

- Tactical evaluation for esports teams  
- AI commentary and highlight generation  
- Game balance and design research  
- Educational dashboards for player improvement  

---

## Intended Usage
- **Training phase:** Learn patterns from historical matches linking team composition, early-game stats, and outcomes.  
- **Prediction phase (API):** Submit early-game data from a new match (14/20-minute snapshot) and receive a **win probability** for the blue team.

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
    "gold_20": 14230,
    "xp_20": 15600,
    "damage_20": 12500,
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
    "gold_20": 14010,
    "xp_20": 14520,
    "damage_20": 11900,
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
