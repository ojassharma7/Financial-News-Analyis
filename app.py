from flask import Flask, render_template, request
from summarization import generate_summary
from bs4 import BeautifulSoup
import requests
from scheduler import start_scheduler  # Assuming you have a scheduler module

app = Flask(__name__)

def scrape_article(url):
    """Scrape article content from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs])
        return content
    except Exception as e:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    query = request.form.get('query')
    url = request.form.get('url')

    if url:
        # Scrape and summarize article from URL
        content = scrape_article(url)
        if content:
            summary = generate_summary(content)
            return render_template('result.html', summary=summary)
        else:
            return render_template('index.html', error="Could not retrieve article from URL.")
    elif query:
        # Summarize based on query
        summary = generate_summary(query)
        return render_template('result.html', summary=summary)
    else:
        return render_template('index.html', error="Please enter either a query or a URL.")

if __name__ == '__main__':
    start_scheduler()  # Start the scheduler (if it is a background task)
    app.run(debug=True)

