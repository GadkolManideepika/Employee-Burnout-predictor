import os
import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# explicitly name the model to avoid HF warnings and to cache locally
MODEL_NAME = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"

# initialize once at import
try:
    sentiment_pipeline = pipeline("sentiment-analysis", model=MODEL_NAME)
except Exception as e:
    # fallback: pipeline may not be available in some environments
    print(f"Could not initialize sentiment pipeline: {e}")
    sentiment_pipeline = None


def run(data):
    results = []
    if sentiment_pipeline is None:
        raise RuntimeError("Sentiment pipeline not available")

    for row in data:
        try:
            analysis = sentiment_pipeline(row["message_text"])[0]
            sentiment_score = analysis["score"] if analysis["label"] == "POSITIVE" else -analysis["score"]
        except Exception as e:
            print(f"Error analyzing row {row}: {e}")
            # default to neutral
            analysis = {"label": "NEUTRAL", "score": 0.0}
            sentiment_score = 0.0

        results.append({
            "employee_id": row["employee_id"],
            "timestamp": row["timestamp"],
            "message_text": row["message_text"],
            "sentiment": analysis["label"],
            "sentiment_score": sentiment_score
        })
    return results

def save_results(results, filepath="mock_data.csv"):
    df = pd.DataFrame(results)
    base_dir = os.path.dirname(__file__)
    full_path = os.path.join(base_dir, filepath)
    df.to_csv(full_path, index=False)
