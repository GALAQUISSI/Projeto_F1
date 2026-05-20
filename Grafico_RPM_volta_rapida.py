import pandas as pd

df = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa.csv')

df_copia = df.copy()

df_copia['last_lap_ms'] = df_copia['last_lap_ms'].shift(-1)
fastest_lap = df_copia[df_copia['last_lap_ms'] > 0]['last_lap_ms'].min()
lap_num = df_copia[df_copia['last_lap_ms'] == fastest_lap]['num_current_lap'].iloc[0]

rpm = df_copia[df_copia['num_current_lap'] == lap_num]['rpm']
distancia = df_copia[df_copia['num_current_lap'] == lap_num]['lap_distance']

from matplotlib import pyplot as plt
import numpy as np

dist_max = distancia.max() #deu Nan?
fig,ax = plt.subplots(figsize=(30,10), facecolor = 'black')
ax.set_facecolor('black')
ax.grid(True, linestyle = '--', linewidth = 1, alpha = 0.5)
ax.plot(distancia, rpm, linestyle='-', linewidth=2, color='blue', label='RPM')
ax.set_xlabel('Distancia', fontsize = 14, color = 'white', labelpad = 10)
ax.set_xticks(np.linspace(0,dist_max, 10))
ax.set_xticklabels([f'{int(x)}m' for x in np.linspace(0,dist_max,10)], color = 'white', fontsize = 12)
ax.set_ylabel('RPM', fontsize = 14, color = 'white', labelpad = 10)
#quero colocar o rpm minimo e max
rpm_max = rpm.max()
ax.set_yticks(np.linspace(min(rpm), max(rpm), 4))
ax.set_yticklabels([f'{int(x)}'for x in np.linspace(min(rpm), max(rpm), 4)],color = 'white', fontsize = 12)
ax.set_title('Grafico RPM', fontsize = 20, color = 'white', pad = 10)
plt.legend()#tem como colocar em qual ponto a legenda vai aparecer
plt.show()

