import pandas as pd
from matplotlib import pyplot as plt

#observação: a volta rapida na corrida foi feita sem drs

df = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa.csv')

df_copia = df.copy()

df_copia['last_lap_ms'] = df_copia['last_lap_ms'].shift(-1)
faste_lap = df_copia[df_copia['last_lap_ms'] > 0]['last_lap_ms'].min()
num_lap = df_copia[df_copia['last_lap_ms'] == faste_lap]['num_current_lap'].iloc[0]

drs = df_copia[df_copia['num_current_lap'] == num_lap]['drs']
distancia = df_copia[df_copia['num_current_lap'] == num_lap]['lap_distance']
dist_max = distancia.max()

import numpy as np

drs_label = np.array([0,1])

fig, ax = plt.subplots(figsize=(20,10), facecolor = 'black')
ax.set_facecolor('black')
ax.grid(linestyle='--', linewidth=1, alpha = 0.5)
ax.plot(distancia, drs, color = 'blue', label = 'Drs', linewidth = 2)
ax.set_xlabel('Distancia', fontsize = 15, color='white', labelpad=10)
ax.set_xticks(np.linspace(0,dist_max,10))
ax.set_xticklabels([f'{int(x)}' for x in np.linspace(0,dist_max, 10)], color = 'white', fontsize = 12)
ax.set_ylabel('DRS (on/off)', fontsize = 15, color ='white', labelpad = 10)
ax.set_yticks(drs_label)
ax.set_yticklabels(drs_label, color = 'white', fontsize = 12)
ax.set_title('DRS Volta Rápida', fontsize = 20, color='white', fontweight = 'bold', pad = 10)
ax.legend()
plt.show()