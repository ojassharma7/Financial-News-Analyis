from flask import Flask, render_template, request, session
from summarization import generate_summary
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required to use session for storing preferences

def scrape_article(url):
    """Scrape article content from a URL."""
    try:
        response = requests.get(url)
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
    preferences = request.form.get('preferences')
    url = request.form.get('url')

    if preferences:
        # Save preferences in the session (or database)
        session['preferences'] = preferences

    if url:
        # Scrape and summarize article from URL
        content = scrape_article(url)
        if content:
            summary = generate_summary(content)
            return render_template('result.html', summary=summary)
        else:
            return render_template('index.html', error="Could not retrieve article from URL.")
    elif query:
        # Summarize based on query and preferences
        personalized_query = f"{query} {session.get('preferences', '')}"
        summary = generate_summary(personalized_query)
        return render_template('result.html', summary=summary)
    else:
        return render_template('index.html', error="Please enter either a query or a URL.")

if __name__ == '__main__':
    app.run(debug=True)


