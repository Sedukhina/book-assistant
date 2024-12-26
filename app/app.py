from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask import Flask, jsonify, render_template
from tts import text_to_speech_ukrainian
from stt import record_and_recognize
from scenarios import process_command
import os
from db.db import init_db

app = Flask(__name__)
app.secret_key = "REPLACE_WITH_A_SECRET_KEY"  # Required for session handling

# In-memory user store (for demo). In production, use a real DB & hashed passwords.
users = {
    "admin": "admin",
}

@app.route("/")
def home():
    # Checka if user is logged in
    if 'username' in session:
        return render_template("home.html", username=session["username"])
    else:
        return redirect(url_for("login"))

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
    response = process_command(text)
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
