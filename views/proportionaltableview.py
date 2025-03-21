from PyQt5.QtWidgets import (
    QTableView, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics


class ProportionalTableView(QTableView):
    """
    QTableView, die manuell angepasste Spaltenbreiten speichert
    und bei Fenstergrößenänderung automatisch skaliert.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalHeader().setStretchLastSection(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.manual_widths = {}  # Speichert manuell veränderte Spaltenbreiten
        self.auto_scaling = False
        self.horizontalHeader().sectionResized.connect(self.on_section_resized)

    def on_section_resized(self, logicalIndex, oldSize, newSize):
        if not self.auto_scaling:
            self.manual_widths[logicalIndex] = newSize

    def resizeEvent(self, event):
        super().resizeEvent(event)
        model = self.model()
        if not model or model.columnCount() == 0:
            return
        total_available = self.viewport().width()
        font_metrics = QFontMetrics(self.horizontalHeader().font())
        num_columns = model.columnCount()

        # Berechne "natürliche" Breiten der Spalten (Headertext-Breite + Puffer)
        natural_widths = []
        for col in range(num_columns):
            header_text = model.headerData(col, Qt.Horizontal, Qt.DisplayRole) or ""
            natural = font_metrics.horizontalAdvance(str(header_text)) + 20
            natural_widths.append(natural)

        manual_sum = sum(self.manual_widths.get(col, 0) for col in range(num_columns))
        non_manual = {col: natural_widths[col] for col in range(num_columns) if col not in self.manual_widths}
        non_manual_sum = sum(non_manual.values())

        self.auto_scaling = True
        if total_available >= manual_sum + non_manual_sum and non_manual_sum:
            available_for_non_manual = total_available - manual_sum
            for col in range(num_columns):
                if col in self.manual_widths:
                    self.setColumnWidth(col, self.manual_widths[col])
                else:
                    new_width = int(non_manual[col] * available_for_non_manual / non_manual_sum)
                    self.setColumnWidth(col, max(new_width, 1))
        else:
            for col in range(num_columns):
                self.setColumnWidth(col, self.manual_widths.get(col, natural_widths[col]))
        self.auto_scaling = False

