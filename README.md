# ProyectEDO
Proyecto de ecuaciones diferenciales 2025-1 modelo quartercar solucion smulado RK5 analitica 

## `comp_sine_overlay.py`

| Elemento | Descripción |
|----------|-------------|
| **Propósito** | Comparar, en una misma gráfica, la respuesta analítica (Laplace) y la numérica (RK4) ante una **excitación senoidal** de 10 mm a 4 Hz. |
| **Entradas clave** | `m`, `c_nom`, `k_nom` – parámetros nominales (250 kg, 1000 Ns/m, 15 000 N/m).<br>`amp_sine`, `f_sine` – amplitud y frecuencia de la pista senoidal. |
| **Funciones internas** | `rk4_step`, `integrate_rk4` – paso e integración RK4 de tamaño fijo.<br>`analytic_sine_response` – fórmula cerrada de la respuesta forzada con $x(0)=v(0)=0$. |
| **Flujo** | 1. Genera la malla temporal (1 ms).<br>2. Integra con RK4.<br>3. Evalúa la solución analítica.<br>4. Dibuja ambas curvas. |
| **Salida** | `comp_sine_overlay.pdf` (superposición Analítica vs RK4). |

---

## `comp_step_overlay.py`

| Elemento | Descripción |
|----------|-------------|
| **Propósito** | Verificar la coincidencia analítica–numérica ante un **escalón** vertical de 5 mm. |
| **Diferencia respecto al script senoidal** | Cambia la entrada `xg_step_func` y la rutina analítica `analytic_step_response`, que gestiona los tres regímenes de amortiguamiento. |
| **Salida** | `comp_step_overlay.pdf` (respuesta al escalón – Analítica vs RK4). |

---

## `error_heatmap.py`

| Elemento | Descripción |
|----------|-------------|
| **Propósito** | Mapear en un **heat-map** el error relativo entre RK4 (h = 1 ms) y la solución analítica del escalón para una malla de rigidez $k$ y amortiguamiento $c$. |
| **Malla de parámetros** | $k \in [5, 16]\,\text{kN/m}$ (8 puntos)<br>$c \in [1, 5]\,\text{kNs/m}$ (8 puntos) |
| **Cálculo del error** | Norma-2: $\displaystyle \frac{\lVert x_{\text{num}} - x_{\text{ref}}\rVert}{\lVert x_{\text{ref}}\rVert}\times 100$ %. |
| **Visualización** | `imshow` con barra de color; ejes etiquetados en unidades SI. |
| **Salida** | `error_heatmap.pdf` (matriz de error relativo). |

---

## `generar_resultados_parametricos.py`

| Elemento | Descripción |
|----------|-------------|
| **Propósito** | Ejecutar un **barrido paramétrico** sobre rigidez $k$ y amortiguamiento $c$ para el modelo quarter-car, evaluando dos métricas: aceleración RMS frente a un escalón (ISO 2631-1) y transmisibilidad máxima $T_{\max}$ frente a senos de 1–10 Hz. |
| **Rango de barrido** | $k \in [8{\,000},25{\,000}]\,\text{N/m}$ (paso 1 000).<br>$c \in [1{\,000},5{\,000}]\,\text{N·s/m}$ (paso 200). |
| **Método numérico** | `solve_ivp(method="RK45")` (paso adaptativo, tolerancias por defecto). |
| **Salidas** | `resultados_parametricos.xlsx` + `resultados_parametricos.csv`, con 6 columnas por combinación:<br>  – $k$, $c$<br>  – RMS [m/s²], $T_{\max}$<br>  – flags lógicos `Cumple_RMS`, `Cumple_T`. |

---

## `rk4.py`

| Elemento | Descripción |
|----------|-------------|
| **Propósito** | Búsqueda rápida de **parámetros óptimos** dentro de sub-rangos ($k\!=\!10$–20 kN/m, $c\!=\!1$–5 kN·s/m) usando la misma lógica de evaluación pero con **RK45** explícito para la simulación en línea. |
| **Criterio de selección** | Se acepta la pareja \((k,c)\) si:<br>  – RMS $<0.315$ m/s²<br>  – $\max T(\omega)<1.2$.<br>La mejor se elige por el menor $T_{\max}$. |
| **Visualizaciones** | 1. Desplazamiento ante escalón para \((k_{\text{opt}},c_{\text{opt}})\).<br>2. Curva $T(\omega)$ con límite 1.2. |
| **Salida por consola** | Imprime el par óptimo y sus métricas. |

---

## `sensibilidad.py`

| Elemento | Descripción |
|----------|-------------|
| **Propósito** | Analizar la **sensibilidad** de las métricas en torno al par óptimo variando $c$ ± 10 % (con $k$ fijo). |
| **Entrada** | `resultados_parametricos.csv` generado por el barrido global. |
| **Salida** | `sensibilidad_optimo.csv` con columnas $c$, RMS y $T_{\max}$.<br>Dos figuras: RMS vs $c$ y $T_{\max}$ vs $c$ con sus límites normativos. |

---

## `visualizacion.py`

| Elemento | Descripción |
|----------|-------------|
| **Propósito** | Crear un **heat-map** de $T_{\max}$ en el plano $(k,c)$ y listar por pantalla las combinaciones que cumplen simultáneamente ambos criterios. |
| **Datos fuente** | `resultados_parametricos.csv`. |
| **Bibliotecas** | `seaborn` (para el mapa de calor). |
| **Salida** | Ventana con el mapa de calor “T_max”, sin archivo persistente. |

---

## `visualizacion2.py`

| Elemento | Descripción |
|----------|-------------|
| **Propósito** | Generar el **heat-map** equivalente pero para la aceleración RMS. |
| **Datos y flujo** | Idénticos a `visualizacion.py`, cambiando la variable pivot (`RMS [m/s^2]`). |
| **Salida** | Ventana con el mapa de calor “RMS”. |

---

## Cómo ejecutar

```bash
# Activar entorno
python -m venv .venv && source .venv/bin/activate
pip install numpy matplotlib

# Generar figuras
python comp_sine_overlay.py
python comp_step_overlay.py
python error_heatmap.py
