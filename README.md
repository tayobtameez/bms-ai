# 🔋 AI-Powered Battery Management System (BMS)

An AI-driven BMS that predicts battery degradation, optimizes charging cycles, and provides real-time monitoring.

## Project Structure

```
bms-ai/
├── data/               # Raw and processed battery datasets
├── models/             # Saved ML models
├── src/
│   ├── degradation/    # Degradation prediction (ML)
│   ├── charging/       # Charging cycle optimizer
│   ├── monitoring/     # Real-time monitoring & alerts
│   └── utils/          # Shared utilities (data loaders, metrics)
├── notebooks/          # Jupyter notebooks for exploration
├── dashboard/          # Web dashboard (Streamlit)
└── tests/              # Unit tests
```

## Modules

| Module | Owner | Description |
|---|---|---|
| `src/degradation/` | ML lead | Predicts State of Health (SoH) using regression/LSTM |
| `src/charging/` | Both | Optimizes CC-CV charging profiles |
| `src/monitoring/` | Both | Real-time telemetry, alerts, dashboard |
| `src/utils/` | Both | Shared data loaders, feature engineering |

## Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/bms-ai.git
cd bms-ai

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the dashboard
streamlit run dashboard/app.py
```

## Dataset
We use the [NASA Battery Dataset](https://www.nasa.gov/content/prognostics-center-of-excellence-data-set-repository) and [CALCE Battery Data](https://calce.umd.edu/battery-data).

## Team
- You — Embedded systems, control loops, charging optimizer
- Your friend — Electrochemistry modeling, degradation prediction
