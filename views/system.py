from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QSpacerItem, QSizePolicy, QComboBox, QDateEdit, QFileDialog, \
    QMessageBox, QSplitter
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QGridLayout, QWidget, QVBoxLayout
from PyQt5.QtCore import QDate

from views.guiElements.treeView import TreeView
from views.guiElements.searchElement import SearchElement


class System_View(QWidget):
    def __init__(self):
        super().__init__()

    def initUI(self):

        splitter = QSplitter(Qt.Vertical, self)
        splitter.setHandleWidth(1)
        splitter.setStyleSheet("QSplitter::handle { background-color: #828282; }")

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(10, 0, 10, 10)

        top_widget = QWidget(self)
        layout.addWidget(top_widget, 65)
        top_layout = QVBoxLayout(top_widget)
        top_layout.setSpacing(0)
        top_layout.setContentsMargins(0, 0, 0, 0)

        t_top_widget = QWidget(top_widget)
        t_top_layout = QHBoxLayout(t_top_widget)
        # t_top_layout.setContentsMargins(0, 0, 0, 0)
        t_top_layout.setSpacing(50)

        top_layout.addWidget(t_top_widget, 90)

        t_t_left_widget = QWidget(t_top_widget)
        t_t_left_layout = QVBoxLayout(t_t_left_widget)
        t_t_left_layout.setContentsMargins(0, 0, 0, 0)

        t_t_right_widget = QWidget(t_top_widget)
        t_t_right_layout = QVBoxLayout(t_t_right_widget)
        t_t_right_layout.setContentsMargins(0, 0, 0, 0)

        t_top_layout.addWidget(t_t_left_widget, 30)
        t_top_layout.addWidget(t_t_right_widget, 70)

        t_bottom_widget = QWidget(top_widget)
        top_layout.addWidget(t_bottom_widget, 10)

        self.bottom_widget = QWidget(self)
        layout.addWidget(self.bottom_widget, 35)
        bottom_layout = QVBoxLayout(self.bottom_widget)
        bottom_layout.setSpacing(0)
        bottom_layout.setContentsMargins(0, 0, 0, 0)

        b_top_widget = QWidget(self.bottom_widget)
        b_top_layout = QHBoxLayout(b_top_widget)
        b_top_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addWidget(b_top_widget, 90)

        b_bottom_widget = QWidget(self.bottom_widget)
        bottom_layout.addWidget(b_bottom_widget, 10)

        b_t_left_widget = QWidget(b_top_widget)
        b_t_right_widget = QWidget(b_top_widget)
        b_top_layout.addWidget(b_t_left_widget, 15)
        b_top_layout.addWidget(b_t_right_widget, 85)

        sfont = QFont("Helvetica", 10)

        self.simple_gui = SearchElement(sfont)
        left_layout = QVBoxLayout(b_t_left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.simple_gui)

        font = QFont("Arial", 14)
        self.treeViewWidget = TreeView(font)
        right_layout = QVBoxLayout(b_t_right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(self.treeViewWidget)

        # Call to add buttons to the bottom widget
        self.setupBottomButtons(b_bottom_widget)
        self.setupTopButtons(t_bottom_widget)
        self.setupInputs(t_t_right_layout, font)
        self.setupImageArea(t_t_left_layout, font)

        splitter.addWidget(top_widget)
        splitter.addWidget(self.bottom_widget)

        splitter.setSizes([650, 350])

        # Add the splitter to the main layout
        layout.addWidget(splitter)

    def setupBottomButtons(self, b_bottom_widget):
        button_layout = QHBoxLayout(b_bottom_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)

        self.help_button = QPushButton('الدعم الفني والمساعدة', b_bottom_widget)
        button_layout.addWidget(self.help_button)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout.addItem(spacer)

        self.update_button = QPushButton('تحديث', b_bottom_widget)
        self.delete_button = QPushButton('حذف', b_bottom_widget)

        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

    def setupTopButtons(self, b_bottom_widget):
        button_layout = QHBoxLayout(b_bottom_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)

        self.exit_button = QPushButton('خروج', b_bottom_widget)
        button_layout.addWidget(self.exit_button)

        # Button "Show" erstellen und auf der linken Seite hinzufügen
        self.show_button = QPushButton('إخفاء', b_bottom_widget)
        button_layout.addWidget(self.show_button)

        # Erstelle den Upload-Button
        self.uploadButton = QPushButton("تحميل الصورة")
        button_layout.addWidget(self.uploadButton)

        # Leeren Abstand hinzufügen, um den Rest nach rechts zu schieben
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_layout.addWidget(left_spacer)

        # QComboBox erstellen und Optionen hinzufügen
        self.print_combo_box = QComboBox(b_bottom_widget)
        self.print_combo_box.addItems(['فوق', 'وسط', 'تحت', "بدون اختيار", "تقرير"])
        button_layout.addWidget(self.print_combo_box)

        # Buttons erstellen
        self.print_button = QPushButton('طباعة', b_bottom_widget)
        self.back_button = QPushButton('السابق', b_bottom_widget)
        self.next_button = QPushButton('التالي', b_bottom_widget)
        self.clear_button = QPushButton('مسح', b_bottom_widget)
        self.new_button = QPushButton('جديد', b_bottom_widget)

        # Buttons zum Layout hinzufügen
        button_layout.addWidget(self.print_button)
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.new_button)
        self.show_button.clicked.connect(self.toggleLowerWidget)

    def setupInputs(self, layout, font):
        self.inputLayout = QGridLayout()

        self.inputs = []

        # Employee
        labelEmployee = QLabel("اسم الموظف")
        labelEmployee.setFont(font)
        self.lineEditEmployee = QLineEdit()
        self.lineEditEmployee.setFont(font)
        self.inputLayout.addWidget(self.lineEditEmployee, 0, 0)
        self.inputLayout.addWidget(labelEmployee, 0, 1)
        self.inputs.append(self.lineEditEmployee)
        self.lineEditEmployee.setText

        # Visa Number
        labelVisaNumber = QLabel("الرقم الألي")
        labelVisaNumber.setFont(font)
        self.lineEditVisaNumber = QLineEdit()
        self.lineEditVisaNumber.setFont(font)
        self.inputLayout.addWidget(self.lineEditVisaNumber, 1, 0)
        self.inputLayout.addWidget(labelVisaNumber, 1, 1)
        self.inputs.append(self.lineEditVisaNumber)

        # VisaTyp
        labelVisaTyp = QLabel("نوع التأشيرة")
        labelVisaTyp.setFont(font)
        self.comboBoxVisaTyp = QComboBox()
        self.comboBoxVisaTyp.setFont(font)
        self.comboBoxVisaTyp.addItems(["زيارة", "سياحة", "مجاملة", "إلحاق", "عمل", "مهمة"])
        self.inputLayout.addWidget(self.comboBoxVisaTyp, 2, 0)
        self.inputLayout.addWidget(labelVisaTyp, 2, 1)
        self.inputs.append(self.comboBoxVisaTyp)

        # Vorname
        labelVorname = QLabel("الأسم")
        labelVorname.setFont(font)
        self.lineEditVorname = QLineEdit()
        self.lineEditVorname.setFont(font)
        self.inputLayout.addWidget(self.lineEditVorname, 3, 0)
        self.inputLayout.addWidget(labelVorname, 3, 1)
        self.inputs.append(self.lineEditVorname)

        # Nachname
        labelNachname = QLabel("اللقب")
        labelNachname.setFont(font)
        self.lineEditNachname = QLineEdit()
        self.lineEditNachname.setFont(font)
        self.inputLayout.addWidget(self.lineEditNachname, 4, 0)
        self.inputLayout.addWidget(labelNachname, 4, 1)
        self.inputs.append(self.lineEditNachname)

        # Passport Nr.
        labelPassportNr = QLabel("رقم الجواز")
        labelPassportNr.setFont(font)
        self.lineEditPassportNr = QLineEdit()
        self.lineEditPassportNr.setFont(font)
        self.inputLayout.addWidget(self.lineEditPassportNr, 5, 0)
        self.inputLayout.addWidget(labelPassportNr, 5, 1)
        self.inputs.append(self.lineEditPassportNr)

        # Proffession
        labelProfession = QLabel("مهنة")
        labelProfession.setFont(font)
        self.lineEditProfession = QLineEdit()
        self.lineEditProfession.setFont(font)
        self.inputLayout.addWidget(self.lineEditProfession, 6, 0)
        self.inputLayout.addWidget(labelProfession, 6, 1)
        self.inputs.append(self.lineEditProfession)

        # Visa Issue Date
        labelVisaIss = QLabel("تاريخ الإصدار")
        labelVisaIss.setFont(font)
        self.dateEditVisaIss = QDateEdit()
        self.dateEditVisaIss.setFont(font)
        self.dateEditVisaIss.setCalendarPopup(True)
        self.dateEditVisaIss.setDate(QDate.currentDate())
        self.inputLayout.addWidget(self.dateEditVisaIss, 7, 0)
        self.inputLayout.addWidget(labelVisaIss, 7, 1)
        self.inputs.append(self.dateEditVisaIss)

        # Duration
        labelDuration = QLabel("مدة الإقامة")
        labelDuration.setFont(font)
        self.comboBoxDuration = QComboBox()
        self.comboBoxDuration.setFont(font)
        self.comboBoxDuration.addItems(["30", "60", "90", "180", "365"])
        self.comboBoxDuration.setCurrentIndex(0)  # Set default selection to "30"
        self.inputLayout.addWidget(self.comboBoxDuration, 8, 0)
        self.inputLayout.addWidget(labelDuration, 8, 1)
        self.inputs.append(self.comboBoxDuration)

        # Visa Validity
        labelVisaValid = QLabel("صالحة إلي")
        labelVisaValid.setFont(font)
        self.dateEditVisaValid = QDateEdit()
        self.dateEditVisaValid.setFont(font)
        self.dateEditVisaValid.setCalendarPopup(True)
        self.dateEditVisaValid.setDate(self.dateEditVisaIss.date().addDays(int(self.comboBoxDuration.currentText())))
        self.dateEditVisaValid.setReadOnly(True)  # Disable manual editing
        self.inputLayout.addWidget(self.dateEditVisaValid, 9, 0)
        self.inputLayout.addWidget(labelVisaValid, 9, 1)
        self.inputs.append(self.dateEditVisaValid)

        # Visa Entry
        labelVisaEntry = QLabel("عدد مرات الدخول")
        labelVisaEntry.setFont(font)
        self.comboBoxVisaEntry = QComboBox()
        self.comboBoxVisaEntry.setFont(font)
        self.comboBoxVisaEntry.addItems(["رحلة واحدة", "متعددة"])
        self.inputLayout.addWidget(self.comboBoxVisaEntry, 10, 0)
        self.inputLayout.addWidget(labelVisaEntry, 10, 1)
        self.inputs.append(self.comboBoxVisaEntry)

        # Work Place
        labelFee = QLabel("رسوم الدخول")
        labelFee.setFont(font)
        self.lineEditFee = QLineEdit()
        self.lineEditFee.setFont(font)
        self.inputLayout.addWidget(self.lineEditFee, 11, 0)
        self.inputLayout.addWidget(labelFee, 11, 1)
        self.inputs.append(self.lineEditFee)

        # Port
        labelPort = QLabel("المنفذ")
        labelPort.setFont(font)
        self.lineEditPort = QComboBox()
        self.lineEditPort.setFont(font)
        self.lineEditPort.addItems(
            ["معيتيقة الدولي","طرابلس العالمي", "بنينة الدولي","منفذ رأس جدير", "سبها الدولي", "مصراتة الدولي","منفذ السلوم"])
        self.inputLayout.addWidget(self.lineEditPort, 12, 0)
        self.inputLayout.addWidget(labelPort, 12, 1)
        self.inputs.append(self.lineEditPort)

        # Work Place
        labelWorkPlace = QLabel("الكفيل (جهة العمل)")
        labelWorkPlace.setFont(font)
        self.lineEditWorkPlace = QLineEdit()
        self.lineEditWorkPlace.setFont(font)
        self.inputLayout.addWidget(self.lineEditWorkPlace, 13, 0)
        self.inputLayout.addWidget(labelWorkPlace, 13, 1)
        self.inputs.append(self.lineEditWorkPlace)

        # Notes
        labelNotes = QLabel("ملاحظات")
        labelNotes.setFont(font)
        self.lineEditNotes = QLineEdit()
        self.lineEditNotes.setFont(font)
        self.inputLayout.addWidget(self.lineEditNotes, 14, 0)
        self.inputLayout.addWidget(labelNotes, 14, 1)
        self.inputs.append(self.lineEditNotes)

        layout.addLayout(self.inputLayout)

        self.dateEditVisaIss.dateChanged.connect(self.update_visa_validity)
        self.comboBoxDuration.currentIndexChanged.connect(self.update_visa_validity)

    # Connect changes
    def update_visa_validity(self):
        issue_date = self.dateEditVisaIss.date()
        duration_days = int(self.comboBoxDuration.currentText())
        new_validity_date = issue_date.addDays(duration_days)
        self.dateEditVisaValid.setDate(new_validity_date)

    def setupImageArea(self, layout, font):
        verticalLayout = QVBoxLayout()

        # Füge einen Spacer hinzu, um das Bild und den Button vertikal zu zentrieren
        verticalLayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Erstelle das Label für das Bild und setze die Größe auf 400x400
        self.imageLabel = QLabel()
        self.imageLabel.setFixedSize(300, 300)  # Größe des Bildes erhöhen
        self.imageLabel.setAlignment(Qt.AlignCenter)

        verticalLayout.addWidget(self.imageLabel, alignment=Qt.AlignCenter)

        verticalLayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        layout.addLayout(verticalLayout)

    def toggleLowerWidget(self):
        # Toggle the visibility of the lower widget
        isVisible = self.bottom_widget.isVisible()
        self.bottom_widget.setVisible(not isVisible)

        # Change the text of the button
        if isVisible:
            self.show_button.setText('إظهار')
        else:
            self.show_button.setText('إخفاء')
