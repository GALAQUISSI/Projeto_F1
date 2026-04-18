import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa.csv')

#como agrupar voltas e o tempo total da volta

tempo = df.groupby('num_current_lap')['last_lap_ms'].max().reset_index()
#como estou usando dados ''passados'' tenho que deslocar o valor para tras
tempo['last_lap_ms'] = tempo['last_lap_ms'].shift(-1)

#comparar last or max current lap para ver, se existe perca de tempo
volta_ori = df.groupby('num_current_lap')['current_lap_ms'].max().reset_index()

#quero pegar o ultimo dado de ori e colocar no ultimo dado de tempo
tempo.loc[17, 'last_lap_ms'] = volta_ori.loc[17, 'current_lap_ms']
#transformando milisegundos para minuto
tempo['last_lap_ms'] = tempo['last_lap_ms']/60000

#como plotar o grafico
plt.figure(figsize=(12,6))
#sns.set_style('darkgrid')
plt.style.use('dark_background')

plt.plot(tempo['num_current_lap'], tempo['last_lap_ms'],color = 'blue', label = 'Tempo de volta', linewidth = 2)
plt.plot(tempo['num_current_lap'], tempo['last_lap_ms'], 'o', color = 'yellow', markersize = 3)
plt.xticks(tempo['num_current_lap'])

plt.xlabel('Lap')
plt.ylabel('Tempo')
plt.legend()
plt.show()