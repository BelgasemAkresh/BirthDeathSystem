import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QFormLayout,
    QLabel, QLineEdit, QSpinBox, QPushButton, QListWidget, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QDialog, QComboBox, QCheckBox, QPlainTextEdit,
    QMessageBox, QInputDialog, QHeaderView, QAbstractItemView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# -----------------------------
# Standard-Konfiguration als Fallback (Default)
# -----------------------------
DEFAULT_CONFIG = {
    "password": "geheim123",
    "db_name": "people.db",
    "ui": {
        "window_width": 1400,
        "window_height": 900,
        "font_size": 14,
        "button_width": 150,
        "button_height": 50,
        "input_field_height": 40
    },
    "tables": {
        "people1": [
            {"name": "الاسم_الاول", "label": "الاسم الأول", "type": "text", "not_null": True, "default": "أحمد"},
            {"name": "اسم_العائلة", "label": "اسم العائلة", "type": "text", "not_null": True, "default": "الحسيني"},
            {"name": "تاريخ_الميلاد", "label": "تاريخ الميلاد", "type": "date", "not_null": False,
             "default": "2000-01-01"}
        ],
        "people2": [
            {"name": "اسم_الموظف", "label": "اسم الموظف", "type": "text", "not_null": True, "default": "موظف افتراضي"},
            {"name": "القسم", "label": "القسم", "type": "dropdown", "options": ["المبيعات", "التطوير", "التسويق"],
             "not_null": True, "default": "المبيعات"},
            {"name": "الراتب", "label": "الراتب", "type": "number", "not_null": False, "default": "1000"}
        ],
        "people3": [
            {"name": "اسم_المنتج", "label": "اسم المنتج", "type": "text", "not_null": True, "default": "منتج افتراضي"},
            {"name": "الفئة", "label": "الفئة", "type": "dropdown", "options": ["إلكترونيات", "منزل", "ملابس"],
             "not_null": True, "default": "إلكترونيات"},
            {"name": "السعر", "label": "السعر", "type": "number", "not_null": True, "default": "50"},
            {"name": "تاريخ_الإنتاج", "label": "تاريخ الإنتاج", "type": "date", "not_null": False,
             "default": "2022-01-01"}
        ]
    }
}


# -----------------------------
# Dialog zum Bearbeiten der Dropdown-Optionen
# -----------------------------
class DropdownOptionsDialog(QDialog):
    def __init__(self, options=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dropdown-Optionen bearbeiten")
        self.resize(400, 300)
        self.options = options[:] if options else []
        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.list_widget.addItems(self.options)
        layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Hinzufügen")
        self.edit_btn = QPushButton("Bearbeiten")
        self.del_btn = QPushButton("Entfernen")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.del_btn)
        layout.addLayout(btn_layout)

        ok_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Abbrechen")
        ok_layout.addWidget(self.ok_btn)
        ok_layout.addWidget(self.cancel_btn)
        layout.addLayout(ok_layout)

        self.add_btn.clicked.connect(self.add_option)
        self.edit_btn.clicked.connect(self.edit_option)
        self.del_btn.clicked.connect(self.remove_option)
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def add_option(self):
        text, ok = QInputDialog.getText(self, "Option hinzufügen", "Neue Option:")
        if ok and text.strip():
            new_option = text.strip()
            self.options.append(new_option)
            self.list_widget.addItem(new_option)

    def edit_option(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            text, ok = QInputDialog.getText(self, "Option bearbeiten", "Neue Option:", text=current_item.text())
            if ok and text.strip():
                new_option = text.strip()
                row = self.list_widget.row(current_item)
                self.options[row] = new_option
                current_item.setText(new_option)

    def remove_option(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            row = self.list_widget.row(current_item)
            self.list_widget.takeItem(row)
            del self.options[row]

    def get_options(self):
        return self.options


# -----------------------------
# Dialog zum Anlegen/Bearbeiten eines Attributs
# -----------------------------
class AttributeDialog(QDialog):
    def __init__(self, parent=None, attr=None):
        super().__init__(parent)
        self.setWindowTitle("Attribut definieren")
        self.resize(400, 300)
        self.attr = attr  # Falls Editierung
        layout = QFormLayout(self)

        self.name_edit = QLineEdit()
        self.label_edit = QLineEdit()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["text", "date", "dropdown", "number", "age"])
        self.notnull_check = QCheckBox("Not Null")
        self.default_edit = QLineEdit()
        # Für Dropdown-Optionen: ein read-only Feld plus Button
        self.options_edit = QLineEdit()
        self.options_edit.setReadOnly(True)
        self.options_btn = QPushButton("Bearbeiten...")
        options_layout = QHBoxLayout()
        options_layout.addWidget(self.options_edit)
        options_layout.addWidget(self.options_btn)

        layout.addRow("Name:", self.name_edit)
        layout.addRow("Label:", self.label_edit)
        layout.addRow("Type:", self.type_combo)
        layout.addRow("", self.notnull_check)
        layout.addRow("Default:", self.default_edit)
        layout.addRow("Options:", options_layout)

        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Abbrechen")
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)

        ok_btn.clicked.connect(self.check_and_accept)
        cancel_btn.clicked.connect(self.reject)
        self.options_btn.clicked.connect(self.edit_options)

        if self.attr:
            self.name_edit.setText(self.attr.get("name", ""))
            self.label_edit.setText(self.attr.get("label", ""))
            self.type_combo.setCurrentText(self.attr.get("type", "text"))
            self.notnull_check.setChecked(self.attr.get("not_null", False))
            self.default_edit.setText(str(self.attr.get("default", "")))
            if self.attr.get("type") == "dropdown":
                opts = self.attr.get("options", [])
                self.options_edit.setText(", ".join(opts))
            else:
                self.options_edit.setText("")
        else:
            self.options_edit.setText("")

    def check_and_accept(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Fehler", "Der Attributname darf nicht leer sein!")
            return
        self.accept()

    def edit_options(self):
        current_options = []
        if self.options_edit.text():
            current_options = [o.strip() for o in self.options_edit.text().split(",") if o.strip()]
        dlg = DropdownOptionsDialog(current_options, self)
        if dlg.exec_() == QDialog.Accepted:
            opts = dlg.get_options()
            self.options_edit.setText(", ".join(opts))

    def get_data(self):
        data = {
            "name": self.name_edit.text().strip(),
            "label": self.label_edit.text().strip(),
            "type": self.type_combo.currentText(),
            "not_null": self.notnull_check.isChecked()
        }
        default = self.default_edit.text().strip()
        if default:
            data["default"] = default
        if self.type_combo.currentText() == "dropdown":
            opts_str = self.options_edit.text().strip()
            if opts_str:
                data["options"] = [o.strip() for o in opts_str.split(",") if o.strip()]
        return data


# -----------------------------
# Global Settings Widget
# -----------------------------
class GlobalSettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)
        self.password_edit = QLineEdit()
        self.dbname_edit = QLineEdit()
        self.window_width_spin = QSpinBox()
        self.window_height_spin = QSpinBox()
        self.font_size_spin = QSpinBox()
        self.button_width_spin = QSpinBox()
        self.button_height_spin = QSpinBox()
        self.input_field_height_spin = QSpinBox()

        self.window_width_spin.setRange(800, 5000)
        self.window_height_spin.setRange(600, 5000)
        self.font_size_spin.setRange(8, 30)
        self.button_width_spin.setRange(50, 500)
        self.button_height_spin.setRange(20, 200)
        self.input_field_height_spin.setRange(20, 100)

        self.password_edit.setText("geheim123")
        self.dbname_edit.setText("people.db")
        self.window_width_spin.setValue(1400)
        self.window_height_spin.setValue(900)
        self.font_size_spin.setValue(14)
        self.button_width_spin.setValue(150)
        self.button_height_spin.setValue(50)
        self.input_field_height_spin.setValue(40)

        layout.addRow("Passwort:", self.password_edit)
        layout.addRow("DB Name:", self.dbname_edit)
        layout.addRow("Fensterbreite:", self.window_width_spin)
        layout.addRow("Fensterhöhe:", self.window_height_spin)
        layout.addRow("Schriftgröße:", self.font_size_spin)
        layout.addRow("Button Breite:", self.button_width_spin)
        layout.addRow("Button Höhe:", self.button_height_spin)
        layout.addRow("Input Feld Höhe:", self.input_field_height_spin)

    def get_data(self):
        return {
            "password": self.password_edit.text().strip(),
            "db_name": self.dbname_edit.text().strip(),
            "ui": {
                "window_width": self.window_width_spin.value(),
                "window_height": self.window_height_spin.value(),
                "font_size": self.font_size_spin.value(),
                "button_width": self.button_width_spin.value(),
                "button_height": self.button_height_spin.value(),
                "input_field_height": self.input_field_height_spin.value()
            }
        }

    def set_data(self, data):
        self.password_edit.setText(data.get("password", ""))
        self.dbname_edit.setText(data.get("db_name", ""))
        ui = data.get("ui", {})
        self.window_width_spin.setValue(ui.get("window_width", 1400))
        self.window_height_spin.setValue(ui.get("window_height", 900))
        self.font_size_spin.setValue(ui.get("font_size", 14))
        self.button_width_spin.setValue(ui.get("button_width", 150))
        self.button_height_spin.setValue(ui.get("button_height", 50))
        self.input_field_height_spin.setValue(ui.get("input_field_height", 40))


# -----------------------------
# Tables Config Widget
# -----------------------------
class TablesConfigWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        self.tables_list = QListWidget()
        top_layout.addWidget(self.tables_list)
        btn_layout = QVBoxLayout()
        self.add_table_btn = QPushButton("Tabelle hinzufügen")
        self.del_table_btn = QPushButton("Tabelle löschen")
        btn_layout.addWidget(self.add_table_btn)
        btn_layout.addWidget(self.del_table_btn)
        top_layout.addLayout(btn_layout)
        main_layout.addLayout(top_layout)

        self.attr_table = QTableWidget(0, 6)
        self.attr_table.setHorizontalHeaderLabels(["Name", "Label", "Type", "Not Null", "Default", "Options"])
        self.attr_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.attr_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        main_layout.addWidget(self.attr_table)

        attr_btn_layout = QHBoxLayout()
        self.add_attr_btn = QPushButton("Attribut hinzufügen")
        self.edit_attr_btn = QPushButton("Attribut bearbeiten")
        self.del_attr_btn = QPushButton("Attribut löschen")
        attr_btn_layout.addWidget(self.add_attr_btn)
        attr_btn_layout.addWidget(self.edit_attr_btn)
        attr_btn_layout.addWidget(self.del_attr_btn)
        main_layout.addLayout(attr_btn_layout)

        self.tables = {}

        self.add_table_btn.clicked.connect(self.add_table)
        self.del_table_btn.clicked.connect(self.del_table)
        self.tables_list.currentItemChanged.connect(self.load_table_attributes)
        self.add_attr_btn.clicked.connect(self.add_attribute)
        self.edit_attr_btn.clicked.connect(self.edit_attribute)
        self.del_attr_btn.clicked.connect(self.del_attribute)

    def add_table(self):
        table_name, ok = QInputDialog.getText(self, "Tabelle hinzufügen", "Tabelle Name:")
        if ok and table_name.strip():
            table_name = table_name.strip()
            if not table_name[0].isalpha():
                QMessageBox.warning(self, "Fehler", "Tabellenname muss mit einem Buchstaben beginnen!")
                return
            if table_name in self.tables:
                QMessageBox.warning(self, "Fehler", "Diese Tabelle existiert bereits!")
                return
            self.tables[table_name] = []
            self.tables_list.addItem(table_name)

    def del_table(self):
        current = self.tables_list.currentItem()
        if current:
            table_name = current.text()
            del self.tables[table_name]
            self.tables_list.takeItem(self.tables_list.row(current))
            self.attr_table.setRowCount(0)

    def load_table_attributes(self, current, previous):
        self.attr_table.setRowCount(0)
        if current:
            table_name = current.text()
            attributes = self.tables.get(table_name, [])
            for attr in attributes:
                row = self.attr_table.rowCount()
                self.attr_table.insertRow(row)
                self.attr_table.setItem(row, 0, QTableWidgetItem(attr.get("name", "")))
                self.attr_table.setItem(row, 1, QTableWidgetItem(attr.get("label", "")))
                self.attr_table.setItem(row, 2, QTableWidgetItem(attr.get("type", "")))
                self.attr_table.setItem(row, 3, QTableWidgetItem("Ja" if attr.get("not_null", False) else "Nein"))
                self.attr_table.setItem(row, 4, QTableWidgetItem(str(attr.get("default", ""))))
                self.attr_table.setItem(row, 5, QTableWidgetItem(
                    ", ".join(attr.get("options", [])) if "options" in attr else ""))

    def add_attribute(self):
        current = self.tables_list.currentItem()
        if not current:
            QMessageBox.warning(self, "Fehler", "Bitte zuerst eine Tabelle auswählen!")
            return
        dlg = AttributeDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            attr = dlg.get_data()
            if not attr.get("name"):
                QMessageBox.warning(self, "Fehler", "Attributname darf nicht leer sein!")
                return
            table_name = current.text()
            self.tables[table_name].append(attr)
            self.load_table_attributes(current, None)

    def edit_attribute(self):
        current = self.tables_list.currentItem()
        if not current:
            QMessageBox.warning(self, "Fehler", "Bitte zuerst eine Tabelle auswählen!")
            return
        selected = self.attr_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Fehler", "Bitte zuerst ein Attribut auswählen!")
            return
        table_name = current.text()
        attr = self.tables[table_name][selected]
        dlg = AttributeDialog(self, attr)
        if dlg.exec_() == QDialog.Accepted:
            self.tables[table_name][selected] = dlg.get_data()
            self.load_table_attributes(current, None)

    def del_attribute(self):
        current = self.tables_list.currentItem()
        if not current:
            QMessageBox.warning(self, "Fehler", "Bitte zuerst eine Tabelle auswählen!")
            return
        selected = self.attr_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Fehler", "Bitte zuerst ein Attribut auswählen!")
            return
        table_name = current.text()
        del self.tables[table_name][selected]
        self.load_table_attributes(current, None)

    def get_data(self):
        return self.tables


# -----------------------------
# ConfigEditor: Hauptfenster für den Konfigurationseditor
# Lädt beim Start die Konfiguration aus "config.text" (falls vorhanden),
# andernfalls wird der Standard verwendet.
# Beim Speichern wird die aktuelle Konfiguration in "config.text" geschrieben.
# -----------------------------
class ConfigEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konfigurationseditor")
        self.resize(800, 600)
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.tabs = QTabWidget()
        self.global_widget = GlobalSettingsWidget()
        self.tables_widget = TablesConfigWidget()
        self.tabs.addTab(self.global_widget, "Global Settings")
        self.tabs.addTab(self.tables_widget, "Tables Config")
        layout.addWidget(self.tabs)

        self.save_btn = QPushButton("Speichern")
        self.save_btn.clicked.connect(self.save_config)
        layout.addWidget(self.save_btn)

        self.output_edit = QPlainTextEdit()
        self.output_edit.setReadOnly(True)
        layout.addWidget(self.output_edit)

        self.config_file = "config.text"
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                content = f.read()
            if content.strip():
                config = json.loads(content)
            else:
                config = DEFAULT_CONFIG
        except Exception as e:
            config = DEFAULT_CONFIG

        # Update GlobalSettingsWidget
        self.global_widget.set_data(config)
        # Update TablesConfigWidget
        tables = config.get("tables", {})
        self.tables_widget.tables = tables
        self.tables_widget.tables_list.clear()
        for table_name in tables.keys():
            self.tables_widget.tables_list.addItem(table_name)
        if self.tables_widget.tables_list.count() > 0:
            self.tables_widget.tables_list.setCurrentRow(0)
        # Zeige die geladene Konfiguration im Textfeld
        json_text = json.dumps(config, indent=4, ensure_ascii=False)
        self.output_edit.setPlainText(json_text)

    def save_config(self):
        config = {}
        config.update(self.global_widget.get_data())
        config["tables"] = self.tables_widget.get_data()
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Erfolg", "Konfiguration erfolgreich gespeichert!")
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler beim Speichern: {str(e)}")
        # Aktualisiere die Ausgabe
        json_text = json.dumps(config, indent=4, ensure_ascii=False)
        self.output_edit.setPlainText(json_text)


# -----------------------------
# Hauptprogramm
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = ConfigEditor()
    editor.show()
    sys.exit(app.exec_())
