import numpy as np
import pandas as pd
import xarray as xr
import glob
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

path = '/home/tabu/Escritorio/Doctorado/ClimDinam/TP1/'
path2 = '/media/tabu/JULIAexterno/climatologia_dinamica/'
#Guardo los datos de observaciones
precip_obs =  xr.open_dataset(path+'DATOS/precip.mon.total.v7_197601-200512_2.5_anu.nc')
climatologia = precip_obs.mean(dim='time')
time = precip_obs.time
timeattrs = precip_obs.time.attrs
time = xr.Dataset({'time':('time',time,timeattrs)})

list_h = []
list_h = glob.glob('CanESM2/pr*historical_r*anu.nc')
pr_hist = []
#Guardo el ensamble en tas_mod
for file in list_h:
    with xr.open_dataset(path2+file) as ds:

    pr = xr.open_dataset(path2+file)
    pr['time'] = time['time']
    pr_hist.append(pr)

pr_ens_hist = pr = xr.open_dataset(path2+'CanESM2/pr_Amon_CanESM2_historical_ensmean_197601-200512_2.5_anu.nc')

#Hago los cálculos


#Cierro los archivos
for i in range(len(list_h)):
    pr = pr_hist[i]
    pr.close()


list_rcp26 = []
list_rcp26 = glob.glob('CanESM2/pr*rcp26_r*207001-209912*anu.nc')
pr_rcp26 = []
#Guardo el ensamble en tas_mod
for file in list_rcp26:
    pr = xr.open_dataset(path2+file)
    pr['time'] = time['time']
    pr_rcp26.append(pr)

pr_ens_rcp26 = pr = xr.open_dataset(path2+'CanESM2/pr_Amon_CanESM2_rcp26_ensmean_207001-209912_2.5_anu.nc')

list_rcp85 = []
list_rcp85 = glob.glob('CanESM2/pr*rcp85_r*207001-209912*anu.nc')
pr_rcp85 = []
#Guardo el ensamble en tas_mod
for file in list_rcp85:
    pr = xr.open_dataset(path2+file)
    pr['time'] = time['time']
    pr_rcp85.append(pr)

pr_ens_rcp85 = pr = xr.open_dataset(path2+'CanESM2/pr_Amon_CanESM2_rcp85_ensmean_207001-209912_2.5_anu.nc')



