import numpy as np

def load_model():
    return None

# ⚠️ order SAME जैसा app.py में call हो रहा है
def predict_food(model, image):
    image = image.convert("RGB")
    img = np.array(image)

    r = img[:, :, 0].mean()
    g = img[:, :, 1].mean()
    b = img[:, :, 2].mean()

    if r > 150 and g < 120:
        return [("Strawberry", 92.0)]
    elif g > 130 and r < 120:
        return [("Broccoli", 90.0)]
    elif r > 120 and g > 120:
        return [("Pizza", 88.0)]
    elif r > 100 and g > 80 and b < 100:
        return [("Burger", 85.0)]
    elif r > 180 and g > 180 and b > 180:
        return [("Rice", 80.0)]
    else:
        return [("Food Item", 75.0)]
