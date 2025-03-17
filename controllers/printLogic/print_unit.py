from controllers.printLogic.pdf_printer import PDF_Printer
from model.kontakt import Kontakt


class Print_Unit:
    def __init__(self, kontakt, printer):
        self.kontakt: Kontakt = kontakt
        self.printer: PDF_Printer = printer

    def print(self):

        if self.kontakt is not None:
            self.printer.print_pic(self.kontakt.image_data, 62, 24)

            self.printer.print_text("السفارة الليبية في برلين", 115, 48)

            l = [['visaNumber', (140, 65)], ['visaArt', (110, 65)], ['vorname', (150, 56)], ['nachname', (112, 56)],
                 ['passport', (140, 48)],
                 ['profession', (130, 48)], ['visaIss', (145, 40)], ['visaValid', (115, 40)], ['duration', (100, 40)],
                 ['entriesNumber', (152, 33)], ['work', (126, 33)]
                 ]

            for i in l:
                self.printer.print_text(str(self.kontakt[i[0]]), i[1][0], i[1][1])

            self.printer.print_text( " المنفذ:  "  + str(self.kontakt["port"]), 155, 26 )

            self.printer.print_text(str(self.kontakt["note"]), 155, 14)
            self.printer.print_text("التوقيع و الختم", 100, 15)

            self.printer.print_text(" الرسوم:  " + str(self.kontakt["entryFee"]), 155, 20)


