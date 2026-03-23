# Prediction Confidence Decay Tracker

> Track your predictions. Measure your confidence. Know your biases.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What Is This?

The **Prediction Confidence Decay Tracker** is a full-stack Python SaaS application that helps individuals and teams log predictions, assign confidence scores, and track how that confidence changes over time — until the prediction resolves.

Most people make predictions vaguely with no accountability. This tool forces you to put a number on your certainty, update it as new evidence arrives, and face the outcome honestly. Over time, it reveals your cognitive biases and measures whether your judgment is actually reliable.

---

## Features

- **Confidence decay tracking** — log how your confidence changes over time with timestamped updates
- **Brier score calibration** — the same formula used by intelligence agencies and superforecasters
- **Bias detection** — automatically flags overconfidence, anchoring, and hedging patterns
- **Decay curve fitting** — uses `scipy.optimize.curve_fit` to model your confidence trajectory
- **Team workspaces** — share predictions within a team and compare calibration scores
- **Full authentication** — JWT-based login and registration with bcrypt password hashing
- **Interactive charts** — Plotly confidence decay line charts with hover tooltips
- **Stripe billing ready** — personal, team, and enterprise pricing tiers
- **REST API** — full FastAPI backend with automatic Swagger documentation

---

## App Walkthrough — Step by Step

Here is the complete user journey through the app with real screenshots taken from the working application.

---

### Step 1 — Dashboard (fresh start)

When you first log in you land on the main dashboard. All counters start at zero. The left side shows **"No predictions yet!"** and the right side has the New prediction form ready to fill in. The sidebar shows your name, email address, and navigation buttons for Dashboard and Calibration.

```
Total: 0  |  Open: 0  |  Accuracy: 0%  |  Resolved: 0
```

This is what every new user sees. The sidebar greeting confirms you are logged in with your own account — your predictions are private and only visible to you.

![Dashboard - fresh start](assets/screenshot/1000029565.jpg)

---

### Step 2 — Fill in a new prediction

On the right side of the dashboard, fill in the **New prediction** form with a specific, measurable prediction:

| Field | Example value |
|---|---|
| Prediction | I will get a data science job by December 2026 |
| Notes | Currently applying to companies |
| Deadline | 2026/11/18 |
| Confidence slider | 82% |
| Category | career |

The confidence slider is the key field — it forces you to commit to a specific number rather than a vague "probably". Click **Save prediction** when done.

![New prediction form](assets/screenshot/1000029566.jpg)

---

### Step 3 — Prediction appears in the list

After saving, the dashboard left side immediately shows the prediction as a card:

- **Title** in bold — "I will get a data science job by December 2026"
- **Confidence: 82% | open** below the title
- A **blue progress bar** showing 82% confidence visually
- A **View** button to open the full detail page

The form on the right resets ready for the next prediction. The stats bar at the top now shows Total: 1, Open: 1.

![Prediction appears in list](assets/screenshot/1000029567.jpg)

---

### Step 4 — Prediction detail page — first data point

Clicking **View** opens the detail page. At the top you see three key metrics:

```
Current confidence: 82%
Change since start: +0%
Status: OPEN
```

Below the metrics is the **Confidence decay chart** — a Plotly interactive chart showing one blue dot at 82% on the date the prediction was created. This single point is the starting position of the decay curve. Hover over the dot to see the exact date and value.

Below the chart is the **Update log** showing the first entry:

```
82% — 2026-03-23 · Initial estimate
```

This log is append-only — entries can never be edited or deleted. This immutability is what makes the data trustworthy.

![Prediction detail - first data point](assets/screenshot/1000029568.jpg)

---

### Step 5 — Update and resolve control panel

Scrolling down the detail page reveals the full control panel split into two columns:

**Left — Update confidence**
- New confidence slider (starts at current value)
- "What changed?" text input for your note explaining why confidence changed
- Update button to save the new entry to the log

**Right — Resolve**
- **Mark correct** (orange — the primary action button)
- Mark wrong
- Delete

You use Update to log ongoing changes as new information arrives. You use Resolve only when the deadline arrives and you know the final outcome.

![Update and resolve control panel](assets/screenshot/1000029569.jpg)

---

### Step 6 — Update confidence down to 41%

New information arrives that makes you less certain — perhaps a rejection from a company or increased competition in the job market. Drag the slider from 82% down to **41%**. Optionally add a note in "What changed?" explaining what happened. Click **Update**.

This demonstrates the core habit — you do not ignore uncomfortable evidence. You face it and log it honestly. The slider forces you to be specific about how much your confidence changed.

![Updating confidence down to 41%](assets/screenshot/1000029570.jpg)

---

### Step 7 — Decay chart shows two connected points

After clicking Update, the **Confidence decay chart** now shows two data points connected by a blue line:

- Point 1: **82%** — the initial estimate
- Point 2: **41%** — after the update

The downward line between them is the "decay" in the tracker name. The Update log below now shows both entries in reverse chronological order:

```
41% — 2026-03-23
82% — 2026-03-23 · Initial estimate
```

Every entry is timestamped and permanent. You can never rewrite history — the record is what it is.

![Decay chart with two connected points](assets/screenshot/1000029571.jpg)

---

### Step 8 — Confidence rises back to 96% — chart shows full journey

More positive evidence arrives — a strong interview, a referral from a connection, or a promising lead. Update confidence upward to **96%**. The detail page now shows:

```
Current confidence: 96%
Change since start: +14%
Status: OPEN
```

The chart now shows **three connected data points** — 82% → 41% → 96% — forming a line that goes down and then back up. This demonstrates a key insight: confidence does not only decay. It rises and falls as real evidence accumulates over time.

The Update log shows the complete history:

```
96% — 2026-03-23
41% — 2026-03-23
82% — 2026-03-23 · Initial estimate
```

![Confidence decay chart showing full 3-point journey](assets/screenshot/1000029572.jpg)

---

### Step 9 — Ready to resolve

When December 2026 arrives, you return to this prediction and click one of the two resolve buttons:

- **Mark correct** — you got the data science job ✅
- **Mark wrong** — you did not get the job ❌

This single action feeds your calibration score. The Brier score, skill score, and bias report on the Calibration page all update automatically based on your resolved predictions. The more predictions you resolve, the more accurate and meaningful your calibration score becomes.

---

### What the full journey proves

The 9 steps above show the complete prediction lifecycle working end to end:

```
Register
  → Dashboard (empty)
    → Add prediction with 82% confidence
      → View detail — 1 point on chart
        → Update confidence DOWN to 41%
          → Chart shows decay line
            → Update confidence UP to 96%
              → Chart shows full 3-point journey
                → December 2026 — Resolve as correct or wrong
                  → Calibration score updates
```

Every step is logged with a timestamp. Every confidence number is permanent. The chart is a mirror of your actual thinking over time — not what you remember thinking, but what you actually logged. That is what makes this tool different from keeping notes or using a spreadsheet.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (pure Python — no JavaScript) |
| Backend API | FastAPI + Uvicorn |
| Database ORM | SQLAlchemy |
| Database | PostgreSQL |
| Auth | python-jose + passlib + bcrypt |
| Data science | NumPy + SciPy + scikit-learn + Pandas |
| Charts | Plotly |
| HTTP client | httpx |
| Config | pydantic-settings |
| Billing | Stripe Python SDK |

---

## Project Structure

```
prediction-tracker/
├── main.py                        # FastAPI entry point
├── .env                           # Environment variables (not committed)
├── requirements.txt               # All Python packages
│
├── backend/
│   ├── config.py                  # Settings loaded from .env
│   ├── auth.py                    # JWT auth + password hashing
│   ├── models/                    # SQLAlchemy database models
│   │   ├── user.py
│   │   ├── prediction.py
│   │   ├── confidence_log.py
│   │   └── workspace.py
│   ├── schemas/                   # Pydantic request/response models
│   │   ├── prediction.py
│   │   └── user.py
│   ├── routers/                   # API endpoints
│   │   ├── users.py               # /api/users — register, login, me
│   │   ├── predictions.py         # /api/predictions — full CRUD
│   │   └── analytics.py           # /api/analytics — calibration, bias, decay
│   └── analytics/                 # Data science core
│       ├── brier.py               # Brier score formula
│       ├── bias.py                # Overconfidence, anchoring, hedging detection
│       └── decay.py               # scipy curve fitting
│
├── database/
│   └── connection.py              # SQLAlchemy engine + session + Base
│
├── frontend/
│   ├── app.py                     # Streamlit entry point + login/register
│   ├── pages/
│   │   ├── dashboard.py           # Stats bar + prediction list + add form
│   │   ├── prediction_detail.py   # Decay chart + update + resolve
│   │   └── calibration.py         # Brier score + bias report
│   └── utils/
│       ├── api_client.py          # All httpx calls to FastAPI
│       └── state.py               # Streamlit session state helpers
│
└── tests/
    ├── unit/
    │   ├── test_brier.py
    │   ├── test_calibration.py
    │   └── test_bias.py
    └── integration/
        └── test_predictions_api.py
```

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 15 or higher
- Git

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/Diksha2605/prediction-tracker.git
cd prediction-tracker
```

**2. Create and activate virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the root folder:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/prediction_tracker
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
STRIPE_SECRET_KEY=sk_test_your_stripe_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
APP_NAME=Prediction Tracker
DEBUG=True
FRONTEND_URL=http://localhost:8501
BACKEND_URL=http://localhost:8000
```

**5. Create the PostgreSQL database**

```bash
psql -U postgres -c "CREATE DATABASE prediction_tracker;"
```

**6. Start the FastAPI backend**

```bash
uvicorn main:app --reload --port 8000
```

API running at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

**7. Start the Streamlit frontend** (open a second terminal)

```bash
streamlit run frontend/app.py
```

App running at `http://localhost:8501`

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/users/register` | Create a new account |
| POST | `/api/users/login` | Login and get JWT token |
| GET | `/api/users/me` | Get current user |
| GET | `/api/predictions` | List all predictions |
| POST | `/api/predictions` | Create a new prediction |
| GET | `/api/predictions/{id}` | Get a single prediction |
| PATCH | `/api/predictions/{id}` | Update a prediction |
| POST | `/api/predictions/{id}/confidence` | Log a confidence update |
| DELETE | `/api/predictions/{id}` | Delete a prediction |
| GET | `/api/analytics/calibration` | Get Brier score and calibration data |
| GET | `/api/analytics/bias` | Get bias report |
| GET | `/api/analytics/decay/{id}` | Get decay curve for a prediction |

Full interactive documentation at `http://localhost:8000/docs`

---

## Understanding Your Calibration Scores

| Score | Excellent | Good | Needs Work |
|---|---|---|---|
| Brier score | 0.0 – 0.1 | 0.1 – 0.2 | 0.2+ |
| Skill score | 0.5+ | 0.2 – 0.5 | Below 0 |
| Overconfidence gap | Near 0 | ±5% | ±15%+ |

**Brier score** — 0.0 is perfect, 0.25 is random guessing, above 0.25 is worse than random.

**Skill score** — how much better than random you are. Positive means you add value over guessing.

**Overconfidence gap** — the difference between your average confidence and your actual accuracy. Positive means you start too confident on average.

---

## Deployment

### Backend — Railway (free tier available)

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

### Frontend — Streamlit Cloud (free)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set main file path to `frontend/app.py`
5. Add your environment variables in the Streamlit Cloud dashboard
6. Click Deploy — your app gets a public URL instantly

---

## Market Context

This project fills a genuine gap in the market. Existing tools are either public platforms (Metaculus), unmaintained hobbyist tools (PredictionBook), or $50,000+ consulting services (Good Judgment Inc.). No commercial B2B SaaS exists for private, team-based prediction tracking with confidence decay analytics.

**Target markets:** Finance & investing · Tech product teams · Healthcare & research · Strategy consulting · Government & intelligence · Education & coaching

---

## Roadmap

- [ ] Email reminders for approaching deadlines
- [ ] Slack and Notion integrations
- [ ] Team calibration leaderboard
- [ ] CSV and Excel export
- [ ] Mobile-responsive UI improvements
- [ ] REST API for enterprise integrations
- [ ] Prediction categories and tagging
- [ ] Public prediction sharing (opt-in)

---

## Contributing

Contributions are welcome. Please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License

```
MIT License

Copyright (c) 2026 Diksha2605

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Acknowledgements

- [Philip Tetlock](https://en.wikipedia.org/wiki/Philip_E._Tetlock) — research on superforecasting and calibration that inspired this project
- [FastAPI](https://fastapi.tiangolo.com) — the fastest Python web framework
- [Streamlit](https://streamlit.io) — the easiest way to build data apps in Python
- [SQLAlchemy](https://sqlalchemy.org) — the Python SQL toolkit

---

*Built with Python · Data science · FastAPI · Streamlit · PostgreSQL*

*© 2026 Diksha2605. All rights reserved.*
