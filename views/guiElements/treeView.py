import sys

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QHeaderView, QTreeWidgetItemIterator


class TreeView(QWidget):
    def __init__(self, font):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setupTreeView(self.layout, font)

    def select_item_by_id(self, sid):
        iterator = QTreeWidgetItemIterator(self.treeView)
        while iterator.value():
            item = iterator.value()
            if item.text(0) == str(sid):
                self.treeView.setCurrentItem(item)
            iterator += 1
        return None

    def setupTreeView(self, layout, font):
        self.treeView = QTreeWidget()
        self.treeView.setFont(font)
        self.treeView.setLayoutDirection(Qt.RightToLeft)  # Set layout direction of tree view to right-to-left
        self.treeView.setHeaderLabels([ "id",
            "  إسم الموظف  ", "  الرقم الألي  ","  نوع التأشيرة  ", "  الأسم  ",
            "  للقب  ", "  رقم الجواز  ", "   مهنة   ",
            "    اريخ الإصدار    " , "  مدة الإقامة  ",
            "    صالحة إلي      ", "  عدد مرات الدخول  ", "  رسوم الدخول   " , "  المنفذ  ",
            "  الكفيل (جهة العمل)  " , "  ملاحظات  "

        ])

        header = self.treeView.header()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)  # Allows manual resizing of columns

        self.treeView.setSelectionMode(self.treeView.ExtendedSelection)  # Set selection mode to extended selection

        # Set initial width for columns based on the text width of the header
        self.treeView.header().setStretchLastSection(False)
        for i in range(self.treeView.columnCount()):
            max_width = header.fontMetrics().boundingRect(self.treeView.headerItem().text(i)).width()
            header.resizeSection(i, max_width + 35)

        layout.addWidget(self.treeView)

