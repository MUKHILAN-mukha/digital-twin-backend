import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


FEATURE_KEYS = [
    "attendance_7d",
    "attendance_30d",
    "attendance_delta",
    "test_score_7d",
    "test_score_30d",
    "test_score_delta",
    "behavior_score_avg",
]


def vectorize(feature_obj: dict) -> np.ndarray:
    return np.array([feature_obj.get(k, 0.0) for k in FEATURE_KEYS]).reshape(1, -1)


def compute_similarity(current_features: dict, historical_records: list, top_k=3):
    current_vector = vectorize(current_features)

    results = []

    for record in historical_records:
        hist_vector = vectorize(record.feature_vector)
        score = cosine_similarity(current_vector, hist_vector)[0][0]

        results.append({
            "similarity": round(float(score), 4),
            "actions_taken": record.actions_taken,
            "outcome": record.outcome,
        })

    results.sort(key=lambda x: x["similarity"], reverse=True)

    return results[:top_k]
