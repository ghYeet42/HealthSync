from flask import Flask, render_template, request, redirect, jsonify
import pymysql
import pymysql.cursors
from pprint import pprint as print
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

######

app = Flask(__name__)
auth = HTTPBasicAuth()

######

@app.route("/")
def index():

    return render_template ("home.html.jinja")

    # return ("<p style=\"color:red;\">Hello!</p>")