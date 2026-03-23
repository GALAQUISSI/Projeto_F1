import pandas as pd
import binascii
import struct

df = pd.read_csv(r"C:\Users\User\Projeto_F1\dados_interlagos_170226\status.csv", sep = ';')

tabela_vazia = []

#calculo offset, 22 carros, cada carro possui 55 bytes
#offset  = header + (id_car * 55) = 29 + (19 * 55) = 1074

posicao_inicial = 1074

for i in range(len(df)):
    #escopo raw_text
    texto_raw = df.iloc[i]['raw_text']
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

