from app.ml.contracts import StudentFeatureVector


def predict_risk(features: StudentFeatureVector) -> dict:
    score = 0

    if features["attendance_rate"] < 0.75:
        score += 2

    if features["avg_sleep_hours"] is not None:
        if features["avg_sleep_hours"] < 6:
            score += 2

    if features["avg_study_hours"] is not None:
        if features["avg_study_hours"] < 1.5:
            score += 1

    if score >= 4:
        risk = "HIGH"
    elif score >= 2:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "risk_level": risk,
        "score": score,
    }
