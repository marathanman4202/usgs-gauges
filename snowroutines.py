# Roy Haggerty 5/21/2015
import pandas as pd
import os
from datetime import datetime 
from datetime import timedelta
import numpy as np
import imp
import sys
sys.path.insert(0, 'C:\\code\\maplot\\')
import constants as cst
from scipy.ndimage import gaussian_filter1d    
#gnrl = imp.load_source('plot_fourier','C:\\code\usgs-gauges\\gageroutines.py')
gnrl = imp.load_source('reassign_by_wyr','C:\\code\usgs-gauges\\preciproutines.py')
def get_snow_data(index_col = 0, local_path = '',retrieve='SWE'):
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
            if retrieve == 'SWE':
                snow_df_list[i].drop(snow_df_list[i].columns[[1,2,3,4,5]], axis=1, inplace=True) # Note: zero indexed
                snow_df_list[i].columns = [filename[:-4]]
            elif retrieve == 'Precip':
                snow_df_list[i].drop(snow_df_list[i].columns[[0,1,2,3,4]], axis=1, inplace=True) # Note: zero indexed
                snow_df_list[i].columns = [filename[:-4]]
            elif retrieve == 'SWEflux':
                # returns column of Precip plus addition (melt) from SWE or minus subtraction (storage) to SWE
                snow_tmp_df = snow_df_list[i][6] \
                            - snow_df_list[i][1].diff()
                snow_df_list[i][1] = snow_tmp_df
                snow_df_list[i].drop(snow_df_list[i].columns[[1,2,3,4,5]], axis=1, inplace=True) # Note: zero indexed
                snow_df_list[i].columns = [filename[:-4]]                
            snow_df_list[i].index.names = ['Date']
    snow_df = pd.concat(snow_df_list,axis=1)

    return snow_df
def getWaterYear(dt):
    """ 
    returns year in terms of water year.  Assumes water year ends Sep 30 (month 9)
    Thanks to ZJS at
    http://stackoverflow.com/questions/26341272/using-groupby-on-pandas-dataframe-to-group-by-financial-year
    """
    year = []
    for date in dt:
        if date.month>9: 
            year.append(date.year+1)
        else:
            year.append(date.year)
    return year    
    
def cummulative_positive_wy_snow_data(df,periods='D'):
    """
    returns pandas dataframe with accummulated SWE for water year
    add only *positive* differences
    
    return cum_df -- pandas df (pandas dataframe)
    """
    ncols = df.shape[1]
    if periods == 'W':
        weekly_df = df.resample('W',how='last')  # weekly values
        diff_weekly = weekly_df.diff()  # dif of weekly values
        diff_weekly = diff_weekly.clip(lower=0.)
        df[:] = np.NaN
        diff = pd.merge(df,diff_weekly,left_index=True,right_index=True,how='left',copy=False)  #replace df with weekly_df
        diff = diff.fillna(method='ffill') # fill between weekly values with value from last date
        cols = diff.columns
        diff = diff.drop([cols[i] for i in range(0,ncols)],axis=1)
    else:
        diff = df.diff()  
        diff= diff.clip(lower=0.)
    diff.insert(0, 'Water Year', getWaterYear(diff.index))
    diff_grouped = diff.groupby(diff['Water Year']).cumsum()
#    value_for_year = diff_grouped.resample('BA-SEP',how='last')  #Assumes water year ends Sep 30
    return diff_grouped
        
def MaxSWE_wy_snow_data(df,ffilter=5):
    """
    returns pandas dataframe with max 15-day (or ffilter-day) running SWE for whole water year Note 5-day ffilter is approx equiv to 15-day running average
    
    return max_df -- pandas df (pandas dataframe)
    """
    filtered_df = df.copy()  #create copy of array to be filtered (needs to be copy, otherwise aliasing issues)
    filtered_df[:] = gaussian_filter1d(df,ffilter,axis=0) #new dataframe w Gaussian-filtered data
    filtered_df.insert(0, 'Water Year', getWaterYear(filtered_df.index))
    filtered_grouped = filtered_df.groupby(filtered_df['Water Year']).cummax()

    return filtered_grouped
    
def meanMaxSWE_snow_data(df,ffilter=5):
    """
    returns mean SWE Max from max 15-day (or ffilter-day) running SWE for whole water year
    
    return meanmax -- pandas df (pandas dataframe)
    """
    df = MaxSWE_wy_snow_data(df,ffilter=ffilter)
    meanmax = df.mean(axis=0)

    return meanmax
        
def normalize_by_median(df):
    """
    returns pandas dataframe with normalized daily data
    
    df = pandas dataframe with daily time index
    return df_norm -- pandas df (pandas dataframe)
    """
    df_norm = df.div(df.groupby(lambda x: x.dayofyear).transform(pd.Series.median))
    # this line thanks to EdChum on stackoverflow
    print df_norm.loc['19920515':'19920615']
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
    
def plot_fourier(df,name,filterf=None):
    """
    plot fourier transform of pandas dataframe
    Thanks to Paul H at http://stackoverflow.com/questions/25735153/plotting-a-fast-fourier-transform-in-python 
    """
    import matplotlib.pyplot as plt
    import scipy.fftpack
    # Nans must be removed or routine generates an error
    df = df.fillna(0.)
    df = df/df.mean()
    y = np.array(df[name])
    N = len(y)
    T = 1./365.
    yf = scipy.fftpack.fft(y)
    yf = 2.0/N * np.abs(yf[0:N/2])
    if filterf != None:
        yf = gaussian_filter1d(yf,filterf)
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
    fig, ax = plt.subplots()
    ax.set_yscale('log')
    ax.set_xscale('log')
#    ax.set_xlim(xmin=0.1)
#    ax.set_xlim(xmax=1)
    ax.set_ylim(ymax=100.)
    ax.set_ylim(ymin = 1.e-5)
    ax.set_title(name)
    ax.plot(xf, yf)
    return xf,yf

def tsplot(df,name):
    """
    simple plotting routine for timeseries.  Just quick & dirty.
    """
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.style.use('ggplot')
    axes=plt.gca()
    axes.set_title(name)
#    axes.set_xlim(['19801001','20150430'])
    #axes.set_ylim([0,10])
    df[name].plot()
    plt.show()    
#Test with the following lines
#Names: 
#name = "Railroad Overpass (710)"
#name = "Santiam Jct. (733)"
###name = "Mckenzie (619)"
#snow_df = get_snow_data(local_path = 'C:\\code\\Willamette Basin snotel data\\')
#snow_df = MaxSWE_wy_snow_data(snow_df)
#snow_df = gnrl.reassign_by_wyr(snow_df)
#print snow_df.tail(16)
#assert False
#tsplot(snow_df['20061001':'20100930'],name)
#assert False
##snow_df = snow_df.loc['19801001':'20140930']
##xf,yf1 = plot_fourier(snow_df['19811001':],name,filterf=10.)
#snow_df = get_snow_data(local_path = 'C:\\code\\Willamette Basin snotel data\\',retrieve="Precip")
#xf,yf2 = plot_fourier(snow_df['19811001':],name,filterf=10.)
##rtd_df = pd.DataFrame(yf1/yf2)
##rtd_df.columns = [name]
##plot_fourier(rtd_df,name)
#
#import matplotlib.pyplot as plt
#fig, ax = plt.subplots()
##ax.set_xscale('log')
##    ax.set_xlim(xmin=0.1)
#ax.set_xlim(xmax=1.)
#ax.set_title(name)
#ax.plot(1./xf, yfdiff)

#snow_basin_index_doy = basin_index_doy(cumdat,doy=91)
#import imp
#gg = imp.load_source('reassign_by_yr','C:\\code\usgs-gauges\\gageroutines.py')
#snow_basin_index_cum91 = gg.reassign_by_yr(snow_basin_index_doy)
#cumdat = cummulative_positive_wy_snow_data(snow_df)
#snow_basin_index_doy = basin_index_doy(cumdat,doy=150)
#gg = imp.load_source('reassign_by_yr','C:\\code\usgs-gauges\\gageroutines.py')
#snow_basin_index_cum150 = gg.reassign_by_yr(snow_basin_index_doy)
#tmp = pd.concat([snow_basin_index_cum91,snow_basin_index_cum150],axis=1)
#snow_basin_index_doy = basin_index_doy(snow_df,doy=91)
#snow_basin_index = gg.reassign_by_yr(snow_basin_index_doy)
#dfplot = pd.concat([snow_basin_index,snow_basin_index_cum],axis = 1)
#print cumdat
#snotel_basin_index = basin_index(snow_df)
#snotelplot= snotel_basin_index.loc['20150101':'20150510']
#tsplot(snotelplot)

#dfplot.columns = ['SWE', 'CUM SWE']
#from pandas import ExcelWriter
#writer = ExcelWriter('CumSWE DOY 91 v 150.xlsx')
#dfplot.to_excel(writer,'Sheet1')
#writer.save()
#tsplot(dfplot)

























