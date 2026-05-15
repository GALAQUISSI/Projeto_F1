import pandas as pd

df = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa.csv')

#grafico de vel x dist volta

#copiar para nao alterar o df_original
df_copia = df.copy()

#alinhar voltas -> nao alinhei por colunas de novo pqp
df_copia['last_lap_ms'] = df_copia['last_lap_ms'].shift(-1)

#selecionar volta mais rapida e volta associada a ela
fast_lap = df_copia[df_copia['last_lap_ms'] > 0]['last_lap_ms'].min()
num_lap = df_copia[df_copia['last_lap_ms'] == fast_lap].iloc[0]['num_current_lap']

#selecionar distancia lap
distancia = df_copia[df_copia['num_current_lap'] == num_lap]['lap_distance']
velocidade = df_copia[df_copia['num_current_lap'] == num_lap]['velocidade']

import matplotlib.pyplot as plt
import numpy as np

#definir figura
fig, ax = plt.subplots(figsize=(15,10), facecolor = 'black')
ax.set_facecolor('black')

dist_max = distancia.max() #pega o maior valor para dividir em partes iguais

#definir setores de acordo com o dataset
# eu so quero saber onde acaba e onde começa independe ta volta
#df_volta_setores = df_copia[df_copia['num_current_lap'] == num_lap].copy()
#idx = df_volta_setores['setor1_ms'].idxmax()
#s1 = df_volta_setores.loc[idx, 'lap_distance']
#print(s1)


ax.plot(distancia, velocidade, color = 'blue', linestyle = '-', linewidth = 2, label = 'Velocidade')
ax.grid(True, color = 'white', linestyle = '--', linewidth = 1,alpha = 0.5)
ax.set_xlabel('Distância',labelpad= 10, fontsize = 12, color = 'white')
ax.set_xticks(np.linspace(0,dist_max,10))
ax.set_xticklabels([f"{int(x)}m" for x in np.linspace(0,dist_max,10)], fontsize = 12, color = 'white')
ax.set_ylabel('Velocidade',labelpad= 10, fontsize = 12, color = 'white')
ax.set_yticks(np.linspace(min(velocidade),max(velocidade),6))
ax.set_yticklabels([f"{int(y)}Km" for y in np.linspace(min(velocidade),max(velocidade),6)], fontsize = 12, color = 'white')
ax.set_title('Gráfico Velocidade Volta Rápida', fontsize = 20, pad = 10, color = 'white')
plt.legend()
plt.show()
