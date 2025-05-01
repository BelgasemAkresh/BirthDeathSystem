import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QApplication
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

        # Überschrift (zentriert)
        text_label_layout = QHBoxLayout()
        text_label = QLabel('دولة ليبيا')
        header_font = QFont("Arial", 26)
        text_label.setFont(header_font)
        text_label.setAlignment(Qt.AlignCenter)
        text_label_layout.addStretch()
        text_label_layout.addWidget(text_label)
        text_label_layout.addStretch()
        main_layout.addLayout(text_label_layout)

        # Überschrift (zentriert)
        text_label_layout = QHBoxLayout()
        text_label = QLabel('وزارة الخارجية و التعاون الدولي')
        header_font = QFont("Arial", 26)
        text_label.setFont(header_font)
        text_label.setAlignment(Qt.AlignCenter)
        text_label_layout.addStretch()
        text_label_layout.addWidget(text_label)
        text_label_layout.addStretch()
        main_layout.addLayout(text_label_layout)

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

        # Um das Label auch vertikal zu zentrieren:
        main_layout.addStretch()  # Obere vertikale Strecke
        main_layout.addLayout(text_label_layout)
        main_layout.addStretch()  # Untere vertikale Strecke
        # Login-Panel: Passwort-Label, Eingabefeld und Button
        login_panel_layout = QVBoxLayout()

        # Überschrift (zentriert)
        text_label_layout = QHBoxLayout()
        text_label = QLabel('منظومة الأحوال المدنية بالقنصلية العامة في دوسلدورف')
        header_font = QFont("Arial", 20)
        text_label.setFont(header_font)
        text_label.setAlignment(Qt.AlignCenter)
        text_label_layout.addStretch()
        text_label_layout.addWidget(text_label)
        text_label_layout.addStretch()
        main_layout.addLayout(text_label_layout)

        # Passwort-Zeile mit Label und Eingabefeld (nebeneinander)
        password_row_layout = QHBoxLayout()
        password_row_layout.addStretch()

        self.label = QLabel('أدخل كلمة المرور:')
        label_font = QFont("Arial", 16)
        self.label.setFont(label_font)
        password_row_layout.addWidget(self.label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        input_width = self.config["ui"].get("input_field_width", 200)
        input_height = self.config["ui"].get("input_field_height", 40)
        self.password_input.setFixedSize(input_width, input_height)
        input_font = QFont("Arial", 12)
        self.password_input.setFont(input_font)
        password_row_layout.addWidget(self.password_input)

        password_row_layout.addStretch()
        login_panel_layout.addLayout(password_row_layout)

        # Abstand zwischen Eingabezeile und Buttons
        login_panel_layout.addSpacing(10)

        # Layout für Buttons: direkt unter der Eingabezeile, rechtsbündig
        buttons_under_label_layout = QHBoxLayout()
        buttons_under_label_layout.addStretch()  # Platz links

        buttons_column = QVBoxLayout()
        buttons_column.setAlignment(Qt.AlignRight)  # Im RTL-Modus sorgt das für "unter Label"-Platzierung

        btn_width = self.label.sizeHint().width() + self.password_input.width()
        btn_height = self.config["ui"].get("button_height", 40)
        button_font = QFont("Arial", 12)

        self.login_button = QPushButton('تسجيل الدخول')
        self.login_button.setFixedSize(btn_width, btn_height)
        self.login_button.setFont(button_font)

        self.exit_button = QPushButton('خروج')
        self.exit_button.setFixedSize(btn_width, btn_height)
        self.exit_button.setFont(button_font)

        buttons_column.addWidget(self.login_button)
        buttons_column.addSpacing(200)
        buttons_column.addWidget(self.exit_button)

        buttons_under_label_layout.addLayout(buttons_column)
        buttons_under_label_layout.addStretch()  # Platz rechts

        login_panel_layout.addLayout(buttons_under_label_layout)

        self.exit_button.clicked.connect(QApplication.quit)

        # Button-Signal verbinden
        self.login_button.clicked.connect(self.on_button_clicked)

        # Login-Panel mittig platzieren
        main_layout.addStretch()
        main_layout.addLayout(login_panel_layout)
        main_layout.addStretch()

        # Footer (zentriert)
        footer_layout = QHBoxLayout()
        footer_text = QLabel('2025 Developed by IT Power&More ')
        footer_text.setStyleSheet("font-size: 16px;")
        logo_path = 'Bilder/logo-improved.png'
        logo_pixmap = QPixmap(logo_path).scaled(80, 80, Qt.KeepAspectRatio)
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)
        link_label = QLabel(
            '<a href="https://www.itpandmore.com" style="color:#D4AF37 ; text-decoration: none;">www.itpandmore.com</a>')
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
