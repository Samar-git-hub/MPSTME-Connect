import os
from flask import Flask, redirect, render_template, request, session, flash, jsonify, send_from_directory
from flask_session import Session
from flask_mail import Mail, Message
from helper import login_required, verification_required, verify_required
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
import random
import mysql.connector as sql
from instance.hashing import hashing
from werkzeug.utils import secure_filename
import requests

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

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

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
    # splitting the email into 2 parts and capitalizing so that its displayed as a complete name in the profile template
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
    
    c1.execute("SELECT profile_pic, bio, skills, interests, softskills, endorsements FROM users WHERE user_id = %s", (sessionid,))
    user_data = c1.fetchone()
    c1.fetchall()  # Consume any remaining results

    c1.execute("SELECT academic_detail_1, academic_detail_2, academic_detail_3 FROM user_academics WHERE user_id = %s", (sessionid,))
    academic_details = c1.fetchone()
    c1.fetchall()  # Consume any remaining results

    c1.execute("SELECT project_1, project_2, project_3 FROM user_projects WHERE user_id = %s", (sessionid,))
    projects = c1.fetchone()
    c1.fetchall()  # Consume any remaining results

    c1.execute("SELECT github, linkedin, instagram FROM user_links WHERE user_id = %s", (sessionid,))
    links = c1.fetchone()
    c1.fetchall()  # Consume any remaining results

    c1.execute("SELECT achievement_1, achievement_2, achievement_3 FROM user_achievements WHERE user_id = %s", (sessionid,))
    achievements = c1.fetchone()
    c1.fetchall()  # Consume any remaining results

    if user_data is None:

            user_data_dict = {
            'profile_pic': '/static/black-white-logo.png',
            'bio': '',
            'skills': '',
            'interests': '',
            'softskills': '',
            'endorsements': '0'
        }

    else:

        user_data_dict = {
            'profile_pic': user_data[0],
            'bio': user_data[1],
            'skills': user_data[2],
            'interests': user_data[3],
            'softskills': user_data[4],
            'endorsements': user_data[5]
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

    return render_template("profile.html", first = first.capitalize(), last = last.capitalize(), user=user_data_dict, academics=academic_details_dict, projects=projects_dict, links=links_dict, achievements=achievements_dict)



@app.route("/details", methods=["GET", "POST"])
@login_required
def details():
    if request.method == 'POST':
        c1.execute("SELECT id FROM user_auth WHERE email = %s", (session["user_id"],)) 
        # session["user_id"] is the email used to identify the current user, session id is the id associated with that user in the database
        user_id = c1.fetchone()[0]
        sessionid = user_id

        # Getting data from all fields, except the profile picture field, as will handle that separately
        bio = request.form.get('bio')
        skills = request.form.get('skills')
        interests = request.form.get('interests')
        softskills = request.form.get('softskills')
        academic_detail_1 = request.form.get('academics-1')
        academic_detail_2 = request.form.get('academics-2')
        academic_detail_3 = request.form.get('academics-3')
        project_1 = request.form.get('projects-1')
        project_2 = request.form.get('projects-2')
        project_3 = request.form.get('projects-3')
        github = request.form.get('links-1')
        linkedin = request.form.get('links-2')
        instagram = request.form.get('links-3')
        achievement_1 = request.form.get('achievements-1')
        achievement_2 = request.form.get('achievements-2')
        achievement_3 = request.form.get('achievements-3')

        c1.execute("""
            INSERT INTO users (user_id, bio, skills, interests, softskills)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                bio = VALUES(bio), skills = VALUES(skills), interests = VALUES(interests), softskills = VALUES(softskills)
            """, (sessionid, bio, skills, interests, softskills))

        c1.execute("""
            INSERT INTO user_academics (user_id, academic_detail_1, academic_detail_2, academic_detail_3)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                academic_detail_1 = VALUES(academic_detail_1),
                academic_detail_2 = VALUES(academic_detail_2),
                academic_detail_3 = VALUES(academic_detail_3)
            """, (sessionid, academic_detail_1, academic_detail_2, academic_detail_3))


        c1.execute("""
            INSERT INTO user_projects (user_id, project_1, project_2, project_3)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                project_1 = VALUES(project_1), project_2 = VALUES(project_2), project_3 = VALUES(project_3)
            """, (sessionid, project_1, project_2, project_3))


        c1.execute("""
            INSERT INTO user_links (user_id, github, linkedin, instagram)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                github = VALUES(github), linkedin = VALUES(linkedin), instagram = VALUES(instagram)
            """, (sessionid, github, linkedin, instagram))


        c1.execute("""
            INSERT INTO user_achievements (user_id, achievement_1, achievement_2, achievement_3)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                achievement_1 = VALUES(achievement_1), achievement_2 = VALUES(achievement_2), achievement_3 = VALUES(achievement_3)
            """, (sessionid, achievement_1, achievement_2, achievement_3))

        # profile picture part
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and validfile(file.filename):

                email = session["user_id"]
                username = email.split('@')[0]
                namelist = username.split(".")
                first = namelist[0]
                second = namelist[1]
                last = ""
                for i in second:
                    if i.isalpha():
                        last += i
                        
                filename = f"{first}_{last}_profilepic.{file.filename.rsplit('.',1)[1].lower()}" 
                dbpath = f"/user-pics/{filename}" 
                # path in the browser, basically like a normal get request to display a favicon or a normal picture, I am making a url which can then have a get request

                # this is an absolute path in the device (not in the database)
                upload_folder = os.path.join(app.instance_path, 'user-pics')
                os.makedirs(upload_folder, exist_ok=True) # makes the upload folder if it doesnt already exist

                file.save(os.path.join(upload_folder, filename)) # saves file to the directory, with a new path

                c1.execute("""
                    INSERT INTO users (user_id, profile_pic)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE
                        profile_pic = VALUES(profile_pic)
                """, (sessionid, dbpath))

        conn.commit()

        return redirect("/details")
    
    else:
        c1.execute("SELECT id FROM user_auth WHERE email = %s", (session["user_id"],))
        user_id = c1.fetchone()[0]
        sessionid = user_id

        # Fetch user data
        c1.execute("SELECT profile_pic, bio, skills, interests, softskills FROM users WHERE user_id = %s", (sessionid,))
        user_data = c1.fetchone()
        c1.fetchall()  

        c1.execute("SELECT academic_detail_1, academic_detail_2, academic_detail_3 FROM user_academics WHERE user_id = %s", (sessionid,))
        academic_details = c1.fetchone()
        c1.fetchall()  

        c1.execute("SELECT project_1, project_2, project_3 FROM user_projects WHERE user_id = %s", (sessionid,))
        projects = c1.fetchone()
        c1.fetchall() 

        c1.execute("SELECT github, linkedin, instagram FROM user_links WHERE user_id = %s", (sessionid,))
        links = c1.fetchone()
        c1.fetchall()  

        c1.execute("SELECT achievement_1, achievement_2, achievement_3 FROM user_achievements WHERE user_id = %s", (sessionid,))
        achievements = c1.fetchone()
        c1.fetchall() 


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
    
@app.route('/search')
@login_required
def search():
    
    return render_template('search.html')

@app.route('/user-pics/<filename>') # crazy stuff, src in html is actually a get request end point
def serve_image(filename):
    return send_from_directory(app.instance_path + '/user-pics', filename)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

