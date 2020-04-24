#Mapas de climatologia y desviacion standard de los campos medios globales de temperatura del periodo historico del modelo CanESM2 y compara con observaciones

import numpy as np
import pandas as pd
import xarray as xr
import glob
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import cartopy.crs as ccrs
import cartopy.feature
from cartopy.util import add_cyclic_point
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['hatch.linewidth'] = 0.5  # previous pdf hatch linewidth

#Defino funciones -----------------------------------------------------------

def anomaly(dato,obs):
   climatology = obs.mean(dim='time')
   sd =  np.sqrt(sum((dato - climatology)**2)/len(dato.time))
   return climatology, sd

# Abrir datos-----------------------------------------------------------------
path = '/home/tabu/Escritorio/Doctorado/ClimDinam/TP1/'
list = []
list = glob.glob('canESM2/pr*historical*anu.nc')
tas_mod = []
#Guardo el ensamble en tas_mod 
for file in list:
    tas = xr.open_dataset(path+file)
    tas_mod.append(tas)

#Guardo las temperaturas en temp_obs
precip_obs =  xr.open_dataset(path+'precip.mon.total.v7_197601-200512_2.5_anu.nc')
climatologia = precip_obs.mean(dim='time')

sd = []
#Armo una lista de modelos
for run in tas_mod:
    clima, std = anomaly(run.pr,precip_obs.precip)
    sd.append(std)

lat = tas_mod[0].lat
lon = tas_mod[0].lon

def mapa(dato,titulo):
    lat = precip_obs.lat
    cyclic_data, cyclic_lon = add_cyclic_point(dato,coord=lon)
    #SoutherHemisphere Stereographic
    fig = plt.figure(figsize=(20, 14),dpi=300,constrained_layout=True)
    fig.suptitle(str(titulo), y=0.9, x=0.5,fontsize=25)
    fig_size = plt.rcParams["figure.figsize"]
    data_crs = ccrs.PlateCarree(central_longitude=0)
    projection = ccrs.PlateCarree()
    ax1 = plt.subplot(projection=projection)
    ax1.set_extent([-180,180, -90, 90], crs=data_crs)
    clevels = np.arange(np.min(dato),np.max(dato),(np.max(dato)-np.min(dato))/11)
    im1=ax1.contourf(cyclic_lon, lat, cyclic_data,clevels,transform=data_crs,cmap='YlGn',extend='both')
    #ax1.add_feature(cartopy.feature.LAND, zorder=100, edgecolor='k')
    ax1.add_feature(cartopy.feature.COASTLINE)
    ax1.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=.5)
    ax1.gridlines(crs=data_crs, linewidth=0.3, linestyle='-')
    #Saco las coordenadas de la figura hasta ahora
    plt0_ax = plt.gca()
    left, bottom1, width, height = plt0_ax.get_position().bounds
    first_plot_left = plt0_ax.get_position().bounds[0]
    #Utilizo las coordenadas para definir la posición de la colorbar
    colorbar_axes = fig.add_axes([first_plot_left + 0.9, bottom1-0.04, 0.01, 1.2*height])
    fig_size[0] = width*4 + 10
    fig_size[1] = height*2 + 3
    plt.rcParams["figure.figsize"] = fig_size
    cbar = plt.colorbar(im1, colorbar_axes, fraction=0.05, pad=0.04,aspect=18, orientation='vertical')
    ticklabs = cbar.ax.get_yticklabels()
    cbar.ax.set_yticklabels(ticklabs, fontsize=16)
    cbar.set_label('Precipitación [mm/año]',fontsize=20)
    return fig

titulo = 'climatologia'
lon = np.linspace(0,360,144)
mapa(climatologia.precip,titulo)
plt.savefig(path+'climatologia_obs_pr.png',bbox_inches='tight')
plt.clf
titulo = 'standard deviation ens mean'
mapa((sd[0]+sd[1]+sd[2]+sd[3]+sd[4])/5,titulo)
plt.savefig(path+'desviacion_standard_ensmean_pr.png',bbox_inches='tight')
plt.clf

