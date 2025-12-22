from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class StockOutView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Xuất hàng"))
        self.setLayout(layout)
