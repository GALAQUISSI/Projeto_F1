import pandas as pd
import binascii
import struct

df = pd.read_csv(r'caminho_data_time_trail.csv')

tabela_vazia = []

for i in range (len(df)):
    texto_raw = df.iloc[i]['texto']
    dados_binario = binascii.unhexlify(texto_raw)
    #pb = personal best, ml = melhor da sessao, rv = rival
    ml = dados_binario[29:53]
    pb = dados_binario[53:77]
    rv = dados_binario[77:101]

    #melhor pessoal da sessao
    ml_car_id = struct.unpack('<B', ml[0:1])[0]
    ml_team_id = struct.unpack('<B', ml[1:2])[0]
    ml_lap_time_MS = struct.unpack('<I', ml[2:6])[0]
    ml_s1 = struct.unpack('<I', ml[6:10])[0]
    ml_s2 = struct.unpack('<I', ml[10:14])[0]
    ml_s3 = struct.unpack('<I', ml[14:18])[0]
    ml_traction_control = struct.unpack('<B', ml[18:19])[0]
    ml_gearbox_assist = struct.unpack('<B', ml[19:20])[0]
    ml_abs = struct.unpack('<B', ml[20:21])[0]
    ml_equal_performance = struct.unpack('<B', ml[21:22])[0]
    ml_custom_setup = struct.unpack('<B', ml[22:23])[0]
    ml_valid = struct.unpack('<B', ml[23:24])[0]

    #melhor ja feito
    pb_car_id = struct.unpack('<B', pb[0:1])[0]
    pb_team_id = struct.unpack('<B', pb[1:2])[0]
    pb_lap_time_MS = struct.unpack('<I', pb[2:6])[0]
    pb_s1 = struct.unpack('<I', pb[6:10])[0]
    pb_s2 = struct.unpack('<I', pb[10:14])[0]
    pb_s3 = struct.unpack('<I', pb[14:18])[0]
    pb_traction_control = struct.unpack('<B', pb[18:19])[0]
    pb_gearbox_assist = struct.unpack('<B', pb[19:20])[0]
    pb_abs = struct.unpack('<B', pb[20:21])[0]
    pb_equal_performance = struct.unpack('<B', pb[21:22])[0]
    pb_custom_setup = struct.unpack('<B', pb[22:23])[0]
    pb_valid = struct.unpack('<B', pb[23:24])[0]

    #rival_data
    rv_car_id = struct.unpack('<B', rv[0:1])[0]
    rv_team_id = struct.unpack('<B', rv[1:2])[0]
    rv_lap_time_MS = struct.unpack('<I', rv[2:6])[0]
    rv_s1 = struct.unpack('<I', rv[6:10])[0]
    rv_s2 = struct.unpack('<I', rv[10:14])[0]
    rv_s3 = struct.unpack('<I', rv[14:18])[0]
    rv_traction_control = struct.unpack('<B', rv[18:19])[0]
    rv_gearbox_assist = struct.unpack('<B', rv[19:20])[0]
    rv_abs = struct.unpack('<B', rv[20:21])[0]
    rv_equal_performance = struct.unpack('<B', rv[21:22])[0]
    rv_custom_setup = struct.unpack('<B', rv[22:23])[0]
    rv_valid = struct.unpack('<B', rv[23:24])[0]

    linha = {
        'tempo': df.iloc[i]['time'],
        'ml_car_id': ml_car_id,
        'ml_team_id': ml_team_id,
        'ml_lap_time_MS': ml_lap_time_MS,
        'ml_s1': ml_s1,
        'ml_s2': ml_s2,
        'ml_s3': ml_s3,
        'ml_traction_control': ml_traction_control,
        'ml_gearbox_assist': ml_gearbox_assist,
        'ml_abs': ml_abs,
        'ml_equal_performance': ml_equal_performance,
        'ml_custom_setup': ml_custom_setup,
        'ml_valid': ml_valid,

        'pb_car_id': pb_car_id,
        'pb_team_id': pb_team_id,
        'pb_s1': pb_s1,
        'pb_s2': pb_s2,
        'pb_s3': pb_s3,
        'pb_traction_control': pb_traction_control,
        'pb_gearbox_assist': pb_gearbox_assist,
        'pb_abs': pb_abs,
        'pb_equal_performance': pb_equal_performance,
        'pb_custom_setup': pb_custom_setup,
        'pb_valid': pb_valid,

        'rv_car_id': rv_car_id,
        'rv_team_id': rv_team_id,
        'rv_s1': rv_s1,
        'rv_s2': rv_s2,
        'rv_s3': rv_s3,
        'rv_traction_control': rv_traction_control,
        'rv_gearbox_assist': rv_gearbox_assist,
        'rv_abs': rv_abs,
        'rv_equal_performance': rv_equal_performance,
        'rv_custom_setup': rv_custom_setup,
        'rv_valid': rv_valid,
    }

    tabela_vazia.append(linha)

df_final = pd.DataFrame(tabela_vazia)
df_final.to_csv('caminho_time_trail.csv', index=False)