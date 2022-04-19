import json
import requests
from elasticsearch import Elasticsearch, helpers
import os

'''
Uses VA Lighthouse API to retrieve facility information such as wait time and satisfaction.  
'''

INDEX_NAME = 'va-facilities-2'

class Facility:
    def __init__(self, name, location, type):
        self.name = name
        self.location = location
        self.type = type

REQUEST_URL = 'https://sandbox-api.va.gov/services/va_facilities/v0/facilities/all'

response = requests.get(
    REQUEST_URL,
    headers={'Accept': 'application/geo+json', 'apikey': os.environ['VA_API_KEY']},
)

json_response = response.json()
print(type(json_response))

doc_list = []

for num, doc in enumerate(json_response['features']):
    print('num: ' + str(num))
    # print('doc: ' + json.dumps(doc))
    name = doc['properties']['name']
    location = doc['geometry']['coordinates']
    type = doc['properties']['facility_type']
    state = doc['properties']['address']['physical']['state']

    facility = Facility(name, location, type)
    dict_facility = facility.__dict__
    dict_facility['state'] = state
    
    if type == 'va_health_facility':
        wait_times = doc['properties']['wait_times']

        satisfaction_data = doc['properties']['satisfaction']['health']

        if "primary_care_urgent" in satisfaction_data:
            dict_facility['primary_care_urgent_score'] = satisfaction_data['primary_care_urgent']

        if "primary_care_routine" in satisfaction_data:
            dict_facility['primary_care_routine_score'] = satisfaction_data['primary_care_routine']

        if "specialty_care_routine" in satisfaction_data:
            dict_facility['specialty_care_routine_score'] = satisfaction_data['specialty_care_routine']
        
        if "specialty_care_urgent" in satisfaction_data:
            dict_facility['specialty_care_urgent_score'] = satisfaction_data['specialty_care_urgent']

        extract_times = wait_times['health']
        for item in extract_times:
            service = item['service']
            established_time = item['established']
            new_time = item['new']

            service_new = service + '-new'
            service_established = service + '-established'
            dict_facility[service_new] = new_time
            dict_facility[service_established] = established_time
        print(dict_facility)

    doc_list.append(dict_facility)

es = Elasticsearch(cloud_id=os.environ['CLOUD_ID'],api_key=os.environ["CLOUD_API_KEY"])
result = es.ping()
print(result)
if result:
    print("Connected to Elasticsearch")
else:
    print("Not connected")


try:
    resp = helpers.bulk(es, doc_list, index=INDEX_NAME)
    # print the response returned by Elasticsearch
    print ("helpers.bulk() RESPONSE:", resp)
    print ("helpers.bulk() RESPONSE:", json.dumps(resp, indent=4))

except Exception as err:
    print("Elasticsearch helpers.bulk() ERROR:", err)
    print("Indexing error: {0}".format(err))

