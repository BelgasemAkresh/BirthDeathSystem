class Login_Controller:
    def __init__(self, view, mainController):
        self.mainController = mainController
        self.view = view
        self.view.initUI()
        self.setup()

    def setup(self):
        self.view.login_button.clicked.connect(self.check_password)

    def check_password(self):
        password = self.view.password_input.text()
        if password == "123":
            self.mainController.showMenu()
            self.mainController.setupMenu()
        else:
            self.mainController.view.show_message("خطأ في كلمة المرور")
