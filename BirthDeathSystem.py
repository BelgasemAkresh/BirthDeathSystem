from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QMessageBox

from model.model import Model
from views.guiElements.help import HelpWidget
from controllers.login import *
from controllers.system import *
from controllers.menu import *
from views.login import Login_View
from views.system import System_View
from views.menu import Menu_View



class MainView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.setGeometry(100, 100, 1600, 800)
        self.setWindowTitle('Visa System')
        self.controller = controller
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Set the window icon
        icon = QIcon("bilder/libyaGovHigh.png")  # Provide the correct path to your image
        self.setWindowIcon(icon)

    def closeEvent(self, event):
        self.controller.closeApplication()
        super().closeEvent(event)

    def show_message(self, msg):
        QMessageBox.critical(self, "Error", msg)
class MainController:
    def __init__(self, app, model):
        self.app = app
        self.model = model
        self.view = MainView(self)

        self.help_widget = HelpWidget()

        self.login_controller = Login_Controller(Login_View(), self)
        self.menu_controller = Menu_Controller(Menu_View(), self)
        self.system_controller = System_Controller(model, System_View(), self)

        self.view.stack.addWidget(self.login_controller.view)
        self.view.stack.addWidget(self.menu_controller.view)
        self.view.stack.addWidget(self.system_controller.view)

        self.menu_controller.addWidgets()

    def closeApplication(self):
        self.model.exit()
        self.app.quit()

    def showHelpWindow(self):
        self.help_widget.show()  # Hilfefenster anzeigen

    def showLogin(self):
        self.view.stack.setCurrentIndex(0)

    def showMenu(self):
        self.view.stack.setCurrentIndex(1)

    def showSystem(self):
        self.view.stack.setCurrentIndex(2)

    def setupSystem(self):
        self.system_controller.view.toggleLowerWidget()

    def setupLogin(self):
        self.login_controller.view.password_input.clear()

    def setupMenu(self):
        pass


    def run(self):
        self.view.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":


    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    darker_palette = QPalette()
    darker_palette.setColor(QPalette.Window, QColor(44, 62, 80))
    darker_palette.setColor(QPalette.WindowText, Qt.white)
    darker_palette.setColor(QPalette.Base, QColor(210, 210, 210))
    darker_palette.setColor(QPalette.AlternateBase, QColor(190, 190, 190))
    darker_palette.setColor(QPalette.ToolTipBase, Qt.white)
    darker_palette.setColor(QPalette.ToolTipText, Qt.black)
    darker_palette.setColor(QPalette.Text, Qt.black)
    darker_palette.setColor(QPalette.Button, QColor(190, 190, 190))
    darker_palette.setColor(QPalette.ButtonText, Qt.black)
    darker_palette.setColor(QPalette.BrightText, Qt.red)
    darker_palette.setColor(QPalette.Link, QColor(32, 100, 188))
    darker_palette.setColor(QPalette.Highlight, QColor(32, 100, 188))
    darker_palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(darker_palette)

    app.setStyleSheet("""
    
        QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }
    
        QPushButton {
            font: 20px;
            padding: 5px 10px;
            min-height: 25px;
            min-width: 100px;
        }

        QComboBox {
            font: 20px;
            padding: 5px 10px;
            min-height: 25px;
            min-width: 150px; /* Ändere die Breite nach Bedarf */
        }
    """)

    model = Model()
    controller = MainController(app, model)
    controller.run()

    sys.exit(app.exec_())