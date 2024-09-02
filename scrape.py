import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['financial_news']
collection = db['articles']

def scrape_article(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the article title
        title = soup.find('h1').get_text()
        
        # Extract the article content
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs])
        
        return {'title': title, 'content': content}
    else:
        print(f"Failed to retrieve article. Status code: {response.status_code}")
        return None

# Example usage
if __name__ == "__main__":
    article_url = 'https://finance.yahoo.com/news/a-key-inflation-metric-is-back-to-trending-below-the-feds-2-target-chart-of-the-week-100047924.html'
    article = scrape_article(article_url)
    if article:
        # Insert the article into MongoDB
        collection.insert_one(article)
        print("Article saved to MongoDB")




