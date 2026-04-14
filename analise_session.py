import pandas as pd
import binascii
import struct

df = pd.read_csv(r'C:\Users\User\Projeto_F1\dados_interlagos_130426\session.csv')

tabela_vazia = []

'''''
neste pacote, não vou pegar todos os dados, logo nao sera tratado
como intervalo e sim posição a posição na linha apos o header (0 - 28)
'''''

lista_hex = df['raw_hex'].tolist()
lista_tempo = df['time'].tolist()

for texto_hex, tempo in zip(lista_hex, lista_tempo):
    dados_binario = binascii.unhexlify(texto_hex)

    weather = dados_binario[29]
    track_temperature = dados_binario[30]
    air_temperature = dados_binario[31]
    total_laps = dados_binario[32]
    track_lenght = struct.unpack('<H', dados_binario[33:35])[0]
    session_type = dados_binario[35]
    track_id = dados_binario[36]
    type_formula = dados_binario[37]
    session_time_left = struct.unpack('<H', dados_binario[38:40])[0]
    session_duration = struct.unpack('<H', dados_binario[40:42])[0]
    pit_speed_limit = dados_binario[42]

    if dados_binario[155] > 0:

        previsao= dados_binario[156:164]
        v = struct.unpack('<BBBbbbbB', previsao)

        time_offset_forecast = v[1]
        weather_forecast = v[2]
        track_temp_change = v[4]
        air_temp_change = v[6]
        rain_percentage = v[7]

    else:
        time_offset_forecast = weather_forecast = rain_percentage = 0
        track_temp_change = air_temp_change = 2  # 2 significa estável

    linha = {
        'tempo': tempo,
        'weather' : weather,
        'track_temperature' : track_temperature,
        'air_temperature' : air_temperature,
        'total_laps' : total_laps,
        'track_lenght' : track_lenght,
        'session_type' : session_type,
        'track_id' : track_id,
        'type_formula' : type_formula,
        'session_time_left' : session_time_left,
        'session_duration' : session_duration,
        'pit_speed_limit' : pit_speed_limit,
        'weather_forecast' : weather_forecast,
        'rain_percentage' : rain_percentage,
        'track_temp_change' : track_temp_change,
        'air_temp_change' : air_temp_change,
        'time_forecast' : time_offset_forecast,
    }

    tabela_vazia.append(linha)

df_final = pd.DataFrame(tabela_vazia)
df_final.to_csv(r'translated_session.csv', index = False)