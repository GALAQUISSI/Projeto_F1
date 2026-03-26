import pandas as pd
import binascii
import struct

#uso de arquivo aleatorio, depois sera feita a captura dos dados para transformação

df = pd.read_csv(r'C:\Projeto_f1\telemetry.csv')

tabela_vazia = []

#calculo offset
linha_base = df.iloc[0]['raw_hex']
linha_binaria = binascii.unhexlify(linha_base)
id_car = linha_binaria[27]
header = 29
posicao_inicial = header + (id_car * 50)

for i in range(len(df)):
    texto_hex = df.iloc[i]['raw_hex']
    dados_binario = binascii.unhexlify(texto_hex)
    meu_carro  = dados_binario[posicao_inicial : posicao_inicial + 50]

    front_wing = struct.unpack('<B', meu_carro[0:1])[0]
    rear_wing = struct.unpack('<B', meu_carro[1:2])[0]
    on_throttle = struct.unpack('<B', meu_carro[2:3])[0]
    off_trottle = struct.unpack('<B', meu_carro[3:4])[0]
    front_camber = struct.unpack('<f', meu_carro[4:8])[0]
    rear_camber = struct.unpack('<f', meu_carro[8:12])[0]
    front_toe = struct.unpack('<f', meu_carro[12:16])[0]
    rear_toe = struct.unpack('<f', meu_carro[16:20])[0]
    front_suspension = struct.unpack('<B', meu_carro[20:21])[0]
    rear_suspension = struct.unpack('<B', meu_carro[21:22])[0]
    front_anti_roll_bar = struct.unpack('<B', meu_carro[22:23])[0]
    rear_anti_roll_bar = struct.unpack('<B', meu_carro[23:24])[0]
    front_suspension_height = struct.unpack('<B', meu_carro[24:25])[0]
    rear_suspension_height = struct.unpack('<B', meu_carro[25:26])[0]
    brake_pressure = struct.unpack('<B', meu_carro[26:27])[0]
    brake_bias = struct.unpack('<B', meu_carro[27:28])[0]
    engine_braking = struct.unpack('<B', meu_carro[28:29])[0]
    tyre_pressure = struct.unpack('<ffff', meu_carro[29:45])
    ballast = struct.unpack('<B', meu_carro[45:46])[0]
    fuel_load = struct.unpack('<f', meu_carro[46:50])[0]

    linha = {
        'front_wing': front_wing,
        'rear_wing': rear_wing,
        'on_throttle': on_throttle,
        'off_trottle': off_trottle,
        'front_camber': front_camber,
        'rear_camber': rear_camber,
        'front_toe': front_toe,
        'rear_toe': rear_toe,
        'front_suspension': front_suspension,
        'rear_suspension': rear_suspension,
        'front_anti_roll_bar': front_anti_roll_bar,
        'rear_anti_roll_bar': rear_anti_roll_bar,
        'front_suspension_height': front_suspension_height,
        'rear_suspension_height': rear_suspension_height,
        'brake_pressure': brake_pressure,
        'brake_bias': brake_bias,
        'engine_braking': engine_braking,
        #pressao pneu
        'rl_tyre_pressure': round(tyre_pressure[0], 1),
        'rr_tyre_pressure': round(tyre_pressure[1], 1),
        'fl_tyre_pressure': round(tyre_pressure[2], 1),
        'fr_tyre_pressure': round(tyre_pressure[3], 1),
        'ballast': ballast,
        'fuel_load': fuel_load,
    }

    tabela_vazia.append(linha)

df_final = pd.DataFrame(tabela_vazia)
df_final.to_csv('setup_f1_25.csv', index=False)