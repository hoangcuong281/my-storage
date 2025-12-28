from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem,
    QMessageBox, QDialog, QFormLayout,
    QComboBox
)
from PyQt5.QtCore import Qt

from services import products_api
from services.categories_api import get_all_categories
from services.suppliers_api import get_all_suppliers

class ValidateComboBox(QComboBox):
    def __init__(self, data_map, field_name, parent=None):
        super().__init__(parent)
        self.data_map = data_map  
        self.field_name = field_name 

        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)

    def focusOutEvent(self, event):
        text = self.currentText().strip()

        if text and text not in self.data_map:
            QMessageBox.warning(
                self,
                "Dữ liệu không hợp lệ",
                f"{self.field_name} '{text}' không tồn tại"
            )
            self.setFocus(Qt.OtherFocusReason)
            return

        super().focusOutEvent(event)

# ===================== DIALOG =====================
class ProductDialog(QDialog):
    def __init__(self, product=None):
        super().__init__()
        self.setWindowTitle("Sản phẩm")
        self.resize(400, 300)

        # -------- INPUT --------
        self.txt_code = QLineEdit()
        self.txt_name = QLineEdit()
        self.txt_price = QLineEdit()
        self.txt_location = QLineEdit()
        self.txt_note = QLineEdit()

        self.txt_price.setPlaceholderText("VD: 11000000 hoặc 11.000.000")

        # -------- COMBOBOX --------
        self.cb_category = ValidateComboBox({}, "Category", self)
        self.cb_supplier = ValidateComboBox({}, "Supplier", self)

        self.cb_category.setEditable(True)
        self.cb_supplier.setEditable(True)

        self.cb_category.setInsertPolicy(QComboBox.NoInsert)
        self.cb_supplier.setInsertPolicy(QComboBox.NoInsert)

        # -------- LOAD DATA --------
        self.categories = get_all_categories()
        self.suppliers = get_all_suppliers()

        self.category_map = {}   # name -> id
        self.supplier_map = {}

        for c in self.categories:
            self.cb_category.addItem(c["name"])
            self.category_map[c["name"]] = c["category_id"]

        for s in self.suppliers:
            self.cb_supplier.addItem(s["name"])
            self.supplier_map[s["name"]] = s["supplier_id"]
            
        self.cb_category.data_map = self.category_map
        self.cb_supplier.data_map = self.supplier_map

        # -------- SET DATA WHEN EDIT --------
        if product:
            self.txt_code.setText(product.get("code", ""))
            self.txt_name.setText(product.get("name", ""))
            self.txt_price.setText(str(product.get("price", "")))
            self.txt_location.setText(product.get("location", ""))
            self.txt_note.setText(product.get("note", ""))

            for name, cid in self.category_map.items():
                if cid == product.get("category_id"):
                    self.cb_category.setCurrentText(name)
                    break

            for name, sid in self.supplier_map.items():
                if sid == product.get("supplier_id"):
                    self.cb_supplier.setCurrentText(name)
                    break

        # -------- LAYOUT --------
        layout = QFormLayout()
        layout.addRow("Mã SP:", self.txt_code)
        layout.addRow("Tên SP:", self.txt_name)
        layout.addRow("Category:", self.cb_category)
        layout.addRow("Supplier:", self.cb_supplier)
        layout.addRow("Giá:", self.txt_price)
        layout.addRow("Vị trí:", self.txt_location)
        layout.addRow("Ghi chú:", self.txt_note)

        btn_save = QPushButton("Lưu")
        btn_save.clicked.connect(self.accept)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    # -------- GET DATA --------
    def get_data(self):
        try:
            return {
                "code": self.txt_code.text().strip(),
                "name": self.txt_name.text().strip(),
                "category_id": self.category_map[self.cb_category.currentText()],
                "supplier_id": self.supplier_map[self.cb_supplier.currentText()],
                "price": int(self.txt_price.text().replace(".", "").replace(",", "")),
                "location": self.txt_location.text().strip(),
                "note": self.txt_note.text().strip()
            }
        except Exception:
            QMessageBox.warning(self, "Lỗi", "Dữ liệu không hợp lệ")
            return None


# ===================== VIEW =====================
class ProductView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản lý sản phẩm")
        self.resize(900, 500)

        self.products = []

        self.init_ui()
        self.load_products()

    # ================= UI =================
    def showEvent(self, event):
        self.load_products()
        super().showEvent(event)
    def init_ui(self):
        main_layout = QVBoxLayout()

        # 🔍 Search
        search_layout = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Nhập mã hoặc tên sản phẩm...")
        btn_search = QPushButton("Tìm")
        btn_search.clicked.connect(self.search_products)

        search_layout.addWidget(QLabel("Tìm kiếm:"))
        search_layout.addWidget(self.txt_search)
        search_layout.addWidget(btn_search)

        # ➕✏️🗑
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("➕ Thêm")
        btn_edit = QPushButton("✏️ Sửa")
        btn_delete = QPushButton("🗑 Xóa")

        btn_add.clicked.connect(self.add_product)
        btn_edit.clicked.connect(self.edit_product)
        btn_delete.clicked.connect(self.delete_product)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.addStretch()

        # 📋 Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Mã SP", "Tên SP", "Category", "Số lượng", "Giá", "Supplier", "Vị trí"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)

        main_layout.addLayout(search_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

    # ================= DATA =================
    def load_products(self):
        self.products = products_api.get_products()
        self.show_products(self.products)

    def show_products(self, products):
        self.table.setRowCount(0)
        for row, p in enumerate(products):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(p["code"]))
            self.table.setItem(row, 1, QTableWidgetItem(p["name"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(p["category_id"])))
            self.table.setItem(row, 3, QTableWidgetItem(f"{p['quantity']:,}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{p['price']:,}"))
            self.table.setItem(row, 5, QTableWidgetItem(str(p["supplier_id"])))
            self.table.setItem(row, 6, QTableWidgetItem(p["location"]))

    # ================= SEARCH =================
    def search_products(self):
        kw = self.txt_search.text().lower().strip()
        if not kw:
            self.show_products(self.products)
            return

        self.show_products([
            p for p in self.products
            if kw in p["name"].lower() or kw in p["code"].lower()
        ])

    # ================= CRUD =================
    def add_product(self):
        dialog = ProductDialog()
        if dialog.exec_():
            data = dialog.get_data()
            if not data:
                return
            products_api.create_product(data)
            self.load_products()

    def edit_product(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Thông báo", "Chọn sản phẩm")
            return

        product = self.products[row]
        dialog = ProductDialog(product)

        if dialog.exec_():
            data = dialog.get_data()
            if not data:
                return
            products_api.update_product(product["product_id"], data)
            self.load_products()

    def delete_product(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Thông báo", "Chọn sản phẩm")
            return

        product = self.products[row]
        if QMessageBox.question(
            self,
            "Xác nhận",
            f"Xóa sản phẩm '{product['name']}'?",
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:
            products_api.delete_product(product["product_id"])
            self.load_products()
