from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem,
    QHBoxLayout, QMessageBox,
    QDialog, QLabel, QLineEdit, QComboBox
)

from services.api_client import APIClient


# ================= USER DIALOG =================
class UserDialog(QDialog):
    def __init__(self, user=None):
        super().__init__()
        self.setWindowTitle("User")
        self.resize(350, 260)

        layout = QVBoxLayout()

        self.txt_username = QLineEdit()
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_fullname = QLineEdit()

        self.cb_role = QComboBox()
        self.cb_role.addItems(["admin", "manager", "staff"])

        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.txt_username)

        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.txt_password)

        layout.addWidget(QLabel("Full name"))
        layout.addWidget(self.txt_fullname)

        layout.addWidget(QLabel("Role"))
        layout.addWidget(self.cb_role)

        # ===== EDIT MODE =====
        self.is_edit = user is not None
        if self.is_edit:
            self.txt_username.setText(user["username"])
            self.txt_username.setDisabled(True)

            self.txt_fullname.setText(user["full_name"])
            self.cb_role.setCurrentText(user["role"])

            self.txt_password.hide()

        # ===== BUTTON =====
        btn_save = QPushButton("Lưu")
        btn_cancel = QPushButton("Huỷ")

        btn_save.clicked.connect(self.validate)
        btn_cancel.clicked.connect(self.reject)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def validate(self):
        if not self.txt_username.text().strip():
            QMessageBox.warning(self, "Lỗi", "Username không được để trống")
            return

        if not self.is_edit and not self.txt_password.text():
            QMessageBox.warning(self, "Lỗi", "Password không được để trống")
            return

        if not self.txt_fullname.text().strip():
            QMessageBox.warning(self, "Lỗi", "Full name không được để trống")
            return

        self.accept()


# ================= USER VIEW =================
class UserView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_users()

    def init_ui(self):
        layout = QVBoxLayout()

        # ===== TABLE =====
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Username", "Full name", "Role"]
        )
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setEditTriggers(self.table.NoEditTriggers)

        # ===== BUTTON =====
        btn_add = QPushButton("➕ Thêm")
        btn_edit = QPushButton("✏️ Sửa")
        btn_delete = QPushButton("🗑️ Xoá")

        btn_add.clicked.connect(self.add_user)
        btn_edit.clicked.connect(self.edit_user)
        btn_delete.clicked.connect(self.delete_user)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)

        layout.addLayout(btn_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

    # ================= LOAD =================
    def load_users(self):
        res = APIClient.get("/users/")
        if res.status_code != 200:
            QMessageBox.warning(self, "Lỗi", res.text)
            return

        users = res.json()
        self.table.setRowCount(len(users))

        for row, u in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(str(u["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(u["username"]))
            self.table.setItem(row, 2, QTableWidgetItem(u["full_name"]))
            self.table.setItem(row, 3, QTableWidgetItem(u["role"]))

    # ================= ADD =================
    def add_user(self):
        dialog = UserDialog()

        if dialog.exec_() != dialog.Accepted:
            return

        res = APIClient.post(
            "/users/",
            json={
                "username": dialog.txt_username.text(),
                "password": dialog.txt_password.text(),
                "full_name": dialog.txt_fullname.text(),
                "role": dialog.cb_role.currentText()
            }
        )

        if res.status_code == 200:
            self.load_users()
        else:
            QMessageBox.warning(self, "Lỗi", res.text)

    # ================= EDIT =================
    def edit_user(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Chọn user cần sửa")
            return

        user = {
            "id": self.table.item(row, 0).text(),
            "username": self.table.item(row, 1).text(),
            "full_name": self.table.item(row, 2).text(),
            "role": self.table.item(row, 3).text()
        }

        dialog = UserDialog(user)

        if dialog.exec_() != dialog.Accepted:
            return

        res = APIClient.put(
            f"/users/{user['id']}",
            json={
                "full_name": dialog.txt_fullname.text(),
                "role": dialog.cb_role.currentText()
            }
        )

        if res.status_code == 200:
            self.load_users()
        else:
            QMessageBox.warning(self, "Lỗi", res.text)

    # ================= DELETE =================
    def delete_user(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Chọn user cần xoá")
            return

        user_id = self.table.item(row, 0).text()

        if QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc muốn xoá user này?"
        ) != QMessageBox.Yes:
            return

        res = APIClient.delete(f"/users/{user_id}")

        if res.status_code == 200:
            self.load_users()
        else:
            QMessageBox.warning(self, "Lỗi", res.text)
