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
gl = imp.load_source('get_gage_data','C:\\code\usgs-gauges\\gageroutines.py')
gl = imp.load_source('get_gage_info','C:\\code\usgs-gauges\\gageroutines.py')
gl = imp.load_source('get_gage_info_dict','C:\\code\usgs-gauges\\gageroutines.py')

# Get gage number, name
# Get Q through summer
# Calculate correlations through summer
  # 1. Correlations Q to Precip
  # 2. Correlations Q to Max SWE

# Names:
Clear_Lake = 14158500
Portland = 14211720
Calapooia = 14173500
Marys = 14171000

gage_data = gl.get_gage_data(Clear_Lake, local_path= 'C:\\code\\Willamette Basin gauge data\\').drop(["Gage number","Data-value qualification code"],axis=1)
gage_info = gl.get_gage_info(local_path= 'C:\\code\\Willamette Basin gauge data\\')
gage_dict = gl.get_gage_info_dict(local_path= 'C:\\code\\Willamette Basin gauge data\\')
print gage_dict[Clear_Lake][0]
firstloop = True
for doyloop in range(155,305,7):
    if firstloop:
        snow_df = snt.get_snow_data(local_path = 'C:\\code\\Willamette Basin snotel data\\')
        snow_df = snt.MaxSWE_wy_snow_data(snow_df) #FOR MAX SWE
        snow_basin_index_doy = snt.basin_index_doy(snow_df,doy=270)  # doy 270 = end of Sep
        snow_basin_index = gg.reassign_by_yr(snow_basin_index_doy)
        gage_list = gg.get_gage_info(local_path= 'C:\\code\\Willamette Basin gauge data\\',index_col=[0,1,2,3])
        firstloop = False
