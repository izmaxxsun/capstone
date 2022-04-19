from elasticsearch import Elasticsearch, helpers
import csv
import json

es = Elasticsearch(cloud_id="My_deployment:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ2MGUxMWIyZGMyZTY0NjhmYjM1ODQ3MjJhZjVjOTUyNyRjZmMzYzVlNTRmZjM0ZjE2OGY4MmFmODI1MjBhZTZkMg==",api_key="a01tNV8zOEJ5ZUE5VTkzUnpjLXc6bHlvUlhxNnBSY2FlNzhrcXo3OXdmUQ==")
result = es.ping()
print(result)
if result:
    print("Connected to Elasticsearch")
else:
    print("Not connected")

with open('Medicare_Part_D_Prescribers_by_Geography_and_Drug_2019.csv') as f:
    reader = csv.DictReader(f)
    
    try:
        resp = helpers.bulk(es, reader, index='drugs-2019-a')
        print ("helpers.bulk() RESPONSE:", resp)
        print ("helpers.bulk() RESPONSE:", json.dumps(resp, indent=4))
    except helpers.BulkIndexError as bulkIndexError:
        print("Indexing error: {0}".format(bulkIndexError))



