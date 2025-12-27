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
from views.user_view import UserView


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user          # {id, username, role}
        self.role = user["role"]

        self.setWindowTitle("Warehouse Management System")
        self.resize(1200, 650)

        self.init_ui()

    def init_ui(self):
        central = QWidget()
        main_layout = QHBoxLayout()

        # ===== SIDEBAR =====
        sidebar = QVBoxLayout()
        sidebar.setSpacing(10)

        title = QLabel(f"👤 {self.user['username']} ({self.role})")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold;")

        btn_products = QPushButton("Sản phẩm")
        btn_suppliers = QPushButton("Nhà cung cấp")
        btn_categories = QPushButton("Nhóm hàng")
        btn_stock_in = QPushButton("Nhập hàng")
        btn_stock_out = QPushButton("Xuất hàng")
        btn_users = QPushButton("Người dùng")  # admin

        # ===== CONTENT =====
        self.stack = QStackedWidget()

        views = {
            "products": ProductView(),
            "suppliers": SupplierView(),
            "categories": CategoryView(),
            "stock_in": StockInView(),
            "stock_out": StockOutView(),
            "users": UserView()
        }

        for v in views.values():
            self.stack.addWidget(v)

        # ===== ROLE PERMISSION =====
        if self.role == "manager":
            sidebar.addWidget(btn_products)
            sidebar.addWidget(btn_suppliers)
            sidebar.addWidget(btn_categories)
            sidebar.addWidget(btn_stock_in)
            sidebar.addWidget(btn_stock_out)

            btn_products.clicked.connect(lambda: self.stack.setCurrentWidget(views["products"]))
            btn_suppliers.clicked.connect(lambda: self.stack.setCurrentWidget(views["suppliers"]))
            btn_categories.clicked.connect(lambda: self.stack.setCurrentWidget(views["categories"]))
            btn_stock_in.clicked.connect(lambda: self.stack.setCurrentWidget(views["stock_in"]))
            btn_stock_out.clicked.connect(lambda: self.stack.setCurrentWidget(views["stock_out"]))

        elif self.role == "staff":
            sidebar.addWidget(btn_stock_in)
            sidebar.addWidget(btn_stock_out)

            btn_stock_in.clicked.connect(lambda: self.stack.setCurrentWidget(views["stock_in"]))
            btn_stock_out.clicked.connect(lambda: self.stack.setCurrentWidget(views["stock_out"]))

        elif self.role == "admin":
            sidebar.addWidget(btn_products)
            sidebar.addWidget(btn_suppliers)
            sidebar.addWidget(btn_categories)
            sidebar.addWidget(btn_stock_in)
            sidebar.addWidget(btn_stock_out)
            sidebar.addWidget(btn_users)

            btn_products.clicked.connect(lambda: self.stack.setCurrentWidget(views["products"]))
            btn_suppliers.clicked.connect(lambda: self.stack.setCurrentWidget(views["suppliers"]))
            btn_categories.clicked.connect(lambda: self.stack.setCurrentWidget(views["categories"]))
            btn_stock_in.clicked.connect(lambda: self.stack.setCurrentWidget(views["stock_in"]))
            btn_stock_out.clicked.connect(lambda: self.stack.setCurrentWidget(views["stock_out"]))
            btn_users.clicked.connect(lambda: self.stack.setCurrentWidget(views["users"]))

        sidebar.insertWidget(0, title)
        sidebar.addStretch()

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setFixedWidth(220)
        sidebar_widget.setStyleSheet("background:#f0f0f0")

        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.stack)

        central.setLayout(main_layout)
        self.setCentralWidget(central)
