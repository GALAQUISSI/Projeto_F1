import pandas as pd

df = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa.csv')

df_copy = df.copy()

#alinhar o df_copy, usando shift -1, selecionar o tempo mais rapido e depois a volta relacionada a esse tempo
df_copy['last_lap_ms'] = df_copy['last_lap_ms'].shift(-1)
fastest_lap = df_copy[df_copy['last_lap_ms'] > 0]['last_lap_ms'].min()
num_lap = df_copy[df_copy['last_lap_ms'] == fastest_lap]['num_current_lap'].iloc[0]

#feito a seleção da volta mais rapida agr é selecionar as caracteristicas para o grafico
#throttle x distancia
throttle = df_copy[df_copy['num_current_lap'] == num_lap]['acelerador']
distancia = df_copy[df_copy['num_current_lap'] == num_lap]['lap_distance']

from matplotlib import pyplot as plt
import numpy as np

dist_max = distancia.max()
thr_max = throttle.max()

fig, ax = plt.subplots(figsize=(20,10), facecolor = 'black')
ax.set_facecolor('black')
ax.grid(True, linestyle = '--', linewidth = 1, alpha = 0.5)
ax.plot(distancia, throttle, label = 'throttle', linewidth = 2, color = 'blue')
ax.set_xlabel('Distancia', fontsize = 14, color = 'white', labelpad = 10)
ax.set_xticks(np.linspace(0,dist_max, 10))
ax.set_xticklabels([f'{int(x)}m' for x in np.linspace(0,dist_max, 10)], fontsize = 12, color = 'white')
ax.set_ylabel('Throttle', fontsize = 14, color = 'white', labelpad = 10)
ax.set_yticks(np.linspace(0,thr_max,6))
ax.set_yticklabels([f'{int (x)}%' for x in np.linspace(0,thr_max, 6)], fontsize = 12, color = 'white')
ax.set_title('Throttle', fontsize = 20, color = 'white', pad = 10)

plt.legend()
plt.show()
