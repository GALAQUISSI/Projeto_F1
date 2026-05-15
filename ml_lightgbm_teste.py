#prever tempo de volta de acordo com algumas features
import pandas as pd
import lightgbm as lgb

df = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa.csv')

#definir features e target
#ver sobre incluir g force, pitch, roll, yaw, pressao pneus, e outros
features = ["velocidade", "acelerador", "freio","marcha", "rpm", "drs", "temperatura_motor", "lap_distance",
            "temp_freio_RL", "temp_freio_RR", "temp_freio_FL", "temp_freio_FR", "temp_sup_pneu_RL",
            "temp_sup_pneu_RR","temp_sup_pneu_FL", "temp_sup_pneu_FR", "temp_int_pneu_RL", "temp_int_pneu_RR",
            "temp_int_pneu_FL", "temp_int_pneu_FR", "ers_battery %", "ers_deploy_mode", "ers_deployed %",
            "fuel_in_tank", "fuel_remaining_laps", "diffuser_damage","actual_tyre" ,"sidepod_damage", "fl_brake_damage", "fl_tyre_blisters",
            "fl_tyre_damage", "fl_tyre_wear", "fl_wing_damage", "fr_brake_damage", "fr_tyre_blisters", "fr_tyre_damage",
            "fr_tyre_wear","fr_wing_damage", "rear_wing_damage", "rl_brake_damage", "rl_tyre_blisters", "rl_tyre_damage", "rl_tyre_wear",
            "rr_brake_damage", "rr_tyre_blisters", "rr_tyre_damage", "rr_tyre_wear", "usable_life"]

#adicionei usable_life pra ele entender o desgaste em relação com a vida do pneu

#mapear pneus para colocar como categorico no modelo
mapa_pneus = {
    16: 'C5 (Softest)', 17: 'C4', 18: 'C3 (Medium)', 19: 'C2', 20: 'C1 (Hardest)',
    21: 'C0', 22: 'C6', 7: 'Inter', 8: 'Wet',
    9: 'Classic Dry', 10: 'Classic Wet',
    11: 'F2 Super Soft', 12: 'F2 Soft', 13: 'F2 Medium', 14: 'F2 Hard', 15: 'F2 Wet'
}

#fazendo a correção dos dados (alinhamento)
df['target'] = df["last_lap_ms"].shift(-1)

#retirando a volta de pit, analise de pace apenas
df_limpo = df[df["pit_status"] == 0].copy()

#retirar as linhas da volta de 18, que recebem como last_lap_ms = Nan
df_limpo = df_limpo.dropna(subset=['target'])

#definir tipo do pneu para o modelo identificar qual o composto
#actual_compound_tyre
df_limpo["actual_tyre"] = df_limpo["actual_tyre"].map(mapa_pneus)
df_limpo["actual_tyre"] = df_limpo["actual_tyre"].astype('category')

#como os dados são ordenados de forma temporal a divisao por slip nao funcionaria, fiz uma divisao media
voltas_train = 14
x_train = df_limpo.loc[df_limpo['num_current_lap'] <= 14, features]
y_train = df_limpo.loc[df_limpo['num_current_lap'] <= 14, 'target']

x_test = df_limpo.loc[df_limpo['num_current_lap'] > 14, features]
y_test = df_limpo.loc[df_limpo['num_current_lap'] > 14, 'target']

import lightgbm as lgbm
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

#base de treino
dtrain = lgbm.Dataset(x_train, label= y_train)
#base de teste
dtest = lgbm.Dataset(x_test, label= y_test, reference=dtrain)

#definir hiperparametros
params = {
    'objective': 'regression',
    'metric': 'rmse',
    'boosting_type' : 'gbdt',
    'learning_rate': 0.05,
    'num_leaves': 31,
    'max_depth': 7, #arvore com tamanho menor
    'force_col_wise' : True
}

modelo = lgb.train(
    params,
    dtrain,
    valid_sets = [dtrain, dtest],
    callbacks=[lgb.early_stopping(stopping_rounds=50)]
)

y_pred = modelo.predict(x_test)
print(f"Erro Médio (MAE): {mean_absolute_error(y_test, y_pred)}")
print(f"Erro Médio (MSE): {mean_squared_error(y_test, y_pred)}")
print(f"R2_score: {r2_score(y_test, y_pred)}")