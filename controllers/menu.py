
class Menu_Controller:
    def __init__(self, view, mainController):
        self.mainController = mainController
        self.view = view
        self.view.initUI()
        self.setup()


    def addWidgets(self):
        pass
#        self.mainController.view.stack.addWidget(self.login_controller.view) # 3
        #self.mainController.view.stack.addWidget(self.menu_controller.view) # 4
        #self.mainController.view.stack.addWidget(self.system_controller.view) # 5
        #self.mainController.view.stack.addWidget(self.menu_controller.view) # 6
        #self.mainController.view.stack.addWidget(self.system_controller.view) # 7

    def setup(self):
        pass
        #self.view.login_button.clicked.connect(self.check_password)

    def check_password(self):
        password = self.view.password_input.text()
        if password == "123":
            self.mainController.showSystem()
            self.mainController.setupSystem()
        else:
            self.mainController.view.show_message("خطأ في كلمة المرور")
