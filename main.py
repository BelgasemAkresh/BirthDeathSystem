import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
     QPushButton,  QLabel, QStackedWidget
)

from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QPalette, QColor

from model.databasemodel import DatabaseModel
from controllers.passwordcontroller import PasswordController
from openconfig import openconfig
from views.passwordview import PasswordView

from controllers.tableeditorcontroller import TableEditorController
from views.tableeditorview import TableEditorView


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
        layout = QVBoxLayout(self)
        label = QLabel("اختر الجدول:")
        layout.addWidget(label)
        for table_name in self.config["tables"]:
            btn = QPushButton(table_name)
            btn.setMinimumSize(self.config["ui"]["button_width"], self.config["ui"]["button_height"])
            btn.clicked.connect(lambda checked, tn=table_name, conf=json.dumps(self.config["tables"][table_name]):
                                self.tableSelected.emit(tn, conf))
            layout.addWidget(btn)


class MainMenuController(QObject):
    """Controller für das Hauptmenü."""
    def __init__(self, view, main_window):
        super().__init__()
        self.view = view
        self.main_window = main_window
        self.view.tableSelected.connect(self.open_table_editor)

    def open_table_editor(self, table_name, config_json):
        self.main_window.open_table_editor(table_name, config_json)


# =============================================================================
# MAIN WINDOW
# =============================================================================

class MainWindow(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowTitle("التطبيق الرئيسي")
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
        table_editor_view = TableEditorView(table_name, attributes, self.config)
        # Controller speichern, damit er nicht garbage-collected wird.
        self.current_table_editor_controller = TableEditorController(
            table_editor_view, table_name, attributes, self.db_model.db, self.config, self
        )
        self.stack.addWidget(table_editor_view)
        self.stack.setCurrentWidget(table_editor_view)


# =============================================================================
# HAUPTPROGRAMM
# =============================================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app_font = QFont()
    app_font.setPointSize(GENERATOR_CONFIG["ui"]["font_size"])
    app.setFont(app_font)
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

        QComboBox {
            font: 20px;
            padding: 5px 10px;
            min-height: 25px;
            min-width: 150px; /* Ändere die Breite nach Bedarf */
        }
    """)



    window = MainWindow(GENERATOR_CONFIG)
    window.show()
    sys.exit(app.exec_())
