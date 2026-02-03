def calculate_confidence(features):
    score = 0.0

    if features.get("jitter", 0) < 0.02:
        score += 0.35
    if features.get("shimmer", 0) < 0.03:
        score += 0.35
    if features.get("pitch_variation", 0) > 20:
        score += 0.30

    return min(score, 1.0)
