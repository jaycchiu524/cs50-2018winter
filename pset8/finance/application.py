import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
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

    # 1. SUM up all shares
    # 2. (GROUP) by symbols = stock["total_shares"]
    # 3. where total_shares > 0, avoid showing in portfolio when all sold
    stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM stocks WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])
    users = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])

    quotes = {}

    balance = users[0]["cash"]
    total = balance

    for stock in stocks:
        quotes[stock["symbol"]] = lookup(stock["symbol"])
        total = total + (quotes[stock["symbol"]]["price"] * stock["total_shares"])

    return render_template("index.html", stocks=stocks, quotes=quotes, balance=balance, total=total )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method =="POST":
        if not request.form.get("symbol"):
            flash("Please enter the symbol of the stock!")
            return render_template("buy.html")

        if not request.form.get("shares"):
            flash("Please enter the number of shares!")
            return render_template("buy.html")

        quote = lookup(request.form.get("symbol"))

        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])

        cash = rows[0]["cash"]
        price = quote["price"]

        total_price = price * int(request.form.get("shares"))

        db.execute("UPdate users SET cash = cash - :price WHERE id = :id", price=total_price, id = session["user_id"])
        db.execute("INSERT INTO stocks(user_id, symbol, price, shares) VALUES(:user_id, :symbol, :price, :shares)",
                                 user_id=session["user_id"],
                                 symbol=request.form.get("symbol"),
                                 price=total_price,
                                 shares=int(request.form.get("shares")))

        flash("Done!")

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    stocks = db.execute("SELECT symbol, price, time, date, shares FROM stocks WHERE user_id = :user_id",
                        user_id = session["user_id"])

    return render_template("history.html", stocks=stocks)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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

    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        if quote == None:
            return apology("Invalid symbol", 400)

        return render_template("quoted.html", name=quote["name"], symbol=quote["symbol"], price=quote["price"])

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        if not request.form.get("username"):
            flash("Please enter your username!")
            return render_template("register.html")

        elif not request.form.get("password"):
            flash("Please enter your password")
            return render_template("register.html")

        elif not request.form.get("confirmation"):
            flash("Please re-enter your password")
            return render_template("register.html")

        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Your re-entered your password incorrectly!")
            return render_template("register.html")

        # hash the password and insert a new user in the database
        hash = generate_password_hash(request.form.get("password"))
        new_user_id = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                                 username=request.form.get("username"), hash=hash)

        if not new_user_id:
            return apology("username taken", 400)

        # Remember which user has logged in
        session["user_id"] = new_user_id

        # Display a flash message
        flash("Registered!")

        # Redirect user to home page
        return render_template("/")

    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    if request.method == "POST":
        symbol_sold = request.form.get("symbol")
        shares_sold = int(request.form.get("shares"))

        stocks = db.execute("SELECT SUM(shares) as total_shares FROM stocks WHERE user_id = :user_id AND symbol = :symbol GROUP BY symbol",
                            user_id = session["user_id"], symbol = symbol_sold)


        if shares_sold > stocks[0]["total_shares"]:
            flash("Not enough shares")
            return render_template("sell.html")

        quotes = lookup(symbol_sold)
        total_price = shares_sold * quotes["price"]

        db.execute("UPdate users SET cash = cash + :price WHERE id = :id", price = total_price, id = session["user_id"])
        db.execute("INSERT INTO stocks(user_id, symbol, price, shares) VALUES(:user_id, :symbol, :price, :shares)",
                                                                        user_id = session["user_id"],
                                                                        symbol  = symbol_sold,
                                                                        price   = quotes["price"],
                                                                        shares  = -(shares_sold) )

        flash("Sold!")
        return redirect("/")

    else:

        stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM stocks WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
                                user_id = session["user_id"])
        return render_template("sell.html",stocks=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
