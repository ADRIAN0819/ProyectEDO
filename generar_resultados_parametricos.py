# generar_resultados_parametricos.py

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

# Modelo Quarter-Car
def quarter_car(t, y, m, c, k, xg_func, xg_dot_func):
    x, v = y
    xg = xg_func(t)
    xg_dot = xg_dot_func(t)
    dxdt = v
    dvdt = (-c*(v - xg_dot) - k*(x - xg)) / m
    return [dxdt, dvdt]

# Señales de entrada
def escalon(t, magnitud=0.005):
    return magnitud if t >= 0 else 0

def escalon_dot(t, magnitud=0.005):
    return 0

def seno(t, amp, freq):
    return amp * np.sin(2 * np.pi * freq * t)

def seno_dot(t, amp, freq):
    return amp * 2 * np.pi * freq * np.cos(2 * np.pi * freq * t)

# Métricas
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
    return rms

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
        tail = x[int((t_sim - 2)/h):]  # últimos 2 segundos
        amp_out = (tail.max() - tail.min()) / 2
        T_vals.append(amp_out / amp)
    return max(T_vals)

# Barrido paramétrico y exportación a Excel
def main():
    m = 250
    k_vals = np.arange(8000, 25001, 1000)
    c_vals = np.arange(1000, 5001, 200)

    records = []
    for k in k_vals:
        for c in c_vals:
            rms = simular_escalon(m, c, k)
            T_max = calcular_transmisibilidad(m, c, k)
            cumple_rms = rms < 0.315
            cumple_T = T_max < 1.2
            records.append({
                'k [N/m]': k,
                'c [N·s/m]': c,
                'RMS [m/s^2]': rms,
                'T_max': T_max,
                'Cumple_RMS': cumple_rms,
                'Cumple_T': cumple_T
            })

    df = pd.DataFrame(records)
    df.to_excel('resultados_parametricos.xlsx', index=False)
    df.to_csv('resultados_parametricos.csv', index=False)
    print("Archivos 'resultados_parametricos.xlsx' y 'resultados_parametricos.csv' generados con éxito.")

if __name__ == "__main__":
    main()