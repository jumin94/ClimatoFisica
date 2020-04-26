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
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['hatch.linewidth'] = 0.5  # previous pdf hatch linewidth

#Defino funciones 
def anomaly(dato,obs):
   climatologia = obs.mean(dim='time')
   anomalia = dato.mean(dim='time') - climatologia
   return climatologia, anomalia

# Abrir datos-----------------------------------------------------------------
path = '/home/tabu/Escritorio/Doctorado/ClimDinam/TP1/'
path2 = '/media/tabu/JULIAexterno/climatologia_dinamica/CanESM5'
#Guardo las temperaturas en temp_obs
precip_obs =  xr.open_dataset(path+'DATOS/precip.mon.total.v7_197601-200512_2.5_anu.nc')
climatologia = precip_obs.mean(dim='time')
time = precip_obs.time
timeattrs = precip_obs.time.attrs
time = xr.Dataset({'time':('time',time,timeattrs)})

list = []
list = glob.glob('canESM2/pr*historical*anu.nc')
tas_mod = []
#Guardo el ensamble en tas_mod
for file in list:
    tas = xr.open_dataset(path+file)
    tas['time'] = time['time']
    tas_mod.append(tas)

tas_ens = (tas_mod[0].pr + tas_mod[1].pr + tas_mod[2].pr + tas_mod[3].pr + tas_mod[4].pr )/5

#Bias porcentual
bias_CanESM2 = (tas_ens/precip_obs.precip)*100 - 100
bias_CanESM2 = bias_CanESM2.mean(dim='time')

#Abro CanESM5
CanESM5_ens = xr.open_dataset(path2+'/pr_Amon_CanESM5_historical_ensmean_2.5_anu.nc')
CanESM5_ens['time'] = time['time']

#Bias porcentual
bias_CanESM5 = (CanESM5_ens.pr/precip_obs.precip)*100 - 100
bias_CanESM5 = bias_CanESM5.mean(dim='time')

lat = tas_mod[0].lat
lon = tas_mod[0].lon

def mapa(dato1,dato2,dato3,titulo):
    #America del sur -------Observaciones-----------------------------------------
    fig = plt.figure(figsize=(10, 18),dpi=300,constrained_layout=True)
    fig.suptitle(str(titulo), y=0.92, x=0.5,fontsize=20)
    fig_size = plt.rcParams["figure.figsize"]
    data_crs = ccrs.PlateCarree(central_longitude=0)
    projection = ccrs.PlateCarree()
    ax1 = plt.subplot(3,1,1,projection=projection)
    ax1.set_extent([275,335, 10, -60], crs=data_crs)
    clevels = np.arange(np.min(dato1),np.max(dato1),(np.max(dato1)-np.min(dato1))/11)
    im1=ax1.contourf(lon, lat, dato1.values,clevels,transform=data_crs,cmap='Blues',extend='both')
    ax1.add_feature(cartopy.feature.COASTLINE)
    ax1.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=.5)
    ax1.gridlines(crs=data_crs, linewidth=0.3, linestyle='-')
    ax1.set_title('Observaciones')
    #Saco las coordenadas de la figura hasta ahora
    plt0_ax = plt.gca()
    left, bottom1, width, height = plt0_ax.get_position().bounds
    first_plot_left = plt0_ax.get_position().bounds[0]
    #Utilizo las coordenadas para definir la posición de la colorbar 1
    colorbar_axes = fig.add_axes([first_plot_left + 0.4, bottom1+0.01, 0.02, 1*height])
    fig_size[0] = width*4 + 10
    fig_size[1] = height*2 + 3
    plt.rcParams["figure.figsize"] = fig_size
    cbar = plt.colorbar(im1, colorbar_axes, fraction=0.05, pad=0.04,aspect=18, orientation='vertical')
    ticklabs = cbar.ax.get_yticklabels()
    cbar.ax.set_yticklabels(ticklabs, fontsize=16)
    cbar.set_label('Precipitación [mm/año]',fontsize=20)
    #America del sur---------------Bias CanESM2--------------------------------------
    ax2 = plt.subplot(3,1,2,projection=projection)
    ax2.set_extent([275,335, 10, -60], crs=data_crs)
    clevels = np.arange(-300,300,50)
    im2=ax2.contourf(lon, lat, dato2.values,clevels,transform=data_crs,cmap='RdBu',extend='both')
    ax2.add_feature(cartopy.feature.COASTLINE)
    ax2.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=.5)
    ax2.gridlines(crs=data_crs, linewidth=0.3, linestyle='-')
    ax2.set_title('CanESM2')
    #America del sur ----------------Bias CanESM5
    ax3 = plt.subplot(3,1,3,projection=projection)
    ax3.set_extent([275,335, 10, -60], crs=data_crs)
    im3=ax3.contourf(lon, lat, dato3.values,clevels,transform=data_crs,cmap='RdBu',extend='both')
    ax3.add_feature(cartopy.feature.COASTLINE)
    ax3.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=.5)
    ax3.gridlines(crs=data_crs, linewidth=0.3, linestyle='-')
    ax3.set_title('CanESM5')
    #Saco las coordenadas de la figura hasta ahora
    plt0_ax = plt.gca()
    left, bottom1, width, height = plt0_ax.get_position().bounds
    first_plot_left = plt0_ax.get_position().bounds[0]
    #Utilizo las coordenadas para definir la posición de la colorbar 2 
    colorbar_axes = fig.add_axes([first_plot_left + 0.4, bottom1+0.0, 0.02, 2*height])
    fig_size[0] = width*4 + 10
    fig_size[1] = height*2 + 3
    plt.rcParams["figure.figsize"] = fig_size
    cbar = plt.colorbar(im2, colorbar_axes, fraction=0.05, pad=0.04,aspect=18, orientation='vertical')
    ticklabs = cbar.ax.get_yticklabels()
    cbar.ax.set_yticklabels(ticklabs, fontsize=16)
    cbar.set_label('Bias porcentual',fontsize=20)  
    return fig

titulo = 'Bias en precipitacion'
mapa(climatologia.precip,bias_CanESM2,bias_CanESM5,titulo)
plt.savefig(path+'Bias_precipitacion.png',bbox_inches='tight')
plt.clf


