def map_risk_level(total_risk: float) -> str:
    if total_risk < 35:
        return "LOW"
    elif total_risk < 65:
        return "MEDIUM"
    return "HIGH"
