import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QLabel, QComboBox, QDateEdit, QSpinBox, QFrame
)
from PyQt5.QtCore import Qt, QDate

from openconfig import openconfig
from views.proportionaltableview import ProportionalTableView

# ================================================================
# Konfiguration laden
# ================================================================

GENERATOR_CONFIG =  openconfig()

class TableEditorView(QWidget):
    """
    Die View für die Bearbeitung einer Tabelle. Sie stellt alle UI-Elemente bereit.
    """
    def __init__(self, table_name, attributes, attributes_without, config):
        super().__init__()
        self.table_name = table_name
        self.attributes = attributes
        self.attributes_without = attributes_without
        self.config = config
        self.selected_record_id = None
        self.setWindowTitle(f"تعديل {table_name}")
        self.setGeometry(100, 100, config["ui"]["window_width"], config["ui"]["window_height"])
        self.setLayoutDirection(Qt.RightToLeft)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Suchleiste: Freies Suchfeld + "بحث نص"-Button
        text_search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث في جميع الحقول")
        self.search_input.setMinimumHeight(self.config["ui"]["input_field_height"])
        text_search_layout.addWidget(self.search_input)
        self.string_search_button = QPushButton("بحث نص")
        self.string_search_button.setMinimumSize(self.config["ui"]["button_width"], self.config["ui"]["button_height"])
        text_search_layout.addWidget(self.string_search_button)
        layout.addLayout(text_search_layout)

        # Datumssuche, falls erforderlich
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
            self.date_search_button.setMinimumSize(self.config["ui"]["button_width"], self.config["ui"]["button_height"])
            date_search_layout.addWidget(self.date_search_button)
            layout.addLayout(date_search_layout)
            self.string_search_button.setChecked(True)
        self.search_mode = "string"

        # Tabelle
        self.table_view = ProportionalTableView()
        layout.addWidget(self.table_view)

        self.input_widgets = {}
        main_layout = QVBoxLayout()  # Hauptlayout für alle Zeilen
        current_row_layout = QHBoxLayout()  # Layout der aktuellen Zeile

        for attr in self.attributes:
            if attr["name"] == "breakline":
                # Zeilenumbruch: Aktuelle Zeile abschließen
                current_row_layout.addStretch(1)
                main_layout.addLayout(current_row_layout)
                # Falls das Breakline-Attribut als Trennlinie markiert ist (label == "line"),
                # wird eine horizontale Trennlinie eingefügt.
                if attr["label"] == "line":
                    divider = QFrame()
                    divider.setFrameShape(QFrame.HLine)
                    divider.setFrameShadow(QFrame.Sunken)
                    main_layout.addWidget(divider)
                # Starte eine neue Zeile
                current_row_layout = QHBoxLayout()
                continue

            label = QLabel(attr["label"] + ":")
            widget = self.create_input_widget(attr)
            self.input_widgets[attr["name"]] = widget

            current_row_layout.addWidget(label)
            current_row_layout.addWidget(widget)

        # Falls noch Widgets in der letzten Zeile vorhanden sind, diese hinzufügen.
        if current_row_layout.count() > 0:
            current_row_layout.addStretch(1)
            main_layout.addLayout(current_row_layout)

        layout.addLayout(main_layout)

        # Button-Leiste: Hinzufügen, Aktualisieren, Löschen, Drucken und Zurück
        btn_layout = QHBoxLayout()
        self.add_button = QPushButton("إضافة")
        self.add_button.setMinimumSize(self.config["ui"]["button_width"], self.config["ui"]["button_height"])
        btn_layout.addWidget(self.add_button)
        self.update_button = QPushButton("تحديث")
        self.update_button.setMinimumSize(self.config["ui"]["button_width"], self.config["ui"]["button_height"])
        self.update_button.setVisible(False)
        btn_layout.addWidget(self.update_button)
        self.delete_button = QPushButton("حذف")
        self.delete_button.setMinimumSize(self.config["ui"]["button_width"], self.config["ui"]["button_height"])
        self.delete_button.setVisible(False)
        btn_layout.addWidget(self.delete_button)
        self.print_button = QPushButton("طباعة")
        self.print_button.setMinimumSize(self.config["ui"]["button_width"], self.config["ui"]["button_height"])
        btn_layout.addWidget(self.print_button)
        self.back_button = QPushButton("عودة")
        self.back_button.setMinimumSize(self.config["ui"]["button_width"], self.config["ui"]["button_height"])
        btn_layout.addWidget(self.back_button)
        layout.addLayout(btn_layout)

    def create_input_widget(self, attr):
        attr_type = attr["type"]
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
            widget = QLineEdit()
        widget.setMinimumHeight(self.config["ui"]["input_field_height"])
        if "default" in attr:
            if attr["type"] == "date":
                date_val = QDate.fromString(attr["default"], "yyyy-MM-dd")
                if date_val.isValid():
                    widget.setDate(date_val)
            elif attr["type"] == "number":
                try:
                    widget.setValue(int(attr["default"]))
                except ValueError:
                    pass
            elif attr["type"] == "dropdown":
                index = widget.findText(attr["default"])
                widget.setCurrentIndex(index if index >= 0 else 0)
            else:
                widget.setText(attr["default"])
        return widget

    def get_input_values(self):
        data = {}
        for attr in self.attributes_without:
            name = attr["name"]
            widget = self.input_widgets[name]
            if attr["type"] == "text":
                data[name] = widget.text().strip()
            elif attr["type"] == "date":
                data[name] = widget.date().toString("yyyy-MM-dd")
            elif attr["type"] == "dropdown":
                data[name] = widget.currentText()
            elif attr["type"] == "number":
                data[name] = str(widget.value())
            else:
                data[name] = widget.text().strip()
        return data

    def set_input_values(self, record):
        for attr in self.attributes_without:
            name = attr["name"]
            widget = self.input_widgets[name]
            value = record.get(name, "")
            if attr["type"] == "text":
                widget.setText(value)
            elif attr["type"] == "date":
                date = QDate.fromString(value, "yyyy-MM-dd")
                widget.setDate(date if date.isValid() else QDate.currentDate())
            elif attr["type"] == "dropdown":
                index = widget.findText(value)
                widget.setCurrentIndex(index if index >= 0 else 0)
            elif attr["type"] == "number":
                try:
                    widget.setValue(int(value))
                except ValueError:
                    widget.setValue(0)
            else:
                widget.setText(value)

    def clear_inputs(self):
        for attr in self.attributes_without:
            widget = self.input_widgets[attr["name"]]
            if attr["type"] == "text":
                widget.clear()
            elif attr["type"] == "date":
                widget.setDate(QDate.currentDate())
            elif attr["type"] == "dropdown":
                widget.setCurrentIndex(0)
            elif attr["type"] == "number":
                widget.setValue(0)
            else:
                widget.clear()
        self.selected_record_id = None
        self.add_button.setVisible(True)
        self.update_button.setVisible(False)
        self.delete_button.setVisible(False)
        self.table_view.clearSelection()

