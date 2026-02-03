def classify(confidence):
    if confidence >= 0.65:
        return "Human"
    elif confidence <= 0.40:
        return "AI"
    else:
        return "Suspicious"



