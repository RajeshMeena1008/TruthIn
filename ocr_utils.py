import re
from PIL import Image

def extract_text_from_image(img: Image.Image) -> str:
    """
    Extract text from a food label image using EasyOCR only.
    No Tesseract dependency (deployment friendly).
    """

    try:
        import easyocr
        import numpy as np

        # ✅ Preprocess image (better accuracy)
        img = img.convert("L")  # grayscale
        img = img.point(lambda x: 0 if x < 140 else 255)  # threshold

        arr = np.array(img)

        # ✅ Load reader (fast + clean)
        reader = easyocr.Reader(["en"], verbose=False)

        results = reader.readtext(arr, detail=0)

        text = "\n".join(results)

        if text.strip():
            return text

        return "No text detected"

    except ImportError:
        return "❌ EasyOCR not installed. Run: pip install easyocr"

    except Exception as e:
        return f"OCR Error: {str(e)}"




def parse_nutrition_from_text(text: str) -> dict:
    """
    Parse nutrition values from raw OCR text.
    Returns a dict with keys: calories, fat, sugar, protein, sodium, carbohydrates.
    """
    text_lower = text.lower()

    def extract_number(pattern: str, default: float) -> float:
        match = re.search(pattern, text_lower)
        if match:
            try:
                return float(match.group(1))
            except (ValueError, IndexError):
                pass
        return default

    # Patterns to search for
    calories = extract_number(
        r"(?:calories?|energy|cal)[^\d]*?(\d+(?:\.\d+)?)\s*(?:kcal)?",
        default=350.0
    )
    fat = extract_number(
        r"(?:total\s+)?fat[^\d]*?(\d+(?:\.\d+)?)\s*g",
        default=10.0
    )
    sugar = extract_number(
        r"(?:total\s+)?sug(?:ar)?s?[^\d]*?(\d+(?:\.\d+)?)\s*g",
        default=8.0
    )
    protein = extract_number(
        r"protein[^\d]*?(\d+(?:\.\d+)?)\s*g",
        default=5.0
    )
    sodium = extract_number(
        r"sodium[^\d]*?(\d+(?:\.\d+)?)\s*mg",
        default=500.0
    )
    carbs = extract_number(
        r"(?:total\s+)?carb(?:ohydrate)?s?[^\d]*?(\d+(?:\.\d+)?)\s*g",
        default=45.0
    )

    return {
        "calories": calories,
        "fat": fat,
        "sugar": sugar,
        "protein": protein,
        "sodium": sodium,
        "carbohydrates": carbs,
        "ingredients": _extract_ingredients(text),
    }


def _extract_ingredients(text: str) -> str:
    """Extract ingredients section from label text."""
    lower = text.lower()
    match = re.search(r"ingredients?[:\s]+(.+?)(?:\n\n|\Z)", lower, re.DOTALL)
    if match:
        raw = match.group(1).replace("\n", " ").strip()
        return raw[:500]  # cap length
    return ""
