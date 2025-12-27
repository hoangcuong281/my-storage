import sys
from PyQt5.QtWidgets import QApplication
from views.login_view import LoginView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginView()
    login.show()
    sys.exit(app.exec_())
