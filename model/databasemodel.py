import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QTableView, QLabel, QMessageBox,
    QComboBox, QDateEdit, QSpinBox, QHeaderView, QStackedWidget
)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5.QtCore import Qt, QDate, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QFontMetrics

from openconfig import openconfig

# ================================================================
# Konfiguration laden
# ================================================================

GENERATOR_CONFIG = openconfig()


def get_sql_type(attr_type):
    if attr_type == "number":
        return "INTEGER"
    return "TEXT"


# =============================================================================
# MODEL
# =============================================================================

class DatabaseModel:
    """Kapselt die Datenbankverbindung und stellt Methoden zur Tabellenerstellung bereit."""
    def __init__(self, config):
        self.config = config
        self.db = self.setup_db()

    def setup_db(self):
        connection_name = "default"
        if QSqlDatabase.contains(connection_name):
            db = QSqlDatabase.database(connection_name)
        else:
            db = QSqlDatabase.addDatabase("QSQLITE", connection_name)
            db.setDatabaseName(self.config["db_name"])
            if not db.open():
                QMessageBox.critical(None, "خطأ في قاعدة البيانات", db.lastError().text())
                sys.exit(1)
        return db

    def create_table(self, table_name, attributes):
        query = QSqlQuery(self.db)
        column_defs = []
        for attr in attributes:
            sql_type = get_sql_type(attr["type"])
            col_def = f'"{attr["name"]}" {sql_type}'
            if attr.get("not_null", False):
                col_def += " NOT NULL"
            if "default" in attr:
                default_val = attr["default"]
                if attr["type"] == "number":
                    col_def += f" DEFAULT {default_val}"
                else:
                    col_def += f" DEFAULT '{default_val}'"
            column_defs.append(col_def)
        columns_sql = ", ".join(column_defs)
        sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {columns_sql}
        )
        """
        if not query.exec(sql):
            QMessageBox.critical(None, "خطأ في قاعدة البيانات",
                                 f"خطأ أثناء إنشاء الجدول {table_name}:\n{query.lastError().text()}")
            sys.exit(1)

