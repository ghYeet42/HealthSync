from flask import Flask, render_template, request, redirect, jsonify
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

@app.route("/")
def index():

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

    return render_template ("signup.html.jinja")


@app.route("/signin", methods=["POST", "GET"])
def signin():
        
        if request.method == "POST":
        
            userName = request.form["username"]

            userPassword = request.form["password"]

            cursor = con.cursor()
            
            cursor.execute(f"SELECT * FROM `users` WHERE `username` = '{userName}'")

            checker = cursor.fetchone()

            if checker == userPassword["password"]:
                return redirect("/feed")
            else:
                print("Skill")

        return render_template("signin.html.jinja")


        #if cursor.fetchone(f"SELECT `email`, `username`, `password` FROM `users`") ==  :
        #if cursor.execute(f"SELECT `email`, `username`, `password` FROM `users`") == :

