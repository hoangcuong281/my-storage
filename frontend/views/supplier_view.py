from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class SupplierView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Quản lý Nhà cung cấp"))
        self.setLayout(layout)
