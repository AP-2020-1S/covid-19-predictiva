import pandas as pd
import numpy as np
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline
import plotly.express as px
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, acf, pacf,arma_order_select_ic
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA
import warnings
warnings.simplefilter('ignore')
from random import seed
from sklearn.model_selection import train_test_split
import datetime as dt
from datetime import datetime
from datetime import date

data = pd.read_csv("data_final.csv", sep = ',') ## cargue datos
data

data['fecha_reporte_web'] = pd.to_datetime(data['fecha_reporte_web']).dt.tz_localize(None) ## se cambia la fecha a tipo fecha

train, test = train_test_split(data, test_size=0.2) ## se dividen los datos con 80% de entrenamiento y 20% de evaluación

train.sample(6) ## imprime 6 registros de la muestra

test.sample(6) ## imprime 6 registros de la muestra

#Function for making a time serie on a designated country and plotting the rolled mean and standard 
def roll(ciudad,case='acumulado_dia_recuperado'):
    ts=data.loc[(data['ciudad_de_ubicaci_n']==ciudad)]  
    ts=ts[['fecha_reporte_web',case]]
    ts=ts.set_index('fecha_reporte_web')
    ts.astype('int64')
    a=len(ts.loc[(ts['acumulado_dia_recuperado']>=10)])
    ts=ts[-a:]
    return (ts.rolling(window=4,center=False).mean().dropna())


sns.set(palette = 'Set1',style='darkgrid')
#Function for making a time serie on a designated country and plotting the rolled mean and standard 
def roll(ciudad,case='acumulado_dia_recuperado'):
    ts=data.loc[(data['ciudad_de_ubicaci_n']==ciudad)]  
    ts=ts[['fecha_reporte_web',case]]
    ts=ts.set_index('fecha_reporte_web')
    ts.astype('int64')
    a=len(ts.loc[(ts['acumulado_dia_recuperado']>=10)])
    ts=ts[-a:]
    return (ts.rolling(window=4,center=False).mean().dropna())


def rollPlot(ciudad, case='acumulado_dia_recuperado'):
    ts=data.loc[(data['ciudad_de_ubicaci_n']==ciudad)]  
    ts=ts[['fecha_reporte_web',case]]
    ts=ts.set_index('fecha_reporte_web')
    ts.astype('int64')
    a=len(ts.loc[(ts['acumulado_dia_recuperado']>=10)])
    ts=ts[-a:]
    plt.figure(figsize=(16,6))
    plt.plot(ts.rolling(window=7,center=False).mean().dropna(),label='Media Móvil')
    plt.plot(ts[case])
    plt.plot(ts.rolling(window=7,center=False).std(),label='std Móvil')
    plt.legend()
    plt.title('Cases distribution in %s with rolling mean and standard' %ciudad)
    plt.xticks([])

tsC6=roll('Medellín')
rollPlot('Medellín')

tsC7=roll('Cali')
rollPlot('Cali')

tsC8=roll('Barranquilla')
rollPlot('Barranquilla')

tsC9=roll('Cartagena de Indias')
rollPlot('Cartagena de Indias')

tsC10=roll('Bogotá D.C.')
rollPlot('Bogotá D.C.')

#Decomposing the ts to find its properties
fig=sm.tsa.seasonal_decompose(tsC6.values,freq=7).plot()

fig=sm.tsa.seasonal_decompose(tsC7.values,freq=7).plot()

fig=sm.tsa.seasonal_decompose(tsC8.values,freq=7).plot()

fig=sm.tsa.seasonal_decompose(tsC9.values,freq=7).plot()

fig=sm.tsa.seasonal_decompose(tsC10.values,freq=7).plot()

#Function to check the stationarity of the time serie using Dickey fuller test
def stationarity(ts):
    print('Results of Dickey-Fuller Test:')
    test = adfuller(ts, autolag='AIC')
    results = pd.Series(test[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for i,val in test[4].items():
        results['Critical Value (%s)'%i] = val
    print (results)

#Para Medellín
tsC=tsC6['acumulado_dia_recuperado'].values
stationarity(tsC)

#Para Cali
tsC=tsC7['acumulado_dia_recuperado'].values
stationarity(tsC)

#Para Barranquilla
tsC=tsC8['acumulado_dia_recuperado'].values
stationarity(tsC)

#Para Cartagena de Indias
tsC=tsC9['acumulado_dia_recuperado'].values
stationarity(tsC)

#Para Bogotá D.C.
tsC=tsC10['acumulado_dia_recuperado'].values
stationarity(tsC)

def corr(ts):
    plot_acf(ts,lags=12,title="ACF")
    plot_pacf(ts,lags=12,title="PACF")
    
#Para Medellín
corr(tsC6)

#Para Cali
corr(tsC7)

#Para Barranquilla
corr(tsC8)

#Para Cartagena de Indias
corr(tsC9)

#Para Bogotá D.C.
corr(tsC10)

train = train.set_index(['fecha_reporte_web'])
test = test.set_index(['fecha_reporte_web'])

def create_features(data,label=None):
    """
    Creates time series features from datetime index.
    """
    df = data.copy()
    df['fecha_reporte_web'] = df.index
    df['hour'] = df['fecha_reporte_web'].dt.hour
    df['dayofweek'] = df['fecha_reporte_web'].dt.dayofweek
    df['quarter'] = df['fecha_reporte_web'].dt.quarter
    df['month'] = df['fecha_reporte_web'].dt.month
    df['year'] = df['fecha_reporte_web'].dt.year
    df['dayofyear'] = df['fecha_reporte_web'].dt.dayofyear
    df['dayofmonth'] = df['fecha_reporte_web'].dt.day
    df['weekofyear'] = df['fecha_reporte_web'].dt.weekofyear
    
    X = df[['hour','dayofweek','quarter','month','year','dayofyear','dayofmonth','weekofyear']]
   
    return X
	
train_features=pd.DataFrame(create_features(train))
test_features=pd.DataFrame(create_features(test))
features_and_target_train = pd.concat([train,train_features], axis=1)
features_and_target_test = pd.concat([test,test_features], axis=1)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
def FunLabelEncoder(df):
    for c in df.columns:
        if df.dtypes[c] == object:
            le.fit(df[c].astype(str))
            df[c] = le.transform(df[c].astype(str))
    return df
features_and_target_train= FunLabelEncoder(features_and_target_train)

x_train= features_and_target_train[['ciudad_de_ubicaci_n','month', 'dayofyear', 'dayofmonth' , 'weekofyear']]
y1 = features_and_target_train[['acumulado_dia_recuperado']]
y2 =features_and_target_train[['acumulado_dia_fallecidos']]
x_test = features_and_target_test[['ciudad_de_ubicaci_n', 'month', 'dayofyear', 'dayofmonth' , 'weekofyear']]

#Mean absolute percentage error
def mape(y1, y_pred): 
    y1, y_pred = np.array(y1), np.array(y_pred)
    return np.mean(np.abs((y1 - y_pred) / y1)) * 100

def split(ts):
    #splitting 85%/15% because of little amount of data
    size = int(len(ts) * 0.85)
    train= ts[:size]
    test = ts[size:]
    return(train,test)

#Mean absolute percentage error
def mape(y1, y_pred): 
    y1, y_pred = np.array(y1), np.array(y_pred)
    return np.mean(np.abs((y1 - y_pred) / y1)) * 100

def split(ts):
    #splitting 85%/15% because of little amount of data
    size = int(len(ts) * 0.85)
    train= ts[:size]
    test = ts[size:]
    return(train,test)


#Arima modeling for ts
def arima(ts,test):
    p=d=q=range(0,6)
    a=99999
    pdq=list(itertools.product(p,d,q))
    
    #Determining the best parameters
    for var in pdq:
        try:
            model = ARIMA(ts, order=var)
            result = model.fit()

            if (result.aic<=a) :
                a=result.aic
                param=var
        except:
            continue
            
    #Modeling
    model = ARIMA(ts, order=param)
    result = model.fit()
    result.plot_predict(start=int(len(ts) * 0.7), end=int(len(ts) * 1.2))
    pred=result.forecast(steps=len(test))[0]
    #Plotting results
    f,ax=plt.subplots()
    plt.plot(pred,c='green', label= 'predictions')
    plt.plot(test, c='red',label='real values')
    plt.legend()
    plt.title('True vs predicted values')
    #Printing the error metrics
    print(result.summary())        
    
    print('\nMean absolute percentage error: %f'%mape(test,pred))
    return (pred)



train,test=split(tsC)
pred=arima(train,test)

#Mean absolute percentage error
def mape(y2, y_pred): 
    y2, y_pred = np.array(y2), np.array(y_pred)
    return np.mean(np.abs((y2 - y_pred) / y2)) * 100

def split(ts):
    #splitting 85%/15% because of little amount of data
    size = int(len(ts) * 0.85)
    train= ts[:size]
    test = ts[size:]
    return(train,test)


#Arima modeling for ts
def arima(ts,test):
    p=d=q=range(0,6)
    a=99999
    pdq=list(itertools.product(p,d,q))
    
    #Determining the best parameters
    for var in pdq:
        try:
            model = ARIMA(ts, order=var)
            result = model.fit()

            if (result.aic<=a) :
                a=result.aic
                param=var
        except:
            continue
            
    #Modeling
    model = ARIMA(ts, order=param)
    result = model.fit()
    result.plot_predict(start=int(len(ts) * 0.7), end=int(len(ts) * 1.2))
    pred=result.forecast(steps=len(test))[0]
    #Plotting results
    f,ax=plt.subplots()
    plt.plot(pred,c='green', label= 'predictions')
    plt.plot(test, c='red',label='real values')
    plt.legend()
    plt.title('True vs predicted values')
    #Printing the error metrics
    print(result.summary())        
    
    print('\nMean absolute percentage error: %f'%mape(test,pred))
    return (pred)



train,test=split(tsC)
pred=arima(train,test)

