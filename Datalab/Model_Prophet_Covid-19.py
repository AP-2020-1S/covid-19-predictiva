import pandas as pd
from fbprophet import Prophet

data = pd.read_csv("data_final.csv", sep=",") ## Se hace lectura de archivo
data

confirmed = data.groupby('fecha_reporte_web').sum()['acumulado_dia_confirmados'].reset_index()
deaths = data.groupby('fecha_reporte_web').sum()['acumulado_dia_fallecidos'].reset_index()
recovered = data.groupby('fecha_reporte_web').sum()['acumulado_dia_recuperado'].reset_index()

confirmed.columns = ['ds','y']
#confirmed['ds'] = confirmed['ds'].dt.date
confirmed['ds'] = pd.to_datetime(confirmed['ds'])
confirmed.tail()

m = Prophet(interval_width=0.95) 
m.fit(confirmed) 
future = m.make_future_dataframe(periods=14) 
future.tail()

#predecir el futuro con fecha y límite superior e inferior del valor y
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

confirmed_forecast_plot = m.plot(forecast)

confirmed_forecast_plot =m.plot_components(forecast)

deaths.columns = ['ds','y']
deaths['ds'] = pd.to_datetime(deaths['ds'])
m = Prophet(interval_width=0.95)
m.fit(deaths)
future = m.make_future_dataframe(periods=14)
future.tail()

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

deaths_forecast_plot = m.plot(forecast)

deaths_forecast_plot = m.plot_components(forecast)

recovered.columns = ['ds','y']
recovered['ds'] = pd.to_datetime(recovered['ds'])
m = Prophet(interval_width=0.95)
m.fit(recovered)
future = m.make_future_dataframe(periods=7)
future.tail()
 
 
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
 
recovered_forecast_plot = m.plot(forecast)

recovered_forecast_plot = m.plot_components(forecast)










