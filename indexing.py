from elasticsearch import Elasticsearch
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['financial_news']
collection = db['articles']

# Connect to Elasticsearch (add scheme='http')
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

def index_articles():
    articles = collection.find({})
    for article in articles:
        # Prepare the document to be indexed
        doc = {
            'title': article['title'],
            'content': article['cleaned_content'],
            'date': article.get('date', 'N/A')
        }
        # Index the document in Elasticsearch
        es.index(index='financial_news', id=str(article['_id']), body=doc)
        print(f"Indexed article: {article['_id']}")

if __name__ == "__main__":
    index_articles(

