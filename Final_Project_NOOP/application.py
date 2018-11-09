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


# Configure application
app = Flask(__name__)

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

@app.route("/")
@login_required
def index():

    #Show all infos for user on index
    history = db.execute("SELECT * FROM history WHERE ID=:ID ORDER BY date_time DESC LIMIT 10", ID=session["user_ID"])
    user = db.execute("SELECT * FROM user WHERE ID=:ID", ID=session["user_ID"])

    return render_template("index.html",rows=history, stocks=user)

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_ID
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure e-mail was submitted
        if not request.form.get("email") and not request.form.get("password"):
            return render_template("login.html", check = 0)

        # Ensure e-mail was submitted
        if not request.form.get("email"):
            return render_template("login.html", check = 1)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", check = 2)

        # Query database for e-mail
        rows = db.execute("SELECT * FROM user WHERE email=:email", email=request.form.get("email"))

        # Ensure e-mail exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return render_template("login.html", check = 3)

        #Remember user and user profil picture
        #Set session for user
        rows = db.execute("SELECT * FROM user WHERE email=:email", email=request.form.get("email"))
        session["user_ID"] = rows[0]["ID"]
        session["username"] = rows[0]["username"]
        session["imgname"] = rows[0]["imgname"]

        x = datetime.datetime.now()
        currentday= x.strftime("%-d")
        currentmonth = x.strftime("%-m")
        currentyear = x.strftime("%Y")

        nr = db.execute("SELECT COUNT(ID) FROM booking WHERE ID=:ID", ID=session["user_ID"])
        nr = nr[0]["COUNT(ID)"]
        for i in range(nr):
            schedule = db.execute("SELECT * FROM booking WHERE ID=:ID LIMIT 1", ID=session["user_ID"])
            booking_ID = schedule[0]["booking_ID"]
            year = schedule[0]["year"]
            month = schedule[0]["month"]
            day = schedule[0]["day"]
            if schedule:
                if (year < currentyear) or (year == currentyear and month < currentmonth) or (year == currentyear and month == currentmonth and day <= currentday):
                    subject = schedule[0]["subject"]
                    income = schedule[0]["income"]
                    expenditure = schedule[0]["expenditure"]
                    if income != 0:
                        db.execute("UPDATE user SET income=income+:income, budget=budget+:income WHERE ID=:ID", ID=session["user_ID"], income=income)
                        db.execute("INSERT INTO history (subject,income,ID) VALUES (:subject,:income,:ID)", subject=subject,income=income,ID=session["user_ID"])
                    elif expenditure != 0:
                        db.execute("UPDATE user SET expenditure=expenditure+:expenditure, budget=budget-:expenditure WHERE ID=:ID", ID=session["user_ID"], expenditure=expenditure)
                        db.execute("INSERT INTO history (subject,expenditure,ID) VALUES (:subject,:expenditure,:ID)", subject=subject,expenditure=expenditure,ID=session["user_ID"])
                    db.execute("DELETE FROM booking WHERE booking_ID=:booking_ID", booking_ID = booking_ID)

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():

    # Forget any user_ID
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        #Get data from db
        rows = db.execute("SELECT * FROM user WHERE email=:email", email=request.form.get("email"))

        #Ensure e-mail don't exists
        if len(rows) == 1:
            return render_template("register.html", check = 0)

        #Ensure e-mail and password is given
        elif not request.form.get("email") and not request.form.get("password"):
            return render_template("register.html", check = 1)

        elif not request.form.get("username"):
            return render_template("register.html", check = 2)

        #Ensure e-mail is given
        elif not request.form.get("email"):
            return render_template("register.html", check = 3)

        #Ensure password is given
        elif not request.form.get("password"):
            return render_template("register.html", check = 4)

        #if password and passwordagain is not equal, return apology
        elif request.form.get("password") != request.form.get("passwordagain"):
            return render_template("register.html", check = 5)

        #Ensure password is at least 8 characters long
        elif len(request.form.get("password")) < 8:
            return render_template("register.html", check = 6)

        #If everything is ok insert new user in db
        result = db.execute("INSERT INTO user (email,password,username) VALUES(:email,:password,:username)", \
                email=request.form.get("email"), password=generate_password_hash(request.form.get("password")), username=request.form.get("username"))

        #Set session for user
        rows = db.execute("SELECT * FROM user WHERE email=:email", email=request.form.get("email"))
        session["user_ID"] = rows[0]["ID"]
        session["username"] = rows[0]["username"]
        stringID = str(rows[0]["ID"])

        prevName = "static/img/defaultprofil.png"
        newName = "static/img/userimg/" + stringID +".png"
        imgname = stringID +".png"
        db.execute("UPDATE user SET imgname=:imgname WHERE ID=:ID",ID=session["user_ID"], imgname=imgname)
        copyfile(prevName, newName)

        rows = db.execute("SELECT imgname FROM user WHERE ID=:ID",ID=session["user_ID"])
        session["imgname"] = rows[0]["imgname"]

        return redirect(url_for("index"))

    else:
        return render_template("register.html")


@app.route("/contact")
def contact():

    return render_template("contact.html")

@app.route("/history")
@login_required
def history():

    #Get history from db for user
    history = db.execute("SELECT * FROM history WHERE ID=:ID ORDER BY date_time LIMIT 10", ID=session["user_ID"])

    return render_template("history.html", rows=history)


@app.route("/user", methods=["GET", "POST"])
@login_required
def user():

    if request.method == "POST":

        if request.form.get("checkreset"):
            #If checked delete history and money
            db.execute("DELETE FROM history WHERE ID=:ID",ID=session["user_ID"])
            db.execute("UPDATE user SET budget=0, income=0, expenditure=0 WHERE ID=:ID", ID=session["user_ID"])
            return redirect(url_for("index"))

        elif request.form.get("changelimitation"):
            db.execute("UPDATE user SET limitation=:limitation WHERE ID=:ID", ID=session["user_ID"], limitation=request.form.get("changelimitation"))
            return redirect(url_for("index"))

        elif 'photo' in request.files:
            rows = db.execute("SELECT * FROM user WHERE ID=:ID", ID=session["user_ID"])
            stringID = str(rows[0]["ID"])
            file = request.files['photo']
            dateiname = file.filename
            namesplit = dateiname.split(".")
            dateiendung = namesplit[1]
            if dateiendung.islower() == True:
                file.filename = stringID + "." + dateiendung
                filepath = "static/img/userimg/" + session["imgname"]
                if os.path.exists(filepath):
                    os.remove(filepath)
                filename = photos.save(file)
                db.execute("UPDATE user SET imgname=:imgname WHERE ID=:ID",ID=session["user_ID"], imgname=file.filename)
                rows = db.execute("SELECT * FROM user WHERE ID=:ID", ID=session["user_ID"])
                session["imgname"] = rows[0]["imgname"]
                return render_template("user.html")

        elif request.form.get("checkdelete"):
            db.execute("DELETE FROM user WHERE ID=:ID", ID=session["user_ID"])
            session.clear()
            return redirect(url_for("register"))

        elif request.form.get("oldpassword") and request.form.get("newpassword") and len(request.form.get("newpassword")) >= 8:
            rows = db.execute("SELECT * FROM user WHERE ID=:ID", ID=session["user_ID"])
            if check_password_hash(rows[0]["password"], request.form.get("oldpassword")):
                db.execute("UPDATE user SET password=:newpassword WHERE ID=:ID", ID=session["user_ID"], newpassword = generate_password_hash(request.form.get("newpassword")))
                session.clear()
                return redirect(url_for("login"))

        elif request.form.get("changeusername"):
            db.execute("UPDATE user SET username=:username WHERE ID=:ID", username = request.form.get("changeusername"), ID=session["user_ID"])
            rows = db.execute("SELECT * FROM user WHERE ID=:ID",ID=session["user_ID"])
            session["username"] = rows[0]["username"]
            return render_template("user.html")
        else:
            limitation = db.execute("SELECT * FROM user WHERE ID=:ID", ID=session["user_ID"])
            return render_template("user.html", reseterrormsg="Check Box!", imgerrormsg="Choose a picture!", limitationerrormsg="Enter limitation!", deleteerrormsg="Check Box!", passworderrormsg="Couldn´t change password", stocks = limitation)
    else:
        limitation = db.execute("SELECT * FROM user WHERE ID=:ID", ID=session["user_ID"])
        return render_template("user.html",reseterrormsg="Use with caution!", stocks=limitation)

@app.route("/transaction", methods=["GET", "POST"])
@login_required
def transaction():

    if request.method == "POST":

        #Ensure everything is given
        if not request.form.get("subject") and not request.form.get("inout"):
            return render_template("transaction.html", check = 4) #Please use the form below

        #Ensure subject is given
        if not request.form.get("subject"):
            return render_template("transaction.html", check = 0) #Please enter a subject

        #Ensure an income or expanditure is given
        if not request.form.get("inout"):
            return render_template("transaction.html", check = 1) #Please enter income or expenditure

        money = request.form.get("inout", type=int)
        #Updates income
        if money > 0:
            #Get subject input from user
            subject = request.form.get("subject")
            #Update user profil in db
            db.execute("UPDATE user SET income=income+:newincome, budget=budget+:newincome WHERE ID=:ID", ID=session["user_ID"], newincome=money)
            #Insert new transaction in history
            db.execute("INSERT INTO history (subject,income,ID) VALUES (:subject,:income,:ID)", subject=subject,income=money,ID=session["user_ID"])
            return redirect(url_for("index"))

        #Updates expanditure
        if money < 0:
            money = money * (-1)
            #Get current budget from user
            rows = db.execute("SELECT * FROM user WHERE ID=:ID", ID=session["user_ID"])
            budget = rows[0]["budget"]
            #Ensure user doesn't overdraft
            if budget-money < rows[0]["limitation"]:
                return render_template("transaction.html",check = 3)

            #Get subject input from user
            subject = request.form.get("subject")
            #Update user profil in db
            db.execute("UPDATE user SET expenditure=expenditure+:newexpenditure, budget=budget-:newexpenditure WHERE ID=:ID", ID=session["user_ID"], newexpenditure=money)
            #Insert new transaction in history
            db.execute("INSERT INTO history (subject,expenditure,ID) VALUES (:subject,:expenditure,:ID)", subject=subject,expenditure=money,ID=session["user_ID"])
            return redirect(url_for("index"))
    else:
        return render_template("transaction.html")

@app.route("/booking", methods=["GET", "POST"])
@login_required
def booking():
    x = datetime.datetime.now()
    currentyear = x.year
    currentmonth = x.month
    currentday = x.day
    if request.method == "POST":
        if request.form.get("day") and request.form.get("month") and request.form.get("year") and request.form.get("inout") and request.form.get("subject"):
            day = request.form.get('day', type=int)
            month = request.form.get('month', type=int)
            year = request.form.get('year', type=int)
            money = request.form.get("inout", type=int)
            subject = request.form.get("subject")

            if (year == currentyear and month == currentmonth and day >= currentday) or (year == currentyear and month > currentmonth and day <= 31 and day >= 1) or (year > currentyear and month >= 1 and month <= 12 and day >= 1 and day <= 31):
                if money > 0:
                    db.execute("INSERT INTO booking (day, month, year, income, subject, ID) VALUES (:day, :month, :year, :income, :subject, :ID)", ID=session["user_ID"], day=day, month = month, year=year, income=money, subject=subject)
                    return redirect(url_for("booking"))
                elif money < 0:
                    money = money * (-1)
                    db.execute("INSERT INTO booking (day, month, year, expenditure, subject, ID) VALUES (:day, :month, :year, :expenditure, :subject, :ID)", ID=session["user_ID"], day=day, month = month, year=year, expenditure=money, subject=subject)
                    return redirect(url_for("booking"))
            else:
                return render_template("booking.html", check = 1)
        else:
            return render_template("booking.html", check = 0)
    else:
        return render_template("booking.html", currentyear = currentyear)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)

# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)