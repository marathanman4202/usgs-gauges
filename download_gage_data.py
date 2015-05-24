"""
downloads USGS gage data to tab-delimited text files on hard drive
Definitely ugly and fast, but it worked
Apologies to future self for bad coding and few comments
"""
# Depends on nwispy, downloadable at github
import sys
import xlrd
import urllib2
import os
import csv
import numpy as np
sys.path.append('c:\\code\\nwispy\\')
from nwispy import nwispy_webservice
#print user_parameters_url
#assert False
pathy = 'C:\\code\\WBgages\\'
#pathy = 'C:\\code\\'
Q_SWE_PRE_params = xlrd.open_workbook('C:\\code\\maplot\\Q-SWE-PRE_temp.xlsx')
#Gauge_num = Q_SWE_PRE_params.sheet_by_index(2).col_values(0)[1:]
Gauge_num = [14144800]
b = []
for gage in Gauge_num:
    gage = int(gage)
    request = {"data type": "monthly", "site number": gage, "start date": "1800-01-01", "end date": "2018-12-15", "parameters": ["00060"]}
    user_parameters_url = nwispy_webservice.encode_url(data_request = request)
    gage_num_str = str(gage)
    filey = gage_num_str+'.txt'
    nwispy_webservice.download_file(user_parameters_url,'dv',filey,pathy)
    response = urllib2.urlopen('http://waterservices.usgs.gov/nwis/site/?format=rdb&sites=' + gage_num_str)  
    outputfile = os.path.join(pathy, gage_num_str+'_loc.txt')        
    with open(outputfile, "wb") as f:
        f.write(response.read())        
    with open(pathy+gage_num_str+'_loc.txt') as f:
        reader = csv.reader(f, delimiter="\t")
        d = list(reader)
    dd = []
    for line in d:
        if line[0][0][0] != '#': 
            mem = line[1:3]
            mem.extend(line[4:6])
            dd.append(mem)
    b.append(dd[2:][0])
    print dd[2:][0]

with open(pathy+"gage_locations.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(b)
assert False   
    
    
    
import csv
with open(pathy+filey) as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)

#print d[0][0][0]
dd = []
for line in d:
    if line[0][0][0] != '#': dd.append(line[2:4])
import numpy as np
a = np.array(dd[2:])


outputfile = os.path.join(pathy, filey[:-4]+'_loc.txt')        
with open(outputfile, "wb") as f:
    f.write(response.read())        
    
with open(pathy+filey[:-4]+'_loc.txt') as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)
    
dd = []
for line in d:
    if line[0][0][0] != '#': 
        mem = line[1:3]
        mem.extend(line[4:6])
        dd.append(mem)
b = np.array(dd[2:])
