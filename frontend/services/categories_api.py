import requests

BASE_URL = "http://127.0.0.1:8000"


def get_all_categories():
    res = requests.get(f"{BASE_URL}/categories")
    res.raise_for_status()
    return res.json()


def create_category(data):
    res = requests.post(f"{BASE_URL}/categories", json=data)
    res.raise_for_status()
    return res.json()


def update_category(category_id, data):
    res = requests.put(f"{BASE_URL}/categories/{category_id}", json=data)
    res.raise_for_status()
    return res.json()


def delete_category(category_id):
    res = requests.delete(f"{BASE_URL}/categories/{category_id}")
    res.raise_for_status()
    return res.json()
