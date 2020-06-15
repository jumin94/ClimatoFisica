#Mapas de bias en precipitacion periodo historico del modelo CanESM2, CanESM5 con respecto a observaciones

import numpy as np
import pandas as pd
import xarray as xr
import glob
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import cartopy.crs as ccrs
import cartopy.feature
from cartopy.util import add_cyclic_point
import matplotlib as mpl
mpl.rcParams['hatch.linewidth'] = 0.5  # previous pdf hatch linewidth

#Defino funciones 
def anomaly(dato,obs):
   climatologia = obs.mean(dim='time')
   anomalia = dato.mean(dim='time') - climatologia
   return climatologia, anomalia

# Abrir datos-----------------------------------------------------------------
path = '/home/tabu/Escritorio/Doctorado/ClimDinam/TP2/'
path2 = '/media/tabu/JULIAexterno/climatologia_dinamica/'

#Abro CanESM2
CanESM2_ens = xr.open_dataset(path2+'CanESM2/pr_Amon_CanESM2_historical_ensmean_197601-200512_2.5_mes.nc')

#Abro CanESM5
CanESM5_ens = xr.open_dataset(path2+'CanESM5/pr_Amon_CanESM5_historical_ensmean1p1f1_2.5_mes.nc')

#Summer monsoon obs HS
def annual_range_HS(dato):
 summer = dato.sel(time=dato['time.season']=='DJF').mean(dim='time').pr
 annual = dato.mean(dim='time').pr
 rango = summer/annual *100 
 return rango

def annual_range_HN(dato):
 summer = dato.sel(time=dato['time.season']=='JJA').mean(dim='time').pr
 annual = dato.mean(dim='time').pr
 rango = summer/annual *100
 return rango


def mapa(dato,titulo):
    #America del sur -------Observaciones-----------------------------------------
    fig = plt.figure(figsize=(10, 18),dpi=300,constrained_layout=True)
    fig_size = plt.rcParams["figure.figsize"]
    data_crs = ccrs.PlateCarree(central_longitude=0)
    projection = ccrs.PlateCarree()
    ax1 = plt.subplot(1,1,1,projection=projection)
    #ax1.set_extent([275,335, 10, -60], crs=data_crs)
    clevels = np.arange(0,300,50)
    im1=ax1.contourf(cyclic_lons, lat, dato,clevels,transform=data_crs,cmap='Blues',extend='both')
    ax1.add_feature(cartopy.feature.COASTLINE)
    ax1.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=.5)
    ax1.gridlines(crs=data_crs, linewidth=0.3, linestyle='-')
    #ax1.set_title('Annual range')
    #Saco las coordenadas de la figura hasta ahora
    plt0_ax = plt.gca()
    left, bottom1, width, height = plt0_ax.get_position().bounds
    first_plot_left = plt0_ax.get_position().bounds[0]
    #Utilizo las coordenadas para definir la posición de la colorbar 1
    colorbar_axes = fig.add_axes([first_plot_left + .9, bottom1, 0.02, 1.2*height])
    fig_size[0] = width*4 + 10
    fig_size[1] = height*2 + 3
    plt.rcParams["figure.figsize"] = fig_size
    fig.suptitle(str(titulo), y=0.68, x=0.5,fontsize=20)
    cbar = plt.colorbar(im1, colorbar_axes, fraction=0.05, pad=0.04,aspect=18, orientation='vertical')
    ticklabs = cbar.ax.get_yticklabels()
    cbar.ax.set_yticklabels(ticklabs, fontsize=16)
    cbar.set_label('summer/annual % ',fontsize=20)
    return fig

titulo = 'Rango anual verano HS CanESM2'
lon = np.arange(0, 362, 362/144)
mon_range_CanESM2 = annual_range_HS(CanESM2_ens)
lat = mon_range_CanESM2.lat
cyclic_data, cyclic_lons = add_cyclic_point(mon_range_CanESM2, coord=lon)
mapa(cyclic_data,titulo)
plt.savefig(path+'Annual_range_CanESM2_HS.png',bbox_inches='tight')
plt.clf

titulo = 'Rango anual verano HS CanESM5'
lon = np.arange(0, 362, 362/144)
mon_range_CanESM5 = annual_range_HS(CanESM5_ens)
lat = mon_range_CanESM5.lat
cyclic_data, cyclic_lons = add_cyclic_point(mon_range_CanESM5, coord=lon)
mapa(cyclic_data,titulo)
plt.savefig(path+'Annual_range_CanESM5_HS.png',bbox_inches='tight')
plt.clf


titulo = 'Rango anual verano HN CanESM2'
lon = np.arange(0, 362, 362/144)
mon_range_CanESM2 = annual_range_HN(CanESM2_ens)
lat = mon_range_CanESM2.lat
cyclic_data, cyclic_lons = add_cyclic_point(mon_range_CanESM2, coord=lon)
mapa(cyclic_data,titulo)
plt.savefig(path+'Annual_range_CanESM2_HN.png',bbox_inches='tight')
plt.clf

titulo = 'Rango anual verano HN CanESM5'
lon = np.arange(0, 362, 362/144)
mon_range_CanESM5 = annual_range_HN(CanESM5_ens)
lat = mon_range_CanESM5.lat
cyclic_data, cyclic_lons = add_cyclic_point(mon_range_CanESM5, coord=lon)
mapa(cyclic_data,titulo)
plt.savefig(path+'Annual_range_CanESM5_HN.png',bbox_inches='tight')
plt.clf


