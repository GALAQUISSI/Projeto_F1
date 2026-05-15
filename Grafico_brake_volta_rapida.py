import pandas as pd

df = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa.csv')

df_cop = df.copy()

#alinhar dados para selecionar volta correta
df_cop['last_lap_ms'] = df_cop['last_lap_ms'].shift(-1)
fastest_time = df_cop[df_cop['last_lap_ms'] > 0]['last_lap_ms'].min()
num_lap = df_cop[df_cop['last_lap_ms'] == fastest_time].iloc[0]['num_current_lap']
#brake esta em porcentagem
brake = df_cop[df_cop['num_current_lap'] == num_lap]['freio']

distance = df_cop[df_cop['num_current_lap'] == num_lap]['lap_distance']

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize = (15,10), facecolor = 'black')
ax.set_facecolor('black')
#definir x, y
ax.plot(distance, brake, color = 'blue', linewidth = 2, linestyle = '-', label = 'Brake')
dist_max = distance.max() #pega o maior valor para dividir em partes iguais
ax.grid(True, linestyle = '--', linewidth = 1, color = 'white', alpha = 0.3)
ax.set_xlabel('Distância',labelpad= 10, fontsize = 12, color = 'white', alpha = 0.3)
ax.set_xticks(np.linspace(0,dist_max,10))
ax.set_xticklabels([f"{int(x)}m" for x in np.linspace(0,dist_max,10)], fontsize = 12, color = 'white')
ax.set_ylabel('Velocidade',labelpad= 10, fontsize = 12, color = 'white')
ax.set_yticks(np.linspace(min(brake),max(brake),6))
ax.set_yticklabels([f"{int(y)}%" for y in np.linspace(min(brake),max(brake),6)], fontsize = 12, color = 'white')
ax.set_title('Gráfico Velocidade Volta Rápida', fontsize = 20, pad = 10, color = 'white')

plt.legend()
plt.show()