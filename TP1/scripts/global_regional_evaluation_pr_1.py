#Toma promedios espaciales y grafica boxplots de temperatura global y regional y la serie temporal 

import numpy as np
import pandas as pd
import xarray as xr
import glob
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
#Defino funciones -----------------------------------------------------------

# Abrir datos-----------------------------------------------------------------
path = '/home/tabu/Escritorio/Doctorado/ClimDinam/TP1/'
list = []
list = glob.glob('canESM2/pr*historical*anu.nc')

#Guardo las temperaturas en temp_obs
precip_obs =  xr.open_dataset(path+'DATOS/precip.mon.total.v7_197601-200512_2.5_anu.nc')

#Calculo auxiliar  para hacer un promedio pesado por la latitud
#lats = np.cos(precip_obs.lat.values*np.pi/180)
#s = sum(lats)
#l = len(precip_obs.lon)
#precip_glob_o = precip_obs.precip.sum(dim='lon')/l
#precip_glob_o = precip_glob_o*lats
#precip_glob_o = precip_obs.precip.mean(dim='lon')*lats
#precip_glob_o = precip_glob_o.sum(dim='lat')/s
precip_glob_o = precip_obs.precip.mean(dim='lat').mean(dim='lon')
mask = precip_obs.precip/precip_obs.precip
time = mask.time
timeattrs = mask.time.attrs
time = xr.Dataset({'time':('time',time,timeattrs)})

pr_mod = []
#Guardo el ensamble en tas_mod y enmascaro el oceano
for file in list:
    pr = xr.open_dataset(path+file)
    pr['time'] = time['time']
    pr_mod.append(pr)

#Calculo anomalias de la temperatura global
pr_glob = []
for run in range(len(pr_mod)):
    pr = pr_mod[run].pr*mask
    #pr = pr.mean(dim='lon')*lats
    #pr = pr.sum(dim='lat')/s
    pr = pr.mean(dim='lon').mean(dim='lat')
    pr_glob.append(pr)

pr_ens = (pr_glob[0] + pr_glob[1] + pr_glob[2] + pr_glob[3] + pr_glob[4] )/5

ens_min = np.zeros(30)
ens_max = np.zeros(30)
for i in range(len(pr_glob[0].values)):
    ens_min[i] = min(pr_glob[0].values[i], pr_glob[1].values[i] , pr_glob[2].values[i] , pr_glob[3].values[i] , pr_glob[4].values[i])
    ens_max[i] = max(pr_glob[0].values[i], pr_glob[1].values[i] , pr_glob[2].values[i] , pr_glob[3].values[i] , pr_glob[4].values[i])

#Como los datos son anuales y tienen formatos distintos de time me armo un t
t = np.arange(datetime(1976,7,1), datetime(2006,7,1), timedelta(days=365.3)).astype(datetime)
years = []
for year in t: years.append(year.strftime('%Y'))


#Plot evaluacion temporal ---------------------------------------------------------------------
fig1 = plt.figure()
ax = fig1.subplots(1)
ax.set_title('CanESM2 ensamble')
for run in range(len(pr_glob)):
    ax.plot(years,pr_glob[run].values,label='member:'+str(run+1))

ax.plot(years,pr_glob.values,'--r',label='ens mean')
ax.plot(years,precip_glob_o.values,'--k',label='obs')
ax.set_xlabel('año')
ax.set_ylabel('Precipitacion global [mm/año]')
plt.xticks(years,rotation='vertical')
plt.legend()
plt.savefig(path+'CanESM2_global_pr_hist_ens_bien.png')
#plt.show()
plt.clf()

fig2 = plt.figure()
ax = fig2.subplots(1)
ax.fill_between(years,ens_min,ens_max,alpha=.2,label='mod spread')
ax.plot(years,pr_ens.values,'--r',label='ens mean')
ax.plot(years,precip_glob_o.values,'--k',label='obs')
ax.set_xlabel('año')
ax.set_ylabel('Precipitacion global [mm/año]')
plt.xticks(years,rotation='vertical')
plt.legend()
plt.savefig(path+'CanESM2_global_pr_hist_spread_bien.png')
#plt.show()
plt.clf()

#Regiones
#Calculo anomalias de la temperatura sudamerica -----------------------------------------
pre_SESA = []
for run in range(len(tas_mod)):
    pr = pr_mod[run].pr*mask
    pr = pr.sel(lat=slice(-35,-22.5)).sel(lon=slice(300,310)).mean(dim='lon').mean(dim='lat')
    pr_SESA.append(tas)

pr_ens_SESA = (pr_anom_SESA[0] + pr_anom_SESA[1] + pr_anom_SESA[2] + pr_anom_SESA[3] + pr_anom_SESA[4] )/5

ens_min_SESA = np.zeros(30)
ens_max_SESA = np.zeros(30)
for i in range(len(pr_anom_SESA[0].values)):
    ens_min_SESA[i] = min(pr_anom_SESA[0].values[i], pr_anom_SESA[1].values[i] , pr_anom_SESA[2].values[i] , pr_anom_SESA[3].values[i] , pr_anom_SESA[4].values[i])
    ens_max_SESA[i] = max(pr_anom_SESA[0].values[i], pr_anom_SESA[1].values[i] , pr_anom_SESA[2].values[i] , pr_anom_SESA[3].values[i] , pr_anom_SESA[4].values[i])

pr_obs_SESA = precip_obs.precip.sel(lat=slice(-35,-22.5)).sel(lon=slice(300,310)).mean(dim='lon').mean(dim='lat')

fig3 = plt.figure()
ax = fig3.subplots(1)
ax.fill_between(years,ens_min_SESA,ens_max_SESA,alpha=.2,label='mod spread')
ax.plot(years,pr_ens_SESA.values,'--r',label='ens mean')
ax.plot(years,pr_obs_SESA.values,'--k',label='obs')
ax.set_xlabel('año')
ax.set_ylabel('Precipitacion SESA [mm/año]')
plt.xticks(years,rotation='vertical')
plt.legend()
plt.savefig(path+'CanESM2_SESA_pr_hist_spread.png')
#plt.show()
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

ens_min_andes = np.zeros(30)
ens_max_andes = np.zeros(30)
for i in range(len(tas_anom_andes[0].values)):
    ens_min_andes[i] = min(tas_anom_andes[0].values[i], tas_anom_andes[1].values[i] , tas_anom_andes[2].values[i] , tas_anom_andes[3].values[i] , tas_anom_andes[4].values[i])
    ens_max_andes[i] = max(tas_anom_andes[0].values[i], tas_anom_andes[1].values[i] , tas_anom_andes[2].values[i] , tas_anom_andes[3].values[i] , tas_anom_andes[4].values[i])

temp_obs_andes = temp_obs.tmp.sel(lat=slice(-71.25,-36.75)).sel(lon=slice(286,289)).mean(dim='lon').mean(dim='lat')
temp_anom_andes = anomaly(temp_obs_andes)

fig4 = plt.figure()
ax = fig4.subplots(1)
ax.fill_between(years,ens_min_andes,ens_max_andes,alpha=.2,label='mod spread')
ax.plot(years,tas_ens_andes.values,'--r',label='ens mean')
ax.plot(years,temp_anom_andes.values,'--k',label='obs')
ax.set_xlabel('año')
ax.set_ylabel('Anomalia de temperatura Andes [K]')
plt.xticks(years,rotation='vertical')
plt.legend()
plt.savefig(path+'CanESM2_andes_temp_hist_spread.png')
#plt.show()
plt.clf()

