def predict(features: dict):
    """
    Temporary ML prediction.

    This will later be replaced by the
    actual Isolation Forest model.
    """

    typing_speed = features.get("typing_speed", 0)
    hold_time = features.get("mean_hold_time", 0)

    # Temporary baseline comparison.
    # These values are ONLY for testing the backend pipeline.
    score = 20

    if typing_speed < 40 or typing_speed > 100:
        score += 30

    if hold_time < 50 or hold_time > 120:
        score += 25

    score = min(score, 100)

    return {
        "anomaly_score": score,
        "confidence": 0.85
    }