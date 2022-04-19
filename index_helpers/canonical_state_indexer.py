from elasticsearch import Elasticsearch, helpers
import csv
import json
from pathlib import Path

base_path = Path(__file__).parent
file_path = (base_path / "source_data/states.csv").resolve()
INDEX_NAME = "canonical-state-geo"

class StateGeo:
    def __init__(self, state, location, name):
        self.state = state
        self.location = location
        self.name = name

doc_list = []

with open(file_path) as f:
    reader = csv.DictReader(f)
    for row in reader:
        state = row['state']
        latitude = row['latitude']
        longitude = row['longitude']
        name = row['name']

        location = latitude + ', ' + longitude

        state_geo = StateGeo(state, location, name).__dict__
        doc_list.append(state_geo)

es = Elasticsearch(cloud_id="My_deployment:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ2MGUxMWIyZGMyZTY0NjhmYjM1ODQ3MjJhZjVjOTUyNyRjZmMzYzVlNTRmZjM0ZjE2OGY4MmFmODI1MjBhZTZkMg==",api_key="a01tNV8zOEJ5ZUE5VTkzUnpjLXc6bHlvUlhxNnBSY2FlNzhrcXo3OXdmUQ==")
result = es.ping()
print(result)
if result:
    print("Connected to Elasticsearch")
    try:
        resp = helpers.bulk(es, doc_list, index=INDEX_NAME)
        print ("helpers.bulk() RESPONSE:", resp)
        print ("helpers.bulk() RESPONSE:", json.dumps(resp, indent=4))
    except helpers.BulkIndexError as bulkIndexError:
        print("Indexing error: {0}".format(bulkIndexError))
else:
    print("Not connected")





