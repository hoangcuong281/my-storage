from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt
from services.products_api import get_all_products


class ProductView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản lý sản phẩm")
        self.resize(900, 500)

        self.products = []

        self.init_ui()
        self.load_products()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # 🔍 Tìm kiếm
        search_layout = QHBoxLayout()
        lbl_search = QLabel("Tìm kiếm:")
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Nhập mã hoặc tên sản phẩm...")
        btn_search = QPushButton("Tìm")

        btn_search.clicked.connect(self.search_products)

        search_layout.addWidget(lbl_search)
        search_layout.addWidget(self.txt_search)
        search_layout.addWidget(btn_search)

        # 📋 Bảng sản phẩm
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Mã SP", "Tên sản phẩm",
            "Danh mục", "Giá", "Tồn kho", "Vị trí"
        ])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)

        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    # 📥 Load toàn bộ sản phẩm
    def load_products(self):
        self.products = get_all_products()
        self.show_products(self.products)

    # 📊 Đổ dữ liệu vào bảng
    def show_products(self, products):
        self.table.setRowCount(0)

        for row, p in enumerate(products):
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(str(p["product_id"])))
            self.table.setItem(row, 1, QTableWidgetItem(p["code"]))
            self.table.setItem(row, 2, QTableWidgetItem(p["name"]))
            self.table.setItem(row, 3, QTableWidgetItem(
                str(p.get("category_id", ""))
            ))
            self.table.setItem(row, 4, QTableWidgetItem(
                f"{p['price']:,}"
            ))
            self.table.setItem(row, 5, QTableWidgetItem(str(p["quantity"])))
            self.table.setItem(row, 6, QTableWidgetItem(
                p.get("location", "")
            ))

            # căn giữa
            self.table.item(row, 0).setTextAlignment(Qt.AlignCenter)
            self.table.item(row, 5).setTextAlignment(Qt.AlignCenter)

    # 🔎 Tìm kiếm theo mã hoặc tên
    def search_products(self):
        keyword = self.txt_search.text().strip().lower()

        if not keyword:
            self.show_products(self.products)
            return

        filtered = [
            p for p in self.products
            if keyword in p["name"].lower()
            or keyword in p["code"].lower()
        ]

        self.show_products(filtered)
