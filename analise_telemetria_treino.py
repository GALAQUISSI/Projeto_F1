import pandas as pd

df = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa.csv')
#df2 = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa_130426.csv')

# VOLTA MAIS RAPIDA DATASET TREINO
#tenho que analisar os dados do dateset do treino por que tem que ver se há necessidade de alinhamento
#talvez o alinhamento fez o grafico ficar 'meio errado'
#na vdd eu tinha usado o alinhamento pq o last_lap_ms é mais preciso do que o current_lap_ms, testar novamente


antes = df.groupby('num_current_lap')['current_lap_ms'].max()
depois = df.groupby('num_current_lap')['last_lap_ms'].max()
#print(antes,depois)

#current_lap esta mais preciso do que last_lap, entao o target vai ter q ser current_lap
#print(df['current_lap_ms'].nunique()) = 42448 meu dataset tem +/- 76000 ou seja a cada x metros que ele carrega
#quantos valores unicos por volta

#processo de limpeza do dataset de treino para os modelos
#print(df['ers_deploy_mode'].unique())
#print(df.groupby('num_current_lap')['ers_deploy_mode'].unique())

#se eu tirar todas as voltas que o ers tava em 0, sao 12 voltas a menos, entao de 35 sobra 23, reduz muito
#graficamente eu deveria tirar pelo menos umas 9
#mais ai a importancia de colocar o outro dataset pq ele sao 18 voltas certinhas pra uso, entao aumenta de umas 25 pra 43 voltas


#o idela para passar para o modelo seria uma coluna de delta de bateria que pegaria o max do setor com o min e faria a dif
#e ai toda linha teria esse resultado, uma coluna de modo de bateria e uma coluna de % de bateria durante a volta mesmo(essa ja tem)
#pra eu saber quantos setores vou dividir a pista eu tenho que ver onde cada volta começa em metros

'''''
Processos:
 - ver distancia se o min e o max sao iguais para todas as voltas,
 - criar copia dataset,
 - retirar voltas com tempo muito acima,
 - criar coluna setores bateria,
 - povoar com os setores de 0 a 20 para cada volta,
 - criar coluna de delta de bateria para cada setor = dif (start - end)
 - normalizar todas as colunas entre 0 e 1, como seria isso para os modos de bateria?
 - o target vai ser current_lap_ms.max() ou seja o tempo final de cada volta, ou o tempo final de cada setor de bateria?
'''''

dist_per_lap = df[df['lap_distance'] > 0].groupby('num_current_lap')['lap_distance'].agg(['min','max'])
print(dist_per_lap)

'''''
maior = 4294.394531
min = 0.159027
                      min          max
num_current_lap                       
1                0.159027  4291.765137
2                2.136719  4293.327148
3                3.991211  4294.240234
4                4.348633  4290.208008
5                0.582031  4294.394531
6                4.943359  4291.542969
7                1.947266  4291.609375
8                1.851562  4292.750000
9                3.261719  4291.609375
10               1.968750  4289.914062
11               0.117188  4292.503906
12               2.941406  4289.894531
13               0.183594  4294.332031
14               4.925781  4293.546875
15               3.910156  4294.062500
16               4.835938  4291.531250
17               2.101562  4292.296875
18               2.851562  4291.414062
19               1.960938  4290.664062
20               1.000000  4293.156250
21               3.718750  4291.359375
22               0.890625  4294.257812
23               2.117188  4293.445312
24               3.890625  4293.671875
25               4.265625  4290.585938
26               1.070312  4292.914062
27               3.539062  4290.828125
28               1.578125  4290.945312
29               1.468750  4293.851562
30               1.804688  4289.984375
31               0.492188  4293.890625
32               1.312500  4290.984375
33               1.281250  4290.750000
34               1.218750  4292.531250
35               3.078125  4293.531250
'''''

'''''
1        [0, 1, 3]
2           [1, 3]
3           [1, 0]
4           [1, 3]
5        [1, 0, 3]
6        [3, 1, 0]
7           [1, 3]
8           [1, 3]
9           [1, 0]
10    [1, 3, 0, 2]
11          [1, 3]
12          [1, 3]
13       [1, 0, 3]
14          [1, 3]
15          [1, 3]
16       [1, 3, 0]
17          [1, 3]
18          [3, 1]
19          [1, 0]
20          [1, 3]
21          [1, 3]
22       [1, 3, 0]
23          [1, 3]
24          [1, 3]
25          [1, 3]
26          [1, 3]
27          [1, 0]
28          [1, 0]
29          [1, 3]
30          [1, 3]
31       [1, 3, 0]
32          [3, 1]
33          [1, 3]
34          [1, 3]
35             [1]
36             [1]
'''''