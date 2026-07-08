import pandas as pd
import numpy as np

#arquivo para manipulação do dataset para modelo lightgbm e regressao linear
#apos cada etapa, a etapa vai ficar comentada para nao refazer cada passo

#retirar linhas com tempo acima (ruído)

df = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa.csv')
#print(df.groupby('num_current_lap')['last_lap_ms'].max())
df_copia = df.copy()
voltas_removidas = [3,5,10,13,16,19,22,27,28,31,36]
df_copia = df_copia[~df_copia['num_current_lap'].isin(voltas_removidas)]
#mantendo apenas as linhas em que a coluna y NÃO está presente em x

#adicionar coluna 'setores_bateria'

#vou dividir a pista em 20 intervalos, pegando o valor de 4295.0 que seria um pouco acima do máx no dataset
intervalos = [i * 214.75 for i in range (21)]
intervalos[-1] = 4295.0  #garantindo que o ultimo seja o máx

df_copia['setores_bateria'] = pd.cut(df_copia['lap_distance'], bins = intervalos, labels = list(range(1,21)),
                                     include_lowest = True) # right = true (default)

#criar coluna de delta para cada setor
# ers_battery %, ers_deploy_mode, ers_deployed (mas ta meio estranho bateria ta em 71 e o gasto ta em 24)
# eu tenho que fazer o mesmo cut so que usando battery como divisao.