# Roy Haggerty 5/21/2015
import pandas as pd
import os
from datetime import datetime 
from datetime import timedelta
import numpy as np
def get_snow_data(index_col = 0, local_path = ''):
    """
    returns pandas dataframe with all snow data from snotel sites
    
    local_path -- path location for data (str) default = ''
    index_col -- column for dates (int) default = 0
    return snow_df -- pandas df (pandas dataframe)
    
    requires snotel data saved to csv files at location local_path
    """
    assert type(local_path) == str
    i = -1
    snow_df_list = []
    print 'getting snow data, stored locally'
    for filename in os.listdir(local_path):
        if filename[-4:]=='.csv':
            i += 1
            skiprows = -1
            with open(local_path+filename, 'r') as ifile:
                for line in ifile:
                    skiprows += 1
                    if not line[0] == '#':
                        skiprows += 1
                        break
            snow_df_list.append(pd.read_csv(local_path+filename,index_col=index_col,\
                parse_dates=[index_col], skiprows=skiprows,header=None))
            snow_df_list[i] = snow_df_list[i].convert_objects(convert_numeric=True)
            snow_df_list[i].index  = pd.to_datetime(snow_df_list[i].index.date)  #convert to Timestamp, set time to 00
            snow_df_list[i].drop(snow_df_list[i].columns[[1,2,3,4,5]], axis=1, inplace=True) # Note: zero indexed
            snow_df_list[i].columns = [filename[:-4]]
            snow_df_list[i].index.names = ['Date']
    snow_df = pd.concat(snow_df_list,axis=1)
    return snow_df
    
def cummulative_snow_data(df):
    """
    returns pandas dataframe with accummulated SWE
    add only positive differences
    
    return cum_df -- pandas df (pandas dataframe)
    """
    df = df.fillna(method='backfill')
#    cum_df = df
    diff = df.diff()
    diff= diff.clip(lower=0.)
    diff = diff.fillna(0.)
    print diff.ix[:,0]
    assert False
    #df1.ix[:,1]
    lastrow = df.ix[df.index[0],:]
    for index, row in df.iterrows():
        dif = lastrow - row
        lastrow = row
        print dif.clip(.1)
#        for value in row:
 #           print row.index
  #          print value
        assert False
    data = np.array(df)
    m = np.shape(df)[0]
    n = np.shape(df)[1]
    data_tmp = np.empty_like(data)
    for i in range(1,m,1):
        for j in range(n):
            dif = data[i,j] - data[i-1,j]
            if dif > 0.: 
                data_tmp[i,j] = data[i-1,j] + dif
            else:
                data_tmp[i,j] = data[i,j]
    df2 = df
    df2
    print data_tmp
    print data
    assert False
        
def normalize_by_median(df):
    """
    returns pandas dataframe with normalized daily data
    
    df = pandas dataframe with daily time index
    return df_norm -- pandas df (pandas dataframe)
    """
    df_norm = df.div(df.groupby(lambda x: x.dayofyear).transform(pd.Series.median))
    # this line thanks to EdChum on stackoverflow

    return df_norm

def basin_index(df):
    """
    returns pandas dataframe with normalized daily basin index
    From snotel website 
        "The basin index is calculated as the sum of the valid 
        current values divided by the sum of the corresponding medians 
        (for snow water equivalent) or averages (for precipitation) and 
        the resulting fraction multiplied by 100."
    df = pandas dataframe with daily time index
    return df_basin_index -- pandas df with normalized basin index (pandas dataframe)
    """
    df_sum = df.sum(axis=1)
    df1 = df.groupby(lambda x: x.dayofyear).transform(pd.Series.median)
    df2 = df1.sum(axis=1)
    df_basin_index = df_sum.div(df2)

    return df_basin_index
    
def basin_index_doy(df,doy=91,start='19801001',end='20150519'):
    """
    returns pandas dataframe with normalized daily basin median for particular day of year
    doy of year is relative to Jan 1 (doy = 1).  Default = Apr 1.
    From snotel website 
        "The basin index is calculated as the sum of the valid 
        current values divided by the sum of the corresponding medians 
        (for snow water equivalent) or averages (for precipitation) and 
        the resulting fraction multiplied by 100."
    start = first possible day of returned data
    end = last possible day of returned data
    df = pandas dataframe with daily time index
    return df_basin_index_doy -- pandas df (pandas dataframe)
    """
    assert type(start) == str
    assert type(end) == str
    df_basin_index = basin_index(df)
    td = timedelta(days=doy)
    dr = pd.date_range(datetime(int(start[:4]),12,31)+td,
                       datetime(int(end  [:4]),int(end[4:6]),int(end[6:8])),
                        freq=pd.DateOffset(months=12, days=0))
    df_basin_index_doy = df_basin_index[dr]
    return df_basin_index_doy

def tsplot(df):
    """
    simple plotting routine for timeseries.  Just quick & dirty.
    """
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.style.use('ggplot')
    axes=plt.gca()
#    axes.set_xlim(['20150101','20150430'])
    #axes.set_ylim([0,10])
    df.plot()
    plt.show()    
#Test with the following lines
snow_df = get_snow_data(local_path = 'C:\\code\\Willamette Basin snotel data\\')
cumdat = cummulative_snow_data(snow_df)
#snotel_basin_index = basin_index(snow_df)
#snotelplot= snotel_basin_index.loc['20150101':'20150510']
#tsplot(snotelplot)