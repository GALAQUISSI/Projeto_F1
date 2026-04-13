import pandas as pd
import binascii
import struct

#uso de arquivo aleatorio, depois sera feita a captura dos dados para transformação
df = pd.read_csv(r'C:\Projeto\car_damage.csv')

tabela_vazia = []

linha_base = df.iloc[0]['raw_hex']
linha_binaria = binascii.unhexlify(linha_base)
car_id = linha_binaria[27]
header = 29

#no pacote damage o tamanho de bytes para cada carro é de 46 bytes
posicao_inicial = 29 + (car_id * 46)

for i in range(len(df)):
  texto_raw = df.iloc[i]['raw_hex']
  dados_binario = binascii.unhexlify(texto_raw)
  meu_carro = dados_binario[posicao_inicial:posicao_inicial+46]

  tyres_wear = struct.unpack('<ffff', meu_carro[0:16])[0]
  tyres_damage = struct.unpack('<BBBB', meu_carro[16:20])[0]
  brakes_damage = struct.unpack('<BBBB', meu_carro[20:24])[0]
  tyre_blisters = struct.unpack('<BBBB', meu_carro[24:28])[0]
  #fl = front left, fr_ = front right
  fl_wing_damage = struct.unpack('<B', meu_carro[28:29])[0]
  fr_wing_damage = struct.unpack('<B', meu_carro[29:30])[0]
  rear_wing_damage = struct.unpack('<B', meu_carro[30:31])[0]
  floor_damage = struct.unpack('<B', meu_carro[31:32])[0]
  diffuser_damage = struct.unpack('<B', meu_carro[32:33])[0]
  sidepod_damage = struct.unpack('<B', meu_carro[33:34])[0]
  drs_fault = struct.unpack('<B', meu_carro[34:35])[0]
  ers_fault = struct.unpack('<B', meu_carro[35:36])[0]
  gear_box_damage = struct.unpack('<B', meu_carro[36:37])[0]
  engine_damage = struct.unpack('<B', meu_carro[37:38])[0]
  engine_MGUH_wear = struct.unpack('<B', meu_carro[38:39])[0]
  engine_ES_wear = struct.unpack('<B', meu_carro[39:40])[0]
  engine_CE_wear = struct.unpack('<B', meu_carro[40:41])[0]
  engine_ICE_wear = struct.unpack('<B', meu_carro[41:42])[0]
  engine_MGUK_wear = struct.unpack('<B', meu_carro[42:43])[0]
  engine_TC_wear = struct.unpack('<B', meu_carro[43:44])[0]
  engine_blown = struct.unpack('<B', meu_carro[44:45])[0]
  engine_seized = struct.unpack('<B', meu_carro[45:46])[0]

  linha = {
   'tempo': df.iloc[i]['time'],
   'rl_tyre_wear' : tyres_wear[0],
   'rr_tyre_wear' : tyres_wear[1],
   'fl_tyre_wear' : tyres_wear[2],
   'fr_tyre_wear' : tyres_wear[3],
   'rl_tyre_damage' : tyres_damage[0],
   'rr_tyre_damage' : tyres_damage[1],
   'fl_tyre_damage' : tyres_damage[2],
   'fr_tyre_damage' : tyres_damage[3],
   'rl_brake_damage' : brakes_damage[0],
   'rr_brake_damage' : brakes_damage[1],
   'fl_brake_damage' : brakes_damage[2],
   'fr_brake_damage' : brakes_damage[3],
   'rl_tyre_blisters' : tyres_wear[0],
   'rr_tyre_blisters' : tyres_wear[1],
   'fl_tyre_blisters' : tyres_wear[2],
   'fr_tyre_blisters' : tyres_wear[3],
   'fl_wing_damage' : fl_wing_damage,
   'fr_wing_damage' : fr_wing_damage,
   'rear_wing_damage' : rear_wing_damage,
   'floor_damage' : floor_damage,
   'diffuser_damage' : diffuser_damage,
   'sidepod_damage' : sidepod_damage,
   'drs_fault' : drs_fault,
   'ers_fault' : ers_fault,
   'gear_box_damage' : gear_box_damage,
   'engine_damage' : engine_damage,
   'engine_MGUH_wear' : engine_MGUH_wear,
   'engine_ES_wear' : engine_ES_wear,
   'engine_CE_wear' : engine_CE_wear,
   'engine_ICE_wear' : engine_ICE_wear,
   'engine_MGUK_wear' : engine_MGUK_wear,
   'engine_TC_wear' : engine_TC_wear,
   'engine_blown' : engine_blown,
   'engine_seized' : engine_seized,
 }

  tabela_vazia.append(linha)

df_final = pd.DataFrame(tabela_vazia)
df_final.to_csv("car_damage.csv", index=False)