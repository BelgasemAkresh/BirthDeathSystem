from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt



class Login_View(QWidget):
    def __init__(self):
        super().__init__()

    def initUI(self):

        main_layout = QVBoxLayout(self)
        image_layout = QHBoxLayout()  # Horizontales Layout für das Bild
        image_path = 'Bilder/libyaGovHigh.png'  # Pfad zum Bild
        pixmap = QPixmap(image_path).scaled(150, 150, Qt.KeepAspectRatio)  # Bild skalieren
        image_label = QLabel()  # Label für das Bild
        image_label.setPixmap(pixmap)  # Bild zum Label hinzufügen
        image_layout.addStretch()  # Strecke vor dem Bild, um es zu zentrieren
        image_layout.addWidget(image_label)  # Bild-Label zum Layout hinzufügen
        image_layout.addStretch()  # Strecke nach dem Bild, um es zu zentrieren
        main_layout.insertLayout(0, image_layout)  # Füge das Bildlayout am Anfang des Hauptlayouts hinzu

        font = QFont("Arial", 20)

        # Text Label, zentriert
        text_label_layout = QHBoxLayout()  # Horizontales Layout für das Text-Label
        text_label = QLabel('منظومة إصدار التأشيرات بالسفارة الليبية ببرلين')  # Text-Label erstellen
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setFont(font)

        font = QFont("Arial", 16)

        text_label_layout.addStretch()  # Strecke vor dem Text, um ihn zu zentrieren
        text_label_layout.addWidget(text_label)  # Text-Label zum Layout hinzufügen
        text_label_layout.addStretch()  # Strecke nach dem Text, um ihn zu zentrieren

        main_layout.addLayout(text_label_layout)  # Füge das Text-Label-Layout zum Hauptlayout hinzu

        # Login-Panel für Label, Eingabefeld und Button, zentriert
        login_panel_layout = QVBoxLayout()
        label_layout = QHBoxLayout()
        self.label = QLabel('أدخل كلمة المرور:')
        self.label.setFont(font)
        label_layout.addStretch()
        label_layout.addWidget(self.label)
        label_layout.addStretch()


        font = QFont("Arial", 14)

        password_input_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedSize(200, 40)
        self.password_input.setFont(font)
        password_input_layout.addStretch()
        password_input_layout.addWidget(self.password_input)
        password_input_layout.addStretch()


        button_layout = QHBoxLayout()
        self.login_button = QPushButton('تسجيل الدخول')
        self.login_button.setFixedSize(200, 40)
        button_layout.addStretch()
        button_layout.addWidget(self.login_button)
        button_layout.addStretch()

        login_panel_layout.addLayout(label_layout)
        login_panel_layout.addLayout(password_input_layout)
        login_panel_layout.addLayout(button_layout)

        # Footer, zentriert
        footer_layout = QHBoxLayout()
        footer_text = QLabel('2024 Developed by ')
        footer_text.setStyleSheet("font-size: 16px;")
        logo_path = 'Bilder/logo1x1-_improved.png'
        logo_pixmap = QPixmap(logo_path).scaled(80, 80, Qt.KeepAspectRatio)
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)
        link_label = QLabel(
            '<a href="https://www.itpandmore.com" style="color: white; text-decoration: none;">www.itpandmore.com</a>')
        link_label.setStyleSheet("color: white; font-size: 16px;")
        link_label.setOpenExternalLinks(True)
        footer_layout.addStretch()
        footer_layout.addWidget(footer_text)
        footer_layout.addWidget(logo_label)
        footer_layout.addWidget(link_label)
        footer_layout.addStretch()

        # Hauptlayout-Zusammenstellung
        main_layout.addStretch()
        main_layout.addLayout(login_panel_layout)
        main_layout.addStretch()
        main_layout.addLayout(footer_layout)

        self.setLayout(main_layout)
