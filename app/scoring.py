def calculate_confidence(features):
    """
    Returns confidence that voice is HUMAN
    Range: 0.0 – 1.0
    """

    jitter = features.get("jitter", 0)
    shimmer = features.get("shimmer", 0)
    pitch_var = features.get("pitch_variation", 0)

    score = 0.0

    # Human voices usually have MORE jitter & shimmer
    if jitter > 0.015:
        score += 0.30
    if shimmer > 0.02:
        score += 0.30
    if pitch_var > 15:
        score += 0.40

    return round(min(score, 1.0), 2)

