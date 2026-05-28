import pandas as pd
import numpy as np

df = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa.csv')

df_copia = df.copy()

df_copia['last_lap_ms'] = df_copia['last_lap_ms'].shift(-1)
fast_lap = df_copia[df_copia['last_lap_ms'] > 0]['last_lap_ms'].min()
lap_num = df_copia[df_copia['last_lap_ms'] == fast_lap]['num_current_lap'].iloc[0]

distancia = df_copia[df_copia['num_current_lap'] == lap_num]['lap_distance']
g_force_l = df_copia[df_copia['num_current_lap'] == lap_num]['g_force_longitudinal']
g_force_lt = df_copia[df_copia['num_current_lap'] == lap_num]['g_force_lateral']
g_force_v = df_copia[df_copia['num_current_lap'] == lap_num]['g_force_vertical']

distancia_max = distancia.max()

g_force_l_mx = round(g_force_l.max(), 2)
g_force_v_mx = round(g_force_v.max(),2)
g_force_lt_mx = round(g_force_lt.max(),2)


g_force_lt_mn = round(g_force_lt.min(),2)
g_force_v_mn = round(g_force_v.min(),2)
g_force_l_mn = round(g_force_l.min(), 2)

values_max_g = np.array([g_force_l_mx, g_force_v_mx, g_force_lt_mx])
values_min_g = np.array([g_force_l_mn, g_force_v_mn, g_force_lt_mn])

max_g = values_max_g.max()
min_g = values_min_g.min()

middle_g = np.median(values_max_g + values_min_g)
middle_g_round = round(middle_g,2)

y_label = np.array([min_g, middle_g_round, max_g])

from matplotlib import pyplot as plt

fig, ax = plt.subplots(figsize=(20,10), facecolor = 'black')
ax.set_facecolor('black')
ax.grid(True, linestyle = '--', linewidth = 1, alpha = 0.5)
ax.plot(distancia, g_force_l, color = 'blue', linewidth = 2, label = 'Longitudinal')
ax.plot(distancia, g_force_v, color = 'red', linewidth = 2, label = 'Vertical')
ax.plot(distancia, g_force_lt, color = 'green', linewidth = 2, label = 'Lateral')

ax.set_xlabel('Distancia', fontsize = 14, labelpad = 10, color = 'white')
ax.set_xticks(np.linspace(0, distancia_max, 10))
ax.set_xticklabels([f'{int(x)}m' for x in np.linspace(0, distancia_max, 10)], fontsize = 12, color = 'white')
ax.set_ylabel('Força G', fontsize = 14, labelpad = 10, color = 'white')
ax.set_yticks(y_label)
ax.set_yticklabels([f'{float(x)} G'for x in y_label], fontsize = 12, color = 'white')
ax.set_title('Grafico Força G', color = 'white', pad = 10, fontsize = 20, fontweight = 'bold')

ax.legend(fontsize = 14, loc = 'upper right')
plt.show()