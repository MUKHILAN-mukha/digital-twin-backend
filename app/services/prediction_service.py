from app.models.prediction import StudentPrediction
from app.ml.risk_mapper import map_risk_level


def create_prediction(
    db,
    student_id,
    risk_score,
    model,
):
    feature_vector = [
        risk_score.academic_risk,
        risk_score.attendance_risk,
        risk_score.behavior_risk,
        risk_score.volatility_risk,
    ]

    probability, confidence = model.predict(feature_vector)

    prediction = StudentPrediction(
        student_id=student_id,
        risk_level=map_risk_level(risk_score.total_risk),
        confidence=confidence,
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction
