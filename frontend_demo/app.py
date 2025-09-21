from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """Renders the main chat page."""
    return render_template('index.html')

if __name__ == '__main__':
    # Запускаем Flask на порту 5000, чтобы не конфликтовать с FastAPI (порт 8000)
    app.run(debug=True, port=5000)
