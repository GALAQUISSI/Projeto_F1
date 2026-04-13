import pandas as pd
import binascii
import struct

df = pd.read_csv(r'csv\tyre_extended.csv')

tabela_vazia = []

lista_hex = df['raw_hex'].tolist()
lista_tempo = df['time'].tolist()

for texto_hex, tempo in zip(lista_hex, lista_tempo):

    dados_binario = binascii.unhexlify(texto_hex)
    if dados_binario[27] != dados_binario[29]:
        continue

    #referencia qual o meu pneu de 0 a 20
    id_pneu = dados_binario[230]
    #cada pneu guarda 10 bytes de informação
    posicao_inicial = 30 + (id_pneu * 10)

    meu_pneu = dados_binario[posicao_inicial : posicao_inicial + 10]

    actual_tyre = struct.unpack('<B', meu_pneu[0:1])[0]
    visual_tyre = struct.unpack('<B', meu_pneu[1:2])[0]
    wear_tyre = struct.unpack('<B', meu_pneu[2:3])[0]
    available_tyre = struct.unpack('<B', meu_pneu[3:4])[0]
    recommended_session = struct.unpack('<B', meu_pneu[4:5])[0]
    life_span = struct.unpack('<B', meu_pneu[5:6])[0]
    usable_life = struct.unpack('<B', meu_pneu[6:7])[0]
    lap_delta_time = struct.unpack('<h', meu_pneu[7:9])[0]
    fitted = struct.unpack('<B', meu_pneu[9:10])[0]

    linha = {
        'tempo': tempo,
        'actual_tyre': actual_tyre,
        'visual_tyre': visual_tyre,
        'wear_tyre': wear_tyre,
        'available_tyre': available_tyre,
        'recommended_session': recommended_session,
        'life_span': life_span,
        'usable_life': usable_life,
        'lap_delta_time': lap_delta_time,
        'fitted': fitted,
    }

    tabela_vazia.append(linha)

df_final = pd.DataFrame(tabela_vazia)
df_final.to_csv('caminho_tyre_data.csv', index = False)