from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem,
    QMessageBox, QDialog, QFormLayout
)
from PyQt5.QtCore import Qt

from services import categories_api


# ================= DIALOG =================
class CategoryDialog(QDialog):
    def __init__(self, category=None):
        super().__init__()
        self.setWindowTitle("Danh mục")

        self.txt_name = QLineEdit()
        self.txt_desc = QLineEdit()

        if category:
            self.txt_name.setText(category["name"])
            self.txt_desc.setText(category.get("description", ""))

        layout = QFormLayout()
        layout.addRow("Tên danh mục:", self.txt_name)
        layout.addRow("Mô tả:", self.txt_desc)

        btn_save = QPushButton("💾 Lưu")
        btn_save.clicked.connect(self.accept)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    def get_data(self):
        if not self.txt_name.text().strip():
            QMessageBox.warning(self, "Lỗi", "Tên danh mục không được để trống")
            return None

        return {
            "name": self.txt_name.text().strip(),
            "description": self.txt_desc.text().strip()
        }


# ================= VIEW =================
class CategoryView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản lý danh mục")
        self.resize(700, 450)

        self.categories = []

        self.init_ui()
        self.load_categories()

    # ---------- UI ----------
    def init_ui(self):
        main_layout = QVBoxLayout()

        # 🔍 Tìm kiếm
        search_layout = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Tìm theo tên danh mục...")
        btn_search = QPushButton("🔍 Tìm")
        btn_search.clicked.connect(self.search_category)

        search_layout.addWidget(QLabel("Tìm kiếm:"))
        search_layout.addWidget(self.txt_search)
        search_layout.addWidget(btn_search)

        # ➕✏️🗑
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("➕ Thêm")
        btn_edit = QPushButton("✏️ Sửa")
        btn_delete = QPushButton("🗑 Xóa")

        btn_add.clicked.connect(self.add_category)
        btn_edit.clicked.connect(self.edit_category)
        btn_delete.clicked.connect(self.delete_category)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.addStretch()

        # 📋 Bảng
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels([
            "Tên danh mục", "Mô tả"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)

        main_layout.addLayout(search_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    # ---------- DATA ----------
    def load_categories(self):
        self.categories = categories_api.get_all_categories()
        self.show_categories(self.categories)

    def show_categories(self, data):
        self.table.setRowCount(0)
        for row, c in enumerate(data):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(c["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(c.get("description", "")))

            self.table.item(row, 0).setTextAlignment(Qt.AlignCenter)

    # ---------- SEARCH ----------
    def search_category(self):
        kw = self.txt_search.text().lower().strip()
        if not kw:
            self.show_categories(self.categories)
            return

        self.show_categories([
            c for c in self.categories
            if kw in c["name"].lower()
        ])

    # ---------- CRUD ----------
    def add_category(self):
        dialog = CategoryDialog()
        if dialog.exec_():
            data = dialog.get_data()
            if not data:
                return
            categories_api.create_category(data)
            self.load_categories()

    def edit_category(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Thông báo", "Chọn danh mục để sửa")
            return

        category = self.categories[row]
        dialog = CategoryDialog(category)

        if dialog.exec_():
            data = dialog.get_data()
            if not data:
                return
            categories_api.update_category(category["category_id"], data)
            self.load_categories()

    def delete_category(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Thông báo", "Chọn danh mục để xóa")
            return

        category = self.categories[row]
        reply = QMessageBox.question(
            self,
            "Xác nhận",
            f"Xóa danh mục '{category['name']}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            categories_api.delete_category(category["category_id"])
            self.load_categories()
