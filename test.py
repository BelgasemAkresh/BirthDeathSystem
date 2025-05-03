import tkinter as tk
from tkinter import messagebox
import random

class FarbRatenSpiel:
    def __init__(self, root):
        self.root = root
        self.root.title("Farb-Raten-Spiel")
        self.versuche = 0
        self.ziel_farbe = self.generiere_farbe()

        # Canvas für Farben
        self.canvas = tk.Canvas(root, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.update_canvas)

        # Eingaben für RGB
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.r_var = tk.IntVar(value=0)
        self.g_var = tk.IntVar(value=0)
        self.b_var = tk.IntVar(value=0)

        self.r_var.trace_add("write", self.pruefe_farbe)
        self.g_var.trace_add("write", self.pruefe_farbe)
        self.b_var.trace_add("write", self.pruefe_farbe)

        tk.Label(self.frame, text="R:").grid(row=0, column=0)
        tk.Spinbox(self.frame, from_=0, to=255, textvariable=self.r_var, width=5).grid(row=0, column=1)

        tk.Label(self.frame, text="G:").grid(row=0, column=2)
        tk.Spinbox(self.frame, from_=0, to=255, textvariable=self.g_var, width=5).grid(row=0, column=3)

        tk.Label(self.frame, text="B:").grid(row=0, column=4)
        tk.Spinbox(self.frame, from_=0, to=255, textvariable=self.b_var, width=5).grid(row=0, column=5)

    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def generiere_farbe(self):
        return (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

    def update_canvas(self, event=None):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Linke Seite = Ziel-Farbe
        self.canvas.create_rectangle(0, 0, width//2, height, fill=self.rgb_to_hex(self.ziel_farbe), outline="")

        # Rechte Seite = Benutzer-Farbe
        benutzer_farbe = (self.r_var.get(), self.g_var.get(), self.b_var.get())
        self.canvas.create_rectangle(width//2, 0, width, height, fill=self.rgb_to_hex(benutzer_farbe), outline="")

    def pruefe_farbe(self, *args):
        self.versuche += 1
        benutzer_farbe = (self.r_var.get(), self.g_var.get(), self.b_var.get())
        self.update_canvas()

        if benutzer_farbe == self.ziel_farbe:
            messagebox.showinfo("Gewonnen!", f"Du hast die Farbe erraten in {self.versuche} Versuchen!")
            self.ziel_farbe = self.generiere_farbe()
            self.versuche = 0
            self.r_var.set(0)
            self.g_var.set(0)
            self.b_var.set(0)
            self.update_canvas()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x300")
    app = FarbRatenSpiel(root)
    root.mainloop()
