import pandas as pd
import struct
import binascii


#esse caminho foi usado no notebook -> generalizar depois
df = pd.read_csv(r'C:\Users\User\Formula1_Project\Data_interlagos_170226\lap.csv')

#armazenar valores
tabela_vazia = []

#calculo do offset: header + (id_carro * 57), em lap_data cada carro utiliza 57 bytes
# 29 + (19 * 60) = 1112
posicao_inicial = 1112

for i in range(len(df)):
    #transfromar em binario
    #definir escopo
    texto_raw = df.iloc[i]['raw_hex']
    #transformar usando unhexlify
    dados_binario = binascii.unhexlify(texto_raw)

    #definir escopo carro
    meu_carro = dados_binario[posicao_inicial : posicao_inicial + 57]
    # usando como base o material disponibilizado pela EA
    # para os desenvolvedores e partindo da leitura e contagem da sequencia de bytes
    # maiusculo é pq nao tem sinal e minusculo é pq tem
    #analisando byte a byte
    #ms = milisegundos, min = minuto
    last_lap_ms =  struct.unpack('<I', meu_carro[0:4])[0]
    current_lap_ms = struct.unpack('<I', meu_carro[4:8])[0]
    setor1_ms_part = struct.unpack('<H', meu_carro[8:10])[0]
    setor1_minuto_part = struct.unpack('<B', meu_carro[10:11])[0]
    #total setor 1:
    setor1_total = (setor1_minuto_part * 60000) + setor1_ms_part
    setor2_ms_part = struct.unpack('<H', meu_carro[11:13])[0]
    setor2_minuto_part = struct.unpack('<B', meu_carro[13:14])[0]
    #total setor 2:
    setor2_total = (setor2_minuto_part * 60000) + setor2_ms_part
    delta_carinfront_ms_part = struct.unpack('<H', meu_carro[14:16])[0]
    delta_carinfront_min_part = struct.unpack('<B', meu_carro[16:17])[0]
    #total delta carinfront:
    total_delta_carinfront = (delta_carinfront_min_part * 60000) + delta_carinfront_ms_part
    delta_leader_ms_part = struct.unpack('<H', meu_carro[17:19])[0]
    delta_leader_min_part = struct.unpack('<B', meu_carro[19:20])[0]
    #total leader:
    total_delta_leader = (delta_leader_min_part * 60000) + delta_leader_ms_part
    lap_distance = struct.unpack('<f', meu_carro[20:24])
    total_distance = struct.unpack('<f', meu_carro[24:28])
    safetycar_delta = struct.unpack('<f', meu_carro[28:32])
    car_position = struct.unpack('<B', meu_carro[32:33])[0]
    current_lap_num = struct.unpack('<B', meu_carro[33:34])[0]
    pit_status = struct.unpack('<B', meu_carro[34:35])[0]
    num_pitstops = struct.unpack('<B', meu_carro[35:36])[0]
    setor = struct.unpack('<B', meu_carro[36:37])[0]
    current_lap_invalid = struct.unpack('<B', meu_carro[37:38])[0]
    penalties = struct.unpack('<B', meu_carro[38:39])[0]
    total_warnings = struct.unpack('<B', meu_carro[39:40])[0]
    corner_cutting_warning = struct.unpack('<B', meu_carro[40:41])[0]
    num_unserverdDT = struct.unpack('<B', meu_carro[41:42])[0]
    num_unserverdSG = struct.unpack('<B', meu_carro[42:43])[0]
    grid_position = struct.unpack('<B', meu_carro[43:44])[0]
    driver_status = struct.unpack('<B', meu_carro[44:45])[0]
    result_status = struct.unpack('<B', meu_carro[45:46])[0]
    pitlane_timer_active = struct.unpack('<B', meu_carro[46:47])[0]
    pitlane_time_inlane_ms = struct.unpack('<H', meu_carro[47:49])[0]
    pitstop_time_ms = struct.unpack('<H', meu_carro[49:51])[0]
    pitstop_shoudserve_pen = struct.unpack('<B', meu_carro[51:52])[0]
    fastest_speed = struct.unpack('<f', meu_carro[52:56])[0]
    num_fastlap = struct.unpack('<B', meu_carro[56:57])[0]
    #calulo_s3_parcial
    setor3_parcial = 0
    if setor1_total > 0 and setor2_total > 0:
        setor3_parcial = current_lap_ms - (setor1_total + setor2_total)
    #gerar dicionario

    linha = {
        'tempo': df.iloc[i]['time'],
        'last_lap_ms': last_lap_ms,
        'current_lap_ms': current_lap_ms,
        'setor1_ms': setor1_total,
        'setor2_ms': setor2_total,
        'setor3_ms': setor3_parcial,
        'delta_carinfront_ms': total_delta_carinfront,
        'delta_leader_ms': total_delta_leader,
        'lap_distance': lap_distance,
        'total_distance': total_distance,
        'delta_safetycar': safetycar_delta,
        'grid_position': grid_position,
        'car_position': car_position,
        'num_current_lap': current_lap_num,
        'pit_status': pit_status,
        'num_pitstops': num_pitstops,
        'num_setor': setor, #qual setor eu to
        'current_lap_invalid': current_lap_invalid,
        'penalties': penalties,
        'total_warnings': total_warnings,
        'corner_cutting_warning': corner_cutting_warning,
        'num_unserverdDT': num_unserverdDT,
        'num_unserverdSG': num_unserverdSG,
        'driver_status': driver_status,
        'result_status': result_status,
        'pitlane_timer_active': pitlane_timer_active,
        'pitlane_time_inlane_ms': pitlane_time_inlane_ms,
        'pitstop_time_ms': pitstop_time_ms,
        'pitstop_shouldserve_pen': pitstop_shoudserve_pen,
        'fastest_speed': fastest_speed,
        'num_fastlap': num_fastlap
    }

    tabela_vazia.append(linha)

df_final = pd.DataFrame(tabela_vazia)
df_final.to_csv("lap_data_interlagos170226.csv", index=False)