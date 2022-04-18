import csv
from pathlib import Path
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch

INDEX_NAME = "my-approx-knn-index"

sentence_transformer = SentenceTransformer("all-mpnet-base-v2")

es_client = Elasticsearch(cloud_id="My_deployment:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ2MGUxMWIyZGMyZTY0NjhmYjM1ODQ3MjJhZjVjOTUyNyRjZmMzYzVlNTRmZjM0ZjE2OGY4MmFmODI1MjBhZTZkMg==",
                          api_key="a01tNV8zOEJ5ZUE5VTkzUnpjLXc6bHlvUlhxNnBSY2FlNzhrcXo3OXdmUQ==")

with open('faq_extract_sbert.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        question = row['Question']
        answer = row['Answer']
        embedding = sentence_transformer.encode(question)

        data = {
            "question": question,
            "sbert_encoding": embedding,
            "answer": answer,
        }

        response = es_client.index(
            index=INDEX_NAME,
            document=data
        )

        print(response)
