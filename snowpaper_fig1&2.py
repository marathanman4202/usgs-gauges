# Fig 1 & 2
# Roy Haggerty 6/3/2015
import numpy as np
from scipy import stats
import pandas as pd
import imp
import os
from datetime import datetime 
from datetime import timedelta
import sys
sys.path.insert(0, 'C:\\code\\maplot\\')
import constants as cst
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec

path_gage   = 'C:\\code\usgs-gauges\\gageroutines.py'
path_gage_data = 'C:\\code\\Willamette Basin gauge data\\'
path_snow   = 'C:\\code\usgs-gauges\\snowroutines.py'
path_snow_data = 'C:\\code\\Willamette Basin snotel data\\'
path_precip = 'C:\\code\usgs-gauges\\preciproutines.py'
path_pngs = 'C:\\Users\\haggertr\\Desktop\\Documents\\work - OSU\\research\\WW2100\\Research\\snow\paper figs\\'

snt = imp.load_source('get_snow_data','C:\\code\\usgs-gauges\\snowroutines.py')
snt = imp.load_source('basin_index_doy','C:\\code\\usgs-gauges\\snowroutines.py')
snt = imp.load_source('basin_index','C:\\code\\usgs-gauges\\snowroutines.py')
snt = imp.load_source('cummulative_positive_wy_snow_data','C:\\code\\usgs-gauges\\snowroutines.py')
snt = imp.load_source('MaxSWE_wy_snow_data','C:\\code\\usgs-gauges\\snowroutines.py')
snt = imp.load_source('normalize_by_median','C:\\code\\usgs-gauges\\snowroutines.py')
snt = imp.load_source('meanMaxSWE_snow_data','C:\\code\\usgs-gauges\\snowroutines.py')
snt = imp.load_source('getWaterYear','C:\\code\\usgs-gauges\\snowroutines.py')
gg = imp.load_source('get_avg_discharge_by_moy','C:\\code\\usgs-gauges\\gageroutines.py')    
gg = imp.load_source('get_avg_discharge_by_month','C:\\code\\usgs-gauges\\gageroutines.py')    
gg = imp.load_source('get_gage_info','C:\\code\\usgs-gauges\\gageroutines.py')
gg = imp.load_source('gage_data_filtered', 'C:\\code\\usgs-gauges\\gageroutines.py')
gg = imp.load_source('reassign_by_yr','C:\\code\usgs-gauges\\gageroutines.py')
pp = imp.load_source('get_precip_data','C:\\code\\usgs-gauges\\preciproutines.py')
pp = imp.load_source('get_value_by_moyrange','C:\\code\\usgs-gauges\\preciproutines.py')
pp = imp.load_source('reassign_by_wyr','C:\\code\\usgs-gauges\\preciproutines.py')
pp = imp.load_source('basin_index','C:\\code\\usgs-gauges\\preciproutines.py')


def fig12plot(xf,yf,xf2,yf2,xf_precip,yf_precip,gage_name,select_gage,R2_SWE,R2_PRE):
    snow_df = snt.get_snow_data(local_path = path_snow_data)
    meanmax = snt.meanMaxSWE_snow_data(snow_df)
    snow_df = snow_df/meanmax
    basin_index = pd.DataFrame(snt.basin_index(snow_df))
    basin_index.insert(0, 'Water Year', snt.getWaterYear(basin_index.index))
    basin_index_wy = basin_index.groupby('Water Year')
    print basin_index_wy
    assert False
    snow_df = snt.MaxSWE_wy_snow_data(snow_df) #FOR MAX SWE
    snow_basin_index_doy = snt.basin_index_doy(snow_df,doy=270)  # doy 270 = end of Sep
    snow_basin_index = gg.reassign_by_yr(snow_basin_index_doy)    
    
    fig = plt.figure(1, figsize=(6.4,8.))
    width_ratios=[6.4,6.4]
    height_ratios = [4.,4.]
    wspace = 0.     # horizontal space btwn figs
    hspace = 0.12     # vertical space btwn figs
    
    ###### Figure canvas 
    gs1 = gridspec.GridSpec(2,1, width_ratios=width_ratios,
                            height_ratios=height_ratios,
                            wspace = wspace)
        
    gs1.update(left=0.1, right = 1.5, wspace=wspace, hspace = hspace)

    window = fig.add_subplot(gs1[0,0])
    par = window.twinx()
    colors = np.array(R2_SWE)
    colors_precip = np.array(R2_PRE)
    window.set_ylim(ymax = 1.)
    window.set_ylim(ymin = 0.)
    window.scatter(xf,yf,marker='H',s=60,c=colors, cmap=cm.Blues)
    window.scatter(xf_precip,yf_precip,marker='v',s=60,c=colors_precip, cmap=cm.Reds)
    par.plot(xf2, yf2, 'k')
    #window.legend([line1, line2], ['$Correlation$', '$Discharge$'],loc='best',frameon=False)
    window.set_title(gage_name + ' Gage # '+str(select_gage)+'\n')
    window.set_ylabel("$Axis\, 1\,$ [-]", fontsize=14)
    window.set_xlim(150,310)
#    par.set_ylabel("$Avg\, Discharge\,$[m$^{\t{3}}$/s]", fontsize=14)

    window2 = fig.add_subplot(gs1[1,0])
    par2 = window2.twinx()
    colors = np.array(R2_SWE)
    colors_precip = np.array(R2_PRE)
    window2.set_ylim(ymax = 1.)
    window2.set_ylim(ymin = 0.)
    window2.scatter(xf,yf,marker='H',s=60,c=colors, cmap=cm.Blues)
    window2.scatter(xf_precip,yf_precip,marker='v',s=60,c=colors_precip, cmap=cm.Reds)
    par2.plot(xf2, yf2, 'k')
    #window.legend([line1, line2], ['$Correlation$', '$Discharge$'],loc='best',frameon=False)
    window2.set_ylabel("$Axis\, 2\,$ [-]", fontsize=14)
    window2.set_xlabel("$Julian\, Day$", fontsize=14)
    window2.set_xlim(150,310)
    par2.set_ylabel("$Avg\, Discharge\,$[m$^{\t{3}}$/s]", fontsize=14)

    plt.show()
#    graph_name_png = 'PRE-SWE '+gage_name + ' Gage # '+str(select_gage)+'.png'
#    plt.savefig(path_pngs+graph_name_png, format="png", dpi=300)
#    plt.close(1)
    #ax.plot(doy_range,mean_discharge)

data_tmp = np.array(np.genfromtxt('testdata.csv', delimiter=',',skip_header=1)) # Read csv file
xf = data_tmp[:,0]
xf = xf[np.logical_not(np.isnan(xf))]
yf = data_tmp[:,1]
yf = yf[np.logical_not(np.isnan(yf))]
xf_precip = xf
yf_precip = yf
R2_SWE = data_tmp[:,2]
R2_SWE = R2_SWE[np.logical_not(np.isnan(R2_SWE))]
xf2 = data_tmp[:,3]
yf2 = data_tmp[:,4]*cst.cfs_to_m3

fig12plot(xf,yf,xf2,yf2,xf_precip,yf_precip,'Title',01234,R2_SWE,R2_SWE)