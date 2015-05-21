# Roy Haggerty 5/21/2015
import pandas as pd
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

#Test with the following lines
#testpd = get_gage_data(14144800, local_path = 'C:\\code\\Willamette Basin gauge data\\')
#print testpd.tail()