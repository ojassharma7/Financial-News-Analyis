from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        query = request.form['query']
        if not query.strip():
            return render_template('index.html', error="Query cannot be empty")

        summary = generate_summary(query)
        if summary:docker build -t my-flask-app .

            return render_template('result.html', summary=summary)
        else:
            return render_template('index.html', error="No relevant articles found")
    except Exception as e:
        return render_template('index.html', error=f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)


