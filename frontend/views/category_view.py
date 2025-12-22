from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class CategoryView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Quản lý Nhóm hàng"))
        self.setLayout(layout)
