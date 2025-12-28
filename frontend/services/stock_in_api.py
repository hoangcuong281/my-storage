from services.api_client import APIClient

# Lấy danh sách đơn nhập
def get_all_stock_in():
    res = APIClient.get("/stock/stockin")
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
    res = APIClient.post("/stock/stockin", json=payload)
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
    res = APIClient.put(f"/stock/stockin/{stock_in_id}", json=payload)
    res.raise_for_status()
    return res.json()

# Xóa đơn nhập
def delete_stock_in(stock_in_id):
    res = APIClient.delete(f"/stock/stockin/{stock_in_id}")
    res.raise_for_status()
    return res.json()
