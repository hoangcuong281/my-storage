import requests

BASE_URL = "http://127.0.0.1:8000"

def get_all_products():
    res = requests.get(f"{BASE_URL}/products")
    res.raise_for_status()
    return res.json()
