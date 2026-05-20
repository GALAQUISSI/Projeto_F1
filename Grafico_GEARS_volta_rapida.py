import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa.csv')

df_copia = df.copy()

df_copia['last_lap_ms'] = df_copia['last_lap_ms'].shift(-1)
fastest_lap = df_copia[df_copia['last_lap_ms'] > 0]['last_lap_ms'].min()
lap_num = df_copia[df_copia['last_lap_ms'] == fastest_lap]['num_current_lap'].iloc[0]

gears = df_copia[df_copia['num_current_lap'] == lap_num]['marcha']
distancia = df_copia[df_copia['num_current_lap'] == lap_num]['lap_distance']
dist_max = distancia.max()

import numpy as np
#definindo pontos do y
y_points = np.array([2,3,6,8])

fig, ax = plt.subplots(figsize=(20,10), facecolor = 'black')
ax.set_facecolor('black')
ax.grid(True, linestyle='--',linewidth=1, alpha=0.5)
ax.plot(distancia,gears, linestyle='-', linewidth=2,color='blue', label = 'Gears')
#definir os pontos da metragem utilizando a função para dividir em 10 pontos, pegando o intervalo [0 -> dist_max (4291.xxxx)]
ax.set_xlabel('Distancia', color = 'white', labelpad = 10, fontsize = 14)
ax.set_xticks(np.linspace(0,dist_max,10))
ax.set_xticklabels([f'{int(x)}m'for x in np.linspace(0,dist_max,10)], color = 'white', fontsize = 12)
ax.set_ylabel('Gears', color = 'white', labelpad = 10, fontsize = 14)
ax.set_yticks(y_points)
ax.set_yticklabels(y_points, color = 'white', fontsize = 12)
ax.set_title('Grafico Marchas Volta Rapida', fontsize = 20, color = 'white', pad = 10)
plt.legend()
plt.show()
