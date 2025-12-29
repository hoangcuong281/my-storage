from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QDialog, QFormLayout,
    QComboBox, QLineEdit, QDateEdit, QHeaderView
)
from PyQt5.QtCore import Qt, QDate

from services import stock_in_api, products_api, suppliers_api


# ================= DIALOG =================
class StockInDialog(QDialog):
    def __init__(self, stock=None):
        super().__init__()
        self.setWindowTitle("Đơn nhập hàng")

        self.products = products_api.get_products()
        self.suppliers = suppliers_api.get_all_suppliers()

        self.cb_product = QComboBox()
        self.cb_supplier = QComboBox()
        self.txt_quantity = QLineEdit()
        self.txt_price = QLineEdit()
        self.date_import = QDateEdit()
        self.date_import.setCalendarPopup(True)
        self.date_import.setDate(QDate.currentDate())

        # Thêm danh sách sản phẩm
        for p in self.products:
            self.cb_product.addItem(f"{p['code']} - {p['name']}", p["product_id"])
        # Thêm danh sách nhà cung cấp
        for s in self.suppliers:
            self.cb_supplier.addItem(s["name"], s["supplier_id"])

        if stock:
            self.cb_product.setCurrentIndex(self.cb_product.findData(stock["product_id"]))
            self.cb_supplier.setCurrentIndex(self.cb_supplier.findData(stock["supplier_id"]))
            self.txt_quantity.setText(str(stock["quantity"]))
            self.txt_price.setText(str(stock["import_price"]))
            self.date_import.setDate(QDate.fromString(stock["import_date"], "yyyy-MM-dd"))

        layout = QFormLayout()
        layout.addRow("Sản phẩm:", self.cb_product)
        layout.addRow("Nhà cung cấp:", self.cb_supplier)
        layout.addRow("Số lượng:", self.txt_quantity)
        layout.addRow("Giá nhập:", self.txt_price)
        layout.addRow("Ngày nhập:", self.date_import)

        btn_save = QPushButton("💾 Lưu")
        btn_save.clicked.connect(self.accept)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    def get_data(self):
        try:
            quantity = int(self.txt_quantity.text())
            price = float(self.txt_price.text())
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Số lượng và giá phải là số")
            return None

        return {
            "product_id": self.cb_product.currentData(),
            "supplier_id": self.cb_supplier.currentData(),
            "quantity": quantity,
            "import_price": price,
            "import_date": self.date_import.date().toString("yyyy-MM-dd")
        }


# ================= VIEW =================
class StockInView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nhập hàng")
        self.resize(850, 450)

        self.stock_list = []

        self.init_ui()
        self.load_stock()

    def init_ui(self):
        layout = QVBoxLayout()

        # Nút thêm, sửa, xóa
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("➕ Thêm")
        btn_edit = QPushButton("✏️ Sửa")
        btn_delete = QPushButton("🗑 Xóa")
        btn_add.clicked.connect(self.add_stock)
        btn_edit.clicked.connect(self.edit_stock)
        btn_delete.clicked.connect(self.delete_stock)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.addStretch()

        # Bảng hiển thị: Xóa cột ID, chỉ hiện thông tin
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Sản phẩm", "Nhà cung cấp", "Số lượng", "Giá nhập", "Ngày"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addLayout(btn_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_stock(self):
        self.stock_list = stock_in_api.get_all_stock_in()
        self.show_stock()

    def show_stock(self):
        self.table.setRowCount(0)
        # Map product_id -> tên sản phẩm, supplier_id -> tên nhà cung cấp
        product_map = {p['product_id']: p['name'] for p in products_api.get_products()}
        supplier_map = {s['supplier_id']: s['name'] for s in suppliers_api.get_all_suppliers()}

        for row, s in enumerate(self.stock_list):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(product_map.get(s["product_id"], "")))
            self.table.setItem(row, 1, QTableWidgetItem(supplier_map.get(s.get("supplier_id"), "")))
            self.table.setItem(row, 2, QTableWidgetItem(str(s["quantity"])))
            self.table.setItem(row, 3, QTableWidgetItem(f"{s['import_price']:,}"))
            self.table.setItem(row, 4, QTableWidgetItem(s["import_date"]))

            self.table.item(row, 2).setTextAlignment(Qt.AlignCenter)
            self.table.item(row, 3).setTextAlignment(Qt.AlignRight)

    def add_stock(self):
        dlg = StockInDialog()
        if dlg.exec_():
            data = dlg.get_data()
            if data:
                stock_in_api.create_stock_in(data)
                self.load_stock()

    def edit_stock(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Chọn đơn nhập")
            return

        stock = self.stock_list[row]
        dlg = StockInDialog(stock)
        if dlg.exec_():
            data = dlg.get_data()
            if data:
                stock_in_api.update_stock_in(stock["stock_in_id"], data)
                self.load_stock()

    def delete_stock(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Chọn đơn nhập")
            return

        stock = self.stock_list[row]
        if QMessageBox.question(self, "Xác nhận", "Xóa đơn nhập này?") == QMessageBox.Yes:
            stock_in_api.delete_stock_in(stock["stock_in_id"])
            self.load_stock()
