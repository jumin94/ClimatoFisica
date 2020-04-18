#Toma promedios espaciales globales de temperatura del periodo historico del modelo CanESM2 y compara con observaciones

import numpy as np
import pandas as pd
import xarray as xr
import glob
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
#Defino funciones -----------------------------------------------------------

def anomaly(dato):
   climatology = dato.groupby('time.month').mean('time')
   anomalia =  dato.groupby('time.month') - climatology
   return anomalia

# Abrir datos-----------------------------------------------------------------
path = '/home/tabu/Escritorio/Doctorado/ClimDinam/TP1/' 
list = []
list = glob.glob('canESM2/tas*historical*.nc')
tas_mod = []
#Guardo el ensamble en tas_mod 
for file in list:
    tas = xr.open_dataset(path+file)
    tas_mod.append(tas)

#Guardo las temperaturas en temp_obs
temp_obs =  xr.open_dataset(path+'tmp_cru_ts3.20_197601-200512_2.5_anu.nc')

#Calculo auxiliar  para hacer un promedio pesado por la latitud
lats = np.cos(tas_mod[0].lat.values*np.pi/180)
s = sum(lats)

#Calculo anomalias de la temperatura global
tas_glob = []
for run in range(len(tas_mod)):
    tas = tas_mod[run].tas.mean(dim='lon')*lats
    tas_glob.append(tas.sum(dim='lat')/s)

tas_anom = []
for run in range(len(tas_glob)):
    tas_anom.append(anomaly(tas_glob[run]))

tas_ens = (tas_anom[0] + tas_anom[1] + tas_anom[2] + tas_anom[3] + tas_anom[4] )/5

ens_min = np.zeros(30)
ens_max = np.zeros(30)
for i in range(len(tas_anom[0].values)):
    ens_min[i] = min(tas_anom[0].values[i], tas_anom[1].values[i] , tas_anom[2].values[i] , tas_anom[3].values[i] , tas_anom[4].values[i])
    ens_max[i] = max(tas_anom[0].values[i], tas_anom[1].values[i] , tas_anom[2].values[i] , tas_anom[3].values[i] , tas_anom[4].values[i])


#Calculo las anomalias de los datos
tas_glob_o = temp_obs.tmp.mean(dim='lon')*lats
tas_anom_o = anomaly(tas_glob_o.sum(dim='lat')/s)

#Como los datos son anuales y tienen formatos distintos de time me armo un t
t = np.arange(datetime(1976,7,1), datetime(2006,7,1), timedelta(days=365.3)).astype(datetime)
years = []
for year in t: years.append(year.strftime('%Y'))

#Plot 
fig1 = plt.figure()
ax = fig1.subplots(1)
ax.set_title('CanESM2 ensamble')
for run in range(len(tas_anom)):
    ax.plot(years,tas_anom[run].values,label='member:'+str(run+1))
    
ax.plot(years,tas_ens.values,'--r',label='ens mean')
ax.plot(years,tas_anom_o.values,'--k',label='obs')
ax.set_xlabel('año')
ax.set_ylabel('Anomalia de temperatura global [K]')
plt.xticks(years,rotation='vertical')
plt.legend()
plt.savefig(path+'CanESM2_global_temp_hist_ens.png')
#plt.show()
plt.clf()

fig2 = plt.figure()
ax = fig2.subplots(1)
ax.fill_between(years,ens_min,ens_max,alpha=.2,label='mod spread')
ax.plot(years,tas_ens.values,'--r',label='ens mean')
ax.plot(years,tas_anom_o.values,'--k',label='obs')
ax.set_xlabel('año')
ax.set_ylabel('Anomalia de temperatura global [K]')
plt.xticks(years,rotation='vertical')
plt.legend()
plt.savefig(path+'CanESM2_global_temp_hist_spread.png')
#plt.show()
plt.clf()



#Analisis estacional

