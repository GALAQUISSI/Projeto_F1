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

#otimizar xlabel
voltas = df['num_current_lap'].unique()

#tamanho da imagem
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize = (12,6))

#trocar nome da legenda, esta mal legivel e ver o que melhorar no grafico

ax.plot(fl_tyre['num_current_lap'], fl_tyre['fl_tyre_wear'], label = 'FL_tyre', linewidth = 2)
ax.plot(fr_tyre['num_current_lap'], fr_tyre['fr_tyre_wear'], label = 'FR_tyre', linewidth = 2)
ax.plot(rl_tyre['num_current_lap'], rl_tyre['rl_tyre_wear'], label = 'RL_tyre', linewidth = 2)
ax.plot(rr_tyre['num_current_lap'], rr_tyre['rr_tyre_wear'], label = 'RR_tyre', linewidth = 2)

ax.grid(True, color = 'white', linestyle = '--', linewidth = 1, alpha = 0.2)
ax.axvline(pit_stop[0], linestyle = ':', color = 'red', label = 'Pit_stop', linewidth = 1, alpha = 0.7)
ax.axvline(pit_stop[1], linestyle = ':', color = 'red', linewidth = 1, alpha = 0.5)
ax.set_xticks(voltas)
ax.set_title('Desgaste Pneu', color='white', fontsize = 20, fontweight = 'bold', pad = 10)
ax.set_xlabel('Voltas', color='white', fontsize = 14, labelpad = 10)
ax.set_ylabel('Desgaste (%)', color='white', fontsize = 14, labelpad = 10)

ax.spines['top'].set_visible(False)
plt.legend()
plt.show()

'''''
FORMA ANTIGA DE PLOTAR O GRÁFICO

plt.figure(figsize=(10,6))
#definindo fundo
#sns.set_theme(style = 'darkgrid') -> tema generico, para alterar tem colocar de outra forma
#tem que colocar com base no matplotlib
sns.set_style(style='darkgrid', rc={'grid.linestyle': '--', 'grid.color' : 'white', 'grid.alpha' : 0.2})

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
'''''