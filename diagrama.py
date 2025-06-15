import matplotlib.pyplot as plt

# Configuración general
fig, ax = plt.subplots(figsize=(6, 14))
ax.axis('off')

# Propiedades de los recuadros
box_style = dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1)

# Lista de pasos y sus posiciones verticales
steps = [
    "Formular EDO",
    "Definir criterios de confort\ny validación",
    "Resolución analítica\n(Laplace y RK4 manual)",
    "Simulación numérica\ncon RK45",
    "Barrido paramétrico",
    "Exportar resultados\na CSV/XLSX",
    "Filtrar y generar\nmapas de calor",
    "Seleccionar par óptimo\n(k, c)",
    "Analizar sensibilidad\n(±10%)",
    "Comparar sol. analítica\nvs. numérica",
    "Comparar con caso\noscilador libre"
]
y_positions = list(range(10, -1, -1))

# Dibujar recuadros y flechas
for idx, step in enumerate(steps):
    y = y_positions[idx]
    ax.text(0.5, y, step, ha='center', va='center', fontsize=10, bbox=box_style)
    if idx < len(steps) - 1:
        y_next = y_positions[idx + 1]
        ax.arrow(0.5, y - 0.2, 0, (y_next + 0.2) - y, length_includes_head=True,
                 head_width=0.02, head_length=0.1, fc='black', ec='black')

# Ajustar límites y guardar
ax.set_xlim(0, 1)
ax.set_ylim(-1, 11)
plt.tight_layout()
plt.savefig("diagrama_flujo_general.png", dpi=300)
plt.show()
