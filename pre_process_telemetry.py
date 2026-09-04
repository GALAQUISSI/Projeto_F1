import pandas as pd
import numpy as np

#arquivo para manipulação do dataset para modelo lightgbm e regressao linear
#apos cada etapa, a etapa vai ficar comentada para nao refazer cada passo


df = pd.read_csv(r'C:\Users\User\Projeto_F1\telemetria_completa.csv')

df_copia = df.copy()
voltas_removidas = [3,5,10,13,16,19,22,27,28,31,36]
df_copia = df_copia[(df_copia['lap_distance'] >= 0) & (~df_copia['num_current_lap'].isin(voltas_removidas))]
#mantendo apenas as linhas em que a coluna y NÃO está presente em x

#adicionar coluna 'setores_bateria'

#vou dividir a pista em 20 intervalos, pegando o valor de 4295.0 que seria um pouco acima do máx no dataset
intervalos = [i * 214.75 for i in range (21)]
intervalos[-1] = 4295.0  #garantindo que o ultimo seja o máx

df_copia['setores_bateria'] = pd.cut(df_copia['lap_distance'], bins = intervalos, labels = list(range(1,21)),
                                     include_lowest = True) # right = true (default)

#criar coluna de delta para cada setor


df_dummies = pd.get_dummies(df_copia['setores_bateria'], prefix = 'setor_bateria_', drop_first = True, dtype = int)
df_copia = pd.concat([df_copia, df_dummies], axis = 1)

#fazer dummies para variaveis categoricas

df_dummies_tyre = pd.get_dummies(df_copia['actual_compound_tyre'], prefix = 'actual_compound_tyre_', drop_first = True, dtype = int)
df_copia = pd.concat([df_copia, df_dummies_tyre], axis = 1)

df_dummies_ers = pd.get_dummies(df_copia['ers_deploy_mode'], prefix = 'ers_deploy_mode_', drop_first = True, dtype = int)
df_copia = pd.concat([df_copia, df_dummies_ers], axis = 1)

df_dummies_fuel = pd.get_dummies(df_copia['fuel_mix'], prefix = 'type_fuel_mix', drop_first = True, dtype = int)
df_copia = pd.concat([df_copia, df_dummies_fuel], axis = 1)

df_copia = df_copia.sort_values(by = ['num_current_lap', 'current_lap_ms'])

#  ->  nome_nova_coluna = ('coluna_original', função)

df_filtrado = df_copia.groupby(['num_current_lap', 'setores_bateria']).agg(
    tempo_setor_ms = ('current_lap_ms', lambda x : x.iloc[-1] - x.iloc[0]),
    delta_bateria = ('ers_battery %', lambda x : x.iloc[-1] - x.iloc[0]),
    velocidade_md = ('velocidade', 'mean'),
    velocidade_maxima = ('velocidade', 'max'),
    acelerador_md = ('acelerador', 'mean'),
    freio_md = ('freio', 'mean'),
    freio_max = ('freio', 'max'),
    rpm_md = ('rpm', 'mean'),
    num_current_lap = ('num_current_lap', lambda x : x.iloc[0]),
    temp_motor_md = ('temperatura_motor', 'mean'),
    temp_freio_RL_md = ('temp_freio_RL', 'mean'),#
    temp_freio_RR_md = ('temp_freio_RR', 'mean'),#
    temp_freio_FL_md = ('temp_freio_FL', 'mean'),#
    temp_freio_FR_md = ('temp_freio_FR', 'mean'),#
    temp_sup_pneu_RL_md = ('temp_sup_pneu_RL', 'mean'),
    temp_sup_pneu_RR_md = ('temp_sup_pneu_RR', 'mean'),
    temp_sup_pneu_FL_md = ('temp_sup_pneu_FL', 'mean'),
    temp_sup_pneu_FR_md = ('temp_sup_pneu_FR', 'mean'),
    temp_int_pneu_RL_md = ('temp_int_pneu_RL', 'mean'),
    temp_int_pneu_RR_md = ('temp_int_pneu_RR', 'mean'),
    temp_int_pneu_FL_md = ('temp_int_pneu_FL', 'mean'),
    temp_int_pneu_FR_md = ('temp_int_pneu_FR', 'mean'),
    pressao_pneu_RL_md = ('pressao_pneu_RL', 'mean'),
    pressao_pneu_RR_md = ('pressao_pneu_RR', 'mean'),
    pressao_pneu_FL_md = ('pressao_pneu_FL', 'mean'),
    pressao_pneu_FR_md = ('pressao_pneu_FR', 'mean'),

    #nao sei se gera ruido (testar)
    #g_force_lateral_md = ('g_force_lateral', 'mean'),
    #g_force_longitudinal_md = ('g_force_longitudinal', 'mean'),
    #g_force_vertical_md = ('g_force_vertical', 'mean'),
    #pitch_md = ('pitch', 'mean'),
    #roll_md = ('roll', 'mean'),
    #yaw_md = ('yaw', 'mean'),

    delta_fuel_in_tank = ('fuel_in_tank', lambda x : x.iloc[-1] - x.iloc[0]),
    tyre_age_laps = ('tyre_age_laps', lambda x : x.iloc[0]),
    fl_brake_damage_md = ('fl_brake_damage', 'mean'),
    fl_tyre_damage_md = ('fl_tyre_damage', 'mean'),
    fl_tyre_wear_md = ('fl_tyre_wear', 'mean'),
    fl_wing_damage_md = ('fl_wing_damage', 'mean'),
    floor_damage_max = ('floor_damage', 'max'),
    fr_brake_damage_md = ('fr_brake_damage', 'mean'),
    fr_tyre_damage_md = ('fr_tyre_damage', 'mean'),
    fr_tyre_wear_md = ('fr_tyre_wear', 'mean'),
    fr_wing_damage_mx = ('fr_wing_damage', 'max'),
    rear_wing_damage_mx = ('rear_wing_damage', 'max'),
    rl_brake_damage_md = ('rl_brake_damage', 'mean'),
    rl_tyre_damage_md = ('rl_tyre_damage', 'mean'),
    rl_tyre_wear_md = ('rl_tyre_wear', 'mean'),
    rr_brake_damage_md = ('rr_brake_damage', 'mean'),
    rr_tyre_damage_md = ('rr_tyre_damage', 'mean'),
    rr_tyre_wear_md = ('rr_tyre_wear', 'mean'),
    sidepod_damage_max = ('sidepod_damage', 'max'),
)

df_filtrado.to_csv('df_limpo_reg_v2.csv', index=False)




'''''


#agrupar os tempos pelos setores
df_copia['sector_time'] = df_copia.groupby(['num_current_lap', 'setores_bateria'])

df_copia['delta_bateria_setores'] = df_copia.groupby(['num_current_lap',
                                                      'setores_bateria'])['ers_battery %'].transform(lambda x : x.iloc[-1] - x.iloc[0])

#fazer ers_battery %[0] - ers_battery %[max] (isso por setor) -- como selecionar por setor, fazer groupby


#fazer a normalizacao para o modelo, valores numericos, categoricos como setores ou o proprio lightgbm faz
#de toda forma criar um dataset normalizado para regressao?

#para regressao ussar get_dummies

#tratar dados categoricos de composto de pneu
#dados categoricos de modo de bateria

#eu usar o tempo final de volta como target vai causar um grande overfitting o que esta fora, o certo seria
# mudar o referencial ou seja, colocar o referencial para o tempo final de cada setor

#qual vai ser o target

#df_copia.to_csv("dados_regressao.csv", index = False)
'''''