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
| **Cálculo del error** | Norma 2: $\lVert x_\text{num}-x_\text{ref}\rVert \ /\ \lVert x_\text{ref}\rVert$ en %. |
| **Visualización** | `imshow` con barra de color; ejes etiquetados en unidades SI. |
| **Salida** | `error_heatmap.pdf` (matriz de error relativo). |

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
