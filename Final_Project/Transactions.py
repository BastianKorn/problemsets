import datetime
from cs50 import SQL
from flask import Blueprint, Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, eur

from Formular import FormularParser
from Check import FormularCheck

db = SQL("sqlite:///users.db")

transactionsbp = Blueprint("transactionsbp", __name__)

class UserTransactions(FormularCheck):

    @transactionsbp.route("/transaction",methods=["POST"])
    @login_required
    def transaction():
        transactionData = UserTransactions()
        transactionData.getTransactionData()
        transactionData.checkTransaction()

        if not transactionData.check == None:
            return render_template("transaction.html",check=transactionData.check)

        money = transactionData.money
        #Updates income
        if money > 0:
            #Get subject input from user
            subject = transactionData.subject
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
            subject = transactionData.subject
            #Update user profil in db
            db.execute("UPDATE user SET expenditure=expenditure+:newexpenditure, budget=budget-:newexpenditure WHERE ID=:ID", ID=session["user_ID"], newexpenditure=money)
            #Insert new transaction in history
            db.execute("INSERT INTO history (subject,expenditure,ID) VALUES (:subject,:expenditure,:ID)", subject=subject,expenditure=money,ID=session["user_ID"])
            return redirect(url_for("index"))

    @transactionsbp.route("/booking",methods=["POST"])
    @login_required
    def setBooking():
        bookingData = UserTransactions()
        bookingData.getBookingData()

        if bookingData.day and bookingData.month and bookingData.year and bookingData.money and bookingData.subject:
            if (bookingData.year == bookingData.currentyear and bookingData.month == bookingData.currentmonth and bookingData.day >= bookingData.currentday) or (bookingData.year == bookingData.currentyear and bookingData.month > bookingData.currentmonth and bookingData.day <= 31 and bookingData.day >= 1) or (bookingData.year > bookingData.currentyear and bookingData.month >= 1 and bookingData.month <= 12 and bookingData.day >= 1 and bookingData.day <= 31):
                if bookingData.money > 0:
                    db.execute("INSERT INTO booking (day, month, year, income, subject, ID) VALUES (:day, :month, :year, :income, :subject, :ID)", ID=session["user_ID"], day=bookingData.day, month = bookingData.month, year=bookingData.year, income=bookingData.money, subject=bookingData.subject)
                    return redirect(url_for("booking"))
                elif bookingData.money < 0:
                    money = bookingData.money * (-1)
                    db.execute("INSERT INTO booking (day, month, year, expenditure, subject, ID) VALUES (:day, :month, :year, :expenditure, :subject, :ID)", ID=session["user_ID"], day=bookingData.day, month = bookingData.month, year=bookingData.year, expenditure=money, subject=bookingData.subject)
                    return redirect(url_for("booking"))
            else:
                return render_template("booking.html", check = 1, currentyear = bookingData.currentyear)
        else:
            return render_template("booking.html", check = 0, currentyear = bookingData.currentyear)

    def booking(self):
        bookingData = UserTransactions()
        bookingData.getBookingData()

        nr = db.execute("SELECT COUNT(ID) FROM booking WHERE ID=:ID", ID=session["user_ID"])
        nr = nr[0]["COUNT(ID)"]
        for i in range(nr):
            schedule = db.execute("SELECT * FROM booking WHERE ID=:ID LIMIT 1", ID=session["user_ID"])
            booking_ID = schedule[0]["booking_ID"]
            year = schedule[0]["year"]
            month = schedule[0]["month"]
            day = schedule[0]["day"]
            if schedule:
                if (year < bookingData.strcurrentyear) or (year == bookingData.strcurrentyear and month < bookingData.strcurrentmonth) or (year == bookingData.strcurrentyear and month == bookingData.strcurrentmonth and day <= bookingData.strcurrentday):
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
