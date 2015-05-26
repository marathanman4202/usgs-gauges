# Roy Haggerty 5/21/2015
import pandas as pd
import numpy as np
from datetime import datetime 
from datetime import timedelta
def get_gage_data(gage_number, file_name = '', index_col = 2, local_path = ''):
    """
    returns pandas dataframe with gage data from gage number
    
    gage_number -- USGS gage number (int)
    local_path -- path location for data (str) default = ''
    file_name -- file name for data (str)
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

def get_gage_info(file_name = 'gage_locations.csv', index_col = [0,2,3], local_path = ''):
    """
    returns list of list of [gage number, lat, long] from csv file
    file_name = csv file
    index_col = column for gage number, lat, long from csv file
    local_path = location of file
    
    return list [gage number, lat, long]
    """
    gage_info_np = np.array(np.genfromtxt(local_path + file_name, delimiter=',',skip_header=0))
    gage_info_np = np.delete(gage_info_np,1,1)  # delete col #1 
    gage_info = gage_info_np.tolist()
    gage_info = [[int(gage_info[i][0]),gage_info[i][1],gage_info[i][2]] for i in range(len(gage_info))]  #convert gage num to int
    
    return gage_info
    
def get_all_gages(file_name = 'gage_locations.csv', index_col = [0,2,3], local_path = ''):
    """
    returns pandas dataframe of all gages
    file_name = csv file
    index_col = column for gage number, lat, long from csv file
    local_path = location of files
    all_gages_df = pandas dataframe with all discharge data
    
    return all_gages_df
    """
    gage_info = get_gage_info(file_name=file_name, index_col=index_col, local_path=local_path)
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
    
    return average discharge in time period for all years
    """
    gage_data = get_gage_data(gage_number, file_name = '', index_col = 2, local_path = local_path)
    avg_discharge = gage_data.resample('M', how='mean')
    
    return avg_discharge
def get_avg_discharge_by_doyrange(gage_number, doystart,doyend, file_name = '', index_col = 2, local_path = ''):
    """
    returns pandas dataframe with discharge in selected doy range for all years
    gage_number = gage number
    index_col = discharge data column
    local_path = location of files
    
    return average discharge in time period for all years
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
    print moystart,domstart,moyend,domend
    gage_data_filtered = gd[((gd.index.month >=moystart) & (gd.index.day >= domstart)) \
                          & ((gd.index.month <=moyend) & (gd.index.day <= domend))]
    
    return gage_data_filtered
def get_avg_discharge_by_moy(df,moy=8):
    """
    returns pandas dataframe with normalized daily discharge for month of year
    df = pandas dataframe with daily time index
    return df_basin_index_moy -- pandas df (pandas dataframe)
    """
    avg_discharge_by_moy = df[(df.index.month==moy)]# & (df.index.day==day)]
    return avg_discharge_by_moy

def reassign_by_yr(df):
    """
    returns pandas dataframe with single value from each year and time reassigned to year
    df = pandas dataframe 
    return value_for_year -- pandas df (pandas dataframe)
    """
    value_for_year = df.resample('A',how='mean')
    return value_for_year
    
#gage_info = get_gage_info(local_path = 'C:\\code\\Willamette Basin gauge data\\')
#print gage_info

#gage_info = get_gage_data(14144800, local_path= 'C:\\code\\Willamette Basin gauge data\\')
gagedata = get_avg_discharge_by_doyrange(14144800,10,12,local_path= 'C:\\code\\Willamette Basin gauge data\\')
print gagedata.head()

#avg_discharge = get_avg_discharge_by_month(14144800, local_path = 'C:\\code\\Willamette Basin gauge data\\')
#avg_discharge_by_month = get_avg_discharge_by_moy(avg_discharge,moy=9)
#print avg_discharge_by_month
#value_for_year = reassign_by_yr(avg_discharge_by_month)
#print value_for_year
