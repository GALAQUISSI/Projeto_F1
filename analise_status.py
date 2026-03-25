import pandas as pd
import binascii
import struct

df = pd.read_csv(r"C:\Users\User\Projeto_F1\dados_interlagos_170226\status.csv")

tabela_vazia = []

#calculo automatico posicao inicial
#como cada pacote o carro possui um diferente tipo de tamanho para os carros
#para status, cada carro possui 55 bytes de informação

linha_base = df.iloc[0]['raw_hex']
linha_binaria = binascii.unhexlify(linha_base)
header = 29 #padrao pela EA Documentation
car_id = linha_binaria[27]

posicao_inicial = header + (car_id * 55)

for i in range(len(df)):
    #escopo raw_text
    texto_raw = df.iloc[i]['raw_hex']
    #transformar em binario
    dados_binario = binascii.unhexlify(texto_raw)

    #escopo meu carro
    meu_carro = dados_binario[posicao_inicial : posicao_inicial + 55]

    #usar struct para transformar bytes em valores, seguindo documento da EA
    # letras em maiusculo é pq nao tem sinal e minusculo é pq tem, <H, <h

    traction_control = struct.unpack('<B', meu_carro[0:1])[0]
    ABS = struct.unpack('<B', meu_carro[1:2])[0]
    fuel_mix = struct.unpack('<B', meu_carro[2:3])[0]
    #break balance in game percentage
    front_brake_bias = struct.unpack('<B', meu_carro[3:4])[0]
    pit_limiter_status = struct.unpack('<B', meu_carro[4:5])[0]
    fuel_in_tank = struct.unpack('<f', meu_carro[5:9])[0]
    fuel_capacity = struct.unpack('<f', meu_carro[9:13])[0]
    fuel_remaining_laps = struct.unpack('<f', meu_carro[13:17])[0]
    max_rpm = struct.unpack('<H', meu_carro[17:19])[0]
    idle_rpm = struct.unpack('<H', meu_carro[19:21])[0]
    max_gears = struct.unpack('<B', meu_carro[21:22])[0]
    drs_allowed = struct.unpack('<B', meu_carro[22:23])[0]
    # se nao for hablitado o drs_activation_distance aparece como 0
    drs_activation_distance = struct.unpack('<H', meu_carro[23:25])[0]
    actual_compound_tyre = struct.unpack('<B', meu_carro[25:26])[0]
    visual_compound_tyre = struct.unpack('<B', meu_carro[26:27])[0]
    tyre_age_laps = struct.unpack('<B', meu_carro[27:28])[0]
    fia_flags = struct.unpack('<b', meu_carro[28:29])[0]
    engine_power_ice = struct.unpack('<f', meu_carro[29:33])[0]
    engine_power_mguk = struct.unpack('<f', meu_carro[33:37])[0]

    #ers em MJ, limte de uso por volta de 4MJ
    ers_store_energy = struct.unpack('<f', meu_carro[37:41])[0]
    ers_deploy_mode = struct.unpack('<B', meu_carro[41:42])[0]
    #recuperação na freada
    ers_harvested_thislap_mguk = struct.unpack('<f', meu_carro[42:46])[0]
    #recuperação via calor do turbo
    ers_harvested_thislap_mguh = struct.unpack('<f', meu_carro[46:50])[0]
    ers_deployed_thislap = struct.unpack('<f', meu_carro[50:54])[0]
    network_paused = struct.unpack('<B', meu_carro[54:55])[0]

    linha = {
        'tempo' : df.iloc[i]['time'],
        'ABS' : ABS,
        'fuel_mix' : fuel_mix,
        'front_brake_bias %' : front_brake_bias,
        'pit_limiter_status' : pit_limiter_status,
        'fuel_in_tank' : fuel_in_tank,
        'fuel_capacity' : fuel_capacity,
        'fuel_remaining_laps' : fuel_remaining_laps,
        'max_rpm' : max_rpm,
        'idle_rpm': idle_rpm,
        'max_gears' : max_gears,
        'drs_allowed' : drs_allowed,
        'drs_activation_distance' : drs_activation_distance,
        'actual_compound_tyre' : actual_compound_tyre,
        'visual_compound_tyre' : visual_compound_tyre,
        'tyre_age_laps' : tyre_age_laps,
        'fia_flags' : fia_flags,
        'engine_power_ice' : engine_power_ice,
        'engine_power_mguk' : engine_power_mguk,
        'ers_store_energy' : ers_store_energy,
        'ers_battery %' : (ers_store_energy/4000000) * 100,
        'ers_deploy_mode' : ers_deploy_mode,
        'ers_harvested_thislap_MGUK' : ers_harvested_thislap_mguk,
        'ers_harvested_MGUK %' : (ers_harvested_thislap_mguk/4000000) * 100,
        'ers_harvested_thislap_MGUH' : ers_harvested_thislap_mguh,
        'ers_harvested_MGUH %' : (ers_harvested_thislap_mguh/4000000) * 100,
        'ers_deployed_thislap' : ers_deployed_thislap,
        'ers_deployed %' : (ers_deployed_thislap/4000000) * 100,
        'network_paused' : network_paused,
    }

    tabela_vazia.append(linha)

df_final = pd.DataFrame(tabela_vazia)
df_final.to_csv("status_data_interlagos_170226.csv", index = False)