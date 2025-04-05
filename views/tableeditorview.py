import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QLabel, QComboBox, QDateEdit, QSpinBox, QFrame, QSizePolicy
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

        # Beispiel: Vorhandene Suchzeile und Datumssuche etc. – belassen wie gehabt
        # -----------------------------------------------------
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

        # Beispiel: Deine Tabelle
        # -----------------------------------------------------
        self.table_view = ProportionalTableView()
        layout.addWidget(self.table_view)

        # Ab hier: Dynamische Gruppierung der Attribute
        # -----------------------------------------------------
        # Neue Layout-Logik für dynamische Gruppen
        self.input_widgets = {}

        # Gruppiere die Attribute nach "breakline"
        groups = []
        current_group = []
        add_line_after_group = False
        print_labels = []

        for attr in self.attributes:
            if attr["name"] == "breakline":
                if attr.get("label") == "print":
                    print_labels = attr.get("options", [])
                elif current_group:
                    groups.append((current_group, add_line_after_group))
                    current_group = []
                    add_line_after_group = False
                elif attr.get("label") == "line":
                    add_line_after_group = True
            else:
                current_group.append(attr)
        if current_group :
            groups.append((current_group, add_line_after_group))

        if print_labels == []:
            print_labels.append(self.table_name)


        # Analyse: maximale Felder pro Reihe bestimmen
        max_fields_in_row = 0
        for group_attrs, _ in groups:
            group_size = len(group_attrs)
            if group_size <= 2:
                fields_per_row = group_size
            elif group_size <= 6:
                fields_per_row = 3
            else:
                fields_per_row = 4
            max_fields_in_row = max(max_fields_in_row, fields_per_row)

        total_columns = max_fields_in_row * 2  # Label + Input je Feld

        # Hauptlayout für die Input-Felder
        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(10)

        current_row = 0
        for group_attrs, add_line in groups:
            group_size = len(group_attrs)
            if group_size <= 2:
                fields_per_row = group_size
            elif group_size <= 6:
                fields_per_row = 3
            else:
                fields_per_row = 4

            col = 0
            for index, attr in enumerate(group_attrs):
                if index > 0 and index % fields_per_row == 0:
                    current_row += 1
                    col = 0

                label = QLabel(attr["label"] + ":")
                label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

                widget = self.create_input_widget(attr)
                self.input_widgets[attr["name"]] = widget

                form_layout.addWidget(label, current_row, col)
                form_layout.addWidget(widget, current_row, col + 1)
                col += 2

            current_row += 1  # nächste Gruppe fängt in neuer Zeile an

            if add_line:
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                form_layout.addWidget(line, current_row, 0, 1, total_columns)
                current_row += 1

        # Stretch: Eingabe-Spalten dehnbar, Labels fix
        for i in range(total_columns):
            if i % 2 == 0:
                form_layout.setColumnStretch(i, 0)
            else:
                form_layout.setColumnStretch(i, 1)

        # Pack das alles in ein VBoxLayout und hänge es ans Hauptlayout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        layout.addLayout(main_layout)

        # Beispiel: Buttons darunter (wie gehabt)
        # -----------------------------------------------------
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

        # Dropdown neben print_button
        self.print_dropdown = QComboBox()
        self.print_dropdown.setFixedHeight(self.config["ui"]["button_height"])  # Höhe passend zu Buttons
        self.print_dropdown.addItems(print_labels)
        btn_layout.addWidget(self.print_dropdown)

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
            # Fallback: einfaches QLineEdit
            widget = QLineEdit()

        widget.setMinimumHeight(self.config["ui"]["input_field_height"])
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Default-Werte setzen
        if "default" in attr:
            if attr_type == "date":
                date_val = QDate.fromString(attr["default"], "yyyy-MM-dd")
                if date_val.isValid():
                    widget.setDate(date_val)
            elif attr_type == "number":
                try:
                    widget.setValue(int(attr["default"]))
                except ValueError:
                    pass
            elif attr_type == "dropdown":
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

