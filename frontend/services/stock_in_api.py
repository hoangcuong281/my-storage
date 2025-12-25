import requests

BASE_URL = "http://127.0.0.1:8000"

# Lấy danh sách đơn nhập
def get_all_stock_in():
    res = requests.get(f"{BASE_URL}/stock/stockin")
    res.raise_for_status()
    return res.json()

# Thêm đơn nhập
def create_stock_in(data):
    payload = {
        "product_id": data["product_id"],
        "supplier_id": data["supplier_id"],
        "quantity": data["quantity"],
        "import_price": data["import_price"],
        "import_date": data["import_date"],
    }
    res = requests.post(f"{BASE_URL}/stock/stockin", json=payload)
    res.raise_for_status()
    return res.json()

# Sửa đơn nhập
def update_stock_in(stock_in_id, data):
    payload = {
        "product_id": data["product_id"],
        "supplier_id": data["supplier_id"],
        "quantity": data["quantity"],
        "import_price": data["import_price"],
        "import_date": data["import_date"],
    }
    res = requests.put(f"{BASE_URL}/stock/stockin/{stock_in_id}", json=payload)
    res.raise_for_status()
    return res.json()

# Xóa đơn nhập
def delete_stock_in(stock_in_id):
    res = requests.delete(f"{BASE_URL}/stock/stockin/{stock_in_id}")
    res.raise_for_status()
    return res.json()
