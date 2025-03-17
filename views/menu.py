from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class Menu_View(QWidget):
    def __init__(self):
        super().__init__()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        # Bild Layout
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
        text_label_layout.addStretch()  # Strecke nach dem Text, um es zu zentrieren

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
        # Layout für die Buttons (3 Reihen)
        button_layout = QVBoxLayout()

        font_buttons = QFont("Arial", 16)

        # Erste Reihe: Button 1 und Button 2
        row1 = QHBoxLayout()
        self.button_heiraten = QPushButton("وافعات الزواج")
        self.button_heiraten.setMinimumSize(500, 100)  # Vergrößerte Mindestgröße
        self.button_heiraten.setFont(font_buttons)
        self.button_scheiden = QPushButton("واقعات الطلاق")
        self.button_scheiden.setMinimumSize(500, 100)  # Vergrößerte Mindestgröße
        self.button_scheiden.setFont(font_buttons)
        row1.addStretch()
        row1.addWidget(self.button_heiraten)
        row1.addSpacing(20)  # Abstand zwischen den Buttons
        row1.addWidget(self.button_scheiden)
        row1.addStretch()

        # Zweite Reihe: Button 3 und Button 4
        row2 = QHBoxLayout()
        self.button_sterben = QPushButton("شهادات الوفاة")
        self.button_sterben.setMinimumSize(500, 100)  # Vergrößerte Mindestgröße
        self.button_sterben.setFont(font_buttons)
        self.button_geboren = QPushButton("شهادات الميلاد")
        self.button_geboren.setMinimumSize(500, 100)  # Vergrößerte Mindestgröße
        self.button_geboren.setFont(font_buttons)
        row2.addStretch()
        row2.addWidget(self.button_sterben)
        row2.addSpacing(20)
        row2.addWidget(self.button_geboren)
        row2.addStretch()

        # Dritte Reihe: Button 5 (zentriert)
        row3 = QHBoxLayout()
        self.button_report = QPushButton("الأحوال المدنية")
        self.button_report.setMinimumSize(500, 100)  # Vergrößerte Mindestgröße
        self.button_report.setFont(font_buttons)
        row3.addStretch()
        row3.addWidget(self.button_report)
        row3.addStretch()

        # Reihen in das Button-Layout einfügen
        button_layout.addLayout(row1)
        button_layout.addSpacing(20)
        button_layout.addLayout(row2)
        button_layout.addSpacing(20)
        button_layout.addLayout(row3)

        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        main_layout.addStretch()

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
