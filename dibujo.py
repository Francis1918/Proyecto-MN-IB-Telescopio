def dibujar_sistema(self, x1, x2, Px, Py, L, B, angulo_espejo, espejo_izq_x, espejo_izq_y, espejo_der_x, espejo_der_y):
    self.ax.clear()
    # color de fondo del grafico
    self.ax.set_facecolor("lightyellow")
    A = (-B / 2, 0)
    B_punto = (B / 2, 0)
    # para cambiar el color de los pistones, se puede usar 'r-' para rojo, 'b-' para azul, etc.
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