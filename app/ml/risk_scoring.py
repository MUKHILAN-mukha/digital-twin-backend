def clamp(value: float, min_v=0.0, max_v=100.0) -> float:
    return max(min_v, min(max_v, value))


def compute_risk_scores(features):
    """
    Explainable, deterministic risk decomposition.
    """

    attendance_risk = clamp(100 - features.attendance_30d)
    academic_risk = clamp(100 - features.test_score_30d)
    behavior_risk = clamp(100 - features.behavior_score_avg)

    volatility_risk = clamp(
        abs(features.attendance_7d - features.attendance_30d)
        + abs(features.test_score_7d - features.test_score_30d)
    )

    total_risk = clamp(
        (0.35 * academic_risk)
        + (0.30 * attendance_risk)
        + (0.20 * behavior_risk)
        + (0.15 * volatility_risk)
    )

    return {
        "academic_risk": academic_risk,
        "attendance_risk": attendance_risk,
        "behavior_risk": behavior_risk,
        "volatility_risk": volatility_risk,
        "total_risk": total_risk,
        # 🔴 REQUIRED FOR AUDIT
        "factor_contributions": {
            "academic": academic_risk,
            "attendance": attendance_risk,
            "behavior": behavior_risk,
            "volatility": volatility_risk,
            "weights": {
                "academic": 0.35,
                "attendance": 0.30,
                "behavior": 0.20,
                "volatility": 0.15,
            },
        },
    }
