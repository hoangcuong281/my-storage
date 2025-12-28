from services.api_client import APIClient

# Lấy danh sách đơn xuất
def get_all_stock_out():
    res = APIClient.get("/stock/stockout")
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
    res = APIClient.post("/stock/stockout", json=payload)
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
    res = APIClient.put(f"/stock/stockout/{stock_out_id}", json=payload)
    res.raise_for_status()
    return res.json()

# Xóa đơn xuất
def delete_stock_out(stock_out_id):
    res = APIClient.delete(f"/stock/stockout/{stock_out_id}")
    res.raise_for_status()
    return res.json()
