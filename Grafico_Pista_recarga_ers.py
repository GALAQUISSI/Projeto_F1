#fazer grafico de pista onde eu veja os pontos onde mais recolhi energia
import pandas as pd
import numpy as np

df = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa.csv')

#gerar copia
df_alinhado = df.copy()

#alinhar o dataset para que os dados de volta esteja na volta correta
df_alinhado['last_lap_ms'] = df_alinhado["last_lap_ms"].shift(-1)

#tinha errado qual coluna deve receber o shift, ou seja se eu colocar o dataset = mudança na colunax errado, deve ser:
#dataset[colunax] = dataset[colunax]mudança

#para filtrar a volta mais rapida tenho que identificar ela
fastest_lap = df_alinhado[df_alinhado["last_lap_ms"] > 0]['last_lap_ms'].min()
#ou seja eu criei uma mascara onde so pego da coluna valores maiores que 0 e depois o minimo dessa coluna
#o minimo seria o tempo mais rapido

#agora eu tenho que pegar a volta que representa esse valor
lap_num = df_alinhado[df_alinhado["last_lap_ms"] == fastest_lap]['num_current_lap'].iloc[0]

#novo dataset para receber filtros
df_grafico = df_alinhado[df_alinhado['num_current_lap'] == lap_num]

#adicionar coluna para calculo total de ers recharged na volta
df_grafico['total_recharge_ers'] = df_grafico['ers_harvested_thislap_MGUH'] + df_grafico['ers_harvested_thislap_MGUK']
#transformando em %
df_grafico['total_recharge_ers'] = (df_grafico['total_recharge_ers'] / 4000000) * 100

#agora como gerar o grafico, eu tenho que usar linecollection de matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

#definir variaveis
x = df_grafico['space_world_positionX']
y = df_grafico['space_world_positionZ']
ers = df_grafico['total_recharge_ers']

#fazer segmentação e junção dos pontos a partir das coordenadas
points = np.array([x,y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
#explicação detalhada func.matriz no caderno

#definindo tamanho da figura e cor de fundo
fig, ax = plt.subplots(figsize=(20,10), facecolor = 'black')
ax.set_facecolor('black')

#normalizao de valores para intervalo 0-1
norm = plt.Normalize(ers.min(), ers.max())

#criação das linhas (segments),padrão de cores (magma) e a normalização (norm)
lines = LineCollection(segments, cmap='magma', norm=norm)

#essa função associa cada valor a uma cor e um segmento da pista (cada coordenada)
lines.set_array(ers)
lines.set_linewidth(10) #espessura da linha
line = ax.add_collection(lines) #adicionar linhas ao grafico

#continuar e revisar plot




