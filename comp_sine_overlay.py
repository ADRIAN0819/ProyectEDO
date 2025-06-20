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
m, c_nom, k_nom = 250.0, 1000.0, 15000.0
amp_sine, f_sine = 0.01, 4.0              # 10 mm – 4 Hz
omega = 2*np.pi*f_sine
y0 = np.array([0.0, 0.0])

def xg_sine_func(t):            # entrada de pista
    return amp_sine * np.sin(omega*t)

# ---------- solución analítica (Laplace / respuesta forzada) ----------
def analytic_sine_response(t, m, c, k, A, omega):
    """Desplazamiento x(t) con x(0)=0, v(0)=0 para entrada A sin(ωt)."""
    wn   = np.sqrt(k/m)                       # frecuencia natural
    zeta = c / (2*np.sqrt(k*m))               # factor de amortiguamiento

    if zeta >= 1.0:
        raise ValueError("El código analítico aquí implementado "
                         "sólo cubre el caso sub-amortiguado (ζ < 1).")

    wd   = wn * np.sqrt(1.0 - zeta**2)        # frecuencia amortiguada

    # amplitud y fase de la respuesta estacionaria
    R   = k * A / np.sqrt((k - m*omega**2)**2 + (c*omega)**2)
    phi = np.arctan2(c*omega, k - m*omega**2)  # atan2 devuelve el signo correcto

    # coeficientes del transitorio (condiciones iniciales x(0)=0, v(0)=0)
    C1 =  R * np.sin(phi)
    C2 = ( zeta*wn*C1 - R*omega*np.cos(phi) ) / wd

    # solución completa: transitorio + forzado
    exp_term = np.exp(-zeta*wn*t)
    x_t = (exp_term * ( C1*np.cos(wd*t) + C2*np.sin(wd*t) )
           + R * np.sin(omega*t - phi))
    return x_t

# ---------- malla temporal ----------
t_end = 5.0
h_coarse = 1e-3           # 1 ms
t_coarse = np.arange(0, t_end + h_coarse, h_coarse)

# ---------- integración RK4 ----------
y_coarse = integrate_rk4(quarter_car, y0, t_coarse,
                         args=(m, c_nom, k_nom, xg_sine_func))[:, 0]

# ---------- referencia analítica ----------
x_analytic = analytic_sine_response(t_coarse, m, c_nom, k_nom,
                                    amp_sine, omega)

# ---------- gráfica ----------
plt.figure(figsize=(8, 4))
plt.plot(t_coarse, x_analytic, label='Analítica (Laplace)')
plt.plot(t_coarse, y_coarse, '--', label='RK4  h=1 ms')
plt.xlabel('t [s]')
plt.ylabel('x [m]')
plt.title('Respuesta a entrada senoidal 10 mm, 4 Hz')
plt.legend()
plt.tight_layout()
plt.savefig('comp_sine_overlay.pdf', dpi=300)
plt.show()

print('Figura guardada en comp_sine_overlay.pdf')