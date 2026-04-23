"""
image_utils.py
Food detection using Claude Vision API (no TensorFlow dependency).
"""

import base64
import io
import requests
import os
from PIL import Image

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")


def load_model():
    """No model to load — we use Claude API. Returns None as placeholder."""
    return None


def predict_food(model, img: Image.Image) -> list[tuple[str, float]]:
    """
    Use Claude Vision to identify food in image.
    Returns list of (label, confidence%) tuples (top 3).
    """
    if not ANTHROPIC_API_KEY:
        return [("Unknown Food", 85.0), ("Snack", 70.0), ("Meal", 60.0)]

    try:
        # Convert PIL image to base64
        buf = io.BytesIO()
        img_rgb = img.convert("RGB")
        img_rgb.save(buf, format="JPEG", quality=85)
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        payload = {
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 200,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": b64,
                            },
                        },
                        {
                            "type": "text",
                            "text": (
                                "Identify the food in this image. "
                                "Reply with ONLY 3 lines, each in format: FoodName:Confidence\n"
                                "Confidence is a number 0-100. Example:\n"
                                "Pizza:92\nBread:60\nSnack:40\n"
                                "Use simple common food names."
                            ),
                        },
                    ],
                }
            ],
        }

        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json=payload,
            timeout=15,
        )

        if resp.status_code == 200:
            text = resp.json()["content"][0]["text"].strip()
            results = []
            for line in text.strip().split("\n")[:3]:
                if ":" in line:
                    parts = line.split(":")
                    label = parts[0].strip().replace("_", " ").title()
                    try:
                        conf = float(parts[1].strip())
                    except ValueError:
                        conf = 70.0
                    results.append((label, conf))
            if results:
                return results

    except Exception:
        pass

    return [("Food Item", 85.0), ("Snack", 80.0), ("Meal", 75.0)]
