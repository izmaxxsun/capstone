from elasticsearch import Elasticsearch, helpers
import csv
import json
import os
from pathlib import Path

INDEX_NAME = 'drugs-2019'
base_path = Path(__file__).parent
file_path = (base_path / "../source_data/medicare_part_d_cms/Medicare_Part_D_Prescribers_by_Geography_and_Drug_2019.csv").resolve()

es = Elasticsearch(cloud_id=os.environ['CLOUD_ID'],api_key=os.environ['CLOUD_API_KEY'])
result = es.ping()
print(result)
if result:
    print("Connected to Elasticsearch")
    with open(file_path) as f:
        reader = csv.DictReader(f)
        
        try:
            resp = helpers.bulk(es, reader, index=INDEX_NAME)
            print ("helpers.bulk() RESPONSE:", resp)
            print ("helpers.bulk() RESPONSE:", json.dumps(resp, indent=4))
        except helpers.BulkIndexError as bulkIndexError:
            print("Indexing error: {0}".format(bulkIndexError))
else:
    print("Not connected")





