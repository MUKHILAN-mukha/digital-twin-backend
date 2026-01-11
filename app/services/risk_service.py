from app.models.risk_score import RiskScore
from app.ml.risk_scoring import compute_risk_scores
from app.services.alert_engine import generate_alerts


def create_risk_score(db, student_id, features):
    scores = compute_risk_scores(features)

    risk = RiskScore(
        student_id=student_id,
        academic_risk=scores["academic_risk"],
        attendance_risk=scores["attendance_risk"],
        behavior_risk=scores["behavior_risk"],
        volatility_risk=scores["volatility_risk"],
        total_risk=scores["total_risk"],
        factor_contributions=scores["factor_contributions"],
    )

    db.add(risk)
    db.commit()
    db.refresh(risk)

    generate_alerts(db, risk)

    return risk
