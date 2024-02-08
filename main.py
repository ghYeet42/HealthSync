from flask import Flask, render_template, request, redirect, jsonify
import flask_login
import pymysql
import pymysql.cursors
from pprint import pprint as print
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

######

app = Flask(__name__)
auth = HTTPBasicAuth()

con = pymysql.connect (
    database = "cscarlett_healthsync",
    user = "cscarlett",
    password = "228941274",
    host = "10.100.33.60",
    cursorclass = pymysql.cursors.DictCursor
)

######

app.secret_key = "br3@D_y_-19!"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User:
     
     is_authenticated = True
     is_anonymous = False
     is_active = True

     def __init__(self, id, pfp, email, username):
          
          self.id = id
          self.pfp = pfp
          self.email = email
          self.username = username

     def get_id(self):
          
          return str(self.id)

######

@login_manager.user_loader 

def load_user(user_id):
     
    cursor = con.cursor()

    cursor.execute(f"(SELECT * FROM `users` WHERE `id` = {user_id}))")

    check = cursor.fetchone()

    cursor.close()

    con.commit()

    if check is None:
         
        return None
    
    return User(check["id"], check ["pfp"], check["email"], check["username"])
     
######

@app.route("/", methods=["POST", "GET"])
def index():
    
    if flask_login.current_user.is_authenticated:
         
        return redirect ("/feed")

    return render_template ("home.html.jinja")

    # return ("<p style=\"color:red;\">Hello!</p>")

######

@app.route("/register", methods=["POST", "GET"])
def signup():

    if request.method == "POST":

        newUserEmail = request.form["email"]

        newUserUsername = request.form["username"]

        newUserPassword = request.form["password"]

        newUserBirthday = request.form["birthday"]
        

        cursor = con.cursor()

        cursor.execute(f"INSERT INTO `users` ( `email`, `username`, `password`, `birthday`) VALUES ('{newUserEmail}', '{newUserUsername}', '{newUserPassword}', '{newUserBirthday}')")

        cursor.close()

        con.commit()

        return redirect("sigin.html.jinja")

    return render_template ("signup.html.jinja")

######

@app.route("/signin", methods=["POST", "GET"])
def signin():
        
        if request.method == "POST":
        
            userName = request.form["username"]

            userPassword = request.form["password"]

            cursor = con.cursor()
            
            cursor.execute(f"SELECT * FROM `users` WHERE `username` = '{userName}'")

            checker = cursor.fetchone()

            if checker is not None and userPassword == checker["password"]:
                 
                 user = load_user(checker["id"])

                 flask_login.login_user(user)

                 return redirect("/feed")

        return render_template("signin.html.jinja") 


        #if cursor.fetchone(f"SELECT `email`, `username`, `password` FROM `users`") ==  :
        #if cursor.execute(f"SELECT `email`, `username`, `password` FROM `users`") == :
        #return redirect("/feed")


@app.route('/feed')
@flask_login.login_required
def feed():
     
     return flask_login.current_user