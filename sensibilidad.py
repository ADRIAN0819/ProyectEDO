import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Cargar los resultados paramétricos
df = pd.read_csv('resultados_parametricos.csv')

# 2. Identificar el par óptimo (mínimo T_max entre los válidos)
df_validos = df[(df['Cumple_RMS']) & (df['Cumple_T'])]
opt_row   = df_validos.loc[df_validos['T_max'].idxmin()]
k_opt     = opt_row['k [N/m]']
c_opt     = opt_row['c [N·s/m]']

print(f"Par óptimo hallado: k = {k_opt} N/m, c = {c_opt} N·s/m")

# 3. Definir rango de c para sensibilidad ±10%
cs = np.linspace(c_opt * 0.9, c_opt * 1.1, 11)

# 4. Extraer RMS y T_max para cada c desde el DataFrame original
sens_records = []
df_k = df[df['k [N/m]']==k_opt].set_index('c [N·s/m]')

for c in cs:
    # redondear al paso de c usado en el CSV (200 Ns/m)
    c_rounded = float(round(c/200))*200
    if c_rounded in df_k.index:
        rms   = df_k.loc[c_rounded, 'RMS [m/s^2]']
        tmax  = df_k.loc[c_rounded, 'T_max']
    else:
        rms, tmax = np.nan, np.nan  # fuera de malla original
    sens_records.append({'c':c_rounded, 'RMS':rms, 'T_max':tmax})

df_sens = pd.DataFrame(sens_records).dropna()

# 5. Guardar a CSV
df_sens.to_csv('sensibilidad_optimo.csv', index=False)
print("Sensibilidad guardada en 'sensibilidad_optimo.csv':")
print(df_sens)

# 6. Graficar
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,4))

ax1.plot(df_sens['c'], df_sens['RMS'], marker='o')
ax1.axhline(0.315, color='r', linestyle='--', label='Límite RMS')
ax1.set_xlabel('c [N·s/m]')
ax1.set_ylabel('RMS [m/s²]')
ax1.set_title('Sensibilidad de RMS (k={} N/m)'.format(int(k_opt)))
ax1.legend(); ax1.grid(True)

ax2.plot(df_sens['c'], df_sens['T_max'], marker='o')
ax2.axhline(1.2, color='r', linestyle='--', label='Límite T_max')
ax2.set_xlabel('c [N·s/m]')
ax2.set_ylabel('T_max')
ax2.set_title('Sensibilidad de T_max (k={} N/m)'.format(int(k_opt)))
ax2.legend(); ax2.grid(True)

plt.tight_layout()
plt.show()
