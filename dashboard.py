import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Employee Burnout Predictor Dashboard")

# read the CSV relative to the repo root/backend folder
base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
csv_path = os.path.join(base, "backend", "mock_data.csv")

# fallback if file doesn't exist
if not os.path.exists(csv_path):
    st.error(f"Could not find data file at {csv_path}. Run the backend first.")
    data = pd.DataFrame()
else:
    data = pd.read_csv(csv_path)

st.subheader("Sentiment Trends")
if "sentiment_score" in data.columns:
    st.line_chart(data.groupby("employee_id")["sentiment_score"].mean())
else:
    st.warning("No sentiment_score column found. Run backend first.")

st.subheader("Burnout Risk Scores")
if "risk_score" in data.columns:
    st.table(data[["employee_id", "risk_score"]])
else:
    st.warning("No risk_score column found. Run backend first.")

# 🔹 New Heatmap Visualization
st.subheader("Team Burnout Risk Heatmap")
if "risk_score" in data.columns:
    # Convert risk levels to numeric values for heatmap
    risk_map = {"Low": 0, "Medium": 1, "High": 2}
    data["risk_numeric"] = data["risk_score"].map(risk_map)

    pivot = data.pivot_table(index="employee_id", values="risk_numeric", aggfunc="mean")

    fig, ax = plt.subplots(figsize=(6,4))
    sns.heatmap(pivot, annot=True, cmap="Reds", cbar_kws={'label': 'Burnout Risk'})
    st.pyplot(fig)
else:
    st.warning("No risk_score column found. Run backend first.")

st.subheader("HR Recommendations")
st.write("Employees flagged as High Risk should receive immediate HR outreach.")
