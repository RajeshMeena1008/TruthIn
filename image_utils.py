import numpy as np

def load_model():
    return None

def predict_food(model, image):
    image = image.convert("RGB")
    img = np.array(image)

    r = img[:, :, 0].mean()
    g = img[:, :, 1].mean()
    b = img[:, :, 2].mean()

    brightness = (r + g + b) / 3

    # 🍓 STRAWBERRY (strong red)
    if r > 160 and g < 120:
        return [("Strawberry", 95.0), ("Apple", 88.0), ("Cherry", 85.0)]

    # 🥦 BROCCOLI (strong green)
    elif g > 140 and r < 120:
        return [("Broccoli", 93.0), ("Spinach", 87.0), ("Cabbage", 82.0)]

    # 🍕 PIZZA (red + yellow mix)
    elif r > 130 and g > 120 and b < 120:
        return [("Pizza", 92.0), ("Pasta", 85.0), ("Sandwich", 80.0)]

    # 🍔 BURGER (brown tone)
    elif r > 110 and g > 80 and b < 90:
        return [("Burger", 91.0), ("Fries", 85.0), ("Sandwich", 82.0)]

    # 🍚 RICE (white / bright)
    elif brightness > 180:
        return [("Rice", 90.0), ("Dal", 85.0), ("Chapati", 80.0)]

    # default fallback
    else:
        return [("Food Item", 85.0), ("Snack", 80.0), ("Meal", 75.0)]
