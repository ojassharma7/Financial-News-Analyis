from flask import Flask, render_template, request
from summarization import generate_summary

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    query = request.form['query']
    summary = generate_summary(query)
    return render_template('result.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)

