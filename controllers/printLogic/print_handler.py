from controllers.printLogic.pdf_printer import PDF_Printer
from controllers.printLogic.print_unit import Print_Unit

DISTANCE = 100
class Print_Hanlder:
    def __init__(self, up=None, mid=None, low=None):
        self.pdf_printer = PDF_Printer()
        self.up = None
        self.mid = None
        self.low = None

        if up is not None:
            self.up = Print_Unit(up, self.pdf_printer)

        if mid is not None:
            self.mid = Print_Unit(mid, self.pdf_printer)

        if low is not None:
            self.low = Print_Unit(low, self.pdf_printer)

        self.print()

    def print(self):
        if self.up is not None:
            self.up.print()
        self.pdf_printer.extraY_image = DISTANCE
        self.pdf_printer.extraY -= DISTANCE *2.83465

        if self.mid is not None:
            self.mid.print()

        self.pdf_printer.extraY_image += DISTANCE
        self.pdf_printer.extraY -= (DISTANCE + 0.5)*2.83465

        if self.low is not None:
            self.low.print()

        self.pdf_printer.save_pdf()
