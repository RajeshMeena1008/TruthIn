# ===== SAFE VERSION (NO TENSORFLOW) =====

def load_model():
    # TensorFlow disabled (deploy safe)
    return None


def predict_food(image, model=None):
    # Dummy prediction (for demo)
    return {
        "prediction": "Food Item",
        "confidence": 85.0,
        "note": "AI model disabled in deploy mode"
    }
