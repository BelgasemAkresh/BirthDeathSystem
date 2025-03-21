import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal

class PasswordView(QWidget):
    """Anzeige des Passwort-Eingabefeldes mit erweitertem Layout (Header, Login-Panel und Footer)."""
    passwordEntered = pyqtSignal(str)

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setLayoutDirection(Qt.RightToLeft)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Header: Bild oben
        image_layout = QHBoxLayout()
        image_layout.addStretch()
        image_path = 'Bilder/libyaGovHigh.png'
        pixmap = QPixmap(image_path).scaled(150, 150, Qt.KeepAspectRatio)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_layout.addWidget(image_label)
        image_layout.addStretch()
        main_layout.addLayout(image_layout)

        # Überschrift (zentriert)
        text_label_layout = QHBoxLayout()
        text_label = QLabel('منظومة إصدار التأشيرات بالسفارة الليبية ببرلين')
        header_font = QFont("Arial", 20)
        text_label.setFont(header_font)
        text_label.setAlignment(Qt.AlignCenter)
        text_label_layout.addStretch()
        text_label_layout.addWidget(text_label)
        text_label_layout.addStretch()
        main_layout.addLayout(text_label_layout)

        # Login-Panel: Passwort-Label, Eingabefeld und Button
        login_panel_layout = QVBoxLayout()

        # Passwort-Label (zentriert)
        label_layout = QHBoxLayout()
        self.label = QLabel('أدخل كلمة المرور:')
        label_font = QFont("Arial", 16)
        self.label.setFont(label_font)
        label_layout.addStretch()
        label_layout.addWidget(self.label)
        label_layout.addStretch()
        login_panel_layout.addLayout(label_layout)

        # Passwort-Eingabefeld (zentriert)
        password_input_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        # Verwende konfigurierbare Größen oder Standardwerte (200x40) wie im alten Widget
        input_width = self.config["ui"].get("input_field_width", 200)
        input_height = self.config["ui"].get("input_field_height", 40)
        self.password_input.setFixedSize(input_width, input_height)
        input_font = QFont("Arial", 12)
        self.password_input.setFont(input_font)
        password_input_layout.addStretch()
        password_input_layout.addWidget(self.password_input)
        password_input_layout.addStretch()
        login_panel_layout.addLayout(password_input_layout)

        # Login-Button (zentriert)
        button_layout = QHBoxLayout()
        self.login_button = QPushButton('تسجيل الدخول')
        btn_width = self.config["ui"].get("button_width", 200)
        btn_height = self.config["ui"].get("button_height", 40)
        self.login_button.setFixedSize(btn_width, btn_height)
        button_font = QFont("Arial", 12)
        self.login_button.setFont(button_font)
        button_layout.addStretch()
        button_layout.addWidget(self.login_button)
        button_layout.addStretch()
        login_panel_layout.addLayout(button_layout)

        # Button-Signal verbinden
        self.login_button.clicked.connect(self.on_button_clicked)

        # Login-Panel mittig platzieren
        main_layout.addStretch()
        main_layout.addLayout(login_panel_layout)
        main_layout.addStretch()

        # Footer (zentriert)
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
        main_layout.addLayout(footer_layout)

    def on_button_clicked(self):
        self.passwordEntered.emit(self.password_input.text())
