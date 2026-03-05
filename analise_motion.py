import pandas as pd
import binascii
import struct

df = pd.read_csv(r'C:\Projeto_f1\dados_interlagos_170226\motion.csv')

#tabela armazenar dados
tabela_vazia = []

#calcular offset
#60 bytes por carro, 22 carros (meu indice = 19), header (29 bytes) -> 29 + (19 * 60) = 1169
posicao_inicial = 1169

for i in range (len(df)):
    #transformar em binario
    text_raw = df.iloc[i]['raw_hex']
    dados_binario = binascii.unhexlify(text_raw)
    #escopo
    meu_carro = dados_binario[posicao_inicial : posicao_inicial + 60]

    #transformar_dados
    #doc.EA:  "For the normalised vectors below, to convert to float values divide by 32767.0f 16-bit signed
    # values are used to pack the data and on the assumption that direction values are always between -1.0fand 1.0f."

    world_positionX = struct.unpack('<f', meu_carro[0:4])[0] #metros
    world_positionY = struct.unpack('<f', meu_carro[4:8])[0]
    world_positionZ = struct.unpack('<f', meu_carro[8:12])[0]
    world_velocityX = struct.unpack('<f', meu_carro[12:16])[0] #metros
    world_velocityY = struct.unpack('<f', meu_carro[16:20])[0]
    world_velocityZ = struct.unpack('<f', meu_carro[20:24])[0]

    #normalised_part
    raw_world_foward_directionX = struct.unpack('<h', meu_carro[24:26])[0]
    final_world_foward_directionX = raw_world_foward_directionX / 32767.0

    raw_world_directionY = struct.unpack('<h', meu_carro[26:28])[0]
    final_world_foward_directionY = raw_world_directionY / 32767.0

    raw_world_directionZ = struct.unpack('<h', meu_carro[28:30])[0]
    final_world_foward_directionZ = raw_world_directionZ / 32767.0

    raw_world_right_directionX = struct.unpack('<h', meu_carro[30:32])[0]
    final_world_right_directionX = raw_world_right_directionX / 32767.0

    raw_world_right_directionY = struct.unpack('<h', meu_carro[32:34])[0]
    final_world_right_directionY = raw_world_right_directionY / 32767.0

    raw_world_right_directionZ = struct.unpack('<h', meu_carro[34:36])[0]
    final_world_right_directionZ = raw_world_right_directionZ / 32767.0

    #g forces
    g_force_lateral = struct.unpack('<f', meu_carro[36:40])[0]
    g_force_longitudinal = struct.unpack('<f', meu_carro[40:44])[0]
    g_force_vertical = struct.unpack('<f', meu_carro[44:48])[0]

    #angles in radians
    yaw = struct.unpack('<f', meu_carro[48:52])[0]
    pitch = struct.unpack('<f', meu_carro[52:56])[0]
    roll = struct.unpack('<f', meu_carro[56:60])[0]

    linha = {
        'tempo': df.iloc[i]['time'],
        'space_world_positionX': world_positionX,
        'space_world_positionY': world_positionY,
        'space_world_positionZ': world_positionZ,
        'space_world_velocityX': world_velocityX,
        'space_world_velocityY': world_velocityY,
        'space_world_velocityZ': world_velocityZ,
        'world_foward_directionX': final_world_foward_directionX,
        'world_foward_directionY': final_world_foward_directionY,
        'world_foward_directionZ': final_world_foward_directionZ,
        'world_right_directionX': final_world_right_directionX,
        'world_right_directionY': final_world_right_directionY,
        'world_right_directionZ': final_world_right_directionZ,
        'g_force_lateral': g_force_lateral,
        'g_force_longitudinal': g_force_longitudinal,
        'g_force_vertical': g_force_vertical,
        'yaw': yaw,
        'pitch': pitch,
        'roll': roll,
    }

    tabela_vazia.append(linha)

df_final = pd.DataFrame(tabela_vazia)
df_final.to_csv("motion_data_interlagos170226.csv", index=False)