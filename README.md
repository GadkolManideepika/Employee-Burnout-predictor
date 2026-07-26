# Employee Burnout Predictor

This repository contains a simple Flask backend and a Streamlit frontend that
analyzes mock employee messages for sentiment and computes a basic ``burnout``
risk score.

## Requirements

Install the Python dependencies into your preferred virtual environment:

```powershell
python -m pip install -r requirements.txt
```

The `requirements.txt` file includes:

```
flask
streamlit
transformers
torch
pandas
seaborn
matplotlib
requests
```

## Running the project

There are two components:

1. **Backend** – serves a single `/analyze` endpoint that reads
   `backend/mock_data.csv`, sends each message to a Hugging‑Face sentiment
   pipeline, computes a risk level, writes the updated CSV back out, and
   prints any high‑risk alerts to stdout.
2. **Frontend** – a Streamlit app that reads `backend/mock_data.csv` and
   displays charts/heatmaps for the sentiment and risk scores.

### Option A – manual (two terminals)

```powershell
# terminal 1: start the backend
cd C:\Users\balag\OneDrive\Desktop\Hackathon
python backend/app.py

# terminal 2: once the backend is running, populate the CSV once
curl http://127.0.0.1:5000/analyze

# still in terminal 2 (or a third), start the dashboard
streamlit run frontend/dashboard.py
```

Visit `http://localhost:8501` to view the dashboard.

### Option B – helper script

A convenience script is provided that launches both servers and invokes
`/analyze` automatically:

```powershell
python start.py
```

It will check for required packages, start the Flask process, call the
endpoint, and then start Streamlit. Use `Ctrl+C` to stop both services.

## Common problems

* **`ModuleNotFoundError`** – make sure you are working from the repository root
  and have run `pip install -r requirements.txt` in the same Python
  environment you are using to run the scripts.
* **Missing CSV columns** – the loader expects the CSV to contain
  `employee_id`, `timestamp`, and `message_text`. The sample data already
  contains these; do not delete them.
* **Infinite restart loop on Windows/OneDrive** – the backend is run with
  `debug=False` so that Flask's watcher does not detect spurious file
  changes. Do not run with `debug=True` when editing inside OneDrive.
* **Transformer warnings about unauthenticated HF requests** – ignore them or
  supply a `HF_TOKEN` environment variable or explicitly configure a model in
  `backend/sentiment_analysis.py`.

## Extending the project

* Add more sophisticated risk logic in `backend/risk_scoring.py`.
* Replace the Hugging‑Face model with a locally trained one.
* Expand the dashboard with additional Streamlit widgets.

---

Feel free to edit the code or raise issues if something stops working.
