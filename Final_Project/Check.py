from cs50 import SQL
from flask import Blueprint, Flask, flash, redirect, render_template, request, session, url_for

from Formular import FormularParser

db = SQL("sqlite:///users.db")

class FormularCheck(FormularParser):

    def checkLogin(self):
        Check = FormularCheck()
        Check.getLoginData()

        # Ensure username was submitted
        if not Check.email and not Check.password:
            self.check = 0

        # Ensure username was submitted
        elif not Check.email:
            self.check = 1

        # Ensure password was submitted
        elif not Check.password:
            self.check = 2

        else:
            self.check = None

    def checkRegister(self):
        Check = FormularCheck()
        Check.getRegisterData()

        #Ensure e-mail and password is given
        if not Check.email and not Check.password:
            self.check = 1

        elif not Check.username:
            self.check = 2

        #Ensure e-mail is given
        elif not Check.email:
            self.check = 3

        #Ensure password is given
        elif not Check.password:
            self.check = 4

        #if password and passwordagain is not equal, return apology
        elif Check.password != Check.passwordagain:
            self.check = 5

        #Ensure password is at least 8 characters long
        elif len(Check.password) < 8:
            self.check = 6

        else:
            self.check = None

    def checkTransaction(self):
        Check = FormularCheck()
        Check.getTransactionData()

        #Ensure everything is given
        if not Check.subject and not Check.inout:
            self.check = 4 #Please use the form below

        #Ensure subject is given
        elif not Check.subject:
            self.check = 0 #Please enter a subject

        #Ensure an income or expanditure is given
        elif not Check.inout:
            self.check = 1 #Please enter income or expenditure

        else:
            self.check = None
