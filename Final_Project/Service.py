from cs50 import SQL
from flask import Blueprint, Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from shutil import copyfile

from Formular import FormularParser
from Transactions import UserTransactions
from Check import FormularCheck

db = SQL("sqlite:///users.db")

servicebp = Blueprint("servicebp", __name__, template_folder='templates')

class UserService(UserTransactions, FormularCheck):

    @servicebp.route("/login", methods=["POST"])
    def login():
        Instanz = UserService()
        Instanz.getLoginData()
        Instanz.checkLogin()

        if not Instanz.check == None:
            return render_template("login.html",check=Instanz.check)

        # Query database for username
        rows = db.execute("SELECT password,ID,username,imgname FROM user WHERE email=:email", email=Instanz.email)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], Instanz.password):
            return render_template("login.html", check = 3)

        #user session
        session["user_ID"] = rows[0]["ID"]
        session["username"] = rows[0]["username"]
        session["imgname"] = rows[0]["imgname"]

        UserTransactions().booking()

        return redirect(url_for("index"))

    @servicebp.route("/register", methods=["POST"])
    def register():
        Instanz = UserService()
        Instanz.getRegisterData()
        Instanz.checkRegister()

        if not Instanz.check == None:
            return render_template("register.html",check=Instanz.check)

        #Get data from db
        rows = db.execute("SELECT * FROM user WHERE email=:email", email=Instanz.email)

        #Ensure e-mail don't exists
        if len(rows) == 1:
            return render_template("register.html", check = 0)

        #If everything is ok insert new user in db
        result = db.execute("INSERT INTO user (email,password,username) VALUES(:email,:password,:username)", \
                email=Instanz.email, password=generate_password_hash(Instanz.password), username=Instanz.username)

        rows = db.execute("SELECT * FROM user WHERE email=:email", email=Instanz.email)

        #Set session for user
        session["user_ID"] = rows[0]["ID"]
        session["username"] = rows[0]["username"]
        stringID = str(rows[0]["ID"])

        UserService.getDefaultProfilImg(stringID)

        return redirect(url_for("index"))


    def getDefaultProfilImg(stringID):
        prevName = "static/img/defaultprofil.png"
        newName = "static/img/userimg/" + stringID +".png"
        imgname = stringID +".png"
        db.execute("UPDATE user SET imgname=:imgname WHERE ID=:ID",ID=session["user_ID"], imgname=imgname)
        copyfile(prevName, newName)

        rows = db.execute("SELECT imgname FROM user WHERE ID=:ID",ID=session["user_ID"])
        session["imgname"] = rows[0]["imgname"]
