#Roy Haggerty 6/1/2015
# Code to plot fraction of discharge correlated to spring precip and Max SWE

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
import matplotlib.cm as cm

def royplot(xf,yf,xf2,yf2,xf_precip,yf_precip,gage_name,select_gage,R2_SWE,R2_PRE):
    fig = plt.figure()
    window = fig.add_subplot(111)
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
    window.set_ylabel("$Fraction\, discharge\, correlated\, to\, Max\, SWE\, or\, F-M\, Precip,$ [-]", fontsize=14)
    window.set_xlabel("$Julian\, Day$", fontsize=14)
    window.set_xlim(150,310)
    par.set_ylabel("$Avg\, Discharge\,$[m$^{\t{3}}$/s]", fontsize=14)
    #plt.show()
    graph_name_png = 'PRE-SWE '+gage_name + ' Gage # '+str(select_gage)+'.png'
    plt.savefig(path_pngs+graph_name_png, format="png", dpi=300)
    plt.close(1)
    #ax.plot(doy_range,mean_discharge)


path_gage   = 'C:\\code\usgs-gauges\\gageroutines.py'
path_gage_data = 'C:\\code\\Willamette Basin gauge data\\'
path_snow   = 'C:\\code\usgs-gauges\\snowroutines.py'
path_snow_data = 'C:\\code\\Willamette Basin snotel data\\'
path_precip = 'C:\\code\usgs-gauges\\preciproutines.py'
path_pngs = 'C:\\code\\maplot pngs\\fraction discharge through time\\'
gg = imp.load_source('get_gage_data', path_gage)
gg = imp.load_source('get_gage_info', path_gage)
gg = imp.load_source('get_gage_info_dict', path_gage)
gg = imp.load_source('get_discharge_by_doyrange', path_gage)
gg = imp.load_source('reassign_by_yr', path_gage)
snt =imp.load_source('get_snow_data', path_snow)
snt =imp.load_source('MaxSWE_wy_snow_data', path_snow)
snt =imp.load_source('basin_index_doy', path_snow)
pp = imp.load_source('get_precip_data','C:\\code\\usgs-gauges\\preciproutines.py')
pp = imp.load_source('get_precip_by_moyrange','C:\\code\\usgs-gauges\\preciproutines.py')
pp = imp.load_source('reassign_by_wyr','C:\\code\\usgs-gauges\\preciproutines.py')
pp = imp.load_source('basin_index','C:\\code\\usgs-gauges\\preciproutines.py')
# Get Q through summer
# Calculate correlations through summer
  # 1. Correlations Q to Precip
  # 2. Correlations Q to Max SWE

# Names:
gage_tuple = {
"McK_Belknap"       : 14158850,
"McK_Clear_Lake"    : 14158500,
"McK_Vida"          : 14162500,
"Will_Portland"     : 14211720,
"Will_Salem"        : 14191000,
"Clack_Three_Lynx"  : 14209500,
"Marys"             : 14171000}
Calapooia = 14173500

significance_cutoff = 0.1

test = False
select_gage = gage_tuple["Will_Portland"]

# gage info list, dict
gage_info = gg.get_gage_info(local_path= path_gage_data, index_col=[0,1,2,3])
gage_dict = gg.get_gage_info_dict(local_path= path_gage_data)
gage_name = gage_dict[select_gage][0]

if not test:
    # snow info, data
    snow_df = snt.get_snow_data(local_path = path_snow_data)
    snow_df = snt.MaxSWE_wy_snow_data(snow_df) #FOR MAX SWE
    snow_basin_index_doy = snt.basin_index_doy(snow_df,doy=270)  # doy 270 = end of Sep
    snow_basin_index = gg.reassign_by_yr(snow_basin_index_doy)

    precip_df = pp.get_precip_data(local_path = 'C:\\code\\Willamette Basin precip data\\')
    precip_by_moyrange = pp.get_value_by_moyrange(precip_df,2,5)
    precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
    precip_basin_index = pp.basin_index(precip_by_wy)
    precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
    
    for select_gage in gage_dict:
#    for idummy in range(0,1):
        gage_name = gage_dict[select_gage][0]
        print 'working on '+ gage_name
        # get info, data for specific gage
        gage_data_df = gg.get_gage_data(select_gage, local_path= path_gage_data).drop(["Gage number","Data-value qualification code"],axis=1) 
        doy_plot = []
        doy_plot_precip = []
        day_start = cst.day_of_year_jun1 
        day_end =   cst.day_of_year_oct31
        doy_range = range(day_start,day_end)
        SWE_frac = []
        Q_SWE0 = []
        Q_SWE1= []
        Delta_Q_SWE1 = []
        R2_SWE = []
        p_value_SWE = []
        PRE_frac = []
        Q_PRE0 = []
        Q_PRE1= []
        Delta_Q_PRE1 = []
        R2_PRE = []
        p_value_PRE = []
        mean_discharge = []
        for doyloop in doy_range:
            mth_name = 'DOY '+ str(doyloop)
            gage_df_doy = gg.get_discharge_by_doyrange(select_gage, doyloop,doyloop+1, 
                 file_name = '', index_col = 2, 
                 local_path = path_gage_data)
            gage_df = gg.reassign_by_yr(gage_df_doy)
            snow_and_gage_df = pd.concat([snow_basin_index,gage_df],axis=1)
            snow_and_gage = np.array(snow_and_gage_df.dropna(axis=0, how='any'))
            precip_and_gage_df = pd.concat([precip_basin_index,gage_df],axis=1)
            precip_and_gage = np.array(precip_and_gage_df.dropna(axis=0, how='any'))
            # slope, intercept, r_value, p_value, std_err
            regression_stats_sg = stats.linregress(snow_and_gage[:,0],snow_and_gage[:,2]) 
            slope = regression_stats_sg[0]
            p_value = regression_stats_sg[3]
            regression_stats_sg_precip = stats.linregress(precip_and_gage[:,0],precip_and_gage[:,2]) 
            slope_precip = regression_stats_sg_precip[0]
            p_value_precip = regression_stats_sg_precip[3]
            mean_discharge.append(gage_df_doy["Discharge (cfs)"].mean())
            if p_value <= significance_cutoff: 
                Q_SWE0.append(regression_stats_sg[1])
                Delta_Q_SWE1.append(slope)
                Q_SWE1.append(slope + regression_stats_sg[1])
                R2_SWE.append(regression_stats_sg[2]*regression_stats_sg[2])
                p_value_SWE.append(regression_stats_sg[3])
                SWE_frac.append(Delta_Q_SWE1[-1]/Q_SWE1[-1])
                doy_plot.append(doyloop)
            if p_value_precip <= significance_cutoff: 
                Q_PRE0.append(regression_stats_sg_precip[1])
                Delta_Q_PRE1.append(slope_precip)
                Q_PRE1.append(slope + regression_stats_sg_precip[1])
                R2_PRE.append(regression_stats_sg_precip[2]*regression_stats_sg_precip[2])
                p_value_PRE.append(regression_stats_sg_precip[3])
                PRE_frac.append(Delta_Q_PRE1[-1]/Q_PRE1[-1])
                doy_plot_precip.append(doyloop)
    
        # Number of samplepoints
        if len(SWE_frac) > 0 or len(PRE_frac) > 0:
            print '# stat sig = ',str(len(SWE_frac)), str(len(PRE_frac))
            yf = SWE_frac
            xf = doy_plot
            yf_precip = PRE_frac
            xf_precip = doy_plot_precip
            yf2 = np.array(mean_discharge)*cst.cfs_to_m3
            xf2 = doy_range
            royplot(xf,yf,xf2,yf2,xf_precip,yf_precip,gage_name,select_gage,R2_SWE,R2_PRE)
else:
    data_tmp = np.array(np.genfromtxt('testdata.csv', delimiter=',',skip_header=1)) # Read csv file
    xf = data_tmp[:,0]
    xf = xf[np.logical_not(np.isnan(xf))]
    yf = data_tmp[:,1]
    yf = yf[np.logical_not(np.isnan(yf))]
    R2_SWE = data_tmp[:,2]
    R2_SWE = R2_SWE[np.logical_not(np.isnan(R2_SWE))]
    xf2 = data_tmp[:,3]
    yf2 = data_tmp[:,4]*cst.cfs_to_m3
#    xf = range(150,300)
#    yf = np.random.random(len(xf))
#    xf2 = xf
#    yf2 = np.array(xf)/2.
    royplot(xf,yf,xf2,yf2,gage_name,select_gage,R2_SWE)
