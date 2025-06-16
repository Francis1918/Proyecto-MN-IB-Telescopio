import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size']   = 12
def crear_widgets(self):
    marco_entrada = tk.Frame(self.raiz)
    marco_entrada.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    etiquetas = [
        ("L (Largo del espejo):", self.L),
        ("B (Base del espejo):", self.B),
        ("D (Longitud mínima de los pistones):", self.D),
        ("d_max (Longitud máxima de los pistones):", self.d_max),
        ("F (Distancia del foco al extremo izquierdo):", self.F),
        ("Px (Coordenada x de P):", self.Px_var),
        ("Py (Coordenada y de P):", self.Py_var)
    ]

    for i, (label, var) in enumerate(etiquetas):
        tk.Label(marco_entrada, text=label).grid(row=i, column=0, sticky=tk.W)
        tk.Entry(marco_entrada, textvariable=var).grid(row=i, column=1)

    tk.Button(marco_entrada, text="Calcular y Dibujar", command=self.calcular_y_dibujar).grid(row=7, column=0,
                                                                                              columnspan=2, pady=5)

    self.etiqueta_salida = tk.Label(self.raiz, text="", font=('Times New Roman', 12))
    self.etiqueta_salida.pack()
    # cambio de color de fondo a 'x' para mejor contraste
    self.figura = plt.Figure(figsize=(8, 8), facecolor='lightgray')
    self.ax = self.figura.add_subplot(111)
    self.canvas = FigureCanvasTkAgg(self.figura, master=self.raiz)
    self.canvas.get_tk_widget().pack()