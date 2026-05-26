from shutil import which

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

df = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa.csv')

df_copia = df.copy()

df_copia['last_lap_ms'] = df_copia['last_lap_ms'].shift(-1)
fast_lap = df_copia[df_copia['last_lap_ms'] > 0]['last_lap_ms'].min()
lap_num = df_copia[df_copia['last_lap_ms'] == fast_lap]['num_current_lap'].iloc[0]

distancia = df_copia[df_copia['num_current_lap'] == lap_num]['lap_distance']
g_force = df_copia[df_copia['num_current_lap'] == lap_num]['g_force_longitudinal']

distancia_max = distancia.max()
g_force_max = g_force.max()
g_f_mx_round = round(g_force_max, 2)
g_force_min = g_force.min()
g_f_mn_round = round(g_force_min, 2)
g_f_med = np.median(g_force)
g_f_med_round = round(g_f_med, 2)

ylabels = np.array([g_f_mn_round, g_f_med_round, g_f_mx_round])

fig, ax = plt.subplots(figsize = (20,10), facecolor = 'black')
ax.set_facecolor('black')
ax.grid(True, linewidth = 1, linestyle = '--', alpha = 0.5)
ax.plot(distancia, g_force, color = 'blue', linewidth = 2, label = 'Força G')
ax.set_xlabel('Distancia', color = 'white', fontsize = 14, labelpad = 10)
ax.set_xticks(np.linspace(0, distancia_max, num = 10))
ax.set_xticklabels([f'{int(x)}m'for x in np.linspace(0, distancia_max, num = 10)], color = 'white', fontsize = 12)
ax.set_ylabel('Força G', color = 'white', fontsize = 14, labelpad = 10)
ax.set_yticks(ylabels)
ax.set_yticklabels([f'{float(x)} G'for x in ylabels], color = 'white', fontsize = 12)
ax.set_title('Grafico Força G Longitudinal', fontsize = 20, fontweight = 'bold', pad = 10, color = 'white')
ax.legend()
plt.show()

#print(g_f_mn_round, g_f_mx_round, g_f_med_round) #-4.2, 1.37, 0.32