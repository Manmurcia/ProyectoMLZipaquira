from flask import Flask, render_template

import re
from datetime import datetime


app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, Flask!"


@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()

    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! Hour: " + str(now)
    return content

@app.route("/menu")
def menu():
    return render_template("Menu.html")

@app.route("/fase1")
def fase1():
    return render_template("Fase1.html")

@app.route("/fase2")
def fase2():
    return render_template("Fase2.html")

@app.route("/fase3")
def fase3():
    return render_template("Fase3.html")


