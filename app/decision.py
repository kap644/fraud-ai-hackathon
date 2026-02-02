def classify(confidence):
    if confidence >= 0.80:
        return "Human"
    elif confidence <= 0.45:
        return "AI"
    else:
        return "Suspicious"
