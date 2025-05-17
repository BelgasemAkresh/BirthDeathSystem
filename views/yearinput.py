import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator

# Mappings für arabische Zahlwörter (vereinfacht und grammatikalisch korrekt)
einheiten = {
    0: "", 1: "واحد", 2: "اثنان", 3: "ثلاثة", 4: "أربعة", 5: "خمسة",
    6: "ستة", 7: "سبعة", 8: "ثمانية", 9: "تسعة"
}

zehner = {
    10: "عشرة", 20: "عشرون", 30: "ثلاثون", 40: "أربعون",
    50: "خمسون", 60: "ستون", 70: "سبعون", 80: "ثمانون", 90: "تسعون"
}

def jahr_in_arabisch(jahr):
    if jahr < 1900 or jahr > 2100:
        return None

    # Behandlung von Jahren ab 2000
    if jahr == 2000:
        return "ألفان"
    elif jahr < 2000:
        rest = jahr - 1900
        jahr_text = "ألف وتسعمائة"
    else:
        rest = jahr - 2000
        jahr_text = "ألفان"

    # Jahr ist zwischen 2001 und 2099
    if rest == 0:
        return jahr_text
    elif rest < 10:
        return f"{jahr_text} و{einheiten[rest]}"
    elif rest < 20:
        if rest == 10:
            return f"{jahr_text} و{zehner[10]}"
        else:
            return f"{jahr_text} و{einheiten[rest - 10]} عشر"
    else:
        z = (rest // 10) * 10
        e = rest % 10
        if e == 0:
            return f"{jahr_text} و{zehner[z]}"
        else:
            return f"{jahr_text} و{einheiten[e]} و{zehner[z]}"


class ArabicYearInput(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Jahr (1900–2100) eingeben")
        self.setValidator(QIntValidator(1900, 2100))  # Nur gültige Jahre zulassen
        self.textChanged.connect(self.on_text_changed)
        self.focusOutEvent = self.on_focus_out  # Fokussierereignis überschreiben
        self.mousePressEvent = self.on_mouse_press  # Mausklick-Ereignis überschreiben
        self.text_valid = True  # Flag für die Gültigkeit der Eingabe

    def on_text_changed(self):
        # Wenn der Benutzer noch dabei ist, etwas zu tippen, aber es eine gültige Zahl gibt
        if self.text().isdigit():
            jahr = int(self.text())
            arabisch = jahr_in_arabisch(jahr)
            if arabisch:
                self.setText(arabisch)
                self.text_valid = True  # Eingabe ist jetzt gültig
            else:
                self.setReadOnly(False)  # Lässt es wieder editierbar, falls ungültig
                self.text_valid = False  # Eingabe ist ungültig

    def on_focus_out(self, event):
        # Löscht den Text nur, wenn der Text ungültig ist und der Benutzer das Eingabefeld verlässt
        if not self.text_valid:
            self.clear()  # Löscht den Text, wenn es keine gültige Zahl ist
        super().focusOutEvent(event)  # Ruft das ursprüngliche Focus-Out-Ereignis auf

    def on_mouse_press(self, event):
        # Wenn auf das Eingabefeld geklickt wird, soll der Text gelöscht werden, um neu einzugeben
        if self.text() and self.text() != "":  # Nur löschen, wenn es bereits Text gibt
            self.clear()  # Löscht den Text, um neue Eingabe zu ermöglichen
            self.setReadOnly(False)  # Macht das Eingabefeld wieder editierbar
            self.text_valid = False  # Markiert den Text als ungültig
        super().mousePressEvent(event)  # Ruft das ursprüngliche Mausklick-Ereignis auf


class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test der ArabicYearInput-Klasse")
        self.setGeometry(100, 100, 400, 150)

        # Label zur Anzeige des Inputs
        self.label = QLabel("Bitte ein Jahr eingeben:")
        self.label.setAlignment(Qt.AlignCenter)

        # Erstelle das benutzerdefinierte Eingabefeld
        self.arabic_input = ArabicYearInput()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.arabic_input)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenster = TestWindow()
    fenster.show()
    sys.exit(app.exec_())
