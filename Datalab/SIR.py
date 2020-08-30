import pandas as pd

N = 50372424 #población inicial estimada con proyección del DANE https://www.dane.gov.co/index.php/estadisticas-por-tema/demografia-y-poblacion/proyecciones-de-poblacion

t_contagio, t_recup, t_muerte = 1.1, 0.44, 0.11 #tasas

df = pd.DataFrame()

for i in range(200):
    tiempo = i    
    if i == 0:
        susc = N - 1
        conta = 0
        conf_acum = 1
        recup_acum = 0
        muert_acum = 0
        recup = 0
        muert = 0
        activ = conf_acum
        d = pd.DataFrame({'Tiempo': [tiempo], 'Susceptibles': [susc], "Confirmados":[conf_acum],"Total recuperados":[recup_acum],"Total muertos":[muert_acum],"Contagios":[conta],"Recuperados":[recup],"Muertos":[muert],"Activos":[activ]})
    else:
        if df['Confirmados'][i-1]>=N:
            conta = 0
        else:
            conta = t_contagio*df['Activos'][i-1]*df['Susceptibles'][i-1]/N
        recup = t_recup*df['Activos'][i-1]
        muert = t_muerte*df['Activos'][i-1]
        activ = df['Activos'][i-1] + conta - recup - muert
        susc = df['Susceptibles'][i-1] - conta
        conf_acum = df['Confirmados'][i-1] + conta
        recup_acum = df['Total recuperados'][i-1] + recup 
        muert_acum = df['Total muertos'][i-1] + muert
        d = pd.DataFrame({'Tiempo': [tiempo], 'Susceptibles': [susc], "Confirmados":[conf_acum],"Total recuperados":[recup_acum],"Total muertos":[muert_acum],"Contagios":[conta],"Recuperados":[recup],"Muertos":[muert],"Activos":[activ]})
    df = df.append(d, ignore_index=True)
    del d
    
lines = df['Susceptibles'].plot.line(x='Tiempo')
lines = df['Confirmados'].plot.line(x='Tiempo')
lines = df['Activos'].plot.line(x='Tiempo')

