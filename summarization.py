from transformers import BartForConditionalGeneration, BartTokenizer
from elasticsearch import Elasticsearch

# Load the BART model and tokenizer
model_name = 'facebook/bart-large-cnn'
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)

# Connect to Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

def retrieve_articles(query):
    # Search for articles in Elasticsearch
    res = es.search(index="financial_news", body={
        "query": {
            "match": {
                "content": query
            }
        },
        "size": 3  # Retrieve the top 3 relevant articles
    })

    articles = [hit["_source"]["content"] for hit in res['hits']['hits']]
    return articles

def summarize(text):
    # Tokenize and generate summary
    inputs = tokenizer.encode(text, return_tensors='pt', max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def generate_summary(query):
    # Retrieve articles
    articles = retrieve_articles(query)
    
    if not articles:
        return "No relevant articles found."

    # Combine articles into one large text block
    combined_text = " ".join(articles)

    # Generate summary
    summary = summarize(combined_text)
    return summary

if __name__ == "__main__":
    query = "stock market"
    summary = generate_summary(query)
    print("Summary:", summary)
