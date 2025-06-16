import math
import numpy as np
from tkinter import messagebox
import tkinter as tk


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
        messagebox.showerror("Error", "Solo ingrese numeros.")
        return

    if Py < 0:
        messagebox.showerror("Error", "Py >= 0.")
        return

    if not (0 < L < B < d_max):
        messagebox.showerror("Error", "Los valores rebasan los límites establecidos:\n")
        return

    if Px == 0 and Py == 0:
        messagebox.showwarning("Advertencia", "Punto origen no es válido. Se usará (1, 1) como una referencia.")
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
        messagebox.showwarning("Advertencia", "Punto fuera de alcance.")

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
        f"Largo del pistón izquierdo (x1): {x1:.2f}\n"
        f"Largo del pistón derecho (x2): {x2:.2f}"
    )
    self.etiqueta_salida.config(text=texto_salida)

    self.dibujar_sistema(x1, x2, Px, Py, L, B, angulo_espejo, espejo_izq_x, espejo_izq_y, espejo_der_x, espejo_der_y)
