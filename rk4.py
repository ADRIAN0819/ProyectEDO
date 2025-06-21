import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Modelo Quarter-Car
def quarter_car(t, y, m, c, k, xg_func, xg_dot_func):
    x, v = y
    xg = xg_func(t)
    xg_dot = xg_dot_func(t)
    dxdt = v
    dvdt = (-c*(v - xg_dot) - k*(x - xg)) / m
    return [dxdt, dvdt]

# --- Señales de entrada ---
def escalon(t, magnitud=0.005):
    return magnitud if t >= 0 else 0

def escalon_dot(t, magnitud=0.005):
    return 0

def seno(t, amp, freq):
    return amp * np.sin(2*np.pi*freq*t)

def seno_dot(t, amp, freq):
    return amp * 2*np.pi*freq * np.cos(2*np.pi*freq*t)

# --- Métricas ---
def calcular_aceleracion_rms(t, x):
    dt = t[1] - t[0]
    a = np.gradient(np.gradient(x, dt), dt)
    return np.sqrt(np.mean(a**2))

def simular_escalon(m, c, k, t_sim=5.0, h=0.001):
    t_eval = np.arange(0, t_sim, h)
    sol = solve_ivp(
        quarter_car, [0, t_sim], [0, 0],
        args=(m, c, k, escalon, escalon_dot),
        t_eval=t_eval, method='RK45'
    )
    x = sol.y[0]
    rms = calcular_aceleracion_rms(sol.t, x)
    return sol.t, x, rms

def calcular_transmisibilidad(m, c, k, freqs=np.arange(1, 11), amp=0.01, t_sim=5.0, h=0.001):
    T_vals = []
    t_eval = np.arange(0, t_sim, h)
    for f in freqs:
        sol = solve_ivp(
            quarter_car, [0, t_sim], [0, 0],
            args=(m, c, k,
                  lambda t: seno(t, amp, f),
                  lambda t: seno_dot(t, amp, f)),
            t_eval=t_eval, method='RK45'
        )
        x = sol.y[0]
        tail = x[int((t_sim-2)/h):]  # últimos 2 segundos
        amp_out = (tail.max() - tail.min()) / 2
        T_vals.append(amp_out / amp)
    return freqs, np.array(T_vals)

# --- Búsqueda de parámetros óptimos ---
m = 250
k_vals = np.arange(10000, 20001, 1000)    # k: 10 000 → 20 000 N/m
c_vals = np.arange(1000, 5001, 200)       # c: 1 000 → 2 000 Ns/m

mejores = []
for k in k_vals:
    for c in c_vals:
        # simulación escalón
        t, x, rms = simular_escalon(m, c, k)
        # transmisibilidad
        freqs, T_vals = calcular_transmisibilidad(m, c, k)
        cumple_rms = (rms < 0.315)
        cumple_T   = np.all(T_vals < 1.2)
        if cumple_rms and cumple_T:
            # almacena (k, c, rms, T_max)
            mejores.append((k, c, rms, T_vals.max()))

# Selección de la mejor combinación (menor T_max)
if mejores:
    mejores.sort(key=lambda x: x[3])
    k_opt, c_opt, rms_opt, Topt = mejores[0]
    print(f"✅ Parámetros óptimos encontrados:\n  k = {k_opt} N/m\n  c = {c_opt} Ns/m")
    print(f"  RMS = {rms_opt:.4f} m/s²\n  T_max = {Topt:.2f}")
    
    # Graficar resultados finales
    # Escalón
    t, x, _ = simular_escalon(m, c_opt, k_opt)
    plt.figure()
    plt.plot(t, x*1000, label='Desplazamiento (mm)')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Desplazamiento (mm)')
    plt.title(f'Respuesta a escalón (k={k_opt}, c={c_opt})')
    plt.grid(); plt.legend()
    
    # Transmisibilidad
    freqs, T_vals = calcular_transmisibilidad(m, c_opt, k_opt)
    plt.figure()
    plt.plot(freqs, T_vals, 'o-', label='T(ω)')
    plt.axhline(1.2, color='r', ls='--', label='Límite 1.2')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Transmisibilidad')
    plt.title(f'Transmisibilidad (k={k_opt}, c={c_opt})')
    plt.grid(); plt.legend()
    
    plt.show()
else:
    print("No se encontró combinación (k,c) que cumpla ambos criterios.")
