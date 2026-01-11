from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.prediction import StudentPrediction
from app.models.user import User
from app.core.permissions import require_roles
from app.ml.feature_builder import build_features
from app.ml.model import predict_risk

router = APIRouter(
    prefix="/ml",
    tags=["ML"],
)
@router.post("/predict/{student_id}")
def run_prediction(
    student_id,
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    features = build_features(db, student_id)
    result = predict_risk(features)

    prediction = StudentPrediction(
        student_id=student_id,
        model_version="v1-rule-based",
        output={
            "features": features,
            "prediction": result,
        },
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return prediction
