#Roy Haggerty 6/1/2015

import pandas as pd
import numpy as np
from datetime import datetime 
from datetime import timedelta
import os
import sys
sys.path.insert(0, 'C:\\code\\maplot\\')
import constants as cst
import imp
from scipy import stats
import matplotlib.pyplot as plt

path_gage   = 'C:\\code\usgs-gauges\\gageroutines.py'
path_gage_data = 'C:\\code\\Willamette Basin gauge data\\'
path_snow   = 'C:\\code\usgs-gauges\\snowroutines.py'
path_snow_data = 'C:\\code\\Willamette Basin snotel data\\'
path_precip = 'C:\\code\usgs-gauges\\preciproutines.py'
gg = imp.load_source('get_gage_data', path_gage)
gg = imp.load_source('get_gage_info', path_gage)
gg = imp.load_source('get_gage_info_dict', path_gage)
gg = imp.load_source('get_discharge_by_doyrange', path_gage)
gg = imp.load_source('reassign_by_yr', path_gage)
snt =imp.load_source('get_snow_data', path_snow)
snt =imp.load_source('MaxSWE_wy_snow_data', path_snow)
snt =imp.load_source('basin_index_doy', path_snow)
# Get Q through summer
# Calculate correlations through summer
  # 1. Correlations Q to Precip
  # 2. Correlations Q to Max SWE

# Names:
McK_Clear_Lake = 14158500
W_Portland = 14211720
Calapooia = 14173500
Marys = 14171000
McK_Vida = 14162500
significance_cutoff = 0.1

select_gage = McK_Vida

# gage info list, dict
gage_info = gg.get_gage_info(local_path= path_gage_data, index_col=[0,1,2,3])
gage_dict = gg.get_gage_info_dict(local_path= path_gage_data)

# snow info, data
snow_df = snt.get_snow_data(local_path = path_snow_data)
snow_df = snt.MaxSWE_wy_snow_data(snow_df) #FOR MAX SWE
snow_basin_index_doy = snt.basin_index_doy(snow_df,doy=270)  # doy 270 = end of Sep
snow_basin_index = gg.reassign_by_yr(snow_basin_index_doy)

# get info, data for specific gage
gage_data_df = gg.get_gage_data(select_gage, local_path= path_gage_data).drop(["Gage number","Data-value qualification code"],axis=1) 
doy_plot = []
doy_range = range(152,320)
SWE_frac = []
Q_SWE0 = []
Q_SWE1= []
Delta_Q_SWE1 = []
R2_SWE = []
p_value_SWE = []
mean_discharge = []
for doyloop in doy_range:
    mth_name = 'DOY '+ str(doyloop)
    gage_df_doy = gg.get_discharge_by_doyrange(select_gage, doyloop,doyloop+1, 
         file_name = '', index_col = 2, 
         local_path = path_gage_data)
    mean_discharge.append(gage_df_doy.mean())
    gage_df = gg.reassign_by_yr(gage_df_doy)
    snow_and_gage_df = pd.concat([snow_basin_index,gage_df],axis=1)
    snow_and_gage = np.array(snow_and_gage_df.dropna(axis=0, how='any'))
    # slope, intercept, r_value, p_value, std_err
    regression_stats_sg = stats.linregress(snow_and_gage[:,0],snow_and_gage[:,2]) 
    slope = regression_stats_sg[0]
    p_value = regression_stats_sg[3]
    if p_value <= significance_cutoff: 
        Q_SWE0.append(regression_stats_sg[1])
        Delta_Q_SWE1.append(slope)
        Q_SWE1.append(slope + regression_stats_sg[1])
        R2_SWE.append(regression_stats_sg[2]*regression_stats_sg[2])
        p_value_SWE.append(regression_stats_sg[3])
        SWE_frac.append(Delta_Q_SWE1[-1]/Q_SWE1[-1])
        doy_plot.append(doyloop)
    
# Number of samplepoints

yf = SWE_frac
xf = doy_plot
fig, ax = plt.subplots()
#ax.set_yscale('log')
#ax.set_xscale('log')
ax.scatter(xf, yf)
#ax.plot(doy_range,mean_discharge)