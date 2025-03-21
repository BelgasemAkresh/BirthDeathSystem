
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import Qt

class TableDataModel(QSqlTableModel):
    """Erweitert QSqlTableModel, um arabische Überschriften anzuzeigen."""
    def __init__(self, attributes, parent=None, db=None):
        super().__init__(parent, db)
        self.attributes = attributes

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return "id"
            try:
                return self.attributes[section - 1]["label"]
            except IndexError:
                return super().headerData(section, orientation, role)
        return super().headerData(section, orientation, role)

