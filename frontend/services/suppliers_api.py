import requests

BASE_URL = "http://127.0.0.1:8000"


def get_all_suppliers():
    res = requests.get(f"{BASE_URL}/suppliers")
    res.raise_for_status()
    return res.json()


def create_supplier(data):
    res = requests.post(f"{BASE_URL}/suppliers", json=data)
    res.raise_for_status()
    return res.json()


def update_supplier(supplier_id, data):
    res = requests.put(f"{BASE_URL}/suppliers/{supplier_id}", json=data)
    res.raise_for_status()
    return res.json()


def delete_supplier(supplier_id):
    res = requests.delete(f"{BASE_URL}/suppliers/{supplier_id}")
    res.raise_for_status()
    return res.json()
