from flask import Flask, jsonify
import os
import data_ingestion, sentiment_analysis, risk_scoring, alerts

app = Flask(__name__)

@app.route("/analyze", methods=["GET"])
def analyze():
    # load data from the package directory regardless of cwd
    data = data_ingestion.load_data("mock_data.csv")
    sentiments = sentiment_analysis.run(data)
    risks = risk_scoring.evaluate(sentiments)

    # Add risk scores to results
    for s in sentiments:
        s["risk_score"] = risks.get(s["employee_id"], "Unknown")

    # Save updated CSV for Streamlit
    sentiment_analysis.save_results(sentiments, "mock_data.csv")

    alerts.notify(risks)
    return jsonify(risks)

if __name__ == "__main__":
    # running in development mode under OneDrive triggers spurious file-change
    # events (watchdog) which cause Flask to endlessly restart. the simple
    # workaround is to turn off the reloader/debug mode when launching locally.
    #
    # You can still inspect logs/errors manually; the pipeline output will be
    # printed to stdout.
    app.run(debug=False)
