from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor
from PyQt5.QtCore import Qt

class HelpWidget(QDialog):
    def __init__(self, parent=None):
        super(HelpWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('مساعدة')
        self.setFixedSize(850, 600)  # Vergrößerte und feste Größe des Fensters
        self.setWindowPalette()

        grid = QGridLayout()
        self.addLogo(grid)
        self.addInfoText(grid)
        self.addContactInfo(grid)
        self.addButtons(grid)

        self.setLayout(grid)
        self.setLayoutDirection(Qt.RightToLeft)  # Rechts-nach-Links Layout für Arabisch

    def setWindowPalette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('white'))
        self.setPalette(palette)

    def addLogo(self, grid):
        logo = QLabel(self)
        pixmap = QPixmap('bilder/logo1x1-_improved.png')
        logo.setPixmap(pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        grid.addWidget(logo, 0, 0, 1, 2, Qt.AlignCenter)

    def addInfoText(self, grid):
        font = QFont()
        font.setPointSize(14)
        label = QLabel("هذا التطبيق تم تطويره بواسطة IT Power and More.")
        label.setFont(font)
        label.setWordWrap(True)
        label.setStyleSheet("color: black;")
        grid.addWidget(label, 1, 0, 1, 2)

    def addContactInfo(self, grid):
        font = QFont()
        font.setPointSize(12)
        contact_label = QLabel(
            "للحصول على المزيد من المساعدة، يرجى التواصل معنا عبر البريد الإلكتروني أو الهاتف، أو يرجى زيارة موقعنا الإلكتروني:\n"
            "\n"
            "البريد الإلكتروني: info@itpandmore.com"
            "\n"
            "الهاتف: "
            "4917683478334+"
        )
        contact_label.setFont(font)
        contact_label.setWordWrap(True)
        contact_label.setStyleSheet("color: black;")
        grid.addWidget(contact_label, 2, 0, 1, 2)

    def addButtons(self, grid):
        font = QFont()
        font.setPointSize(12)
        button_website = QPushButton("زيارة موقعنا الإلكتروني")
        button_website.setFont(font)
        button_website.setStyleSheet("color: black;")
        button_website.clicked.connect(self.open_website)
        grid.addWidget(button_website, 3, 0)

        button_close = QPushButton("إغلاق")
        button_close.setFont(font)
        button_close.setStyleSheet("color: black;")
        button_close.clicked.connect(self.close)
        grid.addWidget(button_close, 3, 1)

    def open_website(self):
        import webbrowser
        webbrowser.open('https://www.itpandmore.com')

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    ex = HelpWidget()
    ex.show()
    sys.exit(app.exec_())
