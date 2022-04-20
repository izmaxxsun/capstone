import csv
from pathlib import Path
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from pathlib import Path
import os

base_path = Path(__file__).parent
file_path = (base_path / "../source_data/faq_extract_sbert.csv").resolve()

INDEX_NAME = "faq-knn-sbert"

sentence_transformer = SentenceTransformer("all-mpnet-base-v2")

es_client = Elasticsearch(cloud_id=os.environ['CLOUD_ID'],
                          api_key=os.environ['CLOUD_API_KEY'])

with open('faq_extract_sbert.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        question = row['Question']
        answer = row['Answer']
        source = row['Source']
        embedding = sentence_transformer.encode(question)

        data = {
            "question": question,
            "sbert_encoding": embedding,
            "answer": answer,
            "source": source
        }

        response = es_client.index(
            index=INDEX_NAME,
            document=data
        )

        print(response)
