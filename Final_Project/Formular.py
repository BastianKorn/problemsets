from cs50 import SQL
from flask import Blueprint, Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

db = SQL("sqlite:///users.db")

class FormularParser:

    def getLoginData(self):
        self.email = request.form.get("email")
        self.password = request.form.get("password")

    def getRegisterData(self):
        self.email = request.form.get("email")
        self.password = request.form.get("password")
        self.username = request.form.get("username")
        self.passwordagain = request.form.get("passwordagain")

    def getUserDatabaseContent(self):
        #Show all infos for user on index
        self.history = db.execute("SELECT * FROM history WHERE ID=:ID ORDER BY date_time", ID=session["user_ID"])
        self.user = db.execute("SELECT * FROM user WHERE ID=:ID", ID=session["user_ID"])
        self.limitation = db.execute("SELECT * FROM user WHERE ID=:ID", ID=session["user_ID"])
        self.recenthistory = db.execute("SELECT * FROM history WHERE ID=:ID ORDER BY date_time DESC LIMIT 10", ID=session["user_ID"])

    def getTransactionData(self):
        self.inout = request.form.get("inout")
        self.money = request.form.get("inout",type=int)
        self.subject = request.form.get("subject")

    def getBookingData(self):
        self.day = request.form.get("day",type=int)
        self.month = request.form.get("month",type=int)
        self.year = request.form.get("year",type=int)
        self.money = request.form.get("inout",type=int)
        self.subject = request.form.get("subject")
        x = datetime.datetime.now()
        self.currentyear = x.year
        self.currentmonth = x.month
        self.currentday = x.day
        self.strcurrentday= x.strftime("%-d")
        self.strcurrentmonth = x.strftime("%-m")
        self.strcurrentyear = x.strftime("%Y")

    def getUserSettingsData(self):
        self.checkreset = request.form.get("checkreset")
        self.changelimitation = request.form.get("changelimitation")
        self.checkdelete = request.form.get("checkdelete")
        self.oldpassword = request.form.get("oldpassword")
        self.newpassword = request.form.get("newpassword")
        self.changeusername = request.form.get("changeusername")
