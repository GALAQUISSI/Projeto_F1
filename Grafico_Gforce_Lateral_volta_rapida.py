'''''
Interpretação dos gráficos de força G

Azul = Lateral (força centrípeta nas curvas)

 - Mostra o quanto o carro e o piloto estão sendo empurrados para os lados durante curvas.
 - Valores altos indicam curvas rápidas e exigem muito do pescoço e tronco do piloto.
 - É útil para avaliar consistência de traçado e comparar entradas/saídas de curva entre voltas.

Verde = Longitudinal (aceleração e frenagem)

 - Picos positivos → aceleração (quando o piloto pisa fundo).
 - Picos negativos → frenagem (quando o piloto freia forte).
 - Permite analisar a eficiência da frenagem, se o piloto está retardando o ponto de freio ou acelerando cedo demais na saída da curva.

Vermelho = Vertical (força sobre o eixo vertical)

 - Relaciona-se com ondulações da pista, zebras e compressão da suspensão.
 - Ajuda a entender como o carro lida com irregularidades e se o piloto está explorando os limites da pista (por exemplo, passando agressivamente sobre zebras).

Como isso influencia a análise de desempenho

 - Consistência: comparar voltas rápidas para ver se o piloto mantém padrões semelhantes de forças G.
 - Estilo de pilotagem: alguns pilotos preferem frear mais cedo e suave (menor pico longitudinal), outros freiam mais tarde e forte.
 - Físico do piloto: forças laterais e longitudinais extremas exigem resistência muscular e podem impactar a performance em corridas longas.
 - Setup do carro: forças verticais ajudam engenheiros a ajustar suspensão e aerodinâmica para maximizar aderência sem comprometer conforto ou controle.

Em resumo:

 - Lateral (azul) → qualidade da curva.
 - Longitudinal (verde) → aceleração/frenagem.
 - Vertical (vermelho) → interação com pista e suspensão.
'''''

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

df = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa.csv')
df_copia = df.copy()

df_copia['last_lap_ms'] = df_copia['last_lap_ms'].shift(-1)
fastest_lap = df_copia[df_copia['last_lap_ms'] > 0]['last_lap_ms'].min()
lap_num = df_copia[df_copia['last_lap_ms'] == fastest_lap]['num_current_lap'].iloc[0]
#tem q filtrar o dataset antes
g_force_lateral = df_copia[df_copia['num_current_lap'] == lap_num]['g_force_lateral']
distancia = df_copia[df_copia['num_current_lap'] == lap_num]['lap_distance']
dist_max = distancia.max()
g_force_max = g_force_lateral.max()
g_force_min = g_force_lateral.min()

fig, ax = plt.subplots(figsize=(20,10), facecolor='black')
ax.set_facecolor('black')
ax.grid(True, linestyle = '--', linewidth = 0.5, alpha = 0.5)
ax.plot(distancia, g_force_lateral , color = 'blue', label = 'G_Force', linewidth = 2)
ax.set_xlabel('Distancia', color = 'white', fontsize = 14, labelpad = 10)
ax.set_xticks(np.linspace(0,dist_max,10))
ax.set_xticklabels([f"{int(x)}m" for x in np.linspace(0,dist_max,10)], color = 'white', fontsize = 12)
ax.set_ylabel('Força G Lateral', color = 'white', fontsize = 14, labelpad = 10)
ax.set_yticks(np.linspace(g_force_min,g_force_max,6))
ax.set_yticklabels([f'{int(x)}'for x in np.linspace(g_force_min,g_force_max,6)], color = 'white', fontsize = 12)
ax.set_title('Grafico Força G Lateral', fontsize = 20, color = 'white', pad = 10)
plt.legend()
plt.show()
