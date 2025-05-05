import contextlib
import sqlite3
import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QDialog, QLineEdit, QDateEdit, QHBoxLayout, QSizePolicy, QGridLayout,
    QScrollArea
)

from PyQt5.QtCore import Qt, pyqtSignal, QObject, QDate
from PyQt5.QtGui import QFont, QPalette, QColor

from datetime import datetime

from model.databasemodel import DatabaseModel
from controllers.passwordcontroller import PasswordController
from openconfig import openconfig
from views.passwordview import PasswordView

from controllers.tableeditorcontroller import TableEditorController
from views.tableeditorview import TableEditorView

import sys
import tempfile
import shutil
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from docxtpl import DocxTemplate
from docx2pdf import convert


GENERATOR_CONFIG = openconfig()





class MainMenuView(QWidget):
    """Hauptmenü, das dynamisch Buttons für alle Tabellen aus der Konfiguration erzeugt."""
    tableSelected = pyqtSignal(str, str)  # (Tabellenname, JSON-String der Tabellen-Konfiguration)

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setLayoutDirection(Qt.RightToLeft)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Titel
        label = QLabel("سجلات الاحوال المدنية")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: rgb(212, 175, 55);
                margin-bottom: 20px;
            }
        """)
        main_layout.addWidget(label)

        # Scroll-Bereich für Buttons
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)

        scroll_content = QWidget()
        scroll_layout = QGridLayout(scroll_content)
        scroll_layout.setSpacing(15)

        # Dynamische Tabellen-Buttons
        row, col = 0, 0
        for idx, table_name in enumerate(self.config["tables"]):
            btn = QPushButton(table_name.replace("_", " "))
            btn.setMinimumSize(self.config["ui"]["button_width"], self.config["ui"]["button_height"])
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgb(52, 52, 52);
                    color: rgb(212, 175, 55);
                    border: 3px solid rgb(212, 175, 55);
                    border-radius: 20px;
                    padding: 200px;
                    font-size: 30px;
                }
                QPushButton:hover {
                    background-color: rgb(70, 70, 70);
                }
            """)
            btn.clicked.connect(lambda checked, tn=table_name, conf=json.dumps(self.config["tables"][table_name]):
                                self.tableSelected.emit(tn, conf))
            scroll_layout.addWidget(btn, row, col)
            col += 1
            if col >= 2:
                col = 0
                row += 1

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # Bericht- und خروج-Buttons in ein horizontales Layout
        button_layout = QHBoxLayout()

        # Bericht-Button
        self.report_btn = QPushButton("إحصائية: تقرير الأحوال المدنية")
        self.report_btn.setMinimumSize(self.config["ui"]["button_width"], self.config["ui"]["button_height"])
        self.report_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(110, 110, 110);
                color: white;
                border: 3px solid white;
                border-radius: 15px;
                padding: 15px;
                font-size: 25px;
            }
            QPushButton:hover {
                background-color: rgb(50, 120, 210);
            }
        """)
        button_layout.addWidget(self.report_btn)

        # خروج-Button
        self.exit_btn = QPushButton("خروج")
        self.exit_btn.setMinimumSize(self.config["ui"]["button_width"], self.config["ui"]["button_height"])
        self.exit_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(110, 110, 110);
                color: white;
                border: 3px solid white;
                border-radius: 15px;
                padding: 15px;
                font-size: 25px;
            }
            QPushButton:hover {
                background-color: rgb(200, 70, 70);
            }
        """)
        self.exit_btn.clicked.connect(QApplication.quit)
        button_layout.addWidget(self.exit_btn)

        # Button-Layout zum Hauptlayout hinzufügen
        main_layout.addLayout(button_layout)

    def closeEvent(self, event):
        QApplication.quit()
        event.accept()


class MainMenuController(QObject):
    """Controller für das Hauptmenü."""
    def __init__(self, view, main_window):
        super().__init__()
        self.view = view
        self.main_window = main_window
        self.view.tableSelected.connect(self.open_table_editor)
        self.view.report_btn.clicked.connect(self.make_report)

    def make_report(self):
        try:
            data = self.get_user_data()
            numbers= self.zaehle_eintraege_zwischen(data[0], data[1])
            heute = datetime.today().strftime('%d-%m-%Y')
            m, f = map(sum, zip(*numbers))

            self.print_record(heute, data[0], data[1],
                              numbers[3][0], numbers[3][1],
                              numbers[0][0],numbers[0][1],
                              numbers[1][0],numbers[1][1],
                              numbers[2][0],numbers[2][1],
                              m, f, data[2], data[3])
        except:
            pass

    def print_record(self, datum, von, bis,
                     mg, fg, mh, fh, ms, fs, mt, ft,
                     m, f,
                     beamtername, beamterkennung,
                     parent_view=None):
        """
        Erzeugt aus einer Docx-Vorlage ein PDF und bietet die Möglichkeit, es zu speichern.
        Dabei werden stdout und stderr umgeleitet, um Probleme bei windowed exe (ohne Konsole) zu vermeiden.
        """
        # Ermitteln des Basisverzeichnisses (für gefrorene exe: sys._MEIPASS, sonst aktuelles Skriptverzeichnis)
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        # Pfad zur Vorlage (sicherstellen, dass der Ordner 'vorlagen' in den Build einbezogen wird)
        template_path = os.path.join(base_path, "vorlagen", "تقرير_الأحوال_المدنية.docx")
        if not os.path.exists(template_path):
            err_msg = f"Template nicht gefunden: {template_path}"
            if parent_view:
                QMessageBox.warning(parent_view, "خطأ", err_msg)
            else:
                print(err_msg)
            return

        # Kontextdaten für die Vorlage
        context = {
            "datum": datum,
            "von": von,
            "bis": bis,
            "mg": mg,
            "fg": fg,
            "mh": mh,
            "fh": fh,
            "ms": ms,
            "fs": fs,
            "mt": mt,
            "ft": ft,
            "m": m,
            "f": f,
            "beamtername": beamtername,
            "beamterkennung": beamterkennung,
        }

        try:
            # Vorlage laden, Kontextdaten einfügen und in ein temporäres Docx speichern
            doc = DocxTemplate(template_path)
            doc.render(context)

            # Verwenden eines schreibbaren temporären Verzeichnisses
            temp_dir = tempfile.gettempdir()
            temp_docx = os.path.join(temp_dir, "temp_filled.docx")
            temp_pdf = os.path.join(temp_dir, "temp_filled.pdf")

            doc.save(temp_docx)

            # Sicherstellen, dass stdout und stderr nicht None sind (wichtig im windowed Modus)
            if sys.stdout is None:
                sys.stdout = open(os.devnull, 'w')
            if sys.stderr is None:
                sys.stderr = open(os.devnull, 'w')

            # Umleiten von stdout und stderr während der Konvertierung
            with open(os.devnull, 'w') as fnull:
                with contextlib.redirect_stdout(fnull), contextlib.redirect_stderr(fnull):
                    convert(temp_docx, temp_pdf)

            # Prüfen, ob die PDF-Datei erstellt wurde
            if not os.path.exists(temp_pdf):
                raise Exception("PDF-Konvertierung fehlgeschlagen – temporäre PDF-Datei wurde nicht gefunden.")

            # Dialog zum Speichern der PDF anzeigen
            save_path, _ = QFileDialog.getSaveFileName(parent_view, "احفظ ملف PDF", "", "PDF Dateien (*.pdf)")
            if save_path:
                shutil.copyfile(temp_pdf, save_path)
                success_msg = f"PDF wurde erfolgreich gespeichert unter:\n{save_path}"
                if parent_view:
                    QMessageBox.information(parent_view, "نجاح", success_msg)
                else:
                    print(success_msg)

            # Aufräumen der temporären Dateien
            if os.path.exists(temp_docx):
                os.remove(temp_docx)
            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)

        except Exception as e:
            error_msg = f"Fehler beim Erstellen des Berichts:\n{str(e)}"
            if parent_view:
                QMessageBox.critical(parent_view, "خطأ", error_msg)
            else:
                print(error_msg)
    def open_table_editor(self, table_name, config_json):
        self.main_window.open_table_editor(table_name, config_json)

    def zaehle_eintraege_zwischen(self, datum_von, datum_bis):
        tabellen_info = [
            ("سجل_واقعات_الزواج", "paar"),
            ("سجل_واقعات_الطلاق", "paar"),
            ("سجل_واقعات_الوفاة", "geschlecht"),
            ("سجل_واقعات_الولادة", "geschlecht")
        ]

        ergebnisse = []

        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            for tabelle, typ in tabellen_info:
                mann = 0
                frau = 0
                try:
                    if typ == "paar":
                        query = f'''
                            SELECT COUNT(*) FROM "{tabelle}"
                            WHERE adddate IS NOT NULL
                            AND DATE(adddate) BETWEEN DATE(?) AND DATE(?)
                        '''
                        cursor.execute(query, (datum_von, datum_bis))
                        result = cursor.fetchone()
                        anzahl = result[0] if result and result[0] is not None else 0
                        mann = anzahl
                        frau = anzahl

                    elif typ == "geschlecht":
                        query = f'''
                            SELECT sex FROM "{tabelle}"
                            WHERE adddate IS NOT NULL
                            AND DATE(adddate) BETWEEN DATE(?) AND DATE(?)
                        '''
                        cursor.execute(query, (datum_von, datum_bis))
                        eintraege = cursor.fetchall()
                        for (geschlecht,) in eintraege:
                            if geschlecht == "ذكر":
                                mann += 1
                            elif geschlecht == "أنثى":
                                frau += 1

                except Exception as e:
                    print(f"Fehler bei Tabelle {tabelle}: {e}")
                    mann = 0
                    frau = 0

                ergebnisse.append((mann, frau))

            conn.close()

        except Exception as e:
            print("Fehler beim Öffnen der Datenbank:", e)
            return ((0, 0), (0, 0), (0, 0), (0, 0))

        return tuple(ergebnisse)

    def get_user_data(self):
        class ArabicDialog(QDialog):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("إدخال البيانات")
                self.setLayoutDirection(Qt.RightToLeft)
                self.init_ui()

            def init_ui(self):
                layout = QVBoxLayout()
                layout.setAlignment(Qt.AlignRight)

                # Zeitraum Titel
                period_title = QLabel("الأحوال المدنية التي تمت خلال الفترة:")
                period_title.setAlignment(Qt.AlignRight)
                layout.addWidget(period_title)

                # Zeitraum Eingabe (من - إلى)
                period_layout = QHBoxLayout()
                self.to_date = QDateEdit()
                self.to_date.setCalendarPopup(True)
                self.to_date.setDate(QDate.currentDate())

                self.from_date = QDateEdit()
                self.from_date.setCalendarPopup(True)
                self.from_date.setDate(QDate.currentDate())

                period_layout.addWidget(QLabel("من"))
                period_layout.addWidget(self.from_date)
                period_layout.addSpacing(10)
                period_layout.addWidget(QLabel("إلى"))
                period_layout.addWidget(self.to_date)
                layout.addLayout(period_layout)

                # Mitarbeitername
                name_label = QLabel("اسم الموظف:")
                name_label.setAlignment(Qt.AlignRight)
                self.name_input = QLineEdit()
                layout.addWidget(name_label)
                layout.addWidget(self.name_input)

                # Titel
                title_label = QLabel("الصفة:")
                title_label.setAlignment(Qt.AlignRight)
                self.title_input = QLineEdit()
                layout.addWidget(title_label)
                layout.addWidget(self.title_input)

                # Bestätigungsbutton
                self.ok_button = QPushButton("موافق")
                self.ok_button.clicked.connect(self.accept)
                layout.addWidget(self.ok_button, alignment=Qt.AlignCenter)

                self.setLayout(layout)

            def get_data(self):
                return (
                    self.from_date.date().toString("yyyy-MM-dd"),
                    self.to_date.date().toString("yyyy-MM-dd"),
                    self.name_input.text(),
                    self.title_input.text()
                )

        app = QApplication.instance()
        owns_app = app is None
        if owns_app:
            app = QApplication(sys.argv)

        dialog = ArabicDialog()
        result = dialog.exec_()
        data = dialog.get_data() if result == QDialog.Accepted else None

        if owns_app:
            app.quit()
        return data


# =============================================================================
# MAIN WINDOW
# =============================================================================

class MainWindow(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowTitle("القنصلية العامة في دوسلدورف")
        self.setGeometry(100, 100, config["ui"]["window_width"], config["ui"]["window_height"])
        self.setLayoutDirection(Qt.RightToLeft)
        self.db_model = DatabaseModel(config)
        self.stack = QStackedWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

        # Passwort-View + Controller
        self.password_view = PasswordView(config)
        self.password_controller = PasswordController(self.password_view, config, self)
        self.stack.addWidget(self.password_view)

        # Hauptmenü-View + Controller
        self.main_menu_view = MainMenuView(config)
        self.main_menu_controller = MainMenuController(self.main_menu_view, self)
        self.stack.addWidget(self.main_menu_view)

        # Referenz auf den aktuellen TableEditorController, um GC zu verhindern
        self.current_table_editor_controller = None

    def go_to_main_menu(self):
        self.stack.setCurrentWidget(self.main_menu_view)

    def go_to_password_screen(self):
        self.stack.setCurrentWidget(self.password_view)

    def open_table_editor(self, table_name, config_json):
        attributes = json.loads(config_json)
        attributes_without = [attr for attr in attributes if attr.get("name") != "breakline"]
        table_editor_view = TableEditorView(table_name, attributes, attributes_without, self.config)

        # Controller speichern, damit er nicht garbage-collected wird.
        self.current_table_editor_controller = TableEditorController(
            table_editor_view, table_name, attributes, attributes_without, self.db_model.db, self.config, self
        )
        self.stack.addWidget(table_editor_view)
        self.stack.setCurrentWidget(table_editor_view)


# =============================================================================
# HAUPTPROGRAMM
# =============================================================================

if __name__ == "__main__":
    import signal
    import os

    app = QApplication(sys.argv)

    app_font = QFont()
    app_font.setPointSize(GENERATOR_CONFIG["ui"]["font_size"])
    app.setFont(app_font)
    app.setStyle("Fusion")

    darker_palette = QPalette()
    darker_palette.setColor(QPalette.Window, QColor(52, 52, 52))
    darker_palette.setColor(QPalette.WindowText, QColor(212, 175, 55))
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
        QComboBox {
            font: 20px;
            padding: 5px 10px;
            min-height: 25px;
            min-width: 150px;
        }
    """)

    window = MainWindow(GENERATOR_CONFIG)
    window.show()

    exit_code = app.exec_()

    # Sicherstellen, dass der Prozess auch wirklich endet
    os.kill(os.getpid(), signal.SIGTERM)
    sys.exit(exit_code)
