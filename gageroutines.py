# Roy Haggerty 5/21/2015
import pandas as pd
import numpy as np
from datetime import datetime 
from datetime import timedelta
import imp
gnrl = imp.load_source('getWaterYear','C:\\code\usgs-gauges\\snowroutines.py')
gnrl = imp.load_source('get_value_by_moyrange','C:\\code\usgs-gauges\\preciproutines.py')
gnrl = imp.load_source('reassign_by_wyr','C:\\code\usgs-gauges\\preciproutines.py')
import sys
sys.path.insert(0, 'C:\\code\\maplot\\')
import constants as cst

def get_gage_data(gage_number, file_name = '', index_col = 2, local_path = ''):
    """
    returns pandas dataframe with gage data from gage number
    
    gage_number -- USGS gage number (int)
    local_path -- path location for data (str) default = ''
    file_name -- file name for data (str). Can be left blank if file name is 'gage_number.txt'
    index_col -- column for dates (int) default = 0
    return gage_df -- pandas df (pandas dataframe)
    """
    assert type(gage_number) == int
    assert type(file_name) == str
    assert type(local_path) == str
    if file_name == '': file_name = str(gage_number) + '.txt'
    skiprows = -1
    with open(local_path+file_name, 'r') as ifile:
        for line in ifile:
            skiprows += 1
            if not line[0] == '#':
                skiprows += 2
                break
    gage_df = pd.read_csv(local_path+file_name,index_col=index_col, parse_dates=[index_col], skiprows=skiprows, sep='\t',header=None) 
    gage_df = gage_df.convert_objects(convert_numeric=True)
    gage_df.index  = pd.to_datetime(gage_df.index.date)  #convert to Timestamp, set time to 00
    del gage_df[0]
    gage_df.columns = ['Gage number','Discharge (cfs)','Data-value qualification code']
    gage_df.index.names = ['Date']
    return gage_df

def get_gage_info(file_name = 'gage_locations.csv', index_col = [0,1,2,3], local_path = ''):
    """
    returns list of list of [gage number, lat, long] from csv file
    file_name = csv file
    index_col = column for gage number [0], gage name [1], lat [2], long [3] from csv file.  Set index_col list to retrieve each of these.
    local_path = location of file
    
    return list [gage number, gage_name, lat, long] or subset depending on index_col
    """
    gage_info_np = np.array(np.genfromtxt(local_path + file_name, delimiter=',',skip_header=0,dtype=None))
    gage_info = gage_info_np.tolist()
    numcol = len(index_col)
    num_gages = len(gage_info)
    gage_info = [[gage_info[i][index_col[j]] for j in range(numcol)] for i in range(num_gages)] # return only values asked for by index_col for all gages
    return gage_info
    
def get_all_gages(file_name = 'gage_locations.csv', index_col = [0,2,3], local_path = ''):
    """
    returns pandas dataframe of all gages. Careful. This could be huge!
    file_name = csv file
    index_col = column for gage number, lat, long from csv file
    local_path = location of files
    all_gages_df = pandas dataframe with all discharge data
    
    return all_gages_df
    """
    gage_info = get_gage_info(file_name=file_name, index_col=[0], local_path=local_path)
    num_gages = len(gage_info)
    gage_numbers_list = [gage_info[i][0] for i in range(num_gages)]
    gage_df_list = []
    i = -1
    for gage_number in gage_numbers_list:
        i += 1
        gage_df_list.append(get_gage_data(gage_number,local_path=local_path))
        gage_df_list[i].drop(gage_df_list[i].columns[[0,2]], axis=1, inplace=True) # Note: zero indexed
        gage_df_list[i].columns = [str(gage_number) + ' Discharge (cfs)']
        gage_df_list[i].index.names = ['Date']
        print gage_number
    all_gages_df = pd.concat(gage_df_list,axis=1)
    
    return all_gages_df

def get_avg_discharge_by_month(gage_number, file_name = '', index_col = 2, local_path = ''):
    """
    returns pandas dataframe with average discharge in time period for all years
    gage_number = gage number
    file_name = csv file
    index_col = discharge data column
    local_path = location of files
    
    return average discharge in time period for each of all years
    """
    gage_data = get_gage_data(gage_number, file_name = '', index_col = 2, local_path = local_path)
    avg_discharge = gage_data.resample('M', how='mean')
    
    return avg_discharge
def get_discharge_by_doyrange(gage_number, doystart,doyend, file_name = '', index_col = 2, local_path = ''):
    """
    returns pandas dataframe with discharge in selected doy range for all years
    gage_number = gage number
    index_col = discharge data column
    local_path = location of files
    
    return discharges in time period for each of all years
    """
    gage_data = get_gage_data(gage_number, file_name = '', index_col = 2, local_path = local_path)
    gd = gage_data

    year = 2015 # arbitrary, only need year to use with datetime
    datestart = datetime(year, 1, 1) + timedelta(doystart - 1)
    moystart = datestart.month
    domstart = datestart.day
    dateend = datetime(year, 1, 1) + timedelta(doyend - 1)
    moyend = dateend.month
    domend = dateend.day
    gd2 = gd[((gd.index.month == moystart) & (gd.index.day >= domstart)) | (gd.index.month > moystart)]
    gage_data_filtered = gd2[((gd2.index.month == moyend) & (gd2.index.day <= domend)) | (gd2.index.month < moyend)]
    return gage_data_filtered
    
def get_avg_discharge_by_moy(df,moy=8):
    """
    returns pandas dataframe with normalized daily discharge for month of year
    df = pandas dataframe with daily time index
    moy = month of year, an integer.  Default = 8.
    return df_basin_index_moy -- pandas df (pandas dataframe)
    """
    avg_discharge_by_moy = df[(df.index.month==moy)]
    return avg_discharge_by_moy

def reassign_by_yr(df):
    """
    returns pandas dataframe with single value from each year and time reassigned to year
    df = pandas dataframe 
    return value_for_year -- pandas df (pandas dataframe)
    """
    value_for_year = df.resample('A',how='mean')
    return value_for_year

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
    T = 1./365.
#    x = np.linspace(0.0, N*T, N)
    yf = scipy.fftpack.fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
    fig, ax = plt.subplots()
    ax.plot(xf, 2.0/N * np.abs(yf[0:N/2]))
    
#gage_info = get_gage_info(local_path = 'C:\\code\\Willamette Basin gauge data\\',index_col=[0,1])
#print gage_info[:3]

gage_data = get_gage_data(14211720, local_path= 'C:\\code\\Willamette Basin gauge data\\')
gage_by_wy = gnrl.reassign_by_wyr(gage_data,how='mean')
print gage_by_wy.loc['18950101':'20141001'].mean()['Discharge (cfs)']*cst.cfs_to_m3*cst.m3s_to_cmy

#print gage_data.iloc[:,1:2]
#print gage_data["Discharge (cfs)"]
plot_fourier(gage_data,name="Discharge (cfs)")

#gagedata = get_avg_discharge_by_doyrange(14144800,10,12,local_path= 'C:\\code\\Willamette Basin gauge data\\')
#print gagedata.head()

#avg_discharge = get_avg_discharge_by_month(14144800, local_path = 'C:\\code\\Willamette Basin gauge data\\')
#avg_discharge_by_month = get_avg_discharge_by_moy(avg_discharge,moy=9)
#print avg_discharge_by_month
#discharge_by_doy = get_discharge_by_doyrange(14144800,160,225,local_path='C:\\code\\Willamette Basin gauge data\\')
#print discharge_by_doy
#assert False
#value_for_year = reassign_by_yr(discharge_by_doy)
#print value_for_year
