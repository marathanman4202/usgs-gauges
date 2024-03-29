# Roy Haggerty 5/27/2015
import pandas as pd
import os
from datetime import datetime 
from datetime import timedelta
import sys
sys.path.insert(0, 'C:\\code\\maplot\\')
import constants as cst

def get_precip_data(index_col = 0, local_path = '',filename=None):
    """
    returns pandas dataframe with all precip data from csv file
    
    local_path -- path location for data (str) default = ''
    index_col -- column for dates (int) default = 0
    return precip_df -- pandas df (pandas dataframe)
    filename -- get specific csv file data if filename is given, otherwise get whatever is there
    
    requires precip data saved to csv files at location local_path
    """
    assert type(local_path) == str
    i = -1
    df_list = []
    print 'getting precip data, stored locally'
    if filename is None:
        filelist = os.listdir(local_path)
    else:
        filelist = [filename]
    for filename in filelist:
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
    df= df['18940101':'20141001'] #remove incomplete data for WY15 from calculation
    df_norm = df.div(df.groupby(lambda x: x.dayofyear).transform(pd.Series.median))
    # this line thanks to EdChum on stackoverflow

    return df_norm

def normalize_by_mean(df):
    """
    returns pandas dataframe with normalized daily data
    
    df = pandas dataframe with daily time index
    return df_norm -- pandas df (pandas dataframe)
    """
    df= df['18940101':'20141001'] #remove incomplete data for WY15 from calculation
    df_norm = df.div(df.groupby(lambda x: x.dayofyear).transform(pd.Series.mean))
    # this line thanks to EdChum on stackoverflow

    return df_norm
def basin_index(df):
    """
    returns pandas dataframe with normalized basin index
    From snotel website 
        "The basin index is calculated as the sum of the valid 
        current values divided by the sum of the corresponding medians  [use mean for precip]
        (for snow water equivalent) or averages (for precipitation) and 
        the resulting fraction multiplied by 100."
    df = pandas dataframe with daily time index
    return df_basin_index -- pandas df with normalized basin index (pandas dataframe)
    """
    df_sum = df.sum(axis=1)
    df1 = df.groupby(lambda x: x.dayofyear).transform(pd.Series.mean)
    df2 = df1.sum(axis=1)
    df_basin_index = df_sum.div(df2)

    return df_basin_index
    
def get_value_by_moyrange(df, moystart,moyend,wy_month_start = 10):
    """
    returns pandas dataframe with precip in selected moy range for all years
    wy_month_start = month that water year starts
    
    return precip in time period for each of all years
    """
    if moystart > moyend and moystart < wy_month_start:
        print 'moystart must be before moyend'; assert False
    elif moystart > 12 or moyend > 12:
        print 'months must be less than or equal to 12'; assert False
    if moystart < wy_month_start:
        df2 = df[(df.index.month >= moystart)]
        df_filtered = df2[(df2.index.month <= moyend)]
    elif moystart >= wy_month_start and moyend >= moystart:
        df2 = df[(df.index.month >= moystart)]
        df_filtered = df2[(df2.index.month <= moyend)]       
    else:
        df2 = df[(df.index.month < wy_month_start) | (df.index.month >= moystart)]
        df_filtered = df2[(df2.index.month <= moyend) | (df2.index.month >= moystart)]
        
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
    
def reassign_by_wyr(df,how='sum'):
    """
    returns pandas dataframe with single value from each water year (Oct 1 - Sep 30) and time reassigned to year
    df = pandas dataframe 
    return value_for_wy -- pandas df (pandas dataframe)
    """
    value_for_wy = df.resample('BA-SEP',how=how)
    return value_for_wy
    
def plot_fourier(df,name):
    """
    plot fourier transform of pandas dataframe
    Thanks to Paul H at http://stackoverflow.com/questions/25735153/plotting-a-fast-fourier-transform-in-python 
    """
    import matplotlib.pyplot as plt
    import scipy.fftpack
    
    # Number of samplepoints

    y = np.array(df[name])
    N = len(y)
    T = 1./12.
    yf = scipy.fftpack.fft(y)
    yf = 2.0/N * np.abs(yf[0:N/2])
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
    fig, ax = plt.subplots()
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.plot(xf, yf)
    
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
    
def scatterplot(df,xdata,ydata,xlabel=None,ylabel=None,title=None):
    """
    simple plotting routine for two timeseries.  Just quick & dirty.
    """
    import matplotlib.pyplot as plt
    twodee = plt.figure().gca()
    twodee.scatter(df[xdata], df[ydata])
    twodee.set_xlabel(xlabel, fontsize = 14)
    twodee.set_ylabel(ylabel, fontsize = 14)
    twodee.set_xlim(left=0.)
    twodee.set_ylim(bottom=0.)
    plt.title(title,fontsize=24)
    plt.gca().patch.set_facecolor('white')
    plt.show()
    
def dostats(df):
    from statsmodels.formula.api import ols
    formula = 'Basin ~ SalemMcNF'
    lm = ols(formula, df).fit()
    print lm.summary()
    return
    
#Test with the following lines
precip_df = get_precip_data(local_path = 'C:\\code\\Willamette Basin precip data\\')
precip_McNF_df = get_precip_data(
    local_path = 'C:\\Users\\haggertr\\Desktop\\Roy\\Research\\WW2100\\Research\snow\\',
    filename='McNary Field precip.csv'
    )
precip_by_moyrange_McNF = get_value_by_moyrange(precip_McNF_df,10,6)
precip_by_wy_McNF = reassign_by_wyr(precip_by_moyrange_McNF)
print precip_by_wy_McNF.mean()
assert False

precip_both_df = pd.concat([precip_df,precip_McNF_df],axis=1)
precip_both_df.columns = ["Basin","SalemMcNF"]
dostats(precip_both_df)

#scatterplot(
#    precip_both_df,'Basin','SalemMcNF',
#    xlabel = '$Basinwide\, Monthly\, Precipitation$ [mm]',
#    ylabel = '$Salem\, McNary\, Field\, Monthly\, Precipitation$ [mm]',
#    title = 'Salem Precip vs Basinwide Precip')

precip_by_moyrange = get_value_by_moyrange(precip_df,2,6)
precip_by_moyrange_McNF = get_value_by_moyrange(precip_McNF_df,2,6)
precip_by_wy = reassign_by_wyr(precip_by_moyrange)
precip_by_wy_McNF = reassign_by_wyr(precip_by_moyrange_McNF)
print precip_by_wy.mean()
print precip_by_wy_McNF.mean()
spr_Precip_both_df = pd.concat([precip_by_wy,precip_by_wy_McNF],axis=1)
spr_Precip_both_df.columns = ["Basin","SalemMcNF"]
dostats(spr_Precip_both_df)
scatterplot(
    spr_Precip_both_df,'Basin','SalemMcNF',
    xlabel = '$Basinwide\, MAMJ\, Precipitation$ [mm]',
    ylabel = '$Salem\, McNary\, Field\, MAMJ\, Precipitation$ [mm]',
    title = 'Salem Precip vs Basinwide Precip')

#tsplot(precip_by_wy)
#print precip_by_wy['19000101':'20141001'].mean()#/1565.6999
#print precip_by_wy
#precip_basin_index = basin_index(precip_by_wy)
#precip_basin_index= precip_basin_index['19950101':'20150510']


#from snowroutines import get_snow_data
#from snowroutines import basin_index_doy as sn_basin_index_doy
#snow_df = get_snow_data(local_path = 'C:\\code\\Willamette Basin snotel data\\')
#snotel_basin_index = sn_basin_index_doy(snow_df)
#snotelplot= snotel_basin_index.loc['18950101':'20140101']*472.
#dfplot = pd.concat([precip_by_wy['18950101':'20141001'],reassign_by_wyr(snotelplot)],axis=1)
#dfplot.columns = ['Precip Feb 1 - Apr 30', 'SNOTEL Basin Index * 472']
#print dfplot

#tsplot(dfplot)
