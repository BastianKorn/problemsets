import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, eur
from flask_uploads import UploadSet, configure_uploads, IMAGES
from shutil import copyfile

import Service
import Settings
import Formular
import Transactions
from Formular import FormularParser
from Settings import UserSettings
from Service import UserService
from Transactions import UserTransactions

# Configure application
app = Flask(__name__)

app.register_blueprint(Service.servicebp)
app.register_blueprint(Settings.settingsbp)
app.register_blueprint(Transactions.transactionsbp)

photos = UploadSet('photos', IMAGES)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOADED_PHOTOS_DEST'] = "static/img/userimg"
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

configure_uploads(app, photos)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalIDate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#Filter to format into Euro €
app.jinja_env.filters["eur"] = eur

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")

@app.route("/", methods=["POST", "GET"])
@login_required
def index():
    if request.method == "POST":
        UserTransactions().deleteLastTransaction()
    Instanz = FormularParser()
    Instanz.getUserDatabaseContent()
    return render_template("index.html",rows=Instanz.recenthistory, stocks=Instanz.user)

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        UserService().login()
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        UserService().register()
    else:
        return render_template("register.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/history")
@login_required
def history():
    #Get history from db for user
    Instanz = FormularParser()
    Instanz.getUserDatabaseContent()
    return render_template("history.html", rows=Instanz.history)


@app.route("/user", methods=["GET", "POST"])
@login_required
def user():
    if request.method == "POST":
        UserSettings().SettingsFunction()
    else:
        limitation = db.execute("SELECT * FROM user WHERE ID=:ID", ID=session["user_ID"])
        return render_template("user.html", stocks=limitation)

@app.route("/transaction", methods=["GET", "POST"])
@login_required
def transaction():
    if request.method == "POST":
        UserTransactions().transaction()
    else:
        return render_template("transaction.html")

@app.route("/booking", methods=["GET", "POST"])
@login_required
def booking():
    Instanz = FormularParser()
    Instanz.getBookingData()
    if request.method == "POST":
        UserTransactions().setBooking()
    else:
        return render_template("booking.html", currentyear = Instanz.currentyear)

def errorhandler(e):
    return apology(e.name, e.code)

# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
