#Toma promedios espaciales globales de temperatura del periodo historico del modelo CanESM2 y compara con observaciones

import numpy as np
import pandas as pd
import xarray as xr
import glob
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
#Defino funciones -----------------------------------------------------------

def anomaly(dato):
   climatology = dato.groupby('time.month').mean('time')
   anomalia =  dato.groupby('time.month') - climatology
   return anomalia

# Abrir datos-----------------------------------------------------------------
path = '/home/tabu/Escritorio/Doctorado/ClimDinam/TP1/' 
list = []
list = glob.glob('canESM2/tas*historical*.nc')
tas_mod = []
#Guardo el ensamble en tas_mod 
for file in list:
    tas = xr.open_dataset(path+file)
    tas_mod.append(tas)

tas = []
#Armo una lista de modelos
for run in tas_mod:
    tas.append(anomaly(run).tas.values)

lat = tas_mod[0].lat
lon = tas_mod[0].lon

#Guardo las temperaturas en temp_obs
temp_obs =  xr.open_dataset(path+'tmp_cru_ts3.20_197601-200512_2.5_anu.nc')


#Correlacion------------------------------------------------------------------
# 1. Hacer correlación con distintos lags en un loop que itere sobre todos 
#los puntos de grilla y devuelva el valor de la correlación. 
# 2. Armar un DataArray para cada lag y plotearlo

def df_shifted(df, target=None, lag=0):
    if not lag and not target:
        return df       
    new = {}
    for c in df.columns:
        if c == target:
            new[c] = df[target]
        else:
            new[c] = df[c].shift(periods=lag)
    return  pd.DataFrame(data=new)

import scipy.stats as stats

def mod_corr(model,obs):
    
   Corrij = pd.DataFrame(columns=['correlation','pvalue','lat','lon'])
    
   for i in range(len(lat)):
    for j in range(len(lon)):
        dato = {'model':model[:,i-1,j-1],'obs':obs[:,i-1,j-1]}
        df = pd.DataFrame(data=dato)
        df_lag = df_shifted(df, 'obs', lag=0)
        corr_index = df_lag.corr().iloc[0,1] #correlation btw PC1 and SST
        r, p = stats.pearsonr(df_lag.dropna()['model'], df_lag.dropna()['obs'])
        corr_index = pd.DataFrame({'correlation':r,'pvalue':p,'lat':[lat[i-1].values.tolist()],'lon':[lon[j-1].values.tolist()]})
        Corrij = pd.concat([Corrij,corr_index],axis=0)
   
   CORR_MAP = {'coef':Corrij.iloc[:,0],'pval':Corrij.iloc[:,1],'lat':Corrij.iloc[:,2],'lon':Corrij.iloc[:,3]}
   CORR_MAPij = pd.DataFrame(CORR_MAP)
   return CORR_MAPij

# Mapa------------------------------------------------------------------------

#Coordenadas-----------------------------------------------------------------
lon = sst.lon
lat = sst.lat

def gen_nc2(df):
    #colnames = ['coef','pval','lat','lon']
    xrray = df.set_index(['lat','lon']).to_xarray()
    xrray['lat'].attrs={'units':'degrees', 'long_name':'Latitude'}
    xrray['lon'].attrs={'units':'degrees', 'long_name':'Longitude'}
    xrray['coef'].attrs={'units':'coef_corr', 'long_name':'coef_corr'}
    xrray['pval'].attrs={'units':'pvalue', 'long_name':'pvalue'}
    return xrray

#Plot --------------------------------------------------------------------------

import cartopy.crs as ccrs
import cartopy.feature
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['hatch.linewidth'] = 0.5  # previous pdf hatch linewidth


def mapa_lags_pval(corr_lag,uno,dos):
    indice = corr_lag.coef
    pval = corr_lag.pval
    lat = corr_lag.lat
    lon = corr_lag.lon
    
    #SoutherHemisphere Stereographic
    fig = plt.figure(figsize=(20, 14),dpi=300,constrained_layout=True)
    fig.suptitle('Correlation model'+str(uno)+' y model'+str(dos), y=0.9, x=0.5,fontsize=25)
    fig_size = plt.rcParams["figure.figsize"]
    data_crs = ccrs.PlateCarree(central_longitude=0)
    projection = ccrs.PlateCarree()
    ax1 = plt.subplot(projection=projection)
    ax1.set_extent([-180,180, -90, 90], crs=data_crs)
    clevels = np.arange(-0.9,0.9,0.1)
    im1=ax1.contourf(lon, lat, indice,clevels,transform=data_crs,cmap='RdBu_r',extend='both')
    levels = [pval.min(),0.01,pval.max()]
    ax1.contourf(lon, lat, pval,levels, transform=data_crs,levels=levels, hatches=["...", ""], alpha=0)
    #ax1.add_feature(cartopy.feature.LAND, zorder=100, edgecolor='k')
    ax1.add_feature(cartopy.feature.COASTLINE)
    #ax1.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=.5)
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
    cbar.set_label('corr index',fontsize=20)   
    return fig

tas_ref = tas[0]
uno,dos = '1','3'
#Lags
corr_map = mod_corr(tas[2],tas_ref)
corr_map = gen_nc2(corr_map)
figure = mapa_lags_pval(corr_map,uno,dos)
corr_map.to_netcsf(path+'corr_mod1_mod3.nc', float_format='%g')
plt.savefig(path+'corr_mod1_mod3.png',bbox_inches='tight')
plt.clf

