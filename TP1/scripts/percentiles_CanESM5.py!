#Toma promedios espaciales y grafica boxplots de temperatura global y regional y la serie temporal 

import numpy as np
import pandas as pd
import xarray as xr
import glob
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
#Defino funciones -----------------------------------------------------------

def anomaly(dato):
   climatology = dato.mean('time')
   anomalia =  dato - climatology
   return anomalia

# Abrir datos-----------------------------------------------------------------
path = '/home/tabu/Escritorio/Doctorado/ClimDinam/TP1/'
path2 = '/media/tabu/JULIAexterno/climatologia_dinamica/CanESM5/'
list = []
list = glob.glob('tas*historical*p2f1_2.5_anu.nc')

#Guardo las temperaturas en temp_obs
temp_obs =  xr.open_dataset(path+'DATOS/tmp_cru_ts3.20_197601-200512_2.5_anu.nc')

#Calculo auxiliar  para hacer un promedio pesado por la latitud
lats = np.cos(temp_obs.lat.values*np.pi/180)
s = sum(lats)
tas_glob_o = temp_obs.tmp.mean(dim='lon')*lats
tas_anom_o = anomaly(tas_glob_o.sum(dim='lat')/s)
#Genero mascara del oceano con las observaciones
mask = temp_obs.tmp/temp_obs.tmp
time = mask.time
timeattrs = mask.time.attrs
time = xr.Dataset({'time':('time',time,timeattrs)})

tas_mod = []
#Guardo el ensamble en tas_mod y enmascaro el oceano
for file in list:
    tas = xr.open_dataset(path2+file)
    tas['time'] = time['time']
    tas_mod.append(tas)

#Calculo anomalias de la temperatura global
tas_glob = []
for run in range(len(tas_mod)):
    tas = tas_mod[run].tas*mask
    tas = tas.mean(dim='lon')*lats
    tas = tas.sum(dim='lat')/s
    tas_glob.append(tas)

tas_anom = []
for run in range(len(tas_glob)):
    tas_anom.append(anomaly(tas_glob[run]))

tas_ens = (tas_anom[0] + tas_anom[1] + tas_anom[2] + tas_anom[3] + tas_anom[4] + tas_anom[5] + tas_anom[6] + tas_anom[7] + tas_anom[8] + tas_anom[9] + tas_anom[10] + tas_anom[11] + tas_anom[12] + tas_anom[13] + tas_anom[14] + tas_anom[15] + tas_anom[16] + tas_anom[17] + tas_anom[18] + tas_anom[19] + tas_anom[20] + tas_anom[21] + tas_anom[22] + tas_anom[23] + tas_anom[24])/25

ens_min = np.zeros(30)
ens_max = np.zeros(30)
for i in range(len(tas_anom[0].values)):
    ens_min[i] = min(tas_anom[0].values[i], tas_anom[1].values[i] , tas_anom[2].values[i] , tas_anom[3].values[i] , tas_anom[4].values[i], tas_anom[5].values[i], tas_anom[6].values[i] , tas_anom[7].values[i] , tas_anom[8].values[i] , tas_anom[9].values[i],tas_anom[10].values[i], tas_anom[11].values[i] , tas_anom[12].values[i] , tas_anom[13].values[i] , tas_anom[14].values[i], tas_anom[15].values[i], tas_anom[16].values[i] , tas_anom[17].values[i] , tas_anom[18].values[i] , tas_anom[19].values[i],tas_anom[20].values[i], tas_anom[21].values[i] , tas_anom[22].values[i] , tas_anom[23].values[i] , tas_anom[24].values[i])
    ens_max[i] = max(tas_anom[0].values[i], tas_anom[1].values[i] , tas_anom[2].values[i] , tas_anom[3].values[i] , tas_anom[4].values[i], tas_anom[5].values[i], tas_anom[6].values[i] , tas_anom[7].values[i] , tas_anom[8].values[i] , tas_anom[9].values[i],tas_anom[10].values[i], tas_anom[11].values[i] , tas_anom[12].values[i] , tas_anom[13].values[i] , tas_anom[14].values[i], tas_anom[15].values[i], tas_anom[16].values[i] , tas_anom[17].values[i] , tas_anom[18].values[i] , tas_anom[19].values[i],tas_anom[20].values[i], tas_anom[21].values[i] , tas_anom[22].values[i] , tas_anom[23].values[i] , tas_anom[24].values[i])

#Como los datos son anuales y tienen formatos distintos de time me armo un t
t = np.arange(datetime(1976,7,1), datetime(2006,7,1), timedelta(days=365.3)).astype(datetime)
years = []
for year in t: years.append(year.strftime('%Y'))


#Plot evaluacion temporal ---------------------------------------------------------------------
fig1 = plt.figure()
ax = fig1.subplots(1)
ax.set_title('CanESM5 ensamble')
for run in range(len(tas_anom)):
    ax.plot(years,tas_anom[run].values,label='member:'+str(run+1))

ax.plot(years,tas_ens.values,'--r',label='ens mean')
ax.plot(years,tas_anom_o.values,'--k',label='obs')
ax.set_xlabel('año')
ax.set_ylabel('Anomalia de temperatura global [K]')
plt.xticks(years,rotation='vertical')
plt.legend()
plt.savefig(path+'plots/CanESM5_global_temp_hist_ens_bien.png')
#plt.show()
plt.clf()

fig2 = plt.figure()
ax = fig2.subplots(1)
ax.set_title('CanESM5 ensamble')
ax.fill_between(years,ens_min,ens_max,alpha=.2,label='mod spread')
ax.plot(years,tas_ens.values,'--r',label='ens mean')
ax.plot(years,tas_anom_o.values,'--k',label='obs')
ax.set_xlabel('año')
ax.set_ylabel('Anomalia de temperatura global [K]')
plt.xticks(years,rotation='vertical')
plt.legend()
plt.savefig(path+'plots/CanESM5_global_temp_hist_spread_bien.png')
#plt.show()
plt.clf()

#Regiones
#Calculo anomalias de la temperatura sudamerica -----------------------------------------
tas_SESA = []
for run in range(len(tas_mod)):
    tas = tas_mod[run].tas*mask
    tas = tas.sel(lat=slice(-35,-22.5)).sel(lon=slice(300,310)).mean(dim='lon').mean(dim='lat')
    tas_SESA.append(tas)

tas_anom = []
for run in range(len(tas_SESA)):
    tas_anom.append(anomaly(tas_SESA[run]))

tas_ens = (tas_anom[0] + tas_anom[1] + tas_anom[2] + tas_anom[3] + tas_anom[4] + tas_anom[5] + tas_anom[6] + tas_anom[7] + tas_anom[8] + tas_anom[9] + tas_anom[10] + tas_anom[11] + tas_anom[12] + tas_anom[13] + tas_anom[14] + tas_anom[15] + tas_anom[16] + tas_anom[17] + tas_anom[18] + tas_anom[19] + tas_anom[20] + tas_anom[21] + tas_anom[22] + tas_anom[23] + tas_anom[24])/25

ens_min = np.zeros(30)
ens_max = np.zeros(30)
for i in range(len(tas_anom[0].values)):
    ens_min[i] = min(tas_anom[0].values[i], tas_anom[1].values[i] , tas_anom[2].values[i] , tas_anom[3].values[i] , tas_anom[4].values[i], tas_anom[5].values[i], tas_anom[6].values[i] , tas_anom[7].values[i] , tas_anom[8].values[i] , tas_anom[9].values[i],tas_anom[10].values[i], tas_anom[11].values[i] , tas_anom[12].values[i] , tas_anom[13].values[i] , tas_anom[14].values[i], tas_anom[15].values[i], tas_anom[16].values[i] , tas_anom[17].values[i] , tas_anom[18].values[i] , tas_anom[19].values[i],tas_anom[20].values[i], tas_anom[21].values[i] , tas_anom[22].values[i] , tas_anom[23].values[i] , tas_anom[24].values[i])
    ens_max[i] = max(tas_anom[0].values[i], tas_anom[1].values[i] , tas_anom[2].values[i] , tas_anom[3].values[i] , tas_anom[4].values[i], tas_anom[5].values[i], tas_anom[6].values[i] , tas_anom[7].values[i] , tas_anom[8].values[i] , tas_anom[9].values[i],tas_anom[10].values[i], tas_anom[11].values[i] , tas_anom[12].values[i] , tas_anom[13].values[i] , tas_anom[14].values[i], tas_anom[15].values[i], tas_anom[16].values[i] , tas_anom[17].values[i] , tas_anom[18].values[i] , tas_anom[19].values[i],tas_anom[20].values[i], tas_anom[21].values[i] , tas_anom[22].values[i] , tas_anom[23].values[i] , tas_anom[24].values[i])

temp_obs_SESA = temp_obs.tmp.sel(lat=slice(-35,-22.5)).sel(lon=slice(300,310)).mean(dim='lon').mean(dim='lat')
temp_anom_SESA = anomaly(temp_obs_SESA)

fig3 = plt.figure()
ax = fig3.subplots(1)
ax.set_title('CanESM5 SESA ensamble')
ax.fill_between(years,ens_min,ens_max,alpha=.2,label='mod spread')
ax.plot(years,tas_ens.values,'--r',label='ens mean')
ax.plot(years,temp_anom_SESA.values,'--k',label='obs')
ax.set_xlabel('año')
ax.set_ylabel('Anomalia de temperatura SESA [K]')
plt.xticks(years,rotation='vertical')
plt.legend()
plt.savefig(path+'plots/CanESM5_SESA_temp_hist_spread.png')
#plt.show()
plt.clf()

#Calculo anomalias de la temperatura sudamerica -----------------------------------------
tas_andes = []
for run in range(len(tas_mod)):
    tas = tas_mod[run].tas*mask
    tas = tas.sel(lat=slice(-71.25,-36.75)).sel(lon=slice(286,289)).mean(dim='lon').mean(dim='lat')
    tas_andes.append(tas)

tas_anom = []
for run in range(len(tas_andes)):
    tas_anom.append(anomaly(tas_andes[run]))

tas_ens = (tas_anom[0] + tas_anom[1] + tas_anom[2] + tas_anom[3] + tas_anom[4] + tas_anom[5] + tas_anom[6] + tas_anom[7] + tas_anom[8] + tas_anom[9] + tas_anom[10] + tas_anom[11] + tas_anom[12] + tas_anom[13] + tas_anom[14] + tas_anom[15] + tas_anom[16] + tas_anom[17] + tas_anom[18] + tas_anom[19] + tas_anom[20] + tas_anom[21] + tas_anom[22] + tas_anom[23] + tas_anom[24])/25

ens_min = np.zeros(30)
ens_max = np.zeros(30)
for i in range(len(tas_anom[0].values)):
    ens_min[i] = min(tas_anom[0].values[i], tas_anom[1].values[i] , tas_anom[2].values[i] , tas_anom[3].values[i] , tas_anom[4].values[i], tas_anom[5].values[i], tas_anom[6].values[i] , tas_anom[7].values[i] , tas_anom[8].values[i] , tas_anom[9].values[i],tas_anom[10].values[i], tas_anom[11].values[i] , tas_anom[12].values[i] , tas_anom[13].values[i] , tas_anom[14].values[i], tas_anom[15].values[i], tas_anom[16].values[i] , tas_anom[17].values[i] , tas_anom[18].values[i] , tas_anom[19].values[i],tas_anom[20].values[i], tas_anom[21].values[i] , tas_anom[22].values[i] , tas_anom[23].values[i] , tas_anom[24].values[i])
    ens_max[i] = max(tas_anom[0].values[i], tas_anom[1].values[i] , tas_anom[2].values[i] , tas_anom[3].values[i] , tas_anom[4].values[i], tas_anom[5].values[i], tas_anom[6].values[i] , tas_anom[7].values[i] , tas_anom[8].values[i] , tas_anom[9].values[i],tas_anom[10].values[i], tas_anom[11].values[i] , tas_anom[12].values[i] , tas_anom[13].values[i] , tas_anom[14].values[i], tas_anom[15].values[i], tas_anom[16].values[i] , tas_anom[17].values[i] , tas_anom[18].values[i] , tas_anom[19].values[i],tas_anom[20].values[i], tas_anom[21].values[i] , tas_anom[22].values[i] , tas_anom[23].values[i] , tas_anom[24].values[i])

temp_obs_andes = temp_obs.tmp.sel(lat=slice(-71.25,-36.75)).sel(lon=slice(286,289)).mean(dim='lon').mean(dim='lat')
temp_anom_andes = anomaly(temp_obs_andes)

fig4 = plt.figure()
ax = fig4.subplots(1)
ax.set_title('CanESM5 Andes ensemble')
ax.fill_between(years,ens_min,ens_max,alpha=.2,label='mod spread')
ax.plot(years,tas_ens.values,'--r',label='ens mean')
ax.plot(years,temp_anom_andes.values,'--k',label='obs')
ax.set_xlabel('año')
ax.set_ylabel('Anomalia de temperatura Andes [K]')
plt.xticks(years,rotation='vertical')
plt.legend()
plt.savefig(path+'plots/CanESM5_andes_temp_hist_spread.png')
#plt.show()
plt.clf()

