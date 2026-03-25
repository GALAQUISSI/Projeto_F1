import pandas as pd
import struct
import binascii

df = pd.read_csv(r'C:\Projeto_f1\dados_interlagos_170226\telemetry.csv')

#tabela para armazenar valores
tabela_vazia = []

#calculo automatico posicao inicial
#como cada pacote o carro possui um diferente tipo de tamanho para os carros
#para telemetry, cada carro possui 60 bytes de informação

linha_base = df.iloc[0]['raw_hex']
linha_binaria = binascii.unhexlify(linha_base)
header = 29 #padrao pela EA Documentation
car_id = linha_binaria[27]

posicao_inicial = header + (car_id * 60)

for i in range(len(df)):
    #coluna raw_hex -> binario
    #selecionando linhas i e coluna raw_hex
    texto_hex = df.iloc[i]['raw_hex']
    dados_binarios = binascii.unhexlify(texto_hex)

    meu_carro = dados_binarios[posicao_inicial : posicao_inicial + 60]

    #usando como base o material disponibilizado pela EA
    #para os desenvolvedores e partindo da leitura e contagem da sequencia de bytes
    # maiusculo é pq nao tem sinal e minusculo é pq tem
    velocidade = struct.unpack('<H', meu_carro[0:2])[0]
    #mutiplica por 100 pq to usando porcentagem
    acelerador = struct.unpack('<f', meu_carro[2:6])[0]* 100
    volante = struct.unpack('<f', meu_carro[6:10])[0]
    freio = struct.unpack('<f', meu_carro[10:14])[0] * 100
    embreagem = struct.unpack('<B', meu_carro[14:15])[0]
    marcha = struct.unpack('<b', meu_carro[15:16])[0]
    rpm = struct.unpack('<H', meu_carro[16:18])[0]
    drs = struct.unpack('<B', meu_carro[18:19])[0]

    #revlightspercent(19) e revlghtsbitvalue (20-22) nao vou utilzar
    #4 uint16 = 8 bytes
    temperatura_freios = struct.unpack('<HHHH', meu_carro[22:30])

    #4uint8 = 4bytes
    temperatura_superficial_pneu = struct.unpack('<BBBB', meu_carro[30:34])
    temperatura_interna_pneu = struct.unpack('<BBBB', meu_carro[34:38])
    temperatura_motor = struct.unpack('<H', meu_carro[38:40])[0]
    pressao_pneu = struct.unpack('<ffff', meu_carro[40:56])
    tipo_superfice = struct.unpack('<BBBB', meu_carro[56:60])

    linha = {
        'tempo': df.iloc[i]['time'],
        'velocidade': velocidade,
        'acelerador': acelerador,
        'volante': volante,
        'freio': freio,
        'embreagem': embreagem,
        'marcha': marcha,
        'rpm': rpm,
        'drs': drs,
        'temperatura_motor': temperatura_motor,
        #temperatura freio
        'temp_freio_RL': temperatura_freios[0],
        'temp_freio_RR': temperatura_freios[1],
        'temp_freio_FL': temperatura_freios[2],
        'temp_freio_FR': temperatura_freios[3],
        #temperatura superficial pneu
        'temp_sup_pneu_RL': temperatura_superficial_pneu[0],
        'temp_sup_pneu_RR': temperatura_superficial_pneu[1],
        'temp_sup_pneu_FL': temperatura_superficial_pneu[2],
        'temp_sup_pneu_FR': temperatura_superficial_pneu[3],
        #temperatura interna pneu
        'temp_int_pneu_RL': temperatura_interna_pneu[0],
        'temp_int_pneu_RR': temperatura_interna_pneu[1],
        'temp_int_pneu_FL': temperatura_interna_pneu[2],
        'temp_int_pneu_FR': temperatura_interna_pneu[3],
        #pressao pneu
        'pressao_pneu_RL': round(pressao_pneu[0], 1),
        'pressao_pneu_RR': round(pressao_pneu[1], 1),
        'pressao_pneu_FL': round(pressao_pneu[2], 1),
        'pressao_pneu_FR': round(pressao_pneu[3], 1),
        #tipo superfice
        'tipo_superfice_Rl': tipo_superfice[0],
        'tipo_superfice_RR': tipo_superfice[1],
        'tipo_superfice_FL': tipo_superfice[2],
        'tipo_superfice_FR': tipo_superfice[3]
    }

    tabela_vazia.append(linha)

df_final = pd.DataFrame(tabela_vazia)
df_final.to_csv("telemtria_f125_interlago170226.csv", index=False)
