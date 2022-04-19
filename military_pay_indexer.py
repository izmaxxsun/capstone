from elasticsearch import Elasticsearch, helpers
import csv
import json
from pathlib import Path

base_path = Path(__file__).parent
file_path = (base_path / "source_data/Military_Pay/Military Basic Pay Enlisted.csv").resolve()
INDEX_NAME = "military-pay-2022"

class Payband:
    def __init__(self, pay_grade, years_exp, monthly_amount):
        self.pay_grade = pay_grade
        self.years_exp = years_exp
        self.monthly_amount = monthly_amount

doc_list = []

with open(file_path) as f:
    reader = csv.DictReader(f)
    for row in reader:
        # print(row)
        pay_grade = row['Pay Grade']
        years_exp = row['Years of Experience']
        monthly_amount = row['Monthly Pay']

        payband = Payband(pay_grade, years_exp, monthly_amount)
        payband_dict = payband.__dict__
        doc_list.append(payband_dict)

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





