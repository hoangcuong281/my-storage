import requests

BASE_URL = "http://127.0.0.1:8000/products"


def get_products(keyword=""):
    params = {"keyword": keyword} if keyword else {}
    return requests.get(BASE_URL, params=params).json()


def create_product(data):
    return requests.post(BASE_URL, json=data).json()


def update_product(product_id, data):
    return requests.put(f"{BASE_URL}/{product_id}", json=data).json()


def delete_product(product_id):
    return requests.delete(f"{BASE_URL}/{product_id}").json()
