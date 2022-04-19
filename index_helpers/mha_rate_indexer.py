from elasticsearch import Elasticsearch, helpers
import csv
import json
from pathlib import Path

base_path = Path(__file__).parent
file_path = (base_path / "source_data/housing/bahwo22.csv").resolve()
INDEX_NAME = "military-bah-rate-2022a"

class Housing:
    def __init__(self, code, pay_grade, rate):
        self.code = code
        self.pay_grade = pay_grade
        self.rate = rate

doc_list = []

with open(file_path) as f:
    reader = csv.DictReader(f)
    for row in reader:
        code = row['CODE']
        E1_rate = row['E1']
        E2_rate = row['E2']
        E3_rate = row['E3']
        E4_rate = row['E4']
        E5_rate = row['E5']
        E6_rate = row['E6']
        E7_rate = row['E7']
        E8_rate = row['E8']
        E9_rate = row['E9']
        W1_rate = row['W1']
        W2_rate = row['W2']
        W3_rate = row['W3']
        W4_rate = row['W4']
        W5_rate = row['W5']
        O1E_rate = row['O1E']
        O2E_rate = row['O2E']
        O3E_rate = row['O3E']
        O1_rate = row['O1']
        O2_rate = row['O2']
        O3_rate = row['O3']
        O4_rate = row['O4']
        O5_rate = row['O5']
        O6_rate = row['O6']
        O7_rate = row['O7']

        e1_housing = Housing(code, "E-1", E1_rate).__dict__
        e2_housing = Housing(code, "E-2", E2_rate).__dict__
        e3_housing = Housing(code, "E-3", E3_rate).__dict__
        e4_housing = Housing(code, "E-4", E4_rate).__dict__
        e5_housing = Housing(code, "E-5", E5_rate).__dict__
        e6_housing = Housing(code, "E-6", E6_rate).__dict__
        e7_housing = Housing(code, "E-7", E7_rate).__dict__
        e8_housing = Housing(code, "E-8", E8_rate).__dict__
        e9_housing = Housing(code, "E-9", E9_rate).__dict__

        o1e_housing = Housing(code, "O1E", O1E_rate).__dict__
        o2e_housing = Housing(code, "O2E", O2E_rate).__dict__
        o3e_housing = Housing(code, "O3E", O3E_rate).__dict__

        w1_housing = Housing(code, "W1", W1_rate).__dict__
        w2_housing = Housing(code, "W2", W2_rate).__dict__
        w3_housing = Housing(code, "W3", W3_rate).__dict__
        w4_housing = Housing(code, "W4", W4_rate).__dict__
        w5_housing = Housing(code, "W5", W5_rate).__dict__

        o1_housing = Housing(code, "O1", O1_rate).__dict__
        o2_housing = Housing(code, "O2", O2_rate).__dict__
        o3_housing = Housing(code, "O3", O3_rate).__dict__
        o4_housing = Housing(code, "O4", O4_rate).__dict__
        o5_housing = Housing(code, "O5", O5_rate).__dict__
        o6_housing = Housing(code, "O6", O6_rate).__dict__
        o7_housing = Housing(code, "O7", O7_rate).__dict__

        doc_list.append(e1_housing)
        doc_list.append(e2_housing)
        doc_list.append(e3_housing)
        doc_list.append(e4_housing)
        doc_list.append(e5_housing)
        doc_list.append(e6_housing)
        doc_list.append(e7_housing)
        doc_list.append(e8_housing)
        doc_list.append(e9_housing)
        doc_list.append(o1e_housing)
        doc_list.append(o1e_housing)
        doc_list.append(o1e_housing)
        doc_list.append(w1_housing)
        doc_list.append(w2_housing)
        doc_list.append(w3_housing)
        doc_list.append(w4_housing)
        doc_list.append(w5_housing)
        doc_list.append(o1_housing)
        doc_list.append(o2_housing)
        doc_list.append(o3_housing)
        doc_list.append(o4_housing)
        doc_list.append(o5_housing)
        doc_list.append(o6_housing)
        doc_list.append(o7_housing)


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





