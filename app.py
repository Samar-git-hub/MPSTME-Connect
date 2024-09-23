from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from helper import login_required

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///connect.db'
db = SQLAlchemy(app)


# with app.app_context():
#     db.engine.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         email TEXT
#     )
#     ''')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        sapid = request.form.get("sapid")
        if not sapid:
            return render_template("error.html", error="Provide a valid university email")
        password = request.form.get("password")
        if not password:
            return render_template("error.html", error="Provide a Password")
        return redirect("/")
    
    else:
        return render_template("login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            return render_template("error.html", error="Provide a valid university email")
        if not email.endswith("@nmims.in"): 
            return render_template("error.html", error="Provide a valid university email")
        password = request.form.get("password")
        if not password:
            return render_template("error.html", error="Provide a Password")
        confirmedpassword = request.form.get("confirmedpassword")
        if not confirmedpassword:
            return render_template("error.html", error="Confirm your password")
        return redirect("/")
    
    else:
        return render_template("register.html")

@app.route("/profile")
@login_required
def profile():
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)