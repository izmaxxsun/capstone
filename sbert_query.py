from elasticsearch import Elasticsearch
from typing import List
from sentence_transformers import SentenceTransformer

KEEP_GOING  = True


sentence_transformer = SentenceTransformer("all-mpnet-base-v2")

es_client = Elasticsearch(cloud_id="My_deployment:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ2MGUxMWIyZGMyZTY0NjhmYjM1ODQ3MjJhZjVjOTUyNyRjZmMzYzVlNTRmZjM0ZjE2OGY4MmFmODI1MjBhZTZkMg==", api_key="a01tNV8zOEJ5ZUE5VTkzUnpjLXc6bHlvUlhxNnBSY2FlNzhrcXo3OXdmUQ==")

INDEX_NAME = "my-approx-knn-index"

def query_question(question: str, top_n: int = 10) -> List[dict]:

    embedding = sentence_transformer.encode(question)
    es_result = es_client.knn_search(
        index=INDEX_NAME,
        knn={
            "field": "sbert_encoding",
            "query_vector": embedding,
            "k": 10,
            "num_candidates": 100
            }
            )
    hits = es_result["hits"]["hits"]
    clean_result = []
    for hit in hits:
        clean_result.append(
                {
                    "question": hit["_source"]["question"],
                    "answer": hit["_source"]["answer"],
                    "score": hit["_score"]
                }
                )
    return clean_result

while(KEEP_GOING):
    print('What you want to Willis?')
    question = input()
    result = query_question(question)
    for elem in result[:5]:
        print(elem)
        print("\n")
    print("Want to ask another question? Y/N")
    response = input()
    if(response == "N"):
        KEEP_GOING = False
    else:
        KEEP_GOING = True
