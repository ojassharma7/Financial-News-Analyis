from apscheduler.schedulers.background import BackgroundScheduler
from summarization import generate_summary
import requests
import json

API_KEY = d32f4609e4e84b1bb862fab0737e6eb0

def fetch_and_summarize_articles():
    url = f'https://newsapi.org/v2/top-headlines?category=business&apiKey={API_KEY}'
    response = requests.get(url)
    articles = response.json().get('articles', [])

    for article in articles:
        title = article['title']
        content = article['content'] or article['description']
        if content:
            summary = generate_summary(content)
            print(f"Title: {title}")
            print(f"Summary: {summary}\n")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_summarize_articles, 'interval', minutes=10)  # Fetch articles every 10 minutes
    scheduler.start()

if __name__ == "__main__":
    start_scheduler()
