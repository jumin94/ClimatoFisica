#Toma promedios espaciales globales de temperatura del periodo historico del modelo CanESM2 y compara con observaciones

import numpy as np
import pandas as pd
import xarray as xr
import glob

#Defino funciones -----------------------------------------------------------

def anomaly(dato):
   climatology = dato.groupby('time.month').mean('time')
   anomalia =  dato.groupby('time.month') - climatology
   return anomalia

# Abrir datos-----------------------------------------------------------------
path = '/home/tabuEscritorio/Doctorado/ClimDinam/TP1/' 
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

#Analisis estacional

