import pandas as pd
import datetime as dt
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as mplt
from pandas import Grouper
import matplotlib.dates as mdates 
import warnings
warnings.filterwarnings("ignore")

url = 'https://www.datos.gov.co/resource/gt2j-8ykr.json?$offset=' ##conexión con la fuente de datos

consolidated_files = pd.DataFrame() ##tabla donde se almacenarán los registros

length = 0
i = 0 ##acumulador para poder establecer el número del registro a leer (funciona junto con offset)

##En cada nueva iteración se leen 1000 registros (este es el máximo por iteración) comenzando por el último encontrado para no repetir
while length % 1000 == 0: ##mientras la cantidad de registros dividido mil no deje residuo significa que aún hay registros por extraer
    offset = str(i*1000) ##offset indica en qué registro comenzar
    df = pd.read_json(url+offset)
    consolidated_files = consolidated_files.append(df, sort=False) ##se agregan los nuevos datos a la tabla sin borrar los anteriores
    length = len(consolidated_files) ##se actualiza la cantidad de registros en la tabla para ser evaluada en la próxima iteración
    i = i + 1
    print('Cargados ' + str(length) + ' registros') ##validador en pantalla de ejecución
del df
print('Cargue completado: ' + str(length) + ' registros') ##validar finalización del cargue de los registros
consolidated_files.to_csv(r'..\Datos\CasosPositivosCOVID19_Colombia.csv')

### **Descripción metadata**


**Ciudad de ubicación:** por seguridad de las personas, algunos datos serán limitados evitando así la exposición y posible identificación en determinados municipios. 

**Edad:** edad del paciente.

**Sexo:** sexo del paciente.

**Tipo:** por seguridad de las personas, algunos datos serán limitados evitando así la exposición y posible identificación en determinados municipios. 

**Estado:** * corresponde a muertes no relacionadas con COVID-19, aún si eran casos activos ** Hay pacientes recuperados para COVID-19, que pueden permanecer en hospitalización por otras comorbilidades.

**Fecha de muerte:** fecha de muerte del paciente.

**Fecha recuperado:** fecha recuperado.

**Fecha reporte Web:** fecha reporte Web.

**Tipo recuperación:** se refiere a la variable de tipo de recuperación que tiene dos opciones: PCR y tiempo. PCR indica que la persona se encuentra recuperada por segunda muestra, en donde dio negativo para el virus; mientras que tiempo significa que son personas que cumplieron 30 días posteriores al inicio de síntomas o toma de muestras que no tienen síntomas, que no tengan más de 70 años ni que estén hospitalizados.



consolidated_files['fecha_recuperado'] = pd.to_datetime(consolidated_files['fecha_recuperado']).dt.tz_localize(None) ## Se cambia el tipo de dato de objeto a datatime
consolidated_files['fecha_reporte_web'] = pd.to_datetime(consolidated_files['fecha_reporte_web']).dt.tz_localize(None) 
consolidated_files['fecha_de_muerte'] = pd.to_datetime(consolidated_files['fecha_de_muerte']).dt.tz_localize(None)

data_filtrada_ciudades = consolidated_files.loc[consolidated_files['ciudad_de_ubicaci_n'].isin(['Medellín','Bogotá D.C','Cali','Barranquilla','Cartagena de Indias'])]
data_filtrada_ciudades ## Se filtran las ciudades principales de trabajo

data_confirmados = data_filtrada_ciudades.loc[~data_filtrada_ciudades['atenci_n'].isin(['Fallecido','Recuperado'])] ## se filtra la columna atenci_n sacando los fallecidos y recuperados para tener los confirmados

data_confirmados.dropna(axis=0, how='all', inplace = True) ## Se eliminan los vacíos
data_confirmados

data_1 = data_confirmados[['fecha_reporte_web','ciudad_de_ubicaci_n', 'edad','atenci_n','sexo', 'tipo', 'estado']]  
data_1 ## Se extraen las columnas de data_confirmados

dataset_confirmados = pd.DataFrame({'conteo_confirmados' : data_1.groupby( ['fecha_reporte_web','ciudad_de_ubicaci_n','edad','sexo','tipo','estado'] ).size()}).reset_index()
dataset_confirmados ## Se convierte a dataframe, se hace agrupación para confirmados y se hace el conteo.


data_fallecidos = data_filtrada_ciudades.loc[data_filtrada_ciudades['atenci_n'].isin(['Fallecido'])]
data_fallecidos ## Se filtran los fallecidos

data_fallecidos.dropna(axis=0, how='all', inplace = True)  ## Se eliminan los vacíos
data_fallecidos  

data_2 = data_fallecidos[['fecha_de_muerte','fecha_reporte_web','ciudad_de_ubicaci_n', 'edad','atenci_n','sexo', 'tipo', 'estado']] 
data_2 ## Se obtienen las columnas de interés para fallecidos

dataset_fallecidos = pd.DataFrame({'conteo_fallecidos' : data_2.groupby( ['fecha_de_muerte','fecha_reporte_web','ciudad_de_ubicaci_n','edad','sexo','tipo','estado'] ).size()}).reset_index()
## Se convierte a dataframe, se hace agrupación para fallecidos y se hace el conteo.


data_recuperado = data_filtrada_ciudades.loc[data_filtrada_ciudades['atenci_n'].isin(['Recuperado'])]
data_recuperado ## se filtra para obtener los recuperados

data_recuperado.dropna(axis=0, how='all', inplace = True)
data_recuperado ## Se eliminan los vacíos

data_3 = data_recuperado[['fecha_recuperado','fecha_reporte_web','ciudad_de_ubicaci_n','edad','atenci_n','sexo', 'tipo', 'estado']] 
data_3 ## Se obtienen las columnas de interés para recuperados

dataset_recuperado = pd.DataFrame({'conteo_recuperado' : data_3.groupby( ['fecha_recuperado','fecha_reporte_web','ciudad_de_ubicaci_n','edad','sexo','tipo','estado'] ).size()}).reset_index()
## Se convierte a dataframe, se hace agrupación para recuperados y se hace el conteo.


df_filtrado = data_filtrada_ciudades[['fecha_reporte_web','fecha_de_muerte','fecha_recuperado','ciudad_de_ubicaci_n', 'estado','sexo','edad','tipo']]
df_filtrado ## Se obtienen las columnas de interés para los joins que se realizarán

df_filtrado = df_filtrado.drop_duplicates() ## Se eliminan los duplicados


new_df = pd.merge(df_filtrado, dataset_confirmados,  how='left', left_on=['fecha_reporte_web','ciudad_de_ubicaci_n','estado','sexo','edad','tipo'], right_on = ['fecha_reporte_web','ciudad_de_ubicaci_n','estado','sexo','edad','tipo'])
new_df ## Se hace left join de las tablas de df_filtrado y dataset_confirmados


new_df1 = pd.merge(new_df, dataset_fallecidos,  how='left', left_on=['fecha_reporte_web','fecha_de_muerte','ciudad_de_ubicaci_n','estado','sexo','edad','tipo'], right_on = ['fecha_reporte_web','fecha_de_muerte','ciudad_de_ubicaci_n','estado','sexo','edad','tipo'])
new_df1 ## Se hace left join de las tablas de new_df y dataset_fallecidos


new_df2 = pd.merge(new_df1, dataset_recuperado,  how='left', left_on=['fecha_reporte_web','fecha_recuperado','ciudad_de_ubicaci_n','estado','sexo','edad','tipo'], right_on = ['fecha_reporte_web','fecha_recuperado','ciudad_de_ubicaci_n','estado','sexo','edad','tipo'])
new_df2  ## Se hace left join de las tablas de new_df1 y dataset_recuperado


new_df2.dropna(axis=0, how='all', inplace = True) ## Se eliminan vacíos

new_df2['casos_activos'] = new_df2.conteo_confirmados - new_df2.conteo_fallecidos - new_df2.conteo_recuperado ## Se calculan los casos activos

new_df2['casos_activos'].mask(new_df2['casos_activos'] < 0, 0, inplace=True) ## si en casos activos da valor negativo lo lleva a cero

ruta = 'new_df2.csv'
new_df2.to_csv(ruta, index = True) ## Se exporta el archivo final



