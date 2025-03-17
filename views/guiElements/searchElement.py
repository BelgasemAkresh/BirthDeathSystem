from PyQt5.QtWidgets import QDateEdit, QLabel, QLineEdit, QPushButton, QGridLayout, QWidget
from PyQt5.QtCore import QDate

class SearchElement(QWidget):
    def __init__(self, font):
        super().__init__()

        grid = QGridLayout(self)

        label1 = QLabel('إسم الموظف')
        label1.setFont(font)

        self.entry1 = QLineEdit()
        self.entry1.setFont(font)
        grid.addWidget(self.entry1, 0, 0)
        grid.addWidget(label1, 0, 1)

        label2 = QLabel('من')
        label2.setFont(font)
        self.entry2 = QDateEdit()
        self.entry2.setFont(font)
        self.entry2.setCalendarPopup(True)
        self.entry2.setDate(QDate.currentDate())
        grid.addWidget(self.entry2, 1, 0)
        grid.addWidget(label2, 1, 1)
        
        label3 = QLabel('إلي')
        label3.setFont(font)
        self.entry3 = QDateEdit()
        self.entry3.setFont(font)
        self.entry3.setCalendarPopup(True)
        self.entry3.setDate(QDate.currentDate())
        grid.addWidget(self.entry3, 2, 0)
        grid.addWidget(label3, 2, 1)

        label4 = QLabel('رقم الجواز')
        label4.setFont(font)
        self.entry4 = QLineEdit()
        self.entry4.setFont(font)
        grid.addWidget(self.entry4, 3, 0)
        grid.addWidget(label4, 3, 1)

        self.reload_button = QPushButton("استعادة")
        self.reload_button.setFont(font)
        self.search_button = QPushButton('بحث')
        self.search_button.setFont(font)

        # Hinzufügen der Buttons in die gleiche Spalte und die letzte Zeile des Rasters
        grid.addWidget(self.reload_button, 4, 0)
        grid.addWidget(self.search_button, 4, 1)

        # Zentriere die Buttons innerhalb ihrer Zellen
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

    def clearSearch(self):
        self.entry1.clear()
        self.entry2.setDate(QDate.currentDate())
        self.entry3.setDate(QDate.currentDate())
        self.entry4.clear()
