from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem,
    QMessageBox, QDialog, QFormLayout
)
from PyQt5.QtCore import Qt

from services import suppliers_api


# ================= DIALOG =================
class SupplierDialog(QDialog):
    def __init__(self, supplier=None):
        super().__init__()
        self.setWindowTitle("Nhà cung cấp")

        self.txt_name = QLineEdit()
        self.txt_phone = QLineEdit()
        self.txt_address = QLineEdit()
        self.txt_note = QLineEdit()

        if supplier:
            self.txt_name.setText(supplier["name"])
            self.txt_phone.setText(supplier.get("phone", ""))
            self.txt_address.setText(supplier.get("address", ""))
            self.txt_note.setText(supplier.get("note", ""))

        layout = QFormLayout()
        layout.addRow("Tên NCC:", self.txt_name)
        layout.addRow("SĐT:", self.txt_phone)
        layout.addRow("Địa chỉ:", self.txt_address)
        layout.addRow("Ghi chú:", self.txt_note)

        btn_save = QPushButton("💾 Lưu")
        btn_save.clicked.connect(self.accept)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    def get_data(self):
        if not self.txt_name.text().strip():
            QMessageBox.warning(self, "Lỗi", "Tên nhà cung cấp không được để trống")
            return None

        return {
            "name": self.txt_name.text().strip(),
            "phone": self.txt_phone.text().strip(),
            "address": self.txt_address.text().strip(),
            "note": self.txt_note.text().strip()
        }


# ================= VIEW =================
class SupplierView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản lý nhà cung cấp")
        self.resize(750, 450)

        self.suppliers = []

        self.init_ui()
        self.load_suppliers()

    # ---------- UI ----------
    def init_ui(self):
        main_layout = QVBoxLayout()

        # 🔍 Tìm kiếm
        search_layout = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Tìm theo tên nhà cung cấp...")
        btn_search = QPushButton("🔍 Tìm")
        btn_search.clicked.connect(self.search_supplier)

        search_layout.addWidget(QLabel("Tìm kiếm:"))
        search_layout.addWidget(self.txt_search)
        search_layout.addWidget(btn_search)

        # ➕✏️🗑
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("➕ Thêm")
        btn_edit = QPushButton("✏️ Sửa")
        btn_delete = QPushButton("🗑 Xóa")

        btn_add.clicked.connect(self.add_supplier)
        btn_edit.clicked.connect(self.edit_supplier)
        btn_delete.clicked.connect(self.delete_supplier)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.addStretch()

        # 📋 Bảng
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Tên NCC", "SĐT", "Địa chỉ", "Ghi chú"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)

        main_layout.addLayout(search_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    # ---------- DATA ----------
    def load_suppliers(self):
        self.suppliers = suppliers_api.get_all_suppliers()
        self.show_suppliers(self.suppliers)

    def show_suppliers(self, data):
        self.table.setRowCount(0)
        for row, s in enumerate(data):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(s["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(s.get("phone", "")))
            self.table.setItem(row, 2, QTableWidgetItem(s.get("address", "")))
            self.table.setItem(row, 3, QTableWidgetItem(s.get("note", "")))

            self.table.item(row, 0).setTextAlignment(Qt.AlignCenter)

    # ---------- SEARCH ----------
    def search_supplier(self):
        kw = self.txt_search.text().lower().strip()
        if not kw:
            self.show_suppliers(self.suppliers)
            return

        self.show_suppliers([
            s for s in self.suppliers
            if kw in s["name"].lower()
        ])

    # ---------- CRUD ----------
    def add_supplier(self):
        dialog = SupplierDialog()
        if dialog.exec_():
            data = dialog.get_data()
            if not data:
                return
            suppliers_api.create_supplier(data)
            self.load_suppliers()

    def edit_supplier(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Thông báo", "Chọn nhà cung cấp để sửa")
            return

        supplier = self.suppliers[row]
        dialog = SupplierDialog(supplier)

        if dialog.exec_():
            data = dialog.get_data()
            if not data:
                return
            suppliers_api.update_supplier(supplier["supplier_id"], data)
            self.load_suppliers()

    def delete_supplier(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Thông báo", "Chọn nhà cung cấp để xóa")
            return

        supplier = self.suppliers[row]
        reply = QMessageBox.question(
            self,
            "Xác nhận",
            f"Xóa nhà cung cấp '{supplier['name']}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            suppliers_api.delete_supplier(supplier["supplier_id"])
            self.load_suppliers()

