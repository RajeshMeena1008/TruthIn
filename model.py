"""
model.py
Trains a Logistic Regression classifier on nutrition data.
Input features: calories, fat, sugar, protein, sodium
Output: Healthy / Moderate / Unhealthy
"""

import os
import numpy as np
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), "nutriscan_model.pkl")
DATA_PATH = os.path.join(os.path.dirname(__file__), "nutriscan_data.csv")

FEATURES = ["calories", "fat", "sugar", "protein", "sodium"]
LABEL_COL = "label"


def _generate_synthetic_data() -> pd.DataFrame:
    np.random.seed(42)
    rows = []
    for _ in range(200):
        rows.append({"calories": np.random.uniform(50,200), "fat": np.random.uniform(0,8),
                     "sugar": np.random.uniform(0,5), "protein": np.random.uniform(10,30),
                     "sodium": np.random.uniform(0,200), "label": "Healthy"})
    for _ in range(200):
        rows.append({"calories": np.random.uniform(200,380), "fat": np.random.uniform(8,18),
                     "sugar": np.random.uniform(5,15), "protein": np.random.uniform(5,15),
                     "sodium": np.random.uniform(200,500), "label": "Moderate"})
    for _ in range(200):
        rows.append({"calories": np.random.uniform(380,600), "fat": np.random.uniform(18,40),
                     "sugar": np.random.uniform(15,50), "protein": np.random.uniform(0,10),
                     "sodium": np.random.uniform(500,1200), "label": "Unhealthy"})
    df = pd.DataFrame(rows)
    df.to_csv(DATA_PATH, index=False)
    return df


def train_model():
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import Pipeline
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score
        import joblib
    except ImportError:
        return None, 0.0

    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        for col in FEATURES + [LABEL_COL]:
            if col not in df.columns:
                df = _generate_synthetic_data()
                break
    else:
        df = _generate_synthetic_data()

    X = df[FEATURES].fillna(0).values
    y = df[LABEL_COL].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline = Pipeline([("scaler", StandardScaler()), ("clf", LogisticRegression(max_iter=500, random_state=42))])
    pipeline.fit(X_train, y_train)
    acc = accuracy_score(y_test, pipeline.predict(X_test))
    joblib.dump(pipeline, MODEL_PATH)
    return pipeline, acc


def _load_or_train():
    try:
        import joblib
        if os.path.exists(MODEL_PATH):
            return joblib.load(MODEL_PATH)
    except Exception:
        pass
    model, _ = train_model()
    return model


def predict_category(nutrition: dict) -> str:
    model = _load_or_train()
    if model is None:
        from scoring import compute_health_score, classify_score
        return classify_score(compute_health_score(nutrition))
    try:
        X = np.array([[
            float(nutrition.get("calories", 0) or 0),
            float(nutrition.get("fat", 0) or 0),
            float(nutrition.get("sugar", 0) or 0),
            float(nutrition.get("protein", 0) or 0),
            float(nutrition.get("sodium", 0) or 0),
        ]])
        return model.predict(X)[0]
    except Exception:
        from scoring import compute_health_score, classify_score
        return classify_score(compute_health_score(nutrition))
