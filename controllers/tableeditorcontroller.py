import contextlib
import os
import shutil
import sys
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import QObject, Qt
from docxtpl import DocxTemplate
from docx2pdf import convert
from model.databasemodel import DatabaseModel
from model.tabledatamodel import TableDataModel

class TableEditorController(QObject):
    def __init__(self, view, table_name, attributes, attributes_without, db, config, main_window):
        super().__init__()
        self.view = view
        self.table_name = table_name
        self.attributes = attributes
        self.attributes_without = attributes_without
        self.db = db
        self.config = config
        self.main_window = main_window
        self.selected_record_id = None
        self.search_mode = "string"
        self.setup_model()
        self.connect_signals()

    def setup_model(self):
        # Erstelle die Tabelle (inklusive "adddate") falls noch nicht vorhanden.
        DatabaseModel(self.config).create_table(self.table_name, self.attributes_without)
        self.model = TableDataModel(self.attributes_without, self.view, self.db)
        self.model.setTable(self.table_name)
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.select()
        self.view.table_view.setModel(self.model)

    def connect_signals(self):
        self.view.search_input.textChanged.connect(self.search)
        if hasattr(self.view, 'date_from'):
            self.view.date_from.dateChanged.connect(self.search)
        if hasattr(self.view, 'date_to'):
            self.view.date_to.dateChanged.connect(self.search)
        self.view.string_search_button.clicked.connect(self.set_string_mode)
        if hasattr(self.view, 'date_search_button'):
            self.view.date_search_button.clicked.connect(self.set_date_mode)
        self.view.add_button.clicked.connect(self.add_entry)
        self.view.update_button.clicked.connect(self.update_entry)
        self.view.delete_button.clicked.connect(self.delete_entry)
        self.view.print_button.clicked.connect(self.print_record)
        self.view.back_button.clicked.connect(self.go_back)
        self.view.table_view.clicked.connect(self.load_selected_record)

    def set_string_mode(self):
        self.search_mode = "string"
        self.search()

    def set_date_mode(self):
        self.search_mode = "date"
        self.search()

    def search(self):
        if self.search_mode == "string":
            free_text = self.view.search_input.text().strip().replace("'", "''")
            if free_text:
                conditions = [f'"{attr["name"]}" LIKE \'%{free_text}%\'' for attr in self.attributes_without]
                final_filter = "(" + " OR ".join(conditions) + ")"
            else:
                final_filter = ""
        elif self.search_mode == "date" and hasattr(self.view, 'date_from') and hasattr(self.view, 'date_to'):
            date_from_str = self.view.date_from.date().toString("yyyy-MM-dd")
            date_to_str = self.view.date_to.date().toString("yyyy-MM-dd")
            conditions = [f'("{attr["name"]}" >= \'{date_from_str}\' AND "{attr["name"]}" <= \'{date_to_str}\')'
                          for attr in self.attributes if attr["type"] == "date"]
            final_filter = "(" + " OR ".join(conditions) + ")" if conditions else ""
        else:
            final_filter = ""
        self.model.setFilter(final_filter)
        self.model.select()

    def load_selected_record(self, index):
        row = index.row()
        record = self.model.record(row)
        self.selected_record_id = record.value("id")
        record_data = {attr["name"]: (record.value(attr["name"]) or "") for attr in self.attributes_without}
        self.view.set_input_values(record_data)
        self.view.add_button.setVisible(False)
        self.view.update_button.setVisible(True)
        self.view.delete_button.setVisible(True)

    def add_entry(self):
        record = self.model.record()
        data = self.view.get_input_values()
        # Fülle alle Eingabefelder in den neuen Datensatz
        for attr in self.attributes_without:
            value = data.get(attr["name"], "")
            if not value and "default" in attr:
                value = attr["default"]
            if attr.get("not_null", False) and not value:
                QMessageBox.warning(self.view, "خطأ", f"حقل {attr['label']} لا يمكن أن يكون فارغاً!")
                return
            record.setValue(attr["name"], value)
        # Setze automatisch die adddate-Spalte mit dem aktuellen Datum
        record.setValue("adddate", datetime.now().strftime("%Y-%m-%d"))
        if not self.model.insertRecord(-1, record):
            QMessageBox.critical(self.view, "خطأ", "لم يتم إضافة السجل!")
        elif self.model.submitAll():
            self.model.select()
            self.view.clear_inputs()
        else:
            QMessageBox.critical(self.view, "خطأ", "خطأ أثناء الحفظ!")

    def update_entry(self):
        if self.selected_record_id is None:
            return
        row_to_update = -1
        for row in range(self.model.rowCount()):
            if self.model.record(row).value("id") == self.selected_record_id:
                row_to_update = row
                break
        if row_to_update == -1:
            QMessageBox.warning(self.view, "خطأ", "لم يتم العثور على السجل!")
            return
        data = self.view.get_input_values()
        for attr in self.attributes_without:
            value = data.get(attr["name"], "")
            if not value and "default" in attr:
                value = attr["default"]
            if attr.get("not_null", False) and not value:
                QMessageBox.warning(self.view, "خطأ", f"حقل {attr['label']} لا يمكن أن يكون فارغاً!")
                return
            self.model.setData(self.model.index(row_to_update, self.model.fieldIndex(attr["name"])), value)
        # Beim Update bleibt "adddate" unverändert.
        if not self.model.submitAll():
            QMessageBox.critical(self.view, "خطأ", "لم يتم تحديث السجل!")
        else:
            self.model.select()
            self.view.clear_inputs()

    def delete_entry(self):
        if self.selected_record_id is None:
            return
        confirmation = QMessageBox.question(
            self.view, "تأكيد الحذف", "هل تريد حقاً حذف هذا السجل؟",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if confirmation == QMessageBox.Yes:
            row_to_delete = -1
            for row in range(self.model.rowCount()):
                if self.model.record(row).value("id") == self.selected_record_id:
                    row_to_delete = row
                    break
            if row_to_delete == -1:
                QMessageBox.warning(self.view, "خطأ", "لم يتم العثور على السجل!")
                return
            if not self.model.removeRow(row_to_delete):
                QMessageBox.critical(self.view, "خطأ", "لم يتم حذف السجل!")
            elif self.model.submitAll():
                self.model.select()
                self.view.clear_inputs()
            else:
                QMessageBox.critical(self.view, "خطأ", "خطأ أثناء الحذف!")

    def print_record(self):
        if self.selected_record_id is None:
            QMessageBox.warning(self.view, "خطأ", "يرجى اختيار سجل أولاً!")
            return

        context = self.view.get_input_values()

        # Heutiges Datum im gewünschten Format
        heutiges_datum = datetime.today().strftime('%d-%m-%Y')
        # Füge es dem Dictionary hinzu
        context['datum'] = heutiges_datum

        template_path = os.path.join("vorlagen", f"{self.view.print_dropdown.currentText()}.docx")
        if not os.path.exists(template_path):
            QMessageBox.warning(self.view, "خطأ", f"لم يتم العثور على القالب: {template_path}")
            return

        try:
            # Dokument laden, Kontext einfügen und temporäres Docx erzeugen
            doc = DocxTemplate(template_path)
            doc.render(context)
            temp_docx = "temp_filled.docx"
            doc.save(temp_docx)

            temp_pdf = "temp_filled.pdf"

            # Sicherstellen, dass stdout und stderr nicht None sind (wichtig im windowed Modus)
            if sys.stdout is None:
                sys.stdout = open(os.devnull, 'w')
            if sys.stderr is None:
                sys.stderr = open(os.devnull, 'w')

            # stdout und stderr temporär in os.devnull umleiten, um Ausgaben von docx2pdf zu unterdrücken
            with open(os.devnull, 'w') as fnull:
                with contextlib.redirect_stdout(fnull), contextlib.redirect_stderr(fnull):
                    convert(temp_docx, temp_pdf)

            # PDF-Speicher-Dialog
            save_path, _ = QFileDialog.getSaveFileName(self.view, "احفظ ملف PDF", "", "PDF Dateien (*.pdf)")
            if save_path:
                shutil.copyfile(temp_pdf, save_path)
                QMessageBox.information(self.view, "نجاح", f"تم حفظ ملف PDF بنجاح في:\n{save_path}")

            # Temporäre Dateien entfernen
            if os.path.exists(temp_docx):
                os.remove(temp_docx)
            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)
        except Exception as e:
            QMessageBox.critical(self.view, "خطأ", f"خطأ أثناء الطباعة:\n{str(e)}")
    def go_back(self):
        self.main_window.go_to_main_menu()
