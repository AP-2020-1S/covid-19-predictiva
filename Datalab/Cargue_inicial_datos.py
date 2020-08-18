import pandas as pd

##El cargue inicial de datos se debería hacer una única vez, luego de esto se
##debe actualizar los nuevos registros y aquellos registros donde se identifiquen
##modificaciones en el estado del paciente (pendiente: definir cómo identificar
##las modificaciones en el estado del paciente)

url = 'https://www.datos.gov.co/resource/gt2j-8ykr.json?$offset=' ##conexión con la fuente de datos

consolidated_files = pd.DataFrame() ##tabla donde se almacenarán los registros

length = 0 ##este parámero deberá cambiar para luego hacer posible el cargue de nuevos registros (actualizarse con el tamaño actual de la tabla)
i = 0 ##acumulador para poder establecer el número del registro a leer (funciona junto con offset)

 #En cada nueva iteración se leen 1000 registros comenzando por el último encontrado para no repetir
while length % 1000 == 0: ##mientras la cantidad de registros dividido mil no deje residuo significa que aún hay registros por extraer
    offset = str(i*1000) ##offset indica en qué registro comenzar
    df = pd.read_json(url+offset)
    consolidated_files = consolidated_files.append(df, sort=False) ##se agregan los nuevos datos a la tabla sin borrar los anteriores
    length = len(consolidated_files) ##se actualiza la cantidad de registros en la tabla
    i = i + 1
    print('Cargados ' + offset + ' registros') ##validador en pantalla de ejecución
del df