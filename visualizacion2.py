import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carga de datos
df = pd.read_csv('resultados_parametricos.csv')

# Pivot para heatmap de RMS
pivot_rms = df.pivot(index='c [N·s/m]', columns='k [N/m]', values='RMS [m/s^2]')

# Gráfico de mapa de calor para RMS
plt.figure(figsize=(6, 5))
sns.heatmap(pivot_rms, annot=False, cmap='viridis')
plt.title('Mapa de calor de RMS')
plt.xlabel('k [N/m]')
plt.ylabel('c [N·s/m]')
plt.tight_layout()
plt.show()