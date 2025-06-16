import math

def dibujar_sistema(self, x1, x2, Px, Py, L, B, angulo_espejo,
                    espejo_izq_x, espejo_izq_y, espejo_der_x, espejo_der_y):
    # 1) Limpio el canvas y fondo
    self.ax.clear()
    self.ax.set_facecolor("lightyellow")

    # 2) Dibujo los pistones y el espejo
    A = (-B/2, 0)
    Bp = ( B/2, 0)
    self.ax.plot([A[0], espejo_izq_x], [A[1], espejo_izq_y],
                 'g-', linewidth=3, label='Pistón Izquierdo')
    self.ax.plot([Bp[0], espejo_der_x], [Bp[1], espejo_der_y],
                 'g-', linewidth=3, label='Pistón Derecho')
    self.ax.plot([espejo_izq_x, espejo_der_x],
                 [espejo_izq_y, espejo_der_y],
                 'c-', linewidth=4, label='Espejo')
    self.ax.plot(Px, Py, 'go', label='Punto P')

    # 3) Calcular el pie de la perpendicular de P sobre la recta espejo
    dx = espejo_der_x - espejo_izq_x
    dy = espejo_der_y - espejo_izq_y
    norma = math.hypot(dx, dy)
    ux, uy = dx/norma, dy/norma     # vector unitario paralelo al espejo

    # proyección escalar de (P - E_izq) sobre (ux,uy)
    dot = (Px - espejo_izq_x)*ux + (Py - espejo_izq_y)*uy
    # pie de perpendicular:
    fx = espejo_izq_x + dot*ux
    fy = espejo_izq_y + dot*uy

    # 4) Dibujo la línea punteada PROYECCIÓN PERPENDICULAR
    self.ax.plot([Px, fx], [Py, fy],
                 'g--', linewidth=1, label='Proyección Perpendicular')

    # 5) Resto de configuración gráfica
    self.ax.set_xlabel('Eje X')
    self.ax.set_ylabel('Eje Y')
    self.ax.set_title('Orientación del Espejo Secundario')
    self.ax.legend()
    self.ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    self.ax.axis('equal')

    # Ajusto límites
    x_min = min(A[0], espejo_izq_x, Px) - 2
    x_max = max(Bp[0], espejo_der_x, Px) + 2
    y_min = 0
    y_max = max(espejo_izq_y, espejo_der_y, Py) + 2
    self.ax.set_xlim(x_min, x_max)
    self.ax.set_ylim(y_min, y_max)

    # Finalmente refresco el canvas
    self.canvas.draw()
