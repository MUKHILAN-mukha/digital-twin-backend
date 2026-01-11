def generate_explanation(risk):
    factors = risk.factor_contributions

    primary = max(
        ["academic", "attendance", "behavior", "volatility"],
        key=lambda k: factors[k],
    )

    return (
        f"Primary risk driver is {primary}. "
        f"Academic={factors['academic']:.1f}, "
        f"Attendance={factors['attendance']:.1f}, "
        f"Behavior={factors['behavior']:.1f}, "
        f"Volatility={factors['volatility']:.1f}."
    )
