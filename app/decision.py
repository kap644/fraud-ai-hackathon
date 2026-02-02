def classify(confidence):
    if confidence >= 0.90:
        return "Human"
    elif confidence <= 0.55:
        return "AI"
    else:
        return "Suspicious"

