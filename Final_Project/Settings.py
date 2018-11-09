import os

from cs50 import SQL
from flask import Blueprint, Flask, flash, redirect, render_template, request, session, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES
from shutil import copyfile
from werkzeug.security import check_password_hash, generate_password_hash

from Formular import FormularParser

db = SQL("sqlite:///users.db")

settingsbp = Blueprint("settingsbp", __name__, template_folder='templates')

photos = UploadSet('photos', IMAGES)

class UserSettings(FormularParser):

    @settingsbp.route("/user", methods=["POST"])
    def SettingsFunction():
        Instanz = UserSettings()
        Instanz.getUserDatabaseContent()
        Instanz.getUserSettingsData()

        if Instanz.checkreset:
            UserSettings.resetUserDatabaseContent()
            return redirect(url_for("index"))
        elif Instanz.changelimitation:
            UserSettings.setLimitation()
            return redirect(url_for("user"))
        elif 'photo' in request.files:
            UserSettings.setProfilImg()
            return redirect(url_for("user"))
        elif Instanz.checkdelete:
            UserSettings.deleteUser()
            return redirect(url_for("register"))
        elif Instanz.changeusername:
            UserSettings.changeUsername()
            return render_template("user.html")
        elif Instanz.oldpassword and Instanz.newpassword and len(Instanz.newpassword) >= 8:
            UserSettings.changePassword()
            return redirect(url_for("login"))
        else:
            return render_template("user.html", reseterrormsg="Check Box!", imgerrormsg="Choose a picture!", limitationerrormsg="Enter limitation!", deleteerrormsg="Check Box!", usernameerrormsg="Enter new username!", passworderrormsg="Couldn´t change password!", stocks = Instanz.limitation)

    def setProfilImg():
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
        else:
            return render_template("user.html", errormsgimg = "Invalid Suffix!", stocks = Instanz.limitation)


    def setLimitation():
        db.execute("UPDATE user SET limitation=:limitation WHERE ID=:ID", ID=session["user_ID"], limitation=request.form.get("changelimitation"))

    def resetUserDatabaseContent():
        db.execute("DELETE FROM history WHERE ID=:ID",ID=session["user_ID"])
        db.execute("UPDATE user SET budget=0, income=0, expenditure=0 WHERE ID=:ID", ID=session["user_ID"])

    def deleteUser():
        db.execute("DELETE FROM user WHERE ID=:ID", ID=session["user_ID"])
        session.clear()

    def changeUsername():
        db.execute("UPDATE user SET username=:username WHERE ID=:ID", username = request.form.get("changeusername"), ID=session["user_ID"])
        rows = db.execute("SELECT * FROM user WHERE ID=:ID",ID=session["user_ID"])
        session["username"] = rows[0]["username"]

    def changePassword():
        rows = db.execute("SELECT * FROM user WHERE ID=:ID", ID=session["user_ID"])
        if check_password_hash(rows[0]["password"], request.form.get("oldpassword")):
            db.execute("UPDATE user SET password=:newpassword WHERE ID=:ID", ID=session["user_ID"], newpassword = generate_password_hash(request.form.get("newpassword")))
            session.clear()