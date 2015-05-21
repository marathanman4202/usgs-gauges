import pandas as pd
import numpy as np
def get_gage_data(gage_number, file_name = '', index_col = 0, local_path = ''):
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
#    with open(path) as f:
#        reader = csv.reader(f, delimiter="\t")
#        d = list(reader)
#    print d[0][2] # 248
    gage_df = pd.read_csv(local_path+file_name,index_col=index_col, parse_dates=[index_col], comment='#', skiprows=0) #sep ="\t", 
    gage_df = gage_df.convert_objects(convert_numeric=True)
    gage_df.index  = pd.to_datetime(gage_df.index.date)  #convert to Timestamp, set time to 00
    assert False
#    ts = pd.Series(gage_df.iloc[:,data_col_num],df.index)
    
    return gage_df

testpd = get_gage_data(1000, local_path = 'C:\\code\\Willamette Basin gauge data\\')