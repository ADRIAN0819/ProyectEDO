import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carga de datos
df = pd.read_csv('resultados_parametricos.csv')

# Filtrado de combinaciones válidas
validas = df[(df['Cumple_RMS']) & (df['Cumple_T'])]
print("Combinaciones válidas:")
print(validas)

# Preparar pivot para heatmap
pivot = df.pivot(index='c [N·s/m]', columns='k [N/m]', values='T_max')

# Gráfico de mapa de calor
plt.figure(figsize=(6, 5))
sns.heatmap(pivot, annot=False, cmap='viridis')
plt.title('Mapa de calor de T_max')
plt.xlabel('k [N/m]')
plt.ylabel('c [N·s/m]')
plt.tight_layout()
plt.show()
