"""
barcode_utils.py
Barcode detection via pyzbar + product lookup via OpenFoodFacts API.
"""

import requests
from PIL import Image

OPENFOODFACTS_API    = "https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
OPENFOODFACTS_SEARCH = "https://world.openfoodfacts.org/cgi/search.pl"


def scan_barcode(img: Image.Image) -> str | None:
    try:
        import numpy as np
        from pyzbar import pyzbar
        arr = np.array(img.convert("L"))
        barcodes = pyzbar.decode(arr)
        if barcodes:
            return barcodes[0].data.decode("utf-8")
        barcodes = pyzbar.decode(np.array(img))
        if barcodes:
            return barcodes[0].data.decode("utf-8")
    except ImportError:
        pass
    except Exception:
        pass
    return None


def fetch_product_from_openfoodfacts(barcode: str | None, name: str | None = None) -> tuple[dict | None, str | None]:
    try:
        if barcode:
            url = OPENFOODFACTS_API.format(barcode=barcode)
            resp = requests.get(url, timeout=8, headers={"User-Agent": "FoodScanAIPRO/1.0"})
            data = resp.json()
            if data.get("status") == 1:
                return _parse_off_product(data.get("product", {}))

        if name:
            params = {"search_terms": name, "search_simple": 1,
                      "action": "process", "json": 1, "page_size": 1}
            resp = requests.get(OPENFOODFACTS_SEARCH, params=params, timeout=8,
                                headers={"User-Agent": "FoodScanAIPRO/1.0"})
            data = resp.json()
            products = data.get("products", [])
            if products:
                result, pname = _parse_off_product(products[0])
                # Validate: product name must be a short, sensible string
                if pname and len(pname.strip()) > 1:
                    return result, pname.strip()

    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        pass
    except Exception:
        pass

    # API failed or no result — return None so caller can use local fallback
    return None, None


def _parse_off_product(product: dict) -> tuple[dict, str]:
    nutriments   = product.get("nutriments", {})
    product_name = (
        product.get("product_name") or
        product.get("product_name_en") or
        "Unknown Product"
    ).strip()

    # Sanitise: take only first line / first 80 chars
    product_name = product_name.split("\n")[0][:80].strip()

    nutrition = {
        "calories":      _safe_float(nutriments.get("energy-kcal_100g") or
                                     (nutriments.get("energy_100g", 0) / 4.184)),
        "fat":           _safe_float(nutriments.get("fat_100g", 0)),
        "sugar":         _safe_float(nutriments.get("sugars_100g", 0)),
        "protein":       _safe_float(nutriments.get("proteins_100g", 0)),
        "sodium":        _safe_float(nutriments.get("sodium_100g", 0)) * 1000,
        "carbohydrates": _safe_float(nutriments.get("carbohydrates_100g", 0)),
        "ingredients":   product.get("ingredients_text", ""),
    }
    return nutrition, product_name


def _safe_float(val) -> float:
    try:
        return round(float(val), 1)
    except (TypeError, ValueError):
        return 0.0
