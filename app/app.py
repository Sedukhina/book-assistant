from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask import Flask, jsonify, render_template

from services.scenarios.scenarios import execute_command
from routes.api.api import api_routes
from routes.book_routes import books_bp
from tts import text_to_speech_ukrainian
from stt import record_and_recognize
from scenarios import process_command,command
import os
from db.db import init_db

app = Flask(__name__)
app.secret_key = "REPLACE_WITH_A_SECRET_KEY"  # Required for session handling

app.register_blueprint(api_routes)
app.register_blueprint(books_bp)

# In-memory user store (for demo). In production, use a real DB & hashed passwords.
users = {
    "admin": "admin",
}

BOOKS = [
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "categories": ["Classic", "Novel"],
        "publishDate": 1925
    },
    {
        "title": "A Brief History of Time",
        "author": "Stephen Hawking",
        "categories": ["Non-fiction", "Physics"],
        "publishDate": 1988
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "categories": ["Classic", "Novel"],
        "publishDate": 1813
    },
    {
        "title": "The Martian",
        "author": "Andy Weir",
        "categories": ["Novel", "Survival"],
        "publishDate": 2011
    },
    {
        "title": "The Selfish Gene",
        "author": "Richard Dawkins",
        "categories": ["Non-fiction", "Biology"],
        "publishDate": 1976
    },
]


@app.route("/")
def home():
    # Checka if user is logged in
    if 'username' in session:
        return render_template("home.html", username=session["username"])
    else:
        return redirect(url_for("login"))


# @app.route("/books",methods=['GET'])
# def books():
#     """
#     Serves the books.html file (client-side logic).
#     """
#     return render_template("books.html")
#
# @app.route("/api/books", methods=["GET"])
# def get_books_api():
#     """
#     Returns a JSON list of filtered books.
#     Filters are passed via query parameters:
#       ?title=...&genre=...&author=...&categories=cat1,cat2&year_from=1900&year_to=2000
#     """
#     title = request.args.get("title", "").strip().lower()
#     genre = request.args.get("genre", "").strip().lower()
#     author = request.args.get("author", "").strip().lower()
#     categories_str = request.args.get("categories", "")  # e.g. "Classic,Novel"
#     year_from_str = request.args.get("year_from", "")
#     year_to_str = request.args.get("year_to", "")
#
#     selected_categories = [c.strip() for c in categories_str.split(",") if c.strip()]
#
#     try:
#         year_from = int(year_from_str) if year_from_str else None
#         year_to = int(year_to_str) if year_to_str else None
#     except ValueError:
#         year_from = None
#         year_to = None
#
#     filtered = []
#     for book in BOOKS:
#         # 1) title check (substring)
#         if title and title not in book["title"].lower():
#             continue
#         # 2) genre check (exact)
#         if genre and genre != book["genre"].lower():
#             continue
#         # 3) author check (substring)
#         if author and author not in book["author"].lower():
#             continue
#         # 4) categories check
#         if selected_categories:
#             if not all(cat in book["categories"] for cat in selected_categories):
#                 continue
#         # 5) year range
#         if year_from and book["publishDate"] < year_from:
#             continue
#         if year_to and book["publishDate"] > year_to:
#             continue
#
#         filtered.append(book)
#
#     return jsonify(filtered)

@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Validate credentials
        if username not in users or users[username] != password:
            # Instead of returning a plain message, flash an error
            flash("Invalid credentials. Please try again.", "error")
            return redirect(url_for("login"))

        # If valid, log the user in
        session["username"] = username
        return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        form_username = request.form["username"]
        form_password = request.form["password"]

        if form_username in users:
            flash("Username already taken!", "error")
            return render_template("register.html")

        users[form_username] = form_password
        session["username"] = form_username  # auto-login
        return redirect(url_for("home"))

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))

@app.route('/chat/record', methods=['GET'])
def chat_record():
    """
    Записує голос, обробляє команду та повертає відповідь із текстом і аудіо.
    """
    text = record_and_recognize()
    response = process_command(text)#

    """
        To use scenarios uncomment code below
    """
    #response = execute_command(text)
    tts_path = "static/response.mp3"

    # Генерація нового аудіофайлу
    if os.path.exists(tts_path):
        os.remove(tts_path)
    text_to_speech_ukrainian(response, tts_path)

    return jsonify({'text': text, 'response': response, 'audio_file': f'/{tts_path}'})

@app.route('/chat', methods=['GET'])
def chat_interface():
    """
    Рендерить HTML-інтерфейс чату.
    """
    return render_template('chat.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5555)
