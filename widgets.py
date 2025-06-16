import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Configuración global de Matplotlib
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size']   = 12

def crear_widgets(self):
    # --- Contenedor principal: 2 columnas ---
    main_frame = tk.Frame(self.raiz)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # --- Columna IZQUIERDA: parámetros y resultados ---
    left_frame = tk.Frame(main_frame)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

    # Marco de entradas
    marco_entrada = tk.LabelFrame(left_frame, text="Parámetros")
    marco_entrada.pack(fill=tk.X, padx=5, pady=5)

    etiquetas = [
        ("L (Largo del espejo):", self.L),
        ("B (Base del espejo):", self.B),
        ("D (Longitud mínima de los pistones):", self.D),
        ("d_max (Longitud máxima de los pistones):", self.d_max),
        ("F (Distancia del foco al extremo izquierdo):", self.F),
        ("Px (Coordenada x de P):", self.Px_var),
        ("Py (Coordenada y de P):", self.Py_var)
    ]
    for i, (texto, var) in enumerate(etiquetas):
        tk.Label(marco_entrada, text=texto).grid(row=i, column=0, sticky=tk.W, pady=2)
        tk.Entry(marco_entrada, textvariable=var, width=10).grid(row=i, column=1, pady=2)

    tk.Button(
        marco_entrada,
        text="Calcular",
        command=self.calcular_y_dibujar
    ).grid(row=len(etiquetas), column=0, columnspan=2, pady=8)

    # Etiqueta de salida (datos calculados)
    self.etiqueta_salida = tk.Label(
        left_frame,
        text="",
        font=('Times New Roman', 12),
        justify=tk.LEFT,
        anchor="nw"
    )
    self.etiqueta_salida.pack(fill=tk.X, padx=5, pady=10)

    # --- Columna DERECHA: gráfico Matplotlib ---
    right_frame = tk.Frame(main_frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    self.figura = plt.Figure(figsize=(6, 5), facecolor='lightgray')
    self.ax = self.figura.add_subplot(111)
    self.canvas = FigureCanvasTkAgg(self.figura, master=right_frame)
    self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
