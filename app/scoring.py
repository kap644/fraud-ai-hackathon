def calculate_confidence(features):
    score = 1.0

    # 1. Spectral flatness (AI voices are smoother)
    if features["flatness"] > 0.20:
        score -= 0.35

    # 2. Pitch variation (AI is controlled)
    if features["pitch_variance"] < 30:
        score -= 0.30

    # 3. Energy too smooth = AI
    if features["energy_variance"] < 0.02:
        score -= 0.25

    # 4. Very low silence = TTS style
    if features["silence_ratio"] < 0.08:
        score -= 0.20

    # 5. Extra paranoia: ultra-clean audio
    if (
        features["flatness"] > 0.18
        and features["energy_variance"] < 0.03
    ):
        score -= 0.20

    return round(max(0.0, min(score, 1.0)), 2)

