import pandas as pd

car_damage = pd.read_csv(r'C:\Users\User\Projeto_F1\dados_interlagos_130426\translated_car_damage.csv').sort_values("tempo")
lap = pd.read_csv(r'C:\Users\User\Projeto_F1\dados_interlagos_130426\translated_lap.csv').sort_values("tempo")
motion = pd.read_csv(r'C:\Users\User\Projeto_F1\dados_interlagos_130426\translated_motion.csv').sort_values("tempo")
status = pd.read_csv(r'C:\Users\User\Projeto_F1\dados_interlagos_130426\translated_status.csv').sort_values("tempo")
telemetry = pd.read_csv(r'C:\Users\User\Projeto_F1\dados_interlagos_130426\translated_telemtria.csv').sort_values("tempo")
tyre_extended = pd.read_csv(r'C:\Users\User\Projeto_F1\dados_interlagos_130426\translated_tyre_data.csv').sort_values("tempo")

'''''
eu uso o sort_values("tempo") para ter certeza que mesmo que um pacote tenha
atrasado, os dataframes se mantenham na ordem correta
'''''
telemetria_completa = telemetry

dados = [motion,lap,status,car_damage,tyre_extended]

for df in dados:
    #selecionar apenas colunas diferentes
    colunas = df.columns.difference(telemetria_completa.columns).tolist()
    colunas.append('tempo')
    #garantir que o referencial tempo esteja no DataFrame

    telemetria_completa = pd.merge_asof(
        telemetria_completa,
        df[colunas],
        on = 'tempo',
        direction = 'backward'
    )

telemetria_completa.to_csv('telemetria_completa.csv', index=False)
