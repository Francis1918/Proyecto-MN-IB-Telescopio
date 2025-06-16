# main.py
import tkinter as tk
from tkinter import PhotoImage
from ventana import AplicacionTelescopio

def main():
    root = tk.Tk()
    root.iconphoto(False, PhotoImage(file='icono.png'))
    ico = PhotoImage(file='icono.png')
    root.iconphoto(False, ico)
    root.option_add("*Font", "{Times New Roman} 12")
    app = AplicacionTelescopio(root)
    root.mainloop()

if __name__ == '__main__':
    main()
