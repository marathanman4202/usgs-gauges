# Roy Haggerty 5/21/2015
import pandas as pd
import os
def get_snow_data(index_col = 0, local_path = ''):
    """
    returns pandas dataframe with all snow data from snotel sites
    
    local_path -- path location for data (str) default = ''
    index_col -- column for dates (int) default = 0
    return snow_df -- pandas df (pandas dataframe)
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

#Test with the following lines
snow_df = get_snow_data(local_path = 'C:\\code\\Willamette Basin snotel data\\')
#snotel_df = pd.concat([snow_df.mean(axis=1),snow_df.median(axis=1)],axis=1)
#snotel_df.columns = ['mean (in)','median (in)']
#snotel_df.index.names = ['Date']
snotel_daily_means = snow_df.groupby(lambda x: x.dayofyear).mean()
snotel_daily_medians = snow_df.groupby(lambda x: x.dayofyear).median()
snotel_df_norm = snow_df.div(snotel_daily_medians, axis=1)
print snotel_df_norm
print snotel_df_norm.describe()