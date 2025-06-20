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
    xg   = xg_func(t)
    return np.array([v, (k*xg - c*v - k*x)/m])

# ---------- solución analítica del escalón (tres regímenes) ----------
def analytic_step(t, m, c, k, A):
    """x(t) para un escalón de amplitud A, cualquier ζ."""
    wn   = np.sqrt(k/m)
    zeta = c / (2*np.sqrt(k*m))

    if zeta < 1.0 - 1e-12:                      # sub-amortiguado
        wd  = wn*np.sqrt(1-zeta**2)
        phi = np.arccos(zeta)
        return A*(1 - np.exp(-zeta*wn*t)*np.sin(wd*t+phi)/np.sqrt(1-zeta**2))

    elif abs(zeta-1.0) <= 1e-12:                # crítico
        return A*(1 - np.exp(-wn*t)*(1 + wn*t))

    else:                                       # sobreamortiguado (ζ>1)
        alpha = wn*np.sqrt(zeta**2 - 1)
        s1 = -wn*zeta + alpha    # ambos < 0
        s2 = -wn*zeta - alpha
        return A*(1 - (np.exp(s1*t)*s2 - np.exp(s2*t)*s1)/(s2 - s1))

# ---------- parámetros ----------
m        = 250.0
y0       = np.array([0.0, 0.0])
A_step   = 0.005                        # 5 mm
def xg_step_func(_t): return A_step

# malla (k,c)
k_vals = np.linspace(5e3, 16e3, 8)
c_vals = np.linspace(1e3, 5e3, 8)

# tiempos (solo malla gruesa, 1 ms)
t_end   = 2.0
h_coarse = 1e-3
t_coarse = np.arange(0, t_end + h_coarse, h_coarse)

errors = np.zeros((len(c_vals), len(k_vals)))

for i_c, c_val in enumerate(c_vals):
    for j_k, k_val in enumerate(k_vals):
        # Numérico: RK4 paso 1 ms
        y_num = integrate_rk4(quarter_car, y0, t_coarse,
                              args=(m, c_val, k_val, xg_step_func))[:,0]
        # Analítico: fórmula completa
        y_ref = analytic_step(t_coarse, m, c_val, k_val, A_step)

        rel_err = np.linalg.norm(y_num - y_ref) / np.linalg.norm(y_ref)
        errors[i_c, j_k] = 100*rel_err      # %

# ---------- gráfica ----------
extent = [k_vals[0], k_vals[-1], c_vals[0], c_vals[-1]]
plt.figure(figsize=(7,5))
im = plt.imshow(errors, origin='lower', extent=extent, aspect='auto')
plt.colorbar(im, label='Error relativo [%]')
plt.xlabel('Rigidez k [N/m]')
plt.ylabel('Amortiguamiento c [Ns/m]')
plt.title('Heat-map de error relativo (RK4 h = 1 ms vs. Laplace)')
plt.tight_layout()
plt.savefig('error_heatmap.pdf', dpi=300)
plt.show()

print('Figura guardada en error_heatmap.pdf')