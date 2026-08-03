#regressao linear para ver a importancia das features para o modelo

''''
Para fazer:

rever pipeline modelo de regressao linear: https://www.datacamp.com/pt/tutorial/sklearn-linear-regression
     - ver como esta o resultado do modelo
     - avaliar construcao do modelo
     - ver coeficientes
     - gerar graficos para analise de residuos

''''
import pandas as pd
import numpy as np

df = pd.read_csv(r'C:\Users\User\Projeto_F1\df_limpo_reg.csv')

df.sort_values('num_current_lap').reset_index(drop = True)

#divisao de treino/teste

treino = df[df['num_current_lap'] <= 14]
teste = df[df['num_current_lap'] > 14]

#target/features
treino_target = treino['tempo_setor_ms']
treino_features = treino.drop(columns=['tempo_setor_ms'])
teste_target = teste['tempo_setor_ms']
teste_features = teste.drop(columns=['tempo_setor_ms'])

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

#valores normalizados
treino_norm = scaler.fit(treino_features)
teste_norm = scaler.transform(teste_features)

model = LinearRegression()
model.fit(treino_norm, treino_target)

y_pred = model.predict(teste_norm)

#avaliacao modelo
r2 = r2_score(teste_target, y_pred)
mse = mean_squared_error(teste_target, y_pred)

#analisar a importancia dos coeficientes
coeficientes = model.coef_
print(coeficientes)