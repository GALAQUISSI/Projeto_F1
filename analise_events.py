import pandas as pd
import struct
import binascii

df = pd.read_csv(r'events.csv')

#tabela para fazer o append
eventos = []

#possiveis strings com car_id
#SSTA, SEND, FTLP, TMPT, RCWN, PENA, DTSV, SGSV, FLBK, RDFL, SCAR
code_with_id = {'FTLP', 'TMPT', 'RCWN', 'PENA', 'DTSV', 'SGSV'}
code_without_id = {'SSTA', 'SEND', 'FLBK', 'RDFL', 'SGSV'}

lista_hex = df['raw_hex'].tolist()
lista_tempo = df['time'].tolist()

for texto_hex, tempo in zip(lista_hex, lista_tempo):
    binario = binascii.unhexlify(texto_hex)
    # tenho que transformar os dados de binario[29:33] em string e ver se bate
    # O ID DO CARRO É O BYTE 33
    #decodificar em ascii
    codigo = binario[29:33].decode('ascii')

    if codigo in code_with_id or codigo in code_without_id:
        car_id = None

        if codigo in code_with_id:
            car_id = binario[33]

    eventos.append({
        'tempo': tempo,
        'codigo': codigo,
        'car_id': car_id,
    })

df_final = pd.DataFrame(eventos)
df_final.to_csv('eventos_data.csv', index=False)