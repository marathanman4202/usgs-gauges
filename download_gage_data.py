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
pathy = 'C:\\code\\Willamette Basin gauge data\\'
#pathy = 'C:\\code\\'
Q_SWE_PRE_params = xlrd.open_workbook('C:\\code\\Willamette Basin gauge data\\Q-SWE-PRE_temp.xlsx')
#Gauge_num = Q_SWE_PRE_params.sheet_by_index(2).col_values(0)[1:]  # for whole list of gages
Gauge_num = [14200100]  # for specific gage
# TRY gage 14200100
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

    #XML extract code to pull drainage area
    from lxml import html
    import requests
    page = requests.get("http://nwis.waterdata.usgs.gov/nwis/inventory?search_site_no="+
    gage_num_str+
    "&search_site_no_match_type=exact&site_tp_cd=ST&drain_area_va_conjunction=and&group_key=county_cd&format=sitefile_output&sitefile_output_format=xml&column_name=agency_cd&column_name=site_no&column_name=station_nm&column_name=site_tp_cd&column_name=huc_cd&column_name=drain_area_va&list_of_search_criteria=search_site_no%2Csite_tp_cd%2Cdrain_area_va")
#    print page.text
#    assert False
#    print "http://nwis.waterdata.usgs.gov/nwis/inventory?search_site_no="+   gage_num_str+\
#    "&search_site_no_match_type=exact&site_tp_cd=ST&drain_area_va_conjunction=and&group_key=county_cd&format=sitefile_output&sitefile_output_format=xml&column_name=agency_cd&column_name=site_no&column_name=station_nm&column_name=site_tp_cd&column_name=huc_cd&column_name=drain_area_va&list_of_search_criteria=search_site_no%2Csite_tp_cd%2Cdrain_area_va"
#    assert False
    tree = html.fromstring(page.content)
    da = (tree.text_content()[-9:-3])
    print da, 'here'
    assert False
    drain_area = tree.label

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
