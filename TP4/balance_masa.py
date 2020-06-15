import numpy as np
import pandas as pd
import xarray as xr
import glob
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

#Datos------------------------------------------------------------------------
path = '/home/tabu/Escritorio/Doctorado/ClimDinam/TP4/'
path1 = '/home/tabu/Escritorio/Doctorado/ClimDinam/TP1/'
path2 = '/media/tabu/JULIAexterno/climatologia_dinamica/'
#Modelos-Precipitacion-------------------------------------
list_h = []
list_h = glob.glob('CanESM2/pr*historical_r*anu.nc')
pr_hist = []
#---------------------
for file in list_h:
    pr = xr.open_dataset(path2+file)
    pr['time'] = time['time']
    pr_hist.append(pr)

pr_ens_hist  = xr.open_dataset(path2+'CanESM2/pr_Amon_CanESM2_historical_ensmean_197601-200512_2.5_anu.nc')

#Modelos-Evaporacion------------------------------------------------------------------------------------
list_h = []
list_h = glob.glob('CanESM2/evspsbl*historical_r*anu.nc')
evspsbl_hist = []
#Guardo el ensamble en tas_mod
for file in list_h:
    evspsbl = xr.open_dataset(path2+file)
    evspsbl['time'] = time['time']
    evspsbl_hist.append(evspsbl)

evspsbl_ens_hist  = xr.open_dataset(path2+'CanESM2/evspsbl_Amon_CanESM2_historical_ensmean_197601-200512_2.5_anu.nc')

#Calculo promedios globales
pr_glob = []
for run in range(len(pr_hist)):
    #weights = np.cos(np.deg2rad(pr_hist[run].lat))
    #pr = pr_hist[run].pr*86400*365
    #area = sum(weights)
    #pr = pr.mean(dim='lon')*weights
    #pr_weight = pr.sum(dim='lat')/area
    #pr_glob.append(((pr_weight*510000000)/(86400*365))/510000000)
    pr_glob.append(global_mean(pr_hist[run],pr_hist[run].pr))

def global_mean(dato,datovalor):
    weights = np.cos(np.deg2rad(dato.lat))
    aux = datovalor*86400*365
    area = sum(weights)
    aux = aux.mean(dim='lon')*weights
    aux_weight = aux.sum(dim='lat')/area
    return(((aux_weight*510000000)/(86400*365))/510000000)

ev_glob = []
for run in range(len(evspsbl_hist)):
    weights = np.cos(np.deg2rad(evspsbl_hist[run].lat))
    ev = evspsbl_hist[run].evspsbl*86400*365
    area = sum(weights)
    ev = ev.mean(dim='lon')*weights
    ev_weight = ev.sum(dim='lat')/area
    ev_glob.append(((ev_weight*510000000)/(86400*365))/510000000)

#Ensamble min y max
ens_min_pr = np.zeros(30)
ens_max_pr = np.zeros(30)
for i in range(len(pr_glob[0].values)):
    ens_min_pr[i] = min(pr_glob[0].values[i], pr_glob[1].values[i] , pr_glob[2].values[i] , pr_glob[3].values[i] , pr_glob[4].values[i])
    ens_max_pr[i] = max(pr_glob[0].values[i], pr_glob[1].values[i] , pr_glob[2].values[i] , pr_glob[3].values[i] , pr_glob[4].values[i])

pr_glob_mean = global_mean(pr_ens_hist,pr_ens_hist.pr)
ev_glob_mean = global_mean(evspsbl_ens_hist,evspsbl_ens_hist.evspsbl)

#Ensamble min y max
ens_min_ev = np.zeros(30)
ens_max_ev = np.zeros(30)
for i in range(len(ev_glob[0].values)):
    ens_min_ev[i] = min(ev_glob[0].values[i], ev_glob[1].values[i] , ev_glob[2].values[i] , ev_glob[3].values[i] , ev_glob[4].values[i])
    ens_max_ev[i] = max(ev_glob[0].values[i], ev_glob[1].values[i] , ev_glob[2].values[i] , ev_glob[3].values[i] , ev_glob[4].values[i])

#Como los datos son anuales y tienen formatos distintos de time me armo un t
t = np.arange(datetime(1976,7,1), datetime(2006,7,1), timedelta(days=365.3)).astype(datetime)
years = []
for year in t: years.append(year.strftime('%Y'))

#Plot----------------------------------------------------------
fig1 = plt.figure()
ax = fig2.subplots(1)
ax.fill_between(years,ens_min_pr,ens_max_pr,alpha=.2,label='ens_spread_pr')
ax.plot(years,pr_glob_mean.values,'--r',label='ens mean pr')
ax.fill_between(years,ens_min_ev,ens_max_ev,alpha=.2,label='ens_spread_evspsbl')
ax.plot(years,ev_glob_mean.values,'--g',label='ens mean evspsbl')
ax.set_xlabel('año')
ax.set_ylabel('Masa [mm/año]')
plt.xticks(years,rotation='vertical')
plt.legend()
plt.title('Balance de masa')
plt.savefig(path+'Precip_Evap_balance.png')
#plt.show()
plt.clf()


