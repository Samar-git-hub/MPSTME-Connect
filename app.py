import os
from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from flask_mail import Mail, Message
from helper import login_required, verification_required, verify_required
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
import random
import mysql.connector as sql
from instance.hashing import hashing
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__, instance_relative_config=True)

mysql_password = os.getenv('MY_SQL_SERVER_PASSWORD')
conn = sql.connect(host = "localhost", user = "root", password = mysql_password, database="mpstme_connect")
c1 = conn.cursor()

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)


app.config['UPLOAD_FOLDER'] = 'instance/user_pics'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def validfile(filename):
    if '.' in filename:
        extension = filename.rsplit('.')[1].lower()
        # rsplit is the same as normal split, just splitting from the first right '.' instead of left
        if extension in ALLOWED_EXTENSIONS:
            return True
    return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear() # clear any previous sessions

    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            return render_template("error.html", error="Provide a valid university email")
        password = request.form.get("password")
        if not password:
            return render_template("error.html", error="Provide a Password")
        
        c1.execute("SELECT * FROM user_auth WHERE email = (%s)", (email, ))
        emails = c1.fetchall()
        if len(emails) != 1:
            return render_template("error.html", error="This email has not been registered! WOOOOOOOOOOOOOOOOOOw wowow")
        
        c1.execute("SELECT password FROM user_auth WHERE email = (%s)", (email, ))
        dbpassword = c1.fetchone()[0] # first element of the returned tuple 
        # (fetchone returns a tuple, fetchall returns a list of tuples)
        c1.execute("SELECT salt FROM user_auth WHERE email = (%s)", (email, ))
        salt = c1.fetchone()[0]
        checkpassword = salt+password
        if not check_password_hash(dbpassword, checkpassword):
            return render_template("error.html", error="Enter valid password")
        
        session["user_id"] = email

        return redirect("/")
    
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email").lower()
        if not email:
            return render_template("error.html", error="Provide a valid university email")
        if not email.endswith("@nmims.in"): 
            return render_template("error.html", error="Provide a valid university email")
        c1.execute("SELECT * FROM user_auth WHERE email = (%s)", (email,))
        rows = c1.fetchall()
        if len(rows) != 0:
            return render_template("error.html", error="Email has already been registered")
        verification_code = random.randint(100000, 999999)
        session['email'] = email
        session['verification_code'] = verification_code
        msg = Message('MPSTME Connect: Verify your email', recipients=[email])
        msg.body = f"""
        Hey, this is a mail from MPSTME Connect.
        
        Thank you for signing up! 
        
        Here is your verification code: {verification_code}
        
        Please enter this code in the app to complete your registration.
        
        Regards,
        MPSTME Connect Team
        """
        mail.send(msg)
        return redirect("/verify")
    
    else:
        return render_template("register.html")

@app.route("/verify", methods=["GET", "POST"])
@verification_required
def verify():
    if request.method == "POST":
        enteredverification = request.form.get("verification")
        if not enteredverification:
            return render_template("error.html", error="Enter verification code")
        
        storedverification = session["verification_code"]

        if not enteredverification == str(storedverification):
            return render_template("error.html", error="Verification code does not match")
        else:
            session["valid"] = "valid"
            return redirect("/signup")
    return render_template("verify.html")  

@app.route("/signup", methods=["GET", "POST"])
@verification_required
@verify_required
def signup():
    if request.method == "POST":
        email = request.form.get("email").lower()
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
        if password != confirmedpassword:
            return render_template("error.html", error="Confirmation password must match the password!")
        c1.execute("SELECT * FROM user_auth WHERE email = (%s)", (email,))
        rows = c1.fetchall()
        if rows:  
            return render_template("error.html", error="Email has already been registered")
        # try again button error handling

        hash, salt = hashing(password)

        c1.execute("INSERT INTO user_auth (email, password, salt) VALUES (%s, %s, %s)", (email, hash, salt))
        conn.commit()
        return redirect("/login")
    else:
        return render_template("signup.html")

@app.route("/profile")
@login_required
def profile():
    email = session["user_id"]
    username = email.split('@')[0]
    namelist = username.split(".")
    first = namelist[0]
    second = namelist[1]
    last = ""
    for i in second:
        if i.isalpha():
            last += i
    
    c1.execute("SELECT id FROM user_auth WHERE email = %s", (session["user_id"],))
    user_id = c1.fetchone()[0]
    sessionid = user_id
    
    c1.execute("SELECT profile_pic FROM users WHERE user_id = %s", (sessionid,))
    profile_picture_tuple = c1.fetchone()

    if profile_picture_tuple:
        profile_picture = profile_picture_tuple[0]
    else:
        profile_picture = None
    # have to do the number of endorsements and academic description logic from the database (make another table)
    return render_template("profile.html", profile_picture=profile_picture, first=first.capitalize(), last=last.capitalize(), number = 5, academic = "wow")

@app.route("/details", methods=["GET", "POST"])
@login_required
def details():
    if request.method == 'POST':

        if 'profile_picture' not in request.files:
            return render_template("error.html", error="No File")        
        
        file = request.files['profile_picture']
        if file.filename == '':
            return render_template("error.html", error="No File Selected")
        
        
        return redirect('/profile')
    
    else:

        c1.execute("SELECT id FROM user_auth WHERE email = %s", (session["user_id"],))
        user_id = c1.fetchone()[0]
        sessionid = user_id

        # taking id from the user_auth table, which is there used as a foreign key to get the values in other tables as user_id

        c1.execute("SELECT profile_pic, bio, skills, interests, softskills FROM users WHERE user_id = %s", (sessionid,))
        user_data = c1.fetchone()

        c1.execute("SELECT academic_detail_1, academic_detail_2, academic_detail_3 FROM user_academics WHERE user_id = %s", (sessionid,))
        academic_details = c1.fetchone()  

        c1.execute("SELECT project_1, project_2, project_3 FROM user_projects WHERE user_id = %s", (sessionid,))
        projects = c1.fetchone() 

        c1.execute("SELECT github, linkedin, instagram FROM user_links WHERE user_id = %s", (sessionid,))
        links = c1.fetchone()

        c1.execute("SELECT achievement_1, achievement_2, achievement_3 FROM user_achievements WHERE user_id = %s", (sessionid,))
        achievements = c1.fetchone()

        if user_data is None:

             user_data_dict = {
                'profile_pic': '/static/black-white-logo.png',
                'bio': '',
                'skills': '',
                'interests': '',
                'softskills': ''
            }

        else:

            user_data_dict = {
                'profile_pic': user_data[0],
                'bio': user_data[1],
                'skills': user_data[2],
                'interests': user_data[3],
                'softskills': user_data[4]
            }
        
        if academic_details is None:

            academic_details_dict = {
                'detail_1': '',
                'detail_2': '',
                'detail_3': ''
            }

        else:

            academic_details_dict = {
                'detail_1': academic_details[0],
                'detail_2': academic_details[1],
                'detail_3': academic_details[2]
            }
        
        if projects is None:

            projects_dict = {
                'project_1': '',
                'project_2': '',
                'project_3': ''
            }

        else:

            projects_dict = {
                'project_1': projects[0],
                'project_2': projects[1],
                'project_3': projects[2]
            }

        if links is None:

            links_dict = {
                'github': '',
                'linkedin': '',
                'instagram': ''
            }

        else:

            links_dict = {
                'github': links[0],
                'linkedin': links[1],
                'instagram': links[2]
            }

        if achievements is None:

            achievements_dict = {
                'achievement_1': '',
                'achievement_2': '',
                'achievement_3': ''
            }

        else:

            achievements_dict = {
                'achievement_1': achievements[0],
                'achievement_2': achievements[1],
                'achievement_3': achievements[2]
            }


        return render_template("details.html", user=user_data_dict, academics=academic_details_dict, projects=projects_dict,
                                links=links_dict, achievements=achievements_dict)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)