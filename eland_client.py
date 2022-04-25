import eland as ed
from elasticsearch import Elasticsearch
import os

# First instantiate an 'Elasticsearch' instance connected to Elastic Cloud
es = Elasticsearch(cloud_id=os.environ['CLOUD_ID'], api_key=os.environ['CLOUD_API_KEY'])

df = ed.DataFrame(es, es_index_pattern="drugs-2019")

print(df.groupby('Brnd_Name').std())