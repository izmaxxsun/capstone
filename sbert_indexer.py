from elasticsearch import Elasticsearch
from typing import List
from sentence_transformers import SentenceTransformer

sentence_transformer = SentenceTransformer("bert-base-nli-mean-tokens")

es_client = Elasticsearch(cloud_id="My_deployment:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ2MGUxMWIyZGMyZTY0NjhmYjM1ODQ3MjJhZjVjOTUyNyRjZmMzYzVlNTRmZjM0ZjE2OGY4MmFmODI1MjBhZTZkMg==",api_key="a01tNV8zOEJ5ZUE5VTkzUnpjLXc6bHlvUlhxNnBSY2FlNzhrcXo3OXdmUQ==")

INDEX_NAME = "my-approx-knn-index"

def index_qa_pairs(qa_pairs):
    for qa_pair in qa_pairs:
        question = qa_pair["question"]
        answer = qa_pair["answer"]
        embedding = sentence_transformer.encode(question)

        data = {
                "question": question,
                "sbert_encoding": embedding,
                "answer": answer
                }

        es_client.index(index=INDEX_NAME, document=data)

qa_pairs = [
    {
        "question": "How do I improve my English speaking?",
        "answer": "Speak more"
    },
    {
        "question": "What should I do to earn money online?",
        "answer": "Start a side hustle"
    },
    {
        "question": "How can I improve my skills?",
        "answer": "Watch some YouTube"
    }
]

index_qa_pairs(qa_pairs)
