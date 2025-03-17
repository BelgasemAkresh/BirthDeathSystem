import re
from io import BytesIO
from PIL import Image, ImageFilter
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import arabic_reshaper
from bidi.algorithm import get_display
import tkinter as tk
from tkinter import filedialog

class PDF_Printer:
    def __init__(self, filename='output.pdf'):
        self.root = tk.Tk()
        self.root.withdraw()
        # Wir verwenden das Tk-Fenster nicht direkt.
        self.filename = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF files", "*.pdf")])
        if self.filename is None:
            self.filename = filename
        self.canvas = canvas.Canvas(self.filename, pagesize=A4)
        self._register_fonts()
        self.extraY = 102*5.6
        self.extraY_image = -1

    def _register_fonts(self):
        pdfmetrics.registerFont(TTFont('Arabic', 'ar.ttf'))
        pdfmetrics.registerFont(TTFont('Helvetica', 'Helvetica.ttf'))

    def _mm_to_points(self, mm):
        return mm * 2.83465

    def _is_arabic(self, text):
        arabic_pattern = re.compile('[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
        return bool(arabic_pattern.search(text))

    def print_text(self, text, x_mm, y_mm, font_size=9):
        x = self._mm_to_points(x_mm + 4)
        y = self._mm_to_points(y_mm) + self.extraY

        if self._is_arabic(text):
            reshaped_text = arabic_reshaper.reshape(text)
            text = get_display(reshaped_text)
            self.canvas.setFont('Arabic', font_size)
            text_width = self.canvas.stringWidth(text, 'Arabic', font_size)
            self.canvas.drawString(x - text_width, y, text)
        else:
            self.canvas.setFont('Helvetica', font_size)
            self.canvas.drawString(x, y, text)

    def print_pic(self, image_data, x_mm, y_mm, x_scale=19, y_scale=22, transparency=240):
        image_stream = BytesIO(image_data)
        image = Image.open(image_stream)

        image_reader = ImageReader(image)
        width, height = image.size
        scaled_width = self._mm_to_points(x_scale)
        scaled_height = self._mm_to_points(y_scale)
        x = self._mm_to_points(x_mm + 6) + 50
        y = self._mm_to_points(-y_mm - self.extraY_image - 20 + 5) + 854

        self.canvas.drawImage(image_reader, x - scaled_width, y - scaled_height, scaled_width, scaled_height,
                              mask='auto')

    def save_pdf(self):


        self.canvas.save()
        self.root.destroy()  # Schließt das Tkinter-Fenster


if __name__ == '__main__':
    image_path = 'C:/Users/belga/LB/python/Visa-V3/23/Bilder/libyaGovHigh.png'
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    # Verwendung der Klasse
    pdf_printer = PDF_Printer()
    pdf_printer.print_text('Hello', 150, 250 + 20)
    pdf_printer.print_text('احمد', 150, 200)
    pdf_printer.print_pic(image_data, 20, 20)
    pdf_printer.save_pdf()
