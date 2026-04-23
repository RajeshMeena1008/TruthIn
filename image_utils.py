import random

def load_model():
    return None

def predict_food(image, model=None):
    foods = [
        ("Pizza", 92.0),
        ("Burger", 88.0),
        ("Broccoli", 85.0),
        ("Apple", 90.0),
        ("Rice", 80.0),
        ("Pasta", 87.0)
    ]
    
    # random result select
    return [random.choice(foods)]
