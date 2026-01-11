from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.models.prediction import StudentPrediction
from app.models.user import User
from app.core.permissions import require_roles

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/risk-distribution")
def risk_distribution(
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    subquery = (
        db.query(
            StudentPrediction.student_id,
            func.max(StudentPrediction.created_at).label("latest")
        )
        .group_by(StudentPrediction.student_id)
        .subquery()
    )

    latest = (
        db.query(StudentPrediction)
        .join(
            subquery,
            (StudentPrediction.student_id == subquery.c.student_id) &
            (StudentPrediction.created_at == subquery.c.latest)
        )
        .all()
    )

    summary = {"low": 0, "medium": 0, "high": 0}

    for p in latest:
        summary[p.risk_level] += 1

    return summary


@router.get("/students")
def student_risk_table(
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    subquery = (
        db.query(
            StudentPrediction.student_id,
            func.max(StudentPrediction.created_at).label("latest")
        )
        .group_by(StudentPrediction.student_id)
        .subquery()
    )

    rows = (
        db.query(StudentPrediction)
        .join(
            subquery,
            (StudentPrediction.student_id == subquery.c.student_id) &
            (StudentPrediction.created_at == subquery.c.latest)
        )
        .all()
    )

    return [
        {
            "student_id": str(p.student_id),
            "risk_level": p.risk_level,
            "confidence": p.confidence,
            "generated_at": p.created_at,
        }
        for p in rows
    ]


@router.get("/student/{student_id}")
def student_risk_history(
    student_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    predictions = (
        db.query(StudentPrediction)
        .filter(StudentPrediction.student_id == student_id)
        .order_by(StudentPrediction.created_at.asc())
        .all()
    )

    return [
        {
            "created_at": p.created_at,
            "risk_level": p.risk_level,
            "confidence": p.confidence,
        }
        for p in predictions
    ]


@router.get("/high-risk")
def high_risk_students(
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    subquery = (
        db.query(
            StudentPrediction.student_id,
            func.max(StudentPrediction.created_at).label("latest")
        )
        .group_by(StudentPrediction.student_id)
        .subquery()
    )

    rows = (
        db.query(StudentPrediction)
        .join(
            subquery,
            (StudentPrediction.student_id == subquery.c.student_id) &
            (StudentPrediction.created_at == subquery.c.latest)
        )
        .filter(StudentPrediction.risk_level == "high")
        .all()
    )

    return [
        {
            "student_id": str(p.student_id),
            "confidence": p.confidence,
        }
        for p in rows
    ]
