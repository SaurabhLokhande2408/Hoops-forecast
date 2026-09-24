# Hoop-Forecast

**Predicting next-season scoring for NBA players with a FastAPI backend and React frontend.**

*No tutorial followed. No code copied. Just curiosity, a dataset, and a lot of broken runs.*

---

## What it does

Given a player's latest available season, Hoop-Forecast predicts how many points per game they will score **next season**.

```
Player: Stephen Curry
Prediction: 26.8 points per game in 2027

MAE : 2.41   MSE : 9.87   RMSE : 3.14   R² : 0.81
```

---

## Project structure

```
NBA/
│
├── backend/
│   ├── app/
│   │   ├── api/routes.py          # REST endpoints under /api
│   │   ├── services/              # Data, features, model, and player logic
│   │   ├── schemas/               # Pydantic request/response models
│   │   └── ml/train.py            # Offline model training command
│   ├── tests/                     # FastAPI endpoint tests
│   └── README.md                  # Backend route reference
├── hoops-forecast-frontend/      # React/Vite client
├── Data_preprocessing/            # Original preprocessing scripts
├── Dataset/                       # Read-only source dataset
├── ML_prediction/                 # Original standalone model script
├── Ml_training/                   # Original train/test split script
├── main.py                        # Original CLI entry point
├── requirements.txt               # Repository-wide Python dependencies
└── README.md
```

---

## The dataset

`Player Per Game.csv` — sourced from [Basketball Reference](https://www.basketball-reference.com/)

Every row is one player's per-game averages for one season. **33,339 rows × 32 columns**, covering 5,372 unique players across 79 seasons (1947–2026).

| Column | Description |
|---|---|
| `season` | Season year (1947–2026) |
| `player` | Full name |
| `age` | Age that season |
| `pos` | Position — PG, SG, SF, PF, C |
| `g` | Games played |
| `mp_per_game` | Minutes per game |
| `fg_percent` | Field goal % |
| `x3p_percent` | 3-point % |
| `ft_percent` | Free throw % |
| `pts_per_game` | ⭐ Points per game — **the value we predict** |
| `ast_per_game` | Assists per game |
| `trb_per_game` | Total rebounds per game |
| `stl_per_game` | Steals per game |
| `blk_per_game` | Blocks per game |

---

## How it works

### 1. Data cleaning — `backend/app/services/data_service.py`

- Missing shooting stats filled with `0` — players who never attempted them effectively have zero
- Missing `age`, `fg_percent`, `ft_percent` etc. filled with their **median**
- Players traded mid-season appear multiple times — kept only the row with most games played
- Dropped irrelevant columns: `lg`, `player_id`, `URL`

### 2. Feature engineering — `backend/app/services/feature_service.py`

The most important step. Three things happen here:

**Target label** — there's no `next_season_pts` column in the raw data, so it's created:
```python
df['next_season_pts'] = df.groupby('player')['pts_per_game'].shift(-1)
```
`shift(-1)` moves each player's points value up by one row, so this season's row gets next season's score as its label.

**One-hot encoding** — `pos` is a string; models don't speak strings. `pd.get_dummies()` converts it into five binary columns: `pos_C`, `pos_PF`, `pos_PG`, `pos_SF`, `pos_SG`.

**Age scaling** — `StandardScaler` normalises age to mean 0, std 1, so it doesn't get drowned out by larger-ranged stats.

### 3. Train/test split — `backend/app/ml/train.py`

80/20 split with `random_state=42`. The model never sees the test set during training.

### 4. Model — `backend/app/services/model_service.py`

```python
model = LinearRegression()
model.fit(X_train, y_train)
```

Linear Regression. Simple and interpretable — the right choice for a first project.

---

## Features used

```python
['pts_per_game', 'age_encoded', 'fg_percent', 'ft_percent', 'x3p_percent',
 'mp_per_game', 'ast_per_game', 'trb_per_game', 'g',
 'stl_per_game', 'blk_per_game',
 'pos_C', 'pos_PF', 'pos_PG', 'pos_SF', 'pos_SG']
```

---

## Setup and run

Create a Python environment from the repository root:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```

Train the model artifacts and start the API:

```bash
cd backend
python -m app.ml.train
uvicorn app.main:app --reload --port 8000
```

The API is available at `http://localhost:8000`, with interactive documentation at `http://localhost:8000/docs`.

Start the React frontend in a second terminal:

```bash
cd hoops-forecast-frontend
npm install
npm run dev
```

The frontend uses `http://localhost:8000/api` by default. To change it, copy `hoops-forecast-frontend/.env.example` to `.env` and set `VITE_API_BASE_URL`.

Run backend tests after training:

```bash
cd backend
pytest
```

The dataset is read from `Dataset/Player Per Game.csv` and is never modified. Backend paths and CORS origins can be overridden in `backend/.env`; see `backend/.env.example`.

## API

All API routes use the `/api` prefix:

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/api/health` | Service and model readiness |
| `GET` | `/api/players?search=cur&limit=8` | Search player names |
| `GET` | `/api/players/{player_name}` | Latest season statistics |
| `GET` | `/api/players/{player_name}/history` | Full season history |
| `POST` | `/api/predict` | Predict next-season points with `{ "player_name": "Stephen Curry" }` |
| `GET` | `/api/model/metrics` | Held-out model metrics and feature list |

Unknown players return `404` responses with close-match suggestions. Invalid request bodies and query parameters return FastAPI `422` responses.

---

## What I learned

This was my first real encounter with ML — not a tutorial, not a guided exercise. Here's what actually clicked.

**Supervised regression.** This is a supervised regression problem — supervised because every row has a known correct answer the model learns from, regression because the output is a continuous number (`24.3 pts`), not a category. Getting the problem type right shapes every decision after it.

**You have to build your own labels.** There's no `next_season_pts` column in the raw data. I had to create it using `shift(-1)` — a pandas trick that slides each player's points up by one row so the current season gets the next season's score as its target. That moment — realising the label doesn't exist and you have to construct it — is when ML stopped feeling like magic and started feeling like engineering.

**Data cleaning is 80% of the work.** The model is two lines. The preprocessing is everything else. Missing values aren't all the same — a `NaN` in `x3p_percent` means the player never shot a three, so `0` is correct. A `NaN` in `age` needs the median, not zero. Players traded mid-season appear multiple times — you need a domain decision about which row to keep, not just a blind drop. Real data is messy in ways tutorials don't prepare you for.

**Encoding turns categories into numbers.** A model can't multiply by the string `"PG"`. One-hot encoding converts `pos` into five binary columns — one fires `1` for the player's position, the rest are `0`. Now the model can assign a separate learned weight to each position.

**Scaling puts features on equal footing.** `age` (18–44) and `fg_percent` (0.0–0.7) live on completely different scales. Without normalisation, the model treats bigger numbers as more important — not because they carry more signal, but just because they're larger. `StandardScaler` transforms each feature to mean 0 and standard deviation 1 so the model competes on signal, not scale.

**How Linear Regression learns.** The model finds the best-fit equation: `predicted_pts = w₁(pts_per_game) + w₂(age_encoded) + ... + b`. Each weight is tuned during training to minimise prediction error. What I liked about it as a first model — every weight is readable. A negative age weight means the model learned older players tend to decline. You can see the logic.

**The train/test split protects against memorisation.** A model evaluated on its own training data looks perfect because it already saw the answers. Holding out 20% of data that the model never touches during training is how you measure whether it actually learned a pattern — that's called generalisation, and it's the whole point of building a model.

**What the metrics actually mean.** MAE is the average prediction error in real points — the most intuitive. RMSE penalises big misses harder, so if it's much larger than MAE, the model is occasionally way off. R² tells you what proportion of the variation in next-season scoring the model explains — 0.81 means 81% of the variation is captured, which is a genuinely good result on noisy real-world data.

---

## Stack

`pandas` · `scikit-learn` · `numpy` · `FastAPI` · `Uvicorn` · `React` · `Vite`

---

<div align="center">
<sub>My first machine learning project built, broken, fixed, and shipped.</sub>
</div>