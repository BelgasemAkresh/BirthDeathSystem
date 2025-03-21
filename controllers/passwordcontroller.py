from PyQt5.QtWidgets import (
    QMessageBox
)
from PyQt5.QtCore import QObject


class PasswordController(QObject):
    def __init__(self, view, config, main_window):
        super().__init__()
        self.view = view
        self.config = config
        self.main_window = main_window
        self.view.passwordEntered.connect(self.check_password)

    def check_password(self, pwd):
        if pwd == self.config["password"]:
            self.main_window.go_to_main_menu()
        else:
            QMessageBox.warning(self.view, "خطأ", "كلمة المرور غير صحيحة!")
