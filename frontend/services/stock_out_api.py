import requests

BASE_URL = "http://127.0.0.1:8000"

# Lấy danh sách đơn xuất
def get_all_stock_out():
    res = requests.get(f"{BASE_URL}/stock/stockout")
    res.raise_for_status()
    return res.json()

# Thêm đơn xuất
def create_stock_out(data):
    payload = {
        "product_id": data["product_id"],
        "quantity": data["quantity"],
        "reason": data["reason"],
        "export_date": data["export_date"],
    }
    res = requests.post(f"{BASE_URL}/stock/stockout", json=payload)
    res.raise_for_status()
    return res.json()

# Sửa đơn xuất
def update_stock_out(stock_out_id, data):
    payload = {
        "product_id": data["product_id"],
        "quantity": data["quantity"],
        "reason": data["reason"],
        "export_date": data["export_date"],
    }
    res = requests.put(f"{BASE_URL}/stock/stockout/{stock_out_id}", json=payload)
    res.raise_for_status()
    return res.json()

# Xóa đơn xuất
def delete_stock_out(stock_out_id):
    res = requests.delete(f"{BASE_URL}/stock/stockout/{stock_out_id}")
    res.raise_for_status()
    return res.json()
