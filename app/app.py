from flask import Flask, render_template
from db.db import init_db

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5555)