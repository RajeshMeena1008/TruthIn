import requests

def get_product_by_barcode(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("status") == 1:
            return data.get("product", {})
        else:
            return None
    except:
        return None
    