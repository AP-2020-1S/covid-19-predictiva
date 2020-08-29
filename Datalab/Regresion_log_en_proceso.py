# import libraries 
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt 
# sklearn specific function to obtain R2 calculations  
from sklearn.metrics import r2_score 

data = pd.read_csv("new_df4.csv", sep=",") ## Se hace lectura de archivo

data['fecha_diagnostico'] = pd.to_datetime(data['fecha_diagnostico']).dt.tz_localize(None)

data['N_day'] = data['fecha_diagnostico'].dt.day

plt.figure(figsize =(8, 5)) 
  
x_data, y_data = (data["N_day"].values, data["casos_activos_FD"].values) 
  
plt.plot(x_data, y_data, 'ro') 
plt.title('Data: Cases Vs Day of infection') 
plt.ylabel('Cases') 
plt.xlabel('Day Number') 

# Definition of the logistic function 
def sigmoid(x, Beta_1, Beta_2): 
     y = 1 / (1 + np.exp(-Beta_1*(x-Beta_2))) 
     return y 
  
# Choosing initial arbitrary beta parameters 
beta_1 = 0.09
beta_2 = 305
  
# application of the logistic function using beta  
Y_pred = sigmoid(x_data, beta_1, beta_2) 
  
# point prediction 
plt.plot(x_data, Y_pred * 15000000000000., label = "Model") 
plt.plot(x_data, y_data, 'ro', label = "Data") 
plt.title('Data Vs Model') 
plt.legend(loc ='best') 
plt.ylabel('Cases') 
plt.xlabel('Day Number') 

