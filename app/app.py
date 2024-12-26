from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "REPLACE_WITH_A_SECRET_KEY"  # Required for session handling

# In-memory user store (for demo). In production, use a real DB & hashed passwords.
users = {}

@app.route("/")
def home():
    # Checka if user is logged in
    if 'username' in session:
        return render_template("home.html", username=session["username"])
    else:
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form_username = request.form["username"]
        form_password = request.form["password"]

        if form_username in users and users[form_username] == form_password:
            session["username"] = form_username
            return redirect(url_for("home"))
        else:
            return "Invalid credentials. Please try again."

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form_username = request.form["username"]
        form_password = request.form["password"]

        if form_username in users:
            return "Username already taken!"

        users[form_username] = form_password
        session["username"] = form_username  # auto-login
        return redirect(url_for("home"))

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))

if __name__ == '__main__':
    # init_db()
    app.run(debug=True, host='0.0.0.0', port=5555)