import numpy as np
import matplotlib.pyplot as plt

# ---------- utilidades numéricas ----------
def rk4_step(f, t, y, h, args=()):
    k1 = f(t, y, *args)
    k2 = f(t + 0.5*h, y + 0.5*h*k1, *args)
    k3 = f(t + 0.5*h, y + 0.5*h*k2, *args)
    k4 = f(t +     h, y +     h*k3, *args)
    return y + (h/6.0)*(k1 + 2*k2 + 2*k3 + k4)

def integrate_rk4(f, y0, t, args=()):
    y = np.zeros((len(t), len(y0)))
    y[0] = y0
    for i in range(len(t) - 1):
        y[i+1] = rk4_step(f, t[i], y[i], t[i+1]-t[i], args)
    return y

def quarter_car(t, y, m, c, k, xg_func):
    x, v = y
    xg = xg_func(t)
    return np.array([v, (k*xg - c*v - k*x) / m])

# ---------- parámetros ----------
m, c_nom, k_nom = 250.0, 1000.0, 15000.0   # SI
xg_step = 0.005                             # 5 mm
y0 = np.array([0.0, 0.0])

def xg_step_func(_t):   # escalón puro
    return xg_step

# ---------- solución analítica (Laplace) ----------
def analytic_step_response(t, m, c, k, A):
    """x(t) para escalón de amplitud A con x(0)=0, v(0)=0."""
    wn   = np.sqrt(k/m)                       # frecuencia natural
    zeta = c / (2*np.sqrt(k*m))               # factor de amortiguamiento

    if zeta >= 1.0:
        # Subamortiguado esperado: si no, cambia la fórmula (sobrecrit.)
        raise ValueError("Este script cubre el caso sub-amortiguado (ζ<1).")

    wd   = wn * np.sqrt(1.0 - zeta**2)        # frecuencia amortiguada
    phi  = np.arccos(zeta)

    # Fórmula estándar del escalón subamortiguado
    x_t = A * ( 1.0
                - np.exp(-zeta*wn*t)
                  * ( np.sin(wd*t + phi) / np.sqrt(1.0 - zeta**2) ) )
    return x_t

# ---------- malla temporal ----------
t_end      = 5.0
h_coarse   = 1e-3           # 1 ms
t_coarse   = np.arange(0, t_end + h_coarse, h_coarse)

# ---------- integración RK4 ----------
y_coarse   = integrate_rk4(quarter_car, y0, t_coarse,
                           args=(m, c_nom, k_nom, xg_step_func))[:, 0]

# ---------- referencia analítica ----------
x_analytic = analytic_step_response(t_coarse, m, c_nom, k_nom, xg_step)

# ---------- gráfica ----------
plt.figure(figsize=(8, 4))
plt.plot(t_coarse, x_analytic, label='Analítica (Laplace)')
plt.plot(t_coarse, y_coarse, '--', label='RK4  h=1 ms')
plt.xlabel('t [s]')
plt.ylabel('x [m]')
plt.title('Respuesta al escalón de 5 mm')
plt.legend()
plt.tight_layout()
plt.savefig('comp_step_overlay.pdf', dpi=300)
plt.show()

print('Figura guardada en comp_step_overlay.pdf')
