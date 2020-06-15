import numpy as np
import pandas as pd
import xarray as xr
import glob
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

#Funciones
#Hago los cálculos
def bandas_lat(dato,indice):
    bandas = [0,5,5,9,9,13,13,17,17,21,21,25,25,29,29,33,33,37,36,40,40,44,44,48,48,52,52,56,56,60,60,64,64,68,68,73]
    weights = np.cos(np.deg2rad(dato.lat))
    weights.name = "weights"
    cont1 = 0
    cont2 = 1
    areas = np.array([3.9,11.6,18.9,25.6,31.5,36.4,40.2,42.8,44.1,44.1,42.8,40.2,36.4,31.5,25.6,18.9,11.6,3.9,255,255])*1000000
    pr_bandas = np.array([])
    for i in range(18):
        index1 = bandas[cont1]
        index2 = bandas[cont2]
        weights_aux = weights[index1:index2]
        aux = dato.evspsbl*86400*365
        aux = aux.mean(dim='time')
        aux = aux.isel(lat=slice(index1,index2)).mean(dim='lon')*weights_aux
        area = sum(weights_aux)
        aux_weight = aux.sum(dim='lat')/area
        pr_bandas = np.append(pr_bandas,aux_weight.values)
        cont1 = cont1 + 2
        cont2 = cont2 + 2
        #print(cont2)
    weights_HN = weights[0:37]
    weights_HS = weights[36:73]
    aux = dato.evspsbl*86400*365
    aux = aux.mean(dim='time')
    auxHN = aux.isel(lat=slice(0,37)).mean(dim='lon')*weights_HN
    auxHS = aux.isel(lat=slice(36,73)).mean(dim='lon')*weights_HS
    area_HN = sum(weights_HN)
    area_HS = sum(weights_HS)
    aux_weightHN = auxHN.sum(dim='lat')/area_HN
    aux_weightHS = auxHS.sum(dim='lat')/area_HS
    pr_bandas = np.append(pr_bandas,aux_weightHN.values)
    pr_bandas = np.append(pr_bandas,aux_weightHS.values)
    pr_bandas = (pr_bandas*areas)/31536000
    pr_bandas = pr_bandas/areas
    pr_bandas_dic = {'90-80N':round(pr_bandas[0],1),'80-70N':round(pr_bandas[1],1),'70-60N':round(pr_bandas[2],1),'60-50N':round(pr_bandas[3],1),'50-40N':round(pr_bandas[4],1),'40-30N':round(pr_bandas[5],1),'30-20N':round(pr_bandas[6],1),'20-10N':round(pr_bandas[7],1),'10-0N':round(pr_bandas[8],1),'0-10S':round(pr_bandas[9],1),'20-10S':round(pr_bandas[10],1),'30-20S':round(pr_bandas[11],1),'40-30S':round(pr_bandas[12],1),'50-40S':round(pr_bandas[13],1),'60-50S':round(pr_bandas[14],1),'70-60S':round(pr_bandas[15],1),'80-70S':round(pr_bandas[16],1),'90-80S':round(pr_bandas[17],1),'90-0N':round(pr_bandas[18],1),'90-0S':round(pr_bandas[19],1)}
    pr_bandas_dic = pd.DataFrame(pr_bandas_dic,index=[str(indice)])
    return pr_bandas_dic

def bandas_lat_pr(dato,indice):
    bandas = [0,5,5,9,9,13,13,17,17,21,21,25,25,29,29,33,33,37,36,40,40,44,44,48,48,52,52,56,56,60,60,64,64,68,68,73]
    weights = np.cos(np.deg2rad(dato.lat))
    weights.name = "weights"
    cont1 = 0
    cont2 = 1
    areas = np.array([3.9,11.6,18.9,25.6,31.5,36.4,40.2,42.8,44.1,44.1,42.8,40.2,36.4,31.5,25.6,18.9,11.6,3.9,255,255])*1000000
    pr_bandas = np.array([])
    for i in range(18):
        index1 = bandas[cont1]
        index2 = bandas[cont2]
        weights_aux = weights[index1:index2]
        aux = dato.pr*86400*365
        aux = aux.mean(dim='time')
        aux = aux.isel(lat=slice(index1,index2)).mean(dim='lon')*weights_aux
        area = sum(weights_aux)
        aux_weight = aux.sum(dim='lat')/area
        pr_bandas = np.append(pr_bandas,aux_weight.values)
        cont1 = cont1 + 2
        cont2 = cont2 + 2
        #print(cont2)
    weights_HN = weights[0:37]
    weights_HS = weights[36:73]
    aux = dato.pr*86400*365
    aux = aux.mean(dim='time')
    auxHN = aux.isel(lat=slice(0,37)).mean(dim='lon')*weights_HN
    auxHS = aux.isel(lat=slice(36,73)).mean(dim='lon')*weights_HS
    area_HN = sum(weights_HN)
    area_HS = sum(weights_HS)
    aux_weightHN = auxHN.sum(dim='lat')/area_HN
    aux_weightHS = auxHS.sum(dim='lat')/area_HS
    pr_bandas = np.append(pr_bandas,aux_weightHN.values)
    pr_bandas = np.append(pr_bandas,aux_weightHS.values)
    pr_bandas = (pr_bandas*areas)/31536000
    pr_bandas = pr_bandas/areas
    pr_bandas_dic = {'90-80N':round(pr_bandas[0],1),'80-70N':round(pr_bandas[1],1),'70-60N':round(pr_bandas[2],1),'60-50N':round(pr_bandas[3],1),'50-40N':round(pr_bandas[4],1),'40-30N':round(pr_bandas[5],1),'30-20N':round(pr_bandas[6],1),'20-10N':round(pr_bandas[7],1),'10-0N':round(pr_bandas[8],1),'0-10S':round(pr_bandas[9],1),'20-10S':round(pr_bandas[10],1),'30-20S':round(pr_bandas[11],1),'40-30S':round(pr_bandas[12],1),'50-40S':round(pr_bandas[13],1),'60-50S':round(pr_bandas[14],1),'70-60S':round(pr_bandas[15],1),'80-70S':round(pr_bandas[16],1),'90-80S':round(pr_bandas[17],1),'90-0N':round(pr_bandas[18],1),'90-0S':round(pr_bandas[19],1)}
    pr_bandas_dic = pd.DataFrame(pr_bandas_dic,index=[str(indice)])
    return pr_bandas_dic


#Dataframe con valores+-------------------------------------------------
C = pd.DataFrame(columns=['90-80S','80-70S','70-60S','60-50S','50-40S','40-30S','30-20S','20-10S','10-0S','0-10N','20-10N','30-20N','40-30N','50-40N','60-50N','70-60N','80-70N','90-80N','90-0S','90-0N'])

#Datos------------------------------------------------------------------------
path = '/home/tabu/Escritorio/Doctorado/ClimDinam/TP4/'
path1 = '/home/tabu/Escritorio/Doctorado/ClimDinam/TP1/'
path2 = '/media/tabu/JULIAexterno/climatologia_dinamica/'
#Observaciones -------------------------------
precip_obs =  xr.open_dataset(path1+'DATOS/precip.mon.total.v7_197601-200512_2.5_anu.nc')
precip_obs['pr'] = precip_obs.precip
climatologia = precip_obs.mean(dim='time')
time = precip_obs.time
timeattrs = precip_obs.time.attrs
time = xr.Dataset({'time':('time',time,timeattrs)})

#Modelos--------------------------------------
list_h = []
list_h = glob.glob('CanESM2/pr*historical_r*anu.nc')
pr_hist = []
#Guardo el ensamble en tas_mod
for file in list_h:
    pr = xr.open_dataset(path2+file)
    pr['time'] = time['time']
    pr_hist.append(pr)

pr_ens_hist  = xr.open_dataset(path2+'CanESM2/pr_Amon_CanESM2_historical_ensmean_197601-200512_2.5_anu.nc')

list_rcp26 = []
list_rcp26 = glob.glob('CanESM2/pr*rcp26_r*207001-209912*anu.nc')
pr_rcp26 = []
#Guardo el ensamble en tas_mod
for file in list_rcp26:
    pr = xr.open_dataset(path2+file)
    pr['time'] = time['time']
    pr_rcp26.append(pr)

pr_ens_rcp26 = xr.open_dataset(path2+'CanESM2/pr_Amon_CanESM2_rcp26_ensmean_207001-209912_2.5_anu.nc')

list_rcp85 = []
list_rcp85 = glob.glob('CanESM2/pr*rcp85_r*207001-209912*anu.nc')
pr_rcp85 = []
#Guardo el ensamble en tas_mod
for file in list_rcp85:
    pr = xr.open_dataset(path2+file)
    pr['time'] = time['time']
    pr_rcp85.append(pr)

pr_ens_rcp85 = xr.open_dataset(path2+'CanESM2/pr_Amon_CanESM2_rcp85_ensmean_207001-209912_2.5_anu.nc')

#Historico ensamble run y miembros
Precip_hist = pd.concat([C,bandas_lat_pr(pr_ens_hist,'ens_hist')],axis=0)
for i in range(len(pr_hist)):
    Precip_hist = pd.concat([Precip_hist,bandas_lat_pr(pr_hist[i],'hist_r'+str(i+1))],axis=0)

Precip_rcp26 = pd.concat([C,bandas_lat_pr(pr_ens_rcp26,'ens_rcp26')],axis=0)
for i in range(len(pr_rcp26)):
    Precip_rcp26 = pd.concat([Precip_rcp26,bandas_lat_pr(pr_rcp26[i],'rcp26_r'+str(i+1))],axis=0)

Precip_rcp85 = pd.concat([C,bandas_lat_pr(pr_ens_rcp85,'ens_rcp85')],axis=0)
for i in range(len(pr_rcp85)):
    Precip_rcp85 = pd.concat([Precip_rcp85,bandas_lat_pr(pr_rcp85[i],'rcp85_r'+str(i+1))],axis=0)

#Precip_hist = Precip_hist.reset_index()
Precip_hist.to_csv(path+'precip_hist.txt')
Precip_rcp26.to_csv(path+'precip_rcp26.txt')
Precip_rcp85.to_csv(path+'precip_rcp85.txt')


#Evaporacion------------------------------------------------------------------------------------
list_h = []
list_h = glob.glob('CanESM2/evspsbl*historical_r*anu.nc')
evspsbl_hist = []
#Guardo el ensamble en tas_mod
for file in list_h:
    evspsbl = xr.open_dataset(path2+file)
    evspsbl['time'] = time['time']
    evspsbl_hist.append(evspsbl)

evspsbl_ens_hist  = xr.open_dataset(path2+'CanESM2/evspsbl_Amon_CanESM2_historical_ensmean_197601-200512_2.5_anu.nc')

list_rcp26 = []
list_rcp26 = glob.glob('CanESM2/evspsbl*rcp26_r*207001-209912*anu.nc')
evspsbl_rcp26 = []
#Guardo el ensamble en tas_mod
for file in list_rcp26:
    evspsbl = xr.open_dataset(path2+file)
    evspsbl['time'] = time['time']
    evspsbl_rcp26.append(evspsbl)

evspsbl_ens_rcp26 = xr.open_dataset(path2+'CanESM2/evspsbl_Amon_CanESM2_rcp26_ensmean_207001-209912_2.5_anu.nc')

list_rcp85 = []
list_rcp85 = glob.glob('CanESM2/evspsbl*rcp85_r*207001-209912*anu.nc')
evspsbl_rcp85 = []
#Guardo el ensamble en tas_mod
for file in list_rcp85:
    evspsbl = xr.open_dataset(path2+file)
    evspsbl['time'] = time['time']
    evspsbl_rcp85.append(evspsbl)

evspsbl_ens_rcp85 = xr.open_dataset(path2+'CanESM2/evspsbl_Amon_CanESM2_rcp85_ensmean_207001-209912_2.5_anu.nc')

#Historico ensamble run y miembros
Evspsbl_hist = pd.concat([C,bandas_lat(evspsbl_ens_hist,'ens_hist')],axis=0)
for i in range(len(evspsbl_hist)):
    Evspsbl_hist = pd.concat([Evspsbl_hist,bandas_lat(evspsbl_hist[i],'hist_r'+str(i+1))],axis=0)

Evspsbl_rcp26 = pd.concat([C,bandas_lat(evspsbl_ens_rcp26,'ens_rcp26')],axis=0)
for i in range(len(evspsbl_rcp26)):
    Evspsbl_rcp26 = pd.concat([Evspsbl_rcp26,bandas_lat(evspsbl_rcp26[i],'rcp26_r'+str(i+1))],axis=0)

Evspsbl_rcp85 = pd.concat([C,bandas_lat(evspsbl_ens_rcp85,'ens_rcp85')],axis=0)
for i in range(len(evspsbl_rcp85)):
    Evspsbl_rcp85 = pd.concat([Evspsbl_rcp85,bandas_lat(evspsbl_rcp85[i],'rcp85_r'+str(i+1))],axis=0)

#Precip_hist = Precip_hist.reset_index()
Evspsbl_hist.to_csv(path+'evspsbl_hist.txt')
Evspsbl_rcp26.to_csv(path+'evspsbl_rcp26.txt')
Evspsbl_rcp85.to_csv(path+'evspsbl_rcp85.txt')


