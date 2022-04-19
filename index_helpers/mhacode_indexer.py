from elasticsearch import Elasticsearch, helpers
import csv
import json
from pathlib import Path

base_path = Path(__file__).parent
file_path = (base_path / "source_data/housing/mhanames22.csv").resolve()
INDEX_NAME = "military-bah-code-2022"

class Housing:
    def __init__(self, code, location, state):
        self.code = code
        self.location = location
        self.state = state

doc_list = []

with open(file_path) as f:
    reader = csv.DictReader(f)
    for row in reader:
        # print(row)
        code_raw = row['CODE']
        code_split = code_raw.split(';')
        code = code_split[0]
        location = code_split[1]
        state = row['STATE'].strip()
    
        housing = Housing(code, location, state)
        housing_dict = housing.__dict__
        # payband_dict = payband.__dict__
        doc_list.append(housing_dict)

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





