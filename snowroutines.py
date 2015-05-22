# Roy Haggerty 5/21/2015
import pandas as pd
import os
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
            print filename
    snow_df = pd.concat(snow_df_list,axis=1)
    return snow_df
    
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
    returns pandas dataframe with normalized daily basin median
    From snotel website 
        "The basin index is calculated as the sum of the valid 
        current values divided by the sum of the corresponding medians 
        (for snow water equivalent) or averages (for precipitation) and 
        the resulting fraction multiplied by 100."
    df = pandas dataframe with daily time index
    return df_norm -- pandas df (pandas dataframe)
    """
    df_sum = df.sum(axis=1)
#    df_median = df.groupby(lambda x: x.dayofyear).median()
#    df_median_sum = df_median.sum(axis=1)
#    df_median_byday = df_median_sum.transform(pd.Series.median)
#    print df_median_byday
#    assert False
    df1 = df.groupby(lambda x: x.dayofyear).transform(pd.Series.median)
    df2 = df1.sum(axis=1)
    df_basin_index = df_sum.div(df2)

    return df_basin_index

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
#snow_df = get_snow_data(local_path = 'C:\\code\\Willamette Basin snotel data\\')
#snotel_basin_index = basin_index(snow_df)
#snotelplot= snotel_basin_index.loc['20150101':'20150510']
#tsplot(snotelplot)