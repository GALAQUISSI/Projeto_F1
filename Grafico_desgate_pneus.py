#grafico de desgate de pneu ao longo da corrida

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import lineStyles

df = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa.csv')

fl_tyre = df.groupby('num_current_lap')['fl_tyre_wear'].last().reset_index()
#estou agrupando por valores unicos na coluna num_current_lap
#pq para cada volta tem x dados, e eu preciso de gerar 1 linha
#nisso, eu uso .last() pq como é acumulativo o dado de desgate, o ultimo é o total do desgaste na volta
#o uso de reset_index se da que eu preciso de num_current_lap como coluna e nao indice
fr_tyre = df.groupby('num_current_lap')['fr_tyre_wear'].last().reset_index()
rl_tyre = df.groupby('num_current_lap')['rl_tyre_wear'].last().reset_index()
rr_tyre = df.groupby('num_current_lap')['rr_tyre_wear'].last().reset_index()

#adicionar linha do pitstop, linha vertical onde pit_status = 1
pit_stop = df.loc[df['pit_status'] == 1, 'num_current_lap'].unique()
#.unique() faz com que pegue so o valor 1 vez ao inves de diversas vezes repetidas

#tamanho da imagem
plt.figure(figsize=(10,6))
#definindo fundo
#sns.set_theme(style = 'darkgrid') -> tema generico, para alterar tem colocar de outra forma
#tem que colocar com base no matplotlib
sns.set_style(style='darkgrid', rc={'grid.linestyle': '--', 'grid.color' : '1.0', 'grid.alpha' : 0.5})

#como mostrar esse grafico agora
plt.plot(fl_tyre['num_current_lap'], fl_tyre['fl_tyre_wear'], label = 'FL_tyre', linewidth = 2)
plt.plot(fr_tyre['num_current_lap'], fr_tyre['fr_tyre_wear'], label = 'FR_tyre', linewidth = 2)
plt.plot(rl_tyre['num_current_lap'], rl_tyre['rl_tyre_wear'], label = 'RL_tyre', linewidth = 2)
plt.plot(rr_tyre['num_current_lap'], rr_tyre['rr_tyre_wear'], label = 'RR_tyre', linewidth = 2)
plt.axvline(pit_stop[0], linestyle = ':', color = 'red', label = 'Pit_stop', linewidth = 2)
plt.axvline(pit_stop[1], linestyle = ':', color = 'red', linewidth = 2)
plt.xticks(df['num_current_lap'])
plt.xlabel('Lap')
plt.ylabel('Wear %')
plt.legend()
plt.show()