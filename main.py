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

@app.route("/register", methods=["POST", "GET"])
def signup():

    if request.method == "POST":

        newUserProfilePicture = request.form["pfp"]

        newUserEmail = request.form["email"]

        newUserUsername = request.form["username"]

        newUserPassword = request.form["password"]

        newUserBirthday = request.form["birthday"]
        

        cursor = con.cursor()

        cursor.execute(f"INSERT INTO `users` (`pfp`, `email`, `username`, `password`, `birthday`) VALUES ('{newUserProfilePicture}', '{newUserEmail}', '{newUserUsername}', '{newUserPassword}', '{newUserBirthday}'")

        cursor.close()

        con.commit()

    return render_template ("signup.html.jinja")
