import tkinter as tk
from widgets import crear_widgets
from calculo import calcular_y_dibujar
from dibujo import dibujar_sistema
class AplicacionTelescopio:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.configure(bg='lightgray')
        self.raiz.title("Telescopio James Webb")

        self.raiz = raiz
        # color de fondo da ventana thinker
        self.raiz.configure(bg='lightgray')
        self.raiz.title("Telescopio James Webb")

        # Definir constantes del sistema
        self.L = tk.DoubleVar(value=12.0)
        self.B = tk.DoubleVar(value=14.0)
        self.D = tk.DoubleVar(value=4.0)
        self.d_max = tk.DoubleVar(value=20.0)
        self.F = tk.DoubleVar(value=6.0)
        self.Px_var = tk.DoubleVar(value=10.0)
        self.Py_var = tk.DoubleVar(value=12.0)
        #  ↓↓↓ Aquí haces el “bind” de las funciones como métodos ↓↓↓
        self.crear_widgets      = crear_widgets.__get__(self, AplicacionTelescopio)
        self.calcular_y_dibujar = calcular_y_dibujar.__get__(self, AplicacionTelescopio)
        self.dibujar_sistema    = dibujar_sistema.__get__(self, AplicacionTelescopio)

        # Y **luego** sí llamas a crear_widgets y calcular_y_dibujar
        self.crear_widgets()
        self.calcular_y_dibujar()

