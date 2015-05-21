# Depends on nwispy, downloadable at github
import sys
sys.path.append('c:\\code\\nwispy\\')
from nwispy import nwispy_webservice
request = {"data type": "monthly", "site number": "14191000", "start date": "2010-01-01", "end date": "2018-12-15", "parameters": ["00060"]}
user_parameters_url = nwispy_webservice.encode_url(data_request = request)
print user_parameters_url
#assert False
pathy = 'C:\\code\\'
filey = 'testfile.txt'
nwispy_webservice.download_file(user_parameters_url,'dv',filey,pathy)
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

import urllib2
import os
response = urllib2.urlopen('http://waterservices.usgs.gov/nwis/site/?format=rdb&sites='+'14191000')  

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
import numpy as np
b = np.array(dd[2:])
