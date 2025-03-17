import sys

from PyQt5.QtCore import QDate, Qt, QByteArray, QBuffer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTreeWidgetItem

from model.kontakt import Kontakt
from views.system import System_View
from controllers.printLogic.print_handler import Print_Hanlder
from controllers.printLogic.report import Report


def safe_get(lst, index):
    try:
        return lst[index]
    except IndexError:
        return None
class System_Controller:
    def __init__(self, model, view, mainController):
        self.current_kontakt:Kontakt = None
        self.current_image = None
        self.current_image_data = None
        self.kontakte = {}
        self.mainController = mainController
        self.model = model
        self.view:System_View = view
        self.view.initUI()
        self.setup()
    def setup(self):
        self.view.uploadButton.clicked.connect(self.uploadImage)
        self.view.new_button.clicked.connect(self.new)
        self.view.simple_gui.search_button.clicked.connect(self.search)
        self.view.simple_gui.reload_button.clicked.connect(self.reload)

        self.view.exit_button.clicked.connect(self.exit)
        self.view.help_button.clicked.connect(self.help)
        self.view.update_button.clicked.connect(self.update)
        self.view.delete_button.clicked.connect(self.delete)

        self.view.print_button.clicked.connect(self.print_content)
        self.view.back_button.clicked.connect(self.go_back)
        self.view.next_button.clicked.connect(self.go_next)
        self.view.clear_button.clicked.connect(self.clear)

        self.view.treeViewWidget.treeView.itemClicked.connect(self.selected)

        self.clear()
        self.reload()
    def print_content(self):
        selected_items = self.view.treeViewWidget.treeView.selectedItems()
        if selected_items:
            try:
                text = self.view.print_combo_box.currentText()
                if text == "بدون اختيار":
                    l = [ ]
                    for i in selected_items:
                        l.append(self.kontakte.get(int(i.text(0))))
                    Print_Hanlder(safe_get(l, 0), safe_get(l, 1), safe_get(l, 2))
                elif text == "تقرير":
                    l = []
                    for i in selected_items:
                        l.append(self.kontakte.get(int(i.text(0))))
                    Report(l)
                elif text == 'تحت':
                    Print_Hanlder(low=self.kontakte.get(int(selected_items[0].text(0))))
                elif text == 'وسط':
                    Print_Hanlder(mid=self.kontakte.get(int(selected_items[0].text(0))))
                elif text == 'فوق':
                    Print_Hanlder(up=self.kontakte.get(int(selected_items[0].text(0))))
            except:
                pass

    def clear(self):
        for  i, input in zip(range(len(self.view.inputs)), self.view.inputs):
            if i==2 or i==8 or i==10 or i==12:
                input.setCurrentIndex(0)
            elif i==7:
                input.setDate(QDate.currentDate())
            elif i==9:
                pass
            else:
                input.setText("")
        self.view.imageLabel.clear()
        self.deselected()
        self.setupFee()
    def new(self):
        if self.check_entries() and self.current_image is not None:
            self.setCurrent_kontakt()
            try:
                self.model.add_kontakt(self.current_kontakt)
            except:
                pass
            self.clear()
            self.reload()
            self.view.treeViewWidget.select_item_by_id(next(iter(self.kontakte)))
        else:
            self.mainController.view.show_message("يرجى ملئ جميع الحقول واختيار صورة")
    def search(self):
        self.kontakte = self.model.search(
            self.view.simple_gui.entry1.text() or None,
            self.view.simple_gui.entry4.text() or None,
            self.view.simple_gui.entry2.date().toString('yyyy-MM-dd'),
            self.view.simple_gui.entry3.date().toString('yyyy-MM-dd'))
        self.setTree()
    def setTree(self):
        self.view.treeViewWidget.treeView.clear()

        for kontakt_key in self.kontakte:
            l = []
            for i in ['id', 'employee', 'visaNumber', 'visaArt', 'vorname', 'nachname','passport', "profession", 'visaIss', 'duration', 'visaValid', 'entriesNumber','entryFee', 'port', 'work', 'note']:
                l.append(str(self.kontakte[kontakt_key][i]))
            QTreeWidgetItem(self.view.treeViewWidget.treeView, l)
    def reload(self):
        self.kontakte = self.model.get_all_kontakte()
        self.setTree()
        self.view.simple_gui.clearSearch()
    def exit(self):
        self.mainController.showLogin()
        self.mainController.setupLogin()
    def help(self):
        self.mainController.showHelpWindow()
    def update(self):
        if self.check_entries() and self.current_kontakt is not None:
            if self.current_kontakt.id is not None:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Question)
                msgBox.setText("هل أنت متأكد أنك تريد تحديث هذا الإدخال؟")
                msgBox.setWindowTitle("تحديث")
                msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                returnValue = msgBox.exec()
                if returnValue == QMessageBox.Yes:
                    self.model.update_kontakt(self.current_kontakt.id, self.entries_to_obj())
                    self.clear()
                    self.reload()
        else:
            self.mainController.view.show_message("يرجى ملئ جميع الحقول واختيار صورة")
    def delete(self):
        if self.current_kontakt is not None:
            if self.current_kontakt.id is not None:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Question)
                msgBox.setText("هل أنت متأكد أنك تريد حذف هذا الإدخال؟")
                msgBox.setWindowTitle("حذف")
                msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                returnValue = msgBox.exec()
                if returnValue == QMessageBox.Yes:
                    self.model.delete_kontakt(self.current_kontakt.id)
                    self.clear()
                    self.reload()

        else:
            self.mainController.view.show_message("يرجى اختيار إدخال")
    def selected(self):
        selected_items = self.view.treeViewWidget.treeView.selectedItems()
        if selected_items:
            id = selected_items[0].text(0)
            self.showKontakt(id)
    def showKontakt(self, id):
        self.current_kontakt = self.kontakte.get(int(id))
        self.obj_to_entries()
        self.uploadImageFromDB()
    def change_selection(self, offset):
        selected_items = self.view.treeViewWidget.treeView.selectedItems()
        if not selected_items:
            return

        current_id = selected_items[0].text(0)
        self.clear()
        self.deselected()

        keys = list(self.kontakte.keys())
        current_index = keys.index(int(current_id))
        new_index = (current_index + offset) % len(keys)
        new_key = keys[new_index]
        self.showKontakt(new_key)
        self.view.treeViewWidget.select_item_by_id(new_key)
    def go_back(self):
        self.change_selection(-1)
    def go_next(self):
        self.change_selection(+1)
    def check_entries(self):
        for i, input in zip(range(len(self.view.inputs)), self.view.inputs):
            if i == 2 or i == 8 or i == 10 or i == 7 or i == 9 or i == 12 or i == 14:
                continue
            elif input.text() == "":
                return False
        return True
    def setCurrent_kontakt(self):
        self.current_kontakt = self.entries_to_obj()
    def entries_to_obj(self):
        return Kontakt(
                employee=self.view.inputs[0].text(),
                visaNumber=self.view.inputs[1].text(),
                visaArt=self.view.inputs[2].currentText(),
                vorname=self.view.inputs[3].text(),
                nachname=self.view.inputs[4].text(),
                passport=self.view.inputs[5].text(),
                profession=self.view.inputs[6].text(),
                visaIss=self.view.inputs[7].date().toString('yyyy-MM-dd'),
                duration=self.view.inputs[8].currentText(),
                visaValid=self.view.inputs[9].date().toString('yyyy-MM-dd'),
                entriesNumber=self.view.inputs[10].currentText(),
                entryFee=self.view.inputs[11].text(),
                port=self.view.inputs[12].currentText(),
                work=self.view.inputs[13].text(),
                note=self.view.inputs[14].text(),
                image_data=self.current_image_data
            )
    def obj_to_entries(self):
        self.view.inputs[0].setText(self.current_kontakt.employee)
        self.view.inputs[1].setText(self.current_kontakt.visaNumber)
        self.view.inputs[2].setCurrentText(self.current_kontakt.visaArt)
        self.view.inputs[3].setText(self.current_kontakt.vorname)
        self.view.inputs[4].setText(self.current_kontakt.nachname)
        self.view.inputs[5].setText(self.current_kontakt.passport)
        self.view.inputs[6].setText(self.current_kontakt.profession)
        self.view.inputs[7].setDate(QDate.fromString(self.current_kontakt.visaIss, "yyyy-MM-dd"))
        self.view.inputs[8].setCurrentText(str(self.current_kontakt.duration))
        self.view.inputs[9].setDate(QDate.fromString(self.current_kontakt.visaValid, "yyyy-MM-dd"))
        self.view.inputs[10].setCurrentText(self.current_kontakt.entriesNumber)
        self.view.inputs[11].setText(self.current_kontakt.entryFee)
        self.view.inputs[12].setCurrentText(self.current_kontakt.port)
        self.view.inputs[13].setText(self.current_kontakt.work)
        self.view.inputs[14].setText(self.current_kontakt.note)
        self.current_image_data = self.current_kontakt.image_data
        self.uploadImageFromDB()
    def uploadImageFromDB(self):
        pixmap = QPixmap()
        pixmap.loadFromData(self.current_image_data)
        self.current_image = pixmap
        self.view.imageLabel.setPixmap(
            self.current_image.scaled(self.view.imageLabel.width(),
                                      self.view.imageLabel.height(),
                                      aspectRatioMode=Qt.KeepAspectRatio))
    def uploadImage(self):
        try:
            imagePath, _ = QFileDialog.getOpenFileName(self.view, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
            if imagePath:
                self.current_image = QPixmap(imagePath)
                if self.current_image.isNull():
                    self.mainController.view.show_message("هناك خطأ في الصورة")
                    return

                self.view.imageLabel.setPixmap(
                    self.current_image.scaled(self.view.imageLabel.width(), self.view.imageLabel.height(), aspectRatioMode=Qt.KeepAspectRatio))

            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QBuffer.ReadWrite)
            self.current_image.save(buffer, imagePath.split(".")[-1])
            buffer.close()
            self.current_image_data = byte_array.data()
        except:
            pass
    def deselected(self):
        self.view.treeViewWidget.treeView.clearSelection()
        self.current_kontakt = None
        self.current_image = None
        self.current_image_data = None
    def setupFee(self):
        try:
            entryFee = list(self.kontakte.values())[0].entryFee
            self.view.lineEditFee.setText(entryFee)
        except:
            pass


