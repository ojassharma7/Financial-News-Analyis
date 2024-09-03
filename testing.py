from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

res = es.search(index="financial_news", body={
    "query": {
        "match": {
            "content": "market"
        }
    }
})

print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(title)s: %(content)s" % hit["_source"])
