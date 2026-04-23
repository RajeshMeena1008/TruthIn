import numpy as np

def load_model():
    return None

def predict_food(image, model=None):
    return "Food item (AI disabled)", 0.0

def load_model():
    global _model
    if _model is None:
        _model = MobileNetV2(weights="imagenet")
    return _model


def predict_food(model, img):
    img = img.resize((224, 224))
    arr = img_to_array(img)
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)

    preds = model.predict(arr)
    decoded = decode_predictions(preds, top=3)[0]

    results = []
    for (_, label, conf) in decoded:
        results.append((label, float(conf * 100)))

    return results
try:
    from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
    TF_AVAILABLE = True
except:
    TF_AVAILABLE = False
