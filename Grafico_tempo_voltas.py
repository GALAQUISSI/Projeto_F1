import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

df = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa.csv')

#como agrupar voltas e o tempo total da volta

mapa_cores = {
    16: '#ff3333', # Soft (Vermelho)
    17: '#ffde21', # Medium (Amarelo)
    18: '#ebebeb', # Hard (Branco/Cinza claro)
    7:  '#33ff33', # Inter (Verde)
    8:  '#3333ff'  # Wet (Azul)
}
#adicionei a coluna com a cor do pneu para plotar no grafico
tempo = df.groupby('num_current_lap').agg({'last_lap_ms':'max', 'visual_compound_tyre':'max'}).reset_index()
#fazendo o mapeamento das cores em relação ao dicionario acima
tempo['cor_pneu'] = tempo['visual_compound_tyre'].map(mapa_cores)
#como estou usando dados ''passados'' tenho que deslocar o valor para tras
tempo['last_lap_ms'] = tempo['last_lap_ms'].shift(-1)

#comparar last or max current lap para ver, se existe perca de tempo
volta_ori = df.groupby('num_current_lap')['current_lap_ms'].max().reset_index()

#quero pegar o ultimo dado de ori e colocar no ultimo dado de tempo
tempo.loc[17, 'last_lap_ms'] = volta_ori.loc[17, 'current_lap_ms']
#transformando milisegundos para minuto
tempo['last_lap_ms'] = tempo['last_lap_ms']/60000


#como plotar o grafico
#esse estilo escuro deve sempre ser antes de definir o fig, ax
plt.style.use('dark_background')

fig, ax = plt.subplots(figsize=(12,6))

ax.plot(tempo['num_current_lap'], tempo['last_lap_ms'],color = 'blue', label = 'Tempo de volta', linewidth = 2)
ax.scatter(tempo['num_current_lap'], tempo['last_lap_ms'], c = tempo['cor_pneu'], s=40, edgecolors='white', linewidths=1, zorder=2)
ax.grid(True, color='white', linestyle='--', linewidth=1,alpha=0.2)

ax.set_title('Tempo de Volta', color='white', fontsize = 20, fontweight = 'bold', pad = 10)
ax.set_xticks(tempo['num_current_lap'])
ax.set_xlabel('Volta', color='white', fontsize = 14, labelpad = 10)
ax.set_ylabel('Tempo', color='white', fontsize = 14, labelpad = 10)

#colocar linha vertical na volta de saida do pit (PIT_OUTLAP)
pit_out_lap = df.loc[df['pit_status'] == 1, 'num_current_lap'].unique()

def formato_tempo_f1(x, pos):
    minutos = int(x)
    segundos = (x - minutos)*60
    return f"{minutos}:{segundos:04.1f}"

ax.yaxis.set_major_formatter(ticker.FuncFormatter(formato_tempo_f1))
ax.yaxis.set_major_locator(ticker.MaxNLocator(12))

#achei que ficou estranho com essa linha
#ax.axvline(pit_out_lap[1], linestyle = ':', color = 'red', label = 'PIT_OUTLAP', linewidth = 1, alpha = 0.5)

#testar retirar axis spines
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
plt.legend()
plt.show()