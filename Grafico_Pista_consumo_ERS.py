import pandas as pd
import numpy as np

#eu quero criar um grafico da pista, da volta mais rapida, logo tenho q selecionar a volta mais rapida
#poderia embutir meu traçado tambem na pista seria bom para visualizar

df = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa.csv')

#copia do dataset
df_alinhado = df.copy()

#consegui fazer o shift na copia
df_alinhado['last_lap_ms'] = df_alinhado['last_lap_ms'].shift(-1)

#agora tenho que filtrar apenas as linhas onde é a volta mais rapida

#tempo da volta mais rapida
fastest_lap = df_alinhado[df_alinhado['last_lap_ms'] > 0]['last_lap_ms'].min()

#volta mais rapida
num_volta_fast = df_alinhado[df_alinhado['last_lap_ms'] == fastest_lap].iloc[0]

#gerando dataset para grafico
#tem q colocar o .copy() para ele ir como um objeto
df_grafico = df_alinhado[df_alinhado['num_current_lap'] == num_volta_fast['num_current_lap']].copy()

#print(fastest_lap)
#print(num_volta_fast['num_current_lap'])
#print(df_grafico.shape)

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

#definindo as variaveis para o grafico

x = df_grafico['space_world_positionX']
y = df_grafico['space_world_positionZ']
ers = df_grafico['ers_battery %']

#segmentação da linha
#padrao linecollection
points = np.array([x,y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

fig, ax = plt.subplots(figsize=(15, 10), facecolor='black')
ax.set_facecolor('black')

norm = plt.Normalize(ers.min(), ers.max())
lc = LineCollection(segments, cmap='viridis', norm=norm)

lc.set_array(ers)
lc.set_linewidth(10)

line = ax.add_collection(lc)

ax.set_xlim(x.min() - 50, x.max() + 50)
ax.set_ylim(y.min() - 50, y.max() + 50)

ax.set_aspect('equal')
ax.axis('off')
ax.invert_yaxis()

cbar = fig.colorbar(line, ax=ax)
cbar.set_label('ERS Battery %', color='white', size=14, labelpad=12)
cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white')

plt.title(f'Interlagos - Mapa de Calor ERS (Volta Mais Rápida)', color='white', size=18, pad = 10)
plt.show()

