from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
import requests
from services.api_client import APIClient


class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đăng nhập")
        self.resize(300, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        btn_login = QPushButton("Đăng nhập")
        btn_login.clicked.connect(self.login)

        layout.addWidget(QLabel("ĐĂNG NHẬP HỆ THỐNG"))
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(btn_login)

        self.setLayout(layout)

    def login(self):
        res = APIClient.post(
            "/auth/login",
            json={
                "username": self.username.text(),
                "password": self.password.text()
            }
        )

        if res.status_code != 200:
            QMessageBox.warning(self, "Lỗi", "Sai tài khoản hoặc mật khẩu")
            return

        user = res.json()["user"]

        from views.main_window import MainWindow
        self.main = MainWindow(user)
        self.main.show()
        self.close()