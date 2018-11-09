import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    #declare portfolios = shares and symbol from portfolio
    portfolios = db.execute("SELECT shares, symbol FROM portfolio WHERE id=:id", id=session["user_id"])

    #declare total
    total = 0

    #Get symbol, stock, shares and count totalprice and total and update price and total from portfolio
    for portfolio in portfolios:
        symbol = portfolio["symbol"]
        stock = lookup(symbol)
        shares = portfolio["shares"]
        totalprice = shares * stock["price"]
        total = total + totalprice
        db.execute("UPDATE portfolio SET price=:price, total=:total WHERE id=:id AND symbol=:symbol", price=usd(stock["price"]), total=usd(totalprice), id=session["user_id"], symbol=symbol)

    #declare cash from user
    cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])

    total = total + cash[0]["cash"]
    portfolio = db.execute("SELECT * from portfolio WHERE id=:id", id=session["user_id"])
    return render_template("index.html", stocks=portfolio, cash=usd(cash[0]["cash"]), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    #if request method is post
    if request.method == "POST":

        #declare stock lookup symbol
        stock = lookup(request.form.get("symbol"))

        #if stock is not valid, return apology
        if not stock:
            return apology("Invalid Symbol")

        #if no input in request form of shares, return apology
        if not request.form.get("shares"):
            return apology("Invalid Shares")

        #declare shares as the integer of the request form of shares
        shares = int(request.form.get("shares"))

        #if shares is not positive, return apology
        if shares < 0:
            return apology("positive numbers only")

        #declare cash from user as usercash
        usercash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])

        #if there is no usercash or if usercash is not enoug, return apology
        if not usercash or float(usercash[0]["cash"]) < stock["price"] * shares:
            return apology("Not enough money")

        #save informations in history
        db.execute("INSERT INTO history (symbol, shares, price, id) VALUES(:symbol, :shares, :price, :id)", \
                    symbol=stock["symbol"], shares=shares, price=usd(stock["price"]), id=session["user_id"])

        #update cash of user
        db.execute("UPDATE users SET cash = cash-:purchase WHERE id=:id", \
                    id=session["user_id"], purchase=stock["price"] * float(shares))

        #select shares from current user
        usershares = db.execute("SELECT shares FROM portfolio WHERE id=:id AND symbol=:symbol", \
                           id=session["user_id"], symbol=stock["symbol"])

        #if user has no shares of the recently bought symbol, then insert into portfolio
        if not usershares:
            db.execute("INSERT INTO portfolio (name, shares, price, total, symbol, id) VALUES(:name, :shares, :price, :total, :symbol, :id)", \
                        name=stock["name"], shares=shares, price=usd(stock["price"]), total=usd(shares * stock["price"]), symbol=stock["symbol"], id=session["user_id"])

        #if user already had shares of the recently bought symbol, then update to new amount of shares
        else:
            totalshares = usershares[0]["shares"] + shares
            db.execute("UPDATE portfolio SET shares=:shares WHERE id=:id AND symbol=:symbol", \
                        shares=totalshares, id=session["user_id"], symbol=stock["symbol"])

        #return to index.html
        return redirect(url_for("index"))

    #if request methode is get
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    #Get everything from history
    history = db.execute("SELECT * from history WHERE id=:id", id=session["user_id"])

    #render history.html with history information
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username=:username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":
        return render_template("quote.html")

    elif request.method == "POST":
        rows = lookup(request.form.get("symbol"))

        #if rows have no input, return apology
        if not rows:
            return apology("Invalid symbol")

        return render_template("quoted.html", stock=rows)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        if not request.form.get("username"):
            check = 1
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        #if password and passwordagain is not equal, return apology
        elif request.form.get("password") != request.form.get("passwordagain"):
            return apology("must provide password", 403)


        result = db.execute("INSERT INTO users (username,hash) VALUES(:username,:hash)", \
                username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        #if username is taken, return apology
        if not result:
            return apology("Username already taken")

        session["user_id"] = result

        return redirect(url_for("index"))

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        #declare stock lookup symbol
        stock = lookup(request.form.get("symbol"))

        #if no input in symbol, return apology
        if not stock:
            return apology("Invalid Symbol")

        if not request.form.get("shares"):
            return apology("Invalid Shares")

        #declare shares as the integer of the request form of shares
        shares = int(request.form.get("shares"))

        #if shares is not positive, return apology
        if shares < 0:
            return apology("positive numbers only")

        #declare shares from user as usershares
        usershares = db.execute("SELECT shares FROM portfolio WHERE id=:id AND symbol=:symbol", \
                                 id=session["user_id"], symbol=stock["symbol"])

        #if there is no usershares or if usershares are not enough, return apology
        if not usershares or int(usershares[0]["shares"]) < shares:
            return apology("Not enough shares")

        #save information in history
        db.execute("INSERT INTO history (symbol, shares, price, id) VALUES(:symbol, :shares, :price, :id)", \
                    symbol=stock["symbol"], shares=-shares, price=usd(stock["price"]), id=session["user_id"])

        #update users
        db.execute("UPDATE users SET cash=cash+:purchase WHERE id=:id", \
                    id=session["user_id"], purchase=stock["price"] * float(shares))

        #decrease usershares by sold shares
        totalshares = usershares[0]["shares"] - shares

        #if no shares left, delete record
        if totalshares == 0:
            db.execute("DELETE FROM portfolio WHERE id=:id AND symbol=:symbol", \
                        id=session["user_id"], symbol=stock["symbol"])
        #if still shares left, update record
        else:
            db.execute("UPDATE portfolio SET shares=:shares WHERE id=:id AND symbol=:symbol", \
                    shares=totalshares, id=session["user_id"], symbol=stock["symbol"])

        return redirect(url_for("index"))

    else:
        datasets = db.execute("SELECT symbol FROM portfolio WHERE id=:id", id=session["user_id"])
        return render_template("sell.html", symbols=datasets)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
