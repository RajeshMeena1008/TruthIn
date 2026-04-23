import numpy as np

def load_model():
    return None

def predict_food(image, model=None):
    img = np.array(image)

    # RGB average
    r = img[:, :, 0].mean()
    g = img[:, :, 1].mean()
    b = img[:, :, 2].mean()

    # ===== SMART RULES =====
    
    # 🍓 Strawberry (red dominant)
    if r > 150 and g < 120:
        return [("Strawberry", 92.0)]
    
    # 🥦 Broccoli (green dominant)
    elif g > 130 and r < 120:
        return [("Broccoli", 90.0)]
    
    # 🍕 Pizza (mix red + yellow)
    elif r > 120 and g > 120:
        return [("Pizza", 88.0)]
    
    # 🍔 Burger (brownish)
    elif r > 100 and g > 80 and b < 100:
        return [("Burger", 85.0)]
    
    # 🍚 Rice (white/light)
    elif r > 180 and g > 180 and b > 180:
        return [("Rice", 80.0)]
    
    # default
    else:
        return [("Food Item", 75.0)]
