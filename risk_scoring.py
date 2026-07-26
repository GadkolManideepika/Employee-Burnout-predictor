def evaluate(sentiments):
    risk_scores = {}
    for s in sentiments:
        emp = s["employee_id"]
        score = s["sentiment_score"]
        risk_scores[emp] = risk_scores.get(emp, 0) + score
    
    risks = {}
    for emp, total in risk_scores.items():
        if total < -2:
            risks[emp] = "High"
        elif total < 0:
            risks[emp] = "Medium"
        else:
            risks[emp] = "Low"
    return risks
