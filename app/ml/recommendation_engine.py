from typing import List, Dict


def generate_recommendations(
    risk_scores: Dict,
    similar_students: List[Dict],
) -> List[Dict]:
    recommendations = []

    # ---- Attendance ----
    if risk_scores["attendance_risk"] > 0.6:
        recommendations.append({
            "area": "attendance",
            "suggestion": "Maintain consistent class attendance and avoid late entries",
            "priority": "HIGH",
        })

    # ---- Academics ----
    if risk_scores["academic_risk"] > 0.6:
        recommendations.append({
            "area": "academics",
            "suggestion": "Adopt structured daily revision and weekly test practice",
            "priority": "HIGH",
        })

    # ---- Behavior ----
    if risk_scores["behavior_risk"] > 0.5:
        recommendations.append({
            "area": "behavior",
            "suggestion": "Improve sleep consistency and reduce late-night screen usage",
            "priority": "MEDIUM",
        })

    # ---- Similar Student Reinforcement ----
    for s in similar_students:
        if s["outcome"] == "Improved":
            recommendations.append({
                "area": "academics",
                "suggestion": f"Students with similar profiles improved by: {s['actions_taken']}",
                "priority": "MEDIUM",
            })

    return _deduplicate(recommendations)
def _deduplicate(recs: List[Dict]) -> List[Dict]:
    seen = set()
    unique = []

    for r in recs:
        key = (r["area"], r["suggestion"])
        if key not in seen:
            seen.add(key)
            unique.append(r)

    return unique
