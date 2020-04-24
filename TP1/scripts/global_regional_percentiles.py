#Toma promedios espaciales y grafica boxplots de temperatura global y regional

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
list = []
list = glob.glob('canESM2/tas*historical*.nc')

#Guardo las temperaturas en temp_obs
temp_obs =  xr.open_dataset(path+'tmp_cru_ts3.20_197601-200512_2.5_anu.nc')

#Calculo auxiliar  para hacer un promedio pesado por la latitud
lats = np.cos(temp_obs.lat.values*np.pi/180)
s = sum(lats)
tas_glob_o = temp_obs.tmp.mean(dim='lon')*lats
tas_anom_o = anomaly(tas_glob_o.sum(dim='lat')/s)
mask = temp_obs.tmp/temp_obs.tmp
time = mask.time
timeattrs = mask.time.attrs
time = xr.Dataset({'time':('time',time,timeattrs)})

tas_mod = []
#Guardo el ensamble en tas_mod y enmascaro el oceano
for file in list:
    tas = xr.open_dataset(path+file)
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

tas_ens = (tas_anom[0] + tas_anom[1] + tas_anom[2] + tas_anom[3] + tas_anom[4] )/5

ens_min = np.zeros(30)
ens_max = np.zeros(30)
for i in range(len(tas_anom[0].values)):
    ens_min[i] = min(tas_anom[0].values[i], tas_anom[1].values[i] , tas_anom[2].values[i] , tas_anom[3].values[i] , tas_anom[4].values[i])
    ens_max[i] = max(tas_anom[0].values[i], tas_anom[1].values[i] , tas_anom[2].values[i] , tas_anom[3].values[i] , tas_anom[4].values[i])

#Como los datos son anuales y tienen formatos distintos de time me armo un t
t = np.arange(datetime(1976,7,1), datetime(2006,7,1), timedelta(days=365.3)).astype(datetime)
years = []
for year in t: years.append(year.strftime('%Y'))


#Plot evaluación de extremos --------------------------------------------------------------------
fig = plt.subplots(nrows=1, ncols=1, figsize=(4, 6), sharey=True)
plot = pd.DataFrame({'Obs':tas_anom_o.values,'media ens':tas_ens.values,'r1':tas_anom[0].values,'r2':tas_anom[1].values,'r3':tas_anom[2].values,'r4':tas_anom[3].values,'r5':tas_anom[4].values})
ax2 = plot.plot.box(patch_artist=True)
ax2.set_aspect(2)
ax2.set_ylabel('Anomalia de temperatura (K)')
ax2.set_title('CanESM2')
plt.savefig(path+'global_temp_boxplot.png', bbox_inches='tight')
plt.clf()

#Regiones
#Calculo anomalias de la temperatura sudamerica -----------------------------------------
tas_SESA = []
for run in range(len(tas_mod)):
    tas = tas_mod[run].tas*mask
    tas = tas.sel(lat=slice(-35,-22.5)).sel(lon=slice(300,310)).mean(dim='lon').mean(dim='lat')
    tas_SESA.append(tas)

tas_anom_SESA = []
for run in range(len(tas_SESA)):
    tas_anom_SESA.append(anomaly(tas_SESA[run]))

tas_ens_SESA = (tas_anom_SESA[0] + tas_anom_SESA[1] + tas_anom_SESA[2] + tas_anom_SESA[3] + tas_anom_SESA[4] )/5

temp_obs_SESA = temp_obs.tmp.sel(lat=slice(-35,-22.5)).sel(lon=slice(300,310)).mean(dim='lon').mean(dim='lat')
temp_anom_SESA = anomaly(temp_obs_SESA)

#Plot evaluación de extremos --------------------------------------------------------------------
fig = plt.subplots(nrows=1, ncols=1, figsize=(4, 6), sharey=True)
plot = pd.DataFrame({'Obs':temp_anom_SESA.values,'media ens':tas_ens_SESA.values,'r1':tas_anom_SESA[0].values,'r2':tas_anom_SESA[1].values,'r3':tas_anom_SESA[2].values,'r4':tas_anom_SESA[3].values,'r5':tas_anom_SESA[4].values})
ax2 = plot.plot.box(patch_artist=True)
ax2.set_aspect(2)
ax2.set_ylabel('Anomalia de temperatura ($\circ$ C)')
ax2.set_title('CanESM2 - SESA - campo medio:'+str(round(np.mean(temp_obs_SESA.values),3)))
plt.savefig(path+'SESA_temp_boxplot.png', bbox_inches='tight')
plt.clf()

#Calculo anomalias de la temperatura sudamerica -----------------------------------------
tas_andes = []
for run in range(len(tas_mod)):
    tas = tas_mod[run].tas*mask
    tas = tas.sel(lat=slice(-71.25,-36.75)).sel(lon=slice(286,289)).mean(dim='lon').mean(dim='lat')
    tas_andes.append(tas)

tas_anom_andes = []
for run in range(len(tas_andes)):
    tas_anom_andes.append(anomaly(tas_andes[run]))

tas_ens_andes = (tas_anom_andes[0] + tas_anom_andes[1] + tas_anom_andes[2] + tas_anom_andes[3] + tas_anom_andes[4] )/5

temp_obs_andes = temp_obs.tmp.sel(lat=slice(-71.25,-36.75)).sel(lon=slice(286,289)).mean(dim='lon').mean(dim='lat')
temp_anom_andes = anomaly(temp_obs_andes)

#Plot evaluación de extremos --------------------------------------------------------------------
fig = plt.subplots(nrows=1, ncols=1, figsize=(4, 6), sharey=True)
plot = pd.DataFrame({'Obs':temp_anom_andes.values,'media ens':tas_ens_andes.values,'r1':tas_anom_andes[0].values,'r2':tas_anom_andes[1].values,'r3':tas_anom_andes[2].values,'r4':tas_anom_andes[3].values,'r5':tas_anom_andes[4].values})
ax2 = plot.plot.box(patch_artist=True)
ax2.set_aspect(2)
ax2.set_ylabel('Anomalia de temperatura ($\circ$ C)')
ax2.set_title('CanESM2 - Andes - campo medio:'+str(round(np.mean(temp_obs_andes.values),3)))
plt.savefig(path+'andes_temp_boxplot.png', bbox_inches='tight')
plt.clf()


