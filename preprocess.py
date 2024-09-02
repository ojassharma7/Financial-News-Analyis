import re
import string
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['financial_news']
collection = db['articles']

def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def preprocess_articles():
    # Retrieve all articles from the database
    articles = collection.find({})
    
    for article in articles:
        raw_text = article['content']
        cleaned_text = clean_text(raw_text)
        
        # Update the article with the cleaned text
        collection.update_one({'_id': article['_id']}, {'$set': {'cleaned_content': cleaned_text}})
        print(f"Processed article: {article['_id']}")

if __name__ == "__main__":
    preprocess_articles()
