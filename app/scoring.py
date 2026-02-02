def calculate_confidence(features):
    score = 1.0

    if features["flatness"] > 0.25:
        score -= 0.30

    if features["pitch_variance"] < 20:
        score -= 0.25

    if features["energy_variance"] < 0.01:
        score -= 0.20

    if features["silence_ratio"] < 0.05:
        score -= 0.15

    return round(max(0.0, min(score, 1.0)), 2)
