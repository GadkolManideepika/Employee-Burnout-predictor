import requests

# Replace with your Slack Incoming Webhook URL (leave empty to disable)
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

def notify(risks):
    for emp, risk in risks.items():
        if risk == "High":
            # Print to console/logs
            alert_msg = f"🚨 BURNOUT ALERT: Employee {emp} is at HIGH risk. Recommend HR check-in and workload review."
            print(alert_msg)
            
            # Try to send to Slack if URL is configured
            if SLACK_WEBHOOK_URL:
                message = {
                    "text": f":rotating_light: Burnout Alert!\nEmployee {emp} is at HIGH burnout risk.\nRecommendation: Schedule HR check-in and workload review."
                }
                try:
                    response = requests.post(SLACK_WEBHOOK_URL, json=message)
                    if response.status_code != 200:
                        print(f"Slack error: {response.text}")
                except Exception as e:
                    print(f"Error sending Slack alert: {e}")
