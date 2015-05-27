# Roy Haggerty 5/27/2015
import pandas as pd
import os
from datetime import datetime 
from datetime import timedelta
def get_precip_data(index_col = 0, local_path = ''):
    """
    returns pandas dataframe with all snow data from snotel sites
    
    local_path -- path location for data (str) default = ''
    index_col -- column for dates (int) default = 0
    return snow_df -- pandas df (pandas dataframe)
    
    requires snotel data saved to csv files at location local_path
    """
    assert type(local_path) == str
    i = -1
    df_list = []
    print 'getting precip data, stored locally'
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
            df_list.append(pd.read_csv(local_path+filename,index_col=index_col,\
                parse_dates=[index_col], skiprows=skiprows,header=None))
            df_list[i] = df_list[i].convert_objects(convert_numeric=True)
            df_list[i].index  = pd.to_datetime(df_list[i].index.date)  #convert to Timestamp, set time to 00
#            df_list[i].drop(df_list[i].columns[[1,2,3,4,5]], axis=1, inplace=True) # Note: zero indexed
            df_list[i].columns = [filename[:-4]]
            df_list[i].index.names = ['Date']
    df = pd.concat(df_list,axis=1)
    return df
    
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
    
def get_precip_by_moyrange(df, moystart,moyend):
    """
    returns pandas dataframe with precip in selected moy range for all years
    
    return precip in time period for each of all years
    """
    df2 = df[(df.index.month >= moystart)]
    df_filtered = df2[(df2.index.month <= moyend)]
    return df_filtered
    
def basin_index_doy(df,doy=91,start='18950101',end='20160601'):
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
    
def reassign_by_wyr(df):
    """
    returns pandas dataframe with single value from each water year (Oct 1 - Sep 30) and time reassigned to year
    df = pandas dataframe 
    return value_for_wy -- pandas df (pandas dataframe)
    """
    value_for_wy = df.resample('BA-SEP',how='mean')
    return value_for_wy
    
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
precip_df = get_precip_data(local_path = 'C:\\code\\Willamette Basin precip data\\')
#print precip_df.head()
precip_by_moyrange = get_precip_by_moyrange(precip_df,1,5)
#print precip_by_moyrange
precip_by_wy = reassign_by_wyr(precip_by_moyrange)
#print precip_by_wy
precip_basin_index = basin_index(precip_by_wy)
print precip_basin_index
precipplot= precip_basin_index['18950101':'20150510']
tsplot(precipplot)