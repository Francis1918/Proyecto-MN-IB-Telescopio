'''
#Modulo para calcular las extensiones x1, x2 de los pistones lineales
#del telescopio
import math
import numpy as np
from typing import Tuple
def compute_pistons(
    L: float,
    B: float,
    D: float,
    d_max: float,
    F: float,
    x: float,
    y: float
) -> Tuple[float, float, Tuple[float, float], Tuple[float, float], Tuple[float, float]]:
    """
    Calcula las extensiones de los dos pistones que orientan el espejo secundario.

    Parámetros:
    -----------
    L : float
        Longitud del espejo secundario.
    B : float
        Separación horizontal entre los dos puntos de anclaje de los pistones.
    D : float
        Longitud mínima (colapsada) de cada pistón.
    d_max : float
        Longitud máxima (extendida) de cada pistón.
    F : float
        Distancia desde el extremo izquierdo del espejo principal al punto de foco.
    x : float
        Coordenada x del punto P en el espacio.
    y : float
        Coordenada y del punto P en el espacio.

    Retorna:
    --------
    x1 : float
        Extensión calculada del pistón izquierdo.
    x2 : float
        Extensión calculada del pistón derecho.
    P1 : Tuple[float, float]
        Coordenadas (x,y) del extremo izquierdo del espejo.
    P2 : Tuple[float, float]
        Coordenadas (x,y) del extremo derecho del espejo.
    u  : Tuple[float, float]
        Vector unitario perpendicular a la dirección P→F (orientación del espejo).

    Notas:
    ------
    - Si |v| = 0 (P coincide con F), lanza ValueError.
    - Las extensiones x1, x2 se clamp a [D, d_max].
    - En caso de múltiples soluciones, escoge la de mayor x1+x2;
      si no cabe, aproxima lo máximo posible.
    """
    # 1) Vector de luz v = (F - x, -y)
    vx = F - x
    vy = -y
    # 2) Norma de v
    norm_v = math.hypot(vx, vy)  # equivalente a sqrt(vx**2 + vy**2)
    if norm_v == 0:
        raise ValueError("El punto P coincide con el foco; vector de dirección nulo.")
    # 3) Vector unitario en la dirección de la luz
    nx = vx / norm_v
    ny = vy / norm_v
    # 4) Vector ortogonal u = (-n_y, n_x)
    ux = -ny
    uy = nx
    # 5) Parámetro t para ubicar el punto medio en la línea P→F
    if F == x:
        raise ValueError("No se puede calcular t: F y x son iguales (división por cero).")
    t = (B/2 - x) / (F - x)

    # Coordenadas del centro del espejo M
    Mx = B / 2
    My = y - t * y
    #print(f"DEBUG: Centro del espejo M: ({Mx}, {My})")
    # 6) Cálculo de los extremos del espejo
    half_L = L / 2.0
    # Extremo izquierdo P1 = M – (L/2)·u
    P1x = Mx - ux * half_L
    P1y = My - uy * half_L
    # Extremo derecho  P2 = M + (L/2)·u
    P2x = Mx + ux * half_L
    P2y = My + uy * half_L

    #print(f"DEBUG: P1 = ({P1x:.3f}, {P1y:.3f}), P2 = ({P2x:.3f}, {P2y:.3f})")
    # 7) Longitudes de pistón antes de clamp:
    x1 = P1y - D
    x2 = P2y - D

    #print(f"DEBUG: x1 = {x1:.3f}, x2 = {x2:.3f}")
    # 8) Clamping a los límites físicos
    x1_clamped = min(max(x1, D), d_max)
    x2_clamped = min(max(x2, D), d_max)
    #print(f"DEBUG: x1_clamped = {x1_clamped:.3f}, x2_clamped = {x2_clamped:.3f}")

    # 9) Retorno de resultados
    return x1_clamped, x2_clamped, (P1x, P1y), (P2x, P2y), (ux, uy)


if __name__ == "__main__":
    # Valores de prueba para verificar Mx, My en el Paso 5
    L = 1.0      # sólo relleno dummy
    B = 10.0
    D = 1.0
    d_max = 5.0
    F = 20.0
    x = 5.0
    y = 20.0

    # Para ver sólo Mx, My, puedes temporalmente imprimirlos dentro de la función
    # o bien capturarlos en la llamada:
    try:
        result = compute_pistons(L, B, D, d_max, F, x, y)
        # result = (x1, x2, P1, P2, u)
        _, _, _, _, _ = result  # ignoramos los demás valores
        # Si añadiste un print dentro de compute_pistons, verás Mx/My en consola
    except NotImplementedError:
        print("Aún no terminaste toda la función, pero el DEBUG de Mx/My debería haber salido.")
    except Exception as e:
        print("Error durante la prueba:", e)


'''



#codigo separado solo con el main de respaldo
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import numpy as np

class AplicacionTelescopio:
    def __init__(self, raiz):
        self.raiz = raiz
        #color de fondo da ventana thinker
        self.raiz.configure(bg='lightgray')
        self.raiz.title("Telescopio James Webb")

        # Definir constantes del sistema
        self.L = tk.DoubleVar(value=12.0)
        self.B = tk.DoubleVar(value=14.0)
        self.D = tk.DoubleVar(value=4.0)
        self.d_max = tk.DoubleVar(value=20.0)
        self.F = tk.DoubleVar(value=6.0)
        self.Px_var = tk.DoubleVar(value=8.0)
        self.Py_var = tk.DoubleVar(value=12.0)

        self.crear_widgets()
        self.calcular_y_dibujar()

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

        tk.Button(marco_entrada, text="Calcular y Dibujar", command=self.calcular_y_dibujar).grid(row=7, column=0, columnspan=2, pady=5)

        self.etiqueta_salida = tk.Label(self.raiz, text="", font=('Arial', 12))
        self.etiqueta_salida.pack()
        #cambio de color de fondo a 'x' para mejor contraste
        self.figura = plt.Figure(figsize=(8, 8),facecolor='lightgray')
        self.ax = self.figura.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.raiz)
        self.canvas.get_tk_widget().pack()

    def calcular_y_dibujar(self):
        try:
            L = self.L.get()
            B = self.B.get()
            D = self.D.get()
            d_max = self.d_max.get()
            F = self.F.get()
            Px = self.Px_var.get()
            Py = self.Py_var.get()
        except tk.TclError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")
            return

        if Py < 0:
            messagebox.showerror("Error", "La coordenada Py debe ser mayor o igual a 0.")
            return

        if not (0 < L < B < d_max):
            messagebox.showerror("Error", "Los parámetros deben cumplir 0 < L < B < d_max.")
            return

        if Px == 0 and Py == 0:
            messagebox.showwarning("Advertencia", "Punto P(0, 0) no es válido. Se usará (1, 1) como referencia.")
            Px = 1
            Py = 1

        encontrado = False
        for My in np.linspace(Py - L / 2, Py + L / 2, 500):
            N_x = -Px
            N_y = My - Py
            if N_x == 0 and N_y == 0:
                continue

            D_x, D_y = -N_y, N_x
            norma = math.hypot(D_x, D_y)
            D_x /= norma
            D_y /= norma

            espejo_izq_x = (-L / 2) * D_x
            espejo_izq_y = My + (-L / 2) * D_y
            espejo_der_x = (L / 2) * D_x
            espejo_der_y = My + (L / 2) * D_y

            x1 = math.hypot(espejo_izq_x + B / 2, espejo_izq_y)
            x2 = math.hypot(espejo_der_x - B / 2, espejo_der_y)

            if espejo_izq_y < 0 or espejo_der_y < 0:
                continue

            if D <= x1 <= d_max and D <= x2 <= d_max:
                encontrado = True
                break

        if not encontrado:
            messagebox.showwarning("Advertencia", "Punto fuera de alcance. Se graficará con pistones en sus límites.")

            x1 = d_max
            x2 = D

            theta = math.atan2(Py, Px)
            D_x = math.cos(theta)
            D_y = math.sin(theta)

            espejo_izq_x = -B / 2 + x2 * D_x
            espejo_izq_y = max(0, x2 * D_y)
            espejo_der_x = B / 2 + x1 * D_x
            espejo_der_y = max(0, x1 * D_y)

            centro_x = (espejo_izq_x + espejo_der_x) / 2
            centro_y = (espejo_izq_y + espejo_der_y) / 2

            espejo_izq_x = centro_x - (L / 2) * D_y
            espejo_izq_y = max(0, centro_y + (L / 2) * D_x)
            espejo_der_x = centro_x + (L / 2) * D_y
            espejo_der_y = max(0, centro_y - (L / 2) * D_x)

            angulo_espejo = math.degrees(theta)
        else:
            angulo_espejo = math.degrees(math.atan2(D_y, D_x))

        texto_salida = (
            f"\u00c1ngulo del espejo respecto a la horizontal: {angulo_espejo:.2f}°\n"
            f"Longitud del pistón izquierdo (x1): {x1:.2f}\n"
            f"Longitud del pistón derecho (x2): {x2:.2f}"
        )
        self.etiqueta_salida.config(text=texto_salida)

        self.dibujar_sistema(x1, x2, Px, Py, L, B, angulo_espejo, espejo_izq_x, espejo_izq_y, espejo_der_x, espejo_der_y)

    def dibujar_sistema(self, x1, x2, Px, Py, L, B, angulo_espejo, espejo_izq_x, espejo_izq_y, espejo_der_x, espejo_der_y):
        self.ax.clear()
        #color de fondo del grafico
        self.ax.set_facecolor("lightyellow")
        A = (-B / 2, 0)
        B_punto = (B / 2, 0)
        #para cambiar el color de los pistones, se puede usar 'r-' para rojo, 'b-' para azul, etc.
        self.ax.plot([A[0], espejo_izq_x], [A[1], espejo_izq_y], 'g-', linewidth=3, label='Pistón Izquierdo')
        self.ax.plot([B_punto[0], espejo_der_x], [B_punto[1], espejo_der_y], 'g-', linewidth=3, label='Pistón Derecho')
        self.ax.plot([espejo_izq_x, espejo_der_x], [espejo_izq_y, espejo_der_y], 'c-', linewidth=4, label='Espejo')
        self.ax.plot(Px, Py, 'go', label='Punto P')

        mx = (espejo_izq_x + espejo_der_x) / 2
        my = (espejo_izq_y + espejo_der_y) / 2
        self.ax.plot([Px, mx], [Py, my], 'g--', linewidth=1, label='Proyección Perpendicular')

        self.ax.set_xlabel('Eje X')
        self.ax.set_ylabel('Eje Y')
        self.ax.set_title('Orientación del Espejo Secundario')
        self.ax.legend()
        self.ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        self.ax.axis('equal')

        x_min = min(-B / 2, espejo_izq_x, Px) - 2
        x_max = max(B / 2, espejo_der_x, Px) + 2
        y_min = 0
        y_max = max(espejo_izq_y, espejo_der_y, Py) + 2

        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)
        self.canvas.draw()
'''


'''

if __name__ == '__main__':
    raiz = tk.Tk()
    aplicacion = AplicacionTelescopio(raiz)
    raiz.mainloop()