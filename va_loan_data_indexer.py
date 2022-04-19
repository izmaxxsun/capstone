from elasticsearch import Elasticsearch, helpers
import csv
import json
from pathlib import Path

base_path = Path(__file__).parent
file_path = (base_path / "source_data/VA_Loans/Purchase-Table-2021.csv").resolve()
INDEX_NAME = "va-lender-purchase-2021"

class Lender:
    def __init__(self, lender_name, lender_rank, loans_guaranteed, avg_loan_amount, total_loan_amount):
        self.lender_name = lender_name
        self.lender_rank = lender_rank
        self.loans_guaranteed = loans_guaranteed
        self.avg_loan_amount = avg_loan_amount
        self.total_loan_amount = total_loan_amount

doc_list = []

with open(file_path) as f:
    reader = csv.DictReader(f)
    for row in reader:
        # print(row)
        lender_name = row['Lender Name']
        lender_rank = row['Rank']
        loans_guaranteed = row['Loans Guaranteed']
        avg_loan_amount = row['Avg. Loan Amount'].strip()
        total_loan_amount= row['Total Loan Amount'].strip()

        lender = Lender(lender_name, lender_rank, loans_guaranteed, avg_loan_amount, total_loan_amount)
        lender_dict = lender.__dict__
        doc_list.append(lender_dict)

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





