# Depends on nwispy, downloadable at github

from nwispy import nwispy_webservice
request = {"data type": "monthly", "site number": "14191000", "start date": "1800-01-01", "end date": "2018-12-15", "parameters": ["00060"]}
user_parameters_url = nwispy_webservice.encode_url(data_request = request)
nwispy_webservice.download_file(user_parameters_url,'dv','testfile.txt','C:\\code\\')