from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget
)
from PyQt5.QtCore import Qt

from views.product_view import ProductView
from views.supplier_view import SupplierView
from views.category_view import CategoryView
from views.stock_in_view import StockInView
from views.stock_out_view import StockOutView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Warehouse Management System")
        self.resize(1200, 650)

        self.init_ui()

    def init_ui(self):
        central = QWidget()
        main_layout = QHBoxLayout()

        # ===== SIDEBAR =====
        sidebar = QVBoxLayout()
        sidebar.setSpacing(10)

        title = QLabel("📦 QUẢN LÝ KHO")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 16px;")

        btn_products = QPushButton("Sản phẩm")
        btn_suppliers = QPushButton("Nhà cung cấp")
        btn_categories = QPushButton("Nhóm hàng")
        btn_stock_in = QPushButton("Nhập hàng")
        btn_stock_out = QPushButton("Xuất hàng")

        for btn in (
            btn_products, btn_suppliers, btn_categories,
            btn_stock_in, btn_stock_out
        ):
            btn.setMinimumHeight(40)

        sidebar.addWidget(title)
        sidebar.addSpacing(20)
        sidebar.addWidget(btn_products)
        sidebar.addWidget(btn_suppliers)
        sidebar.addWidget(btn_categories)
        sidebar.addWidget(btn_stock_in)
        sidebar.addWidget(btn_stock_out)
        sidebar.addStretch()

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setFixedWidth(200)
        sidebar_widget.setStyleSheet(
            "background-color: #f0f0f0;"
        )

        # ===== CONTENT =====
        self.stack = QStackedWidget()
        self.stack.addWidget(ProductView())     # index 0
        self.stack.addWidget(SupplierView())    # index 1
        self.stack.addWidget(CategoryView())    # index 2
        self.stack.addWidget(StockInView())     # index 3
        self.stack.addWidget(StockOutView())    # index 4

        # ===== SIGNAL =====
        btn_products.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_suppliers.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_categories.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_stock_in.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        btn_stock_out.clicked.connect(lambda: self.stack.setCurrentIndex(4))

        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.stack)

        central.setLayout(main_layout)
        self.setCentralWidget(central)
