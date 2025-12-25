from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QDialog, QFormLayout, QComboBox, QLineEdit, QDateEdit
)
from PyQt5.QtCore import Qt, QDate
from services import stock_out_api, products_api

# ================= DIALOG =================
class StockOutDialog(QDialog):
    def __init__(self, stock=None):
        super().__init__()
        self.setWindowTitle("Đơn xuất kho")
        self.resize(400, 250)

        # Lấy danh sách sản phẩm
        self.products = products_api.get_products()

        # Controls
        self.cmb_product = QComboBox()
        for p in self.products:
            self.cmb_product.addItem(f"{p['name']} ({p['code']})", p['product_id'])

        self.cmb_reason = QComboBox()
        self.cmb_reason.addItems(["sell", "damaged", "expired", "adjust"])

        self.txt_quantity = QLineEdit()
        self.txt_quantity.setPlaceholderText("Nhập số lượng")

        self.date_export = QDateEdit()
        self.date_export.setCalendarPopup(True)
        self.date_export.setDate(QDate.currentDate())

        # Nếu chỉnh sửa
        if stock:
            index = self.cmb_product.findData(stock["product_id"])
            if index >= 0:
                self.cmb_product.setCurrentIndex(index)
            self.cmb_reason.setCurrentText(stock["reason"])
            self.txt_quantity.setText(str(stock["quantity"]))
            self.date_export.setDate(QDate.fromString(stock["export_date"], "yyyy-MM-dd"))

        # Layout
        layout = QFormLayout()
        layout.addRow("Sản phẩm:", self.cmb_product)
        layout.addRow("Lý do:", self.cmb_reason)
        layout.addRow("Số lượng:", self.txt_quantity)
        layout.addRow("Ngày xuất:", self.date_export)

        btn_save = QPushButton("💾 Lưu")
        btn_save.clicked.connect(self.accept)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    def get_data(self):
        try:
            quantity = int(self.txt_quantity.text())
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Số lượng phải là số nguyên")
            return None

        return {
            "product_id": self.cmb_product.currentData(),
            "quantity": quantity,
            "reason": self.cmb_reason.currentText(),
            "export_date": self.date_export.date().toString("yyyy-MM-dd")
        }


# ================= VIEW =================
class StockOutView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản lý xuất kho")
        self.resize(900, 500)

        self.stock_list = []
        self.products_map = {p['product_id']: p['name'] for p in products_api.get_products()}

        self.init_ui()
        self.load_stock()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Nút chức năng
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

        # Bảng hiển thị
        self.table = QTableWidget()
        self.table.setColumnCount(4)  # Ẩn ID, chỉ hiển thị thông tin cần
        self.table.setHorizontalHeaderLabels(["Sản phẩm", "Số lượng", "Lý do", "Ngày xuất"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)

        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

    def load_stock(self):
        self.stock_list = stock_out_api.get_all_stock_out()
        self.show_stock()

    def show_stock(self):
        self.table.setRowCount(0)
        for row, s in enumerate(self.stock_list):
            self.table.insertRow(row)
            # Hiển thị tên sản phẩm thay vì product_id
            product_name = self.products_map.get(s["product_id"], "")
            self.table.setItem(row, 0, QTableWidgetItem(product_name))
            self.table.setItem(row, 1, QTableWidgetItem(str(s["quantity"])))
            self.table.setItem(row, 2, QTableWidgetItem(s["reason"]))
            self.table.setItem(row, 3, QTableWidgetItem(s["export_date"]))

            # Căn giữa số lượng
            self.table.item(row, 1).setTextAlignment(Qt.AlignCenter)

    # CRUD
    def add_stock(self):
        dlg = StockOutDialog()
        if dlg.exec_():
            data = dlg.get_data()
            if data:
                stock_out_api.create_stock_out(data)
                self.load_stock()

    def edit_stock(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Thông báo", "Chọn đơn xuất để sửa")
            return
        stock = self.stock_list[row]
        dlg = StockOutDialog(stock)
        if dlg.exec_():
            data = dlg.get_data()
            if data:
                stock_out_api.update_stock_out(stock["stock_out_id"], data)
                self.load_stock()

    def delete_stock(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Thông báo", "Chọn đơn xuất để xóa")
            return
        stock = self.stock_list[row]
        reply = QMessageBox.question(self, "Xác nhận",
                                     f"Xóa đơn xuất sản phẩm {self.products_map.get(stock['product_id'], '')}?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            stock_out_api.delete_stock_out(stock["stock_out_id"])
            self.load_stock()
