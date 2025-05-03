import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QLabel, QComboBox, QDateEdit, QSpinBox, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QDate
from openconfig import openconfig
from views.proportionaltableview import ProportionalTableView


class TableEditorView(QWidget):
    """
    Eine verbesserte View zur Bearbeitung von Tabellendaten mit besserer Anordnung der Eingabefelder.
    """

    def __init__(self, table_name, attributes, attributes_without, config):
        super().__init__()
        self.table_name = table_name
        self.attributes = attributes
        self.attributes_without = attributes_without
        self.config = config
        self.selected_record_id = None
        self.print_labels = [self.table_name]  # Initialisierung hier

        # UI Initialisierung
        self.setWindowTitle(f"تعديل {table_name}")
        self.setGeometry(100, 100, config["ui"]["window_width"], config["ui"]["window_height"])
        self.setLayoutDirection(Qt.RightToLeft)

        self.input_widgets = {}
        self.setup_ui()

    def setup_ui(self):
        """Erstellt die gesamte Benutzeroberfläche."""
        main_layout = QVBoxLayout(self)

        # Suchfunktionen
        self.setup_search_ui(main_layout)

        # Tabelle
        self.table_view = ProportionalTableView()
        main_layout.addWidget(self.table_view)

        # Eingabeformular
        self.setup_form_ui(main_layout)

        # Buttons
        self.setup_button_ui(main_layout)

    def setup_search_ui(self, layout):
        """Erstellt die Suchoberfläche."""
        # Textsuche
        text_search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث في جميع الحقول")
        self.search_input.setMinimumHeight(self.config["ui"]["input_field_height"])
        text_search_layout.addWidget(self.search_input)

        self.string_search_button = QPushButton("بحث نص")
        self.string_search_button.setMinimumSize(
            self.config["ui"]["button_width"],
            self.config["ui"]["button_height"]
        )
        text_search_layout.addWidget(self.string_search_button)
        layout.addLayout(text_search_layout)

        # Datumssuche (falls benötigt)
        if any(attr["type"] == "date" for attr in self.attributes_without):
            date_search_layout = QHBoxLayout()

            from_label = QLabel("من:")
            date_search_layout.addWidget(from_label)

            self.date_from = QDateEdit()
            self.date_from.setCalendarPopup(True)
            self.date_from.setDisplayFormat("yyyy-MM-dd")
            self.date_from.setDate(QDate(1900, 1, 1))
            self.date_from.setMinimumHeight(self.config["ui"]["input_field_height"])
            date_search_layout.addWidget(self.date_from)

            to_label = QLabel("الى:")
            date_search_layout.addWidget(to_label)

            self.date_to = QDateEdit()
            self.date_to.setCalendarPopup(True)
            self.date_to.setDisplayFormat("yyyy-MM-dd")
            self.date_to.setDate(QDate(2100, 12, 31))
            self.date_to.setMinimumHeight(self.config["ui"]["input_field_height"])
            date_search_layout.addWidget(self.date_to)

            date_search_layout.addStretch()

            self.date_search_button = QPushButton("بحث بتاريخ")
            self.date_search_button.setMinimumSize(
                self.config["ui"]["button_width"],
                self.config["ui"]["button_height"]
            )
            date_search_layout.addWidget(self.date_search_button)
            layout.addLayout(date_search_layout)

            self.string_search_button.setChecked(True)

        self.search_mode = "string"

    def setup_form_ui(self, layout):
        """Erstellt das dynamische Eingabeformular."""
        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(10)

        # Gruppierung der Attribute
        groups = []
        current_group = []

        for attr in self.attributes:
            if attr["name"] == "breakline":
                if attr.get("label") == "print":
                    self.print_labels = attr.get("options", [self.table_name])
                elif current_group:
                    groups.append(current_group)
                    current_group = []
            else:
                current_group.append(attr)

        if current_group:
            groups.append(current_group)

        # Formular aufbauen
        current_row = 0
        for group in groups:
            # Maximal 3 Felder pro Zeile
            for i in range(0, len(group), 3):
                row_attrs = group[i:i + 3]

                for col, attr in enumerate(row_attrs):
                    # Label und Eingabefeld erstellen
                    label = QLabel(attr["label"] + ":")
                    label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

                    widget = self.create_input_widget(attr)
                    self.input_widgets[attr["name"]] = widget

                    # Positionierung im Grid (2 Spalten pro Feld: Label + Widget)
                    form_layout.addWidget(label, current_row, col * 2)
                    form_layout.addWidget(widget, current_row, col * 2 + 1)

                current_row += 1

            # Horizontale Linie zwischen Gruppen
            if group != groups[-1]:
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                form_layout.addWidget(line, current_row, 0, 1, 6)  # 6 Spalten (3 Felder * 2)
                current_row += 1

        # Layout-Einstellungen
        for i in range(6):  # 3 Felder * 2 Spalten
            form_layout.setColumnStretch(i, 1 if i % 2 else 0)

        layout.addLayout(form_layout)

    def setup_button_ui(self, layout):
        """Erstellt die Button-Leiste."""
        btn_layout = QHBoxLayout()

        # Aktion-Buttons
        self.add_button = QPushButton("إضافة")
        self.add_button.setMinimumSize(
            self.config["ui"]["button_width"],
            self.config["ui"]["button_height"]
        )
        btn_layout.addWidget(self.add_button)

        self.update_button = QPushButton("تحديث")
        self.update_button.setMinimumSize(
            self.config["ui"]["button_width"],
            self.config["ui"]["button_height"]
        )
        self.update_button.setVisible(False)
        btn_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("حذف")
        self.delete_button.setMinimumSize(
            self.config["ui"]["button_width"],
            self.config["ui"]["button_height"]
        )
        self.delete_button.setVisible(False)
        btn_layout.addWidget(self.delete_button)

        # Drucken-Button mit Auswahl
        self.print_button = QPushButton("طباعة")
        self.print_button.setMinimumSize(
            self.config["ui"]["button_width"],
            self.config["ui"]["button_height"]
        )
        btn_layout.addWidget(self.print_button)

        self.print_dropdown = QComboBox()
        self.print_dropdown.setFixedHeight(self.config["ui"]["button_height"])
        self.print_dropdown.addItems(self.print_labels)  # Hier wird self.print_labels verwendet
        btn_layout.addWidget(self.print_dropdown)

        # Zurück-Button
        self.back_button = QPushButton("عودة")
        self.back_button.setMinimumSize(
            self.config["ui"]["button_width"],
            self.config["ui"]["button_height"]
        )
        btn_layout.addWidget(self.back_button)

        layout.addLayout(btn_layout)

    # Die restlichen Methoden bleiben unverändert wie in der vorherigen Version
    def create_input_widget(self, attr):
        """Erstellt das passende Eingabewidget für den Attributtyp."""
        attr_type = attr["type"]
        widget = None

        if attr_type == "text":
            widget = QLineEdit()
        elif attr_type == "date":
            widget = QDateEdit()
            widget.setCalendarPopup(True)
            widget.setDisplayFormat("yyyy-MM-dd")
            widget.setDate(QDate.currentDate())
        elif attr_type == "dropdown":
            widget = QComboBox()
            widget.addItems(attr.get("options", []))
        elif attr_type == "number":
            widget = QSpinBox()
            widget.setMinimum(0)
            widget.setMaximum(1000000)
        else:
            widget = QLineEdit()  # Fallback

        # Gemeinsame Eigenschaften
        widget.setMinimumHeight(self.config["ui"]["input_field_height"])
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Standardwert setzen
        if "default" in attr:
            self.set_widget_value(widget, attr_type, attr["default"])

        return widget

    def set_widget_value(self, widget, attr_type, value):
        """Setzt den Wert eines Widgets basierend auf seinem Typ."""
        if attr_type == "text":
            widget.setText(value)
        elif attr_type == "date":
            date = QDate.fromString(value, "yyyy-MM-dd")
            if date.isValid():
                widget.setDate(date)
        elif attr_type == "dropdown":
            index = widget.findText(value)
            if index >= 0:
                widget.setCurrentIndex(index)
        elif attr_type == "number":
            try:
                widget.setValue(int(value))
            except ValueError:
                pass

    def get_input_values(self):
        """Gibt die aktuellen Eingabewerte als Dictionary zurück."""
        data = {}
        for attr in self.attributes_without:
            name = attr["name"]
            widget = self.input_widgets[name]
            attr_type = attr["type"]

            if attr_type == "text":
                data[name] = widget.text().strip()
            elif attr_type == "date":
                data[name] = widget.date().toString("yyyy-MM-dd")
            elif attr_type == "dropdown":
                data[name] = widget.currentText()
            elif attr_type == "number":
                data[name] = str(widget.value())
            else:
                data[name] = widget.text().strip()

        return data

    def set_input_values(self, record):
        """Setzt die Eingabewerte basierend auf einem Datensatz."""
        for attr in self.attributes_without:
            name = attr["name"]
            if name in record:
                widget = self.input_widgets[name]
                self.set_widget_value(widget, attr["type"], record[name])

    def clear_inputs(self):
        """Setzt alle Eingabefelder zurück."""
        for attr in self.attributes_without:
            name = attr["name"]
            widget = self.input_widgets[name]
            attr_type = attr["type"]

            if attr_type == "date":
                widget.setDate(QDate.currentDate())
            elif attr_type == "number":
                widget.setValue(0)
            elif attr_type == "dropdown":
                widget.setCurrentIndex(0 if widget.count() > 0 else -1)
            elif attr_type == "text":
                widget.setText(attr.get("default", ""))
            else:
                self.set_widget_value(widget, attr_type, attr.get("default", ""))

        self.selected_record_id = None
        self.add_button.setVisible(True)
        self.update_button.setVisible(False)
        self.delete_button.setVisible(False)
        self.table_view.clearSelection()
