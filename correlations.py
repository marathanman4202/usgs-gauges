# Correlations
# Roy Haggerty 5/27/2015
import numpy as np
from scipy import stats
import pandas as pd
import imp
import os
from datetime import datetime 
from datetime import timedelta
snt = imp.load_source('get_snow_data','C:\\code\\usgs-gauges\\snowroutines.py')
snt = imp.load_source('basin_index_doy','C:\\code\\usgs-gauges\\snowroutines.py')
snt = imp.load_source('cummulative_positive_wy_snow_data','C:\\code\\usgs-gauges\\snowroutines.py')
snt = imp.load_source('MaxSWE_wy_snow_data','C:\\code\\usgs-gauges\\snowroutines.py')
snt = imp.load_source('normalize_by_median','C:\\code\\usgs-gauges\\snowroutines.py')
gg = imp.load_source('get_avg_discharge_by_moy','C:\\code\\usgs-gauges\\gageroutines.py')    
gg = imp.load_source('get_avg_discharge_by_month','C:\\code\\usgs-gauges\\gageroutines.py')    
gg = imp.load_source('get_gage_info','C:\\code\\usgs-gauges\\gageroutines.py')
gg = imp.load_source('gage_data_filtered', 'C:\\code\\usgs-gauges\\gageroutines.py')
gg = imp.load_source('reassign_by_yr','C:\\code\usgs-gauges\\gageroutines.py')
pp = imp.load_source('get_precip_data','C:\\code\\usgs-gauges\\preciproutines.py')
pp = imp.load_source('get_value_by_moyrange','C:\\code\\usgs-gauges\\preciproutines.py')
pp = imp.load_source('reassign_by_wyr','C:\\code\\usgs-gauges\\preciproutines.py')
pp = imp.load_source('basin_index','C:\\code\\usgs-gauges\\preciproutines.py')

using_doy = True
snow_data = []
snow_df = snt.get_snow_data(local_path = 'C:\\code\\Willamette Basin snotel data\\')
snow_df = snow_df.loc['19801001':'20140930']
if using_doy:
    snow_df = snt.cummulative_positive_wy_snow_data(snow_df,periods='W')  # FOR CUMMULATIVE SWE.  COMMENT OUT FOR NON-CUMMULATIVE
    snow_basin_index_doy = snt.basin_index_doy(snow_df,doy=1)
    snow_basin_index = gg.reassign_by_yr(snow_basin_index_doy)
    snow_data.append(['Jan 1 SWE',snow_basin_index])
    snow_basin_index_doy = snt.basin_index_doy(snow_df,doy=32)
    snow_basin_index = gg.reassign_by_yr(snow_basin_index_doy)
    snow_data.append(['Feb 1 SWE',snow_basin_index])
    snow_basin_index_doy = snt.basin_index_doy(snow_df,doy=60)
    snow_basin_index = gg.reassign_by_yr(snow_basin_index_doy)
    snow_data.append(['Mar 1 SWE',snow_basin_index])
    snow_basin_index_doy = snt.basin_index_doy(snow_df,doy=91)
    snow_basin_index = gg.reassign_by_yr(snow_basin_index_doy)
    snow_data.append(['Apr 1 SWE',snow_basin_index])
    snow_basin_index_doy = snt.basin_index_doy(snow_df,doy=121)
    snow_basin_index = gg.reassign_by_yr(snow_basin_index_doy)
    snow_data.append(['May 1 SWE',snow_basin_index])
    snow_basin_index_doy = snt.basin_index_doy(snow_df,doy=152)
    snow_basin_index = gg.reassign_by_yr(snow_basin_index_doy)
    snow_data.append(['Jun 1 SWE',snow_basin_index])
    
    snow_df = snt.MaxSWE_wy_snow_data(snow_df)
    snow_basin_index_doy = snt.basin_index_doy(snow_df,doy=270) #273
    snow_basin_index = gg.reassign_by_yr(snow_basin_index_doy)
    snow_data.append(['Max SWE',snow_basin_index])
    
    
# For Max SWE:
#else:
#    snow_df = snt.MaxSWE_wy_snow_data(snow_df)
#    snow_basin_index_doy = snt.basin_index_doy(snow_df,doy=270) #273
#    snow_basin_index = gg.reassign_by_yr(snow_basin_index_doy)
#    snow_data.append(['Max SWE',snow_basin_index])
    
snow_sv = snow_basin_index  #### <--------------------------------------------------

precip_data = []
precip_df = pp.get_precip_data(local_path = 'C:\\code\\Willamette Basin precip data\\')
precip_by_moyrange = pp.get_value_by_moyrange(precip_df,1,5)
precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
precip_basin_index = pp.basin_index(precip_by_wy)
precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
precip_data.append(['Jan-May Precip',precip_basin_index])
precip_by_moyrange = pp.get_value_by_moyrange(precip_df,2,5)
precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
precip_basin_index = pp.basin_index(precip_by_wy)
precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
precip_data.append(['Feb-May Precip',precip_basin_index])
precip_sv = precip_basin_index  #### <--------------------------------------------------
precip_by_moyrange = pp.get_value_by_moyrange(precip_df,2,6)
precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
precip_basin_index = pp.basin_index(precip_by_wy)
precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
precip_data.append(['Feb-Jun Precip',precip_basin_index])
precip_by_moyrange = pp.get_value_by_moyrange(precip_df,3,5)
precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
precip_basin_index = pp.basin_index(precip_by_wy)
precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
precip_data.append(['Mar-May Precip',precip_basin_index])
precip_by_moyrange = pp.get_value_by_moyrange(precip_df,3,6)
precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
precip_basin_index = pp.basin_index(precip_by_wy)
precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
precip_data.append(['Mar-Jun Precip',precip_basin_index])
precip_by_moyrange = pp.get_value_by_moyrange(precip_df,1,4)
precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
precip_basin_index = pp.basin_index(precip_by_wy)
precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
precip_data.append(['Jan-Apr Precip',precip_basin_index])
precip_by_moyrange = pp.get_value_by_moyrange(precip_df,2,4)
precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
precip_basin_index = pp.basin_index(precip_by_wy)
precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
precip_data.append(['Feb-Apr Precip',precip_basin_index])
precip_by_moyrange = pp.get_value_by_moyrange(precip_df,3,4)
precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
precip_basin_index = pp.basin_index(precip_by_wy)
precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
precip_data.append(['Mar-Apr Precip',precip_basin_index])
precip_by_moyrange = pp.get_value_by_moyrange(precip_df,1,3)
precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
precip_basin_index = pp.basin_index(precip_by_wy)
precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
precip_data.append(['Jan-Mar Precip',precip_basin_index])
precip_by_moyrange = pp.get_value_by_moyrange(precip_df,2,3)
precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
precip_basin_index = pp.basin_index(precip_by_wy)
precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
precip_data.append(['Feb-Mar Precip',precip_basin_index])
precip_by_moyrange = pp.get_value_by_moyrange(precip_df,3,3)
precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
precip_basin_index = pp.basin_index(precip_by_wy)
precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
precip_data.append(['Mar Precip',precip_basin_index])

precip_by_moyrange = pp.get_value_by_moyrange(precip_df,10,10)
precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
precip_basin_index = pp.basin_index(precip_by_wy)
precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
precip_data.append(['Oct Precip',precip_basin_index])
precip_by_moyrange = pp.get_value_by_moyrange(precip_df,11,11)
precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
precip_basin_index = pp.basin_index(precip_by_wy)
precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
precip_data.append(['Nov Precip',precip_basin_index])
precip_by_moyrange = pp.get_value_by_moyrange(precip_df,12,12)
precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
precip_basin_index = pp.basin_index(precip_by_wy)
precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
precip_data.append(['Dec Precip',precip_basin_index])
precip_by_moyrange = pp.get_value_by_moyrange(precip_df,11,2)
precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
precip_basin_index = pp.basin_index(precip_by_wy)
precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
precip_data.append(['Winter Precip',precip_basin_index])

precip_by_moyrange = pp.get_value_by_moyrange(precip_df,10,9)
precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
precip_basin_index = pp.basin_index(precip_by_wy)
precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
precip_data.append(['Ann Precip',precip_basin_index])

snow_precip_pair = pd.concat([snow_sv,precip_sv],axis=1)
snow_precip_pair.columns = ['Cum SWE', 'Precip']
from pandas import ExcelWriter
writer = ExcelWriter('Max SWE to spr Pre.xlsx')
snow_precip_pair.to_excel(writer,'Max SWE to spr Pre')
writer.save()

if using_doy:
    len_snow_sv = 6
else:
    len_snow_sv = 1
significance_cutoff = 0.1

#regression_stats_sg = []
#r_significant = []
#for i_snow in range(len_snow_sv):
#    regression_stats_sg_row = []
#    r_significant_row = []
#    for j_precip in range(9):  
#        snow_and_precip_df = pd.concat([snow_data[i_snow][1],precip_data[j_precip][1]],axis=1)
#        snow_and_precip = np.array(snow_and_precip_df.dropna(axis=0, how='any'))
#        # slope, intercept, r_value, p_value, std_err
#        statssv = stats.linregress(snow_and_precip[:,0],snow_and_precip[:,1])
#        regression_stats_sg_row.append(statssv)
#        if statssv[3]<significance_cutoff: 
#            r_significant_row.append(statssv[2])
#        else: 
#            r_significant_row.append(0.)
#    regression_stats_sg.append(regression_stats_sg_row)
#    r_significant.append(np.square(r_significant_row))
#
#np.savetxt('correlation.csv',np.transpose(r_significant),delimiter=',')
#print r_significant

regression_stats_sg = []
r_significant = []
for i_snow in range(len_snow_sv):
    regression_stats_sg_row = []
    r_significant_row = []
    for j_precip in range(len(precip_data)):  
        snow_and_precip_df = pd.concat([snow_data[i_snow][1],precip_data[j_precip][1]],axis=1)
snowdf   = pd.concat([snow_data[i_snow][1] for i_snow in range(len(snow_data))],axis=1)
precipdf = pd.concat([precip_data[j_precip][1] for j_precip in range(len(precip_data))],axis=1)
snow_and_precip_df = pd.concat([snowdf,precipdf],axis=1)
correlation_matrix = snow_and_precip_df.corr()

#np.savetxt('snow and precip.csv',np.array(snow_and_precip_df),delimiter=',')

np.savetxt('correlation.csv',np.array(correlation_matrix),delimiter=',')
#print covariance_matrix



