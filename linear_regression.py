#regressao linear para ver a importancia das features para o modelo

'''''
Para fazer:

rever pipeline modelo de regressao linear: https://www.datacamp.com/pt/tutorial/sklearn-linear-regression
     - ver como esta o resultado do modelo
     - avaliar construcao do modelo
     - ver coeficientes
     - gerar graficos para analise de residuos

'''''

import pandas as pd
import numpy as np

df = pd.read_csv(r'C:\Users\User\Projeto_F1\df_limpo_reg_v2.csv')

df.sort_values('num_current_lap').reset_index(drop = True)

#divisao de treino/teste

treino = df[df['num_current_lap'] <= 14]
teste = df[df['num_current_lap'] > 14]

#target/features
treino_target = treino['tempo_setor_ms']
treino_features = treino.drop(columns=['tempo_setor_ms', 'num_current_lap'])
teste_target = teste['tempo_setor_ms']
teste_features = teste.drop(columns=['tempo_setor_ms', 'num_current_lap'])

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

#valores normalizados
treino_norm = scaler.fit_transform(treino_features)
teste_norm = scaler.transform(teste_features)

model = LinearRegression()
model.fit(treino_norm, treino_target)

y_pred = model.predict(teste_norm)

#avaliacao modelo
r2 = r2_score(teste_target, y_pred)
mse = mean_squared_error(teste_target, y_pred)

#analisar a importancia dos coeficientes
coeficientes = model.coef_
intercept = model.intercept_

resultados = {
    'colunas' : teste_features.columns,
    'coeficientes' : coeficientes
}

df_res = pd.DataFrame(resultados)
#df_res.sort_values(by = ['coeficientes'])

print(f"Coeficiente de Intercepto: {intercept:2f}\n")
print(f"Resultado Avaliação Modelo: R2: {r2:2f}, MSE: {mse:2f}\n")
#print(f"colunas: {teste_features.columns}")
#print(f"Resultado Coeficientes de inclinação: {coeficientes}\n")
print(df_res.sort_values(by = ['coeficientes'], ascending= True))

#COM 10 VOLTAS DE TRAIN = Resultado Avaliação Modelo: R2: 0.849332, MSE: 207716.081345
#COM 14 VOLTAS DE TRAIN = Resultado Avaliação Modelo: R2: 0.908264, MSE: 126092.591945

'''''
Intercepto Coeficiente Linear B0: indica o valor esperado da variável resposta Y 
quando a variável explicativa X é zero.

Coeficiente Angular Inclinação B1: indica o quanto a variável Y muda, em média, 
para cada aumento de uma unidade em X.

-1.001398e+02, it is in scientific notation (which means -1.001398 * 10^2, or -100.1398)
'''''

'''''
erros:
ValueError: Expected 2D array, got scalar array instead:
array=StandardScaler().
Reshape your data either using array.reshape(-1, 1) if your 
data has a single feature or array.reshape(1, -1) if it contains a single sample.

Eu acreditei que os dados ja haviam sido transformados porem eles foram apenas usados para treinar o scaler
e não já treinar os proprios dados, para fazer isso tem que usar uma função chamada fit_transform
'''''
