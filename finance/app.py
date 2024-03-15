import os

from datetime import datetime
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    purchases = db.execute("SELECT symbol, SUM(shares) FROM purchases WHERE user_id = ? GROUP BY symbol", user_id)
    for purchase in purchases:
        purchase["current_price"] = lookup(purchase["symbol"])["price"]

    cash_rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_rows[0]["cash"]
    total = cash
    for purchase in purchases:
        total += purchase["current_price"] * purchase["SUM(shares)"]

    return render_template("index.html", purchases=purchases, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        dict = lookup(request.form.get("symbol"))
        if dict is None:
            return apology("invalid symbol", 400)
        elif not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        elif not request.form.get("shares") or not request.form.get("shares").isdigit():
            return apology("missing or invalid shares", 400)
        elif int(request.form.get("shares")) <= 0:
            return apology("must be positive", 400)
        else:
            current_price = dict['price']
            symbol = dict['symbol']
            shares = int(request.form.get("shares"))
            user_id = session["user_id"]
            cash_rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
            cash = cash_rows[0]["cash"]
            total_cost = current_price * shares

            if cash < total_cost:
                return apology("insufficient funds", 400)
            new_cash_balance = cash - total_cost
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash_balance, user_id)
            db.execute("INSERT INTO purchases (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",
                       user_id, symbol, shares, total_cost, datetime.now())
            return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    purchases = db.execute("SELECT * FROM purchases WHERE user_id = ? ORDER BY timestamp DESC", user_id)
    sells = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC", user_id)
    for sell in sells:
        sell["shares"] = -sell["shares"]
    transactions = purchases + sells
    transactions.sort(key=lambda x: x["timestamp"], reverse=True)
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        dict = lookup(request.form.get("symbol"))
        if dict is None:
            return apology("invalid symbol", 400)
        else:
            return render_template("quoted.html", dict=dict)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)
        elif not any(char.isalpha() for char in request.form.get("password")) or not any(char.isdigit() for char in request.form.get("password")) or not any(char in "!@#$%^&*()_+-=[]{}|;:'\"<>,.?/~`" for char in request.form.get("password")):
            return apology("password must contain letters, numbers, and symbols", 400)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) > 0:
            return apology("username already exists", 400)

        hashed_password = generate_password_hash(request.form.get("password"))

        username = request.form.get("username")
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)

        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]
        session["user_id"] = user_id

        return redirect("/")

    else:
        return render_template('register.html')


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        desired_shares = request.form.get("shares")

        if not symbol:
            return apology("invalid symbol", 400)
        elif desired_shares == "" or not request.form.get("shares").isdigit():
            return apology("invalid or missing shares", 400)
        else:
            desired_shares = int(request.form.get("shares"))

        if desired_shares <= 0:
            return apology("shares must be positive", 400)

        purchases = db.execute(
            "SELECT id, shares FROM purchases WHERE user_id = ? AND symbol = ? ORDER BY timestamp ASC", user_id, symbol)

        total_user_shares = sum(purchase["shares"] for purchase in purchases)

        if desired_shares > total_user_shares:
            return apology("not enough shares")
        
        dict = lookup(symbol)
        current_price = dict["price"]
        total = current_price * desired_shares

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total, user_id)

        remaining = desired_shares

        for purchase in purchases:
            if remaining <= 0:
                break

            shares_left = min(purchase["shares"], remaining)
            remaining -= shares_left

            db.execute("UPDATE purchases SET shares = ? WHERE id = ?", purchase["shares"] - shares_left, purchase["id"])

        if remaining == 0:
            db.execute("DELETE FROM purchases WHERE user_id = ? AND symbol = ? AND shares = 0", user_id, symbol)

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",
                   user_id, symbol, desired_shares, current_price, datetime.now())

        return redirect("/")

    else:
        purchases = db.execute("SELECT DISTINCT symbol FROM purchases WHERE user_id = ?", user_id)
        return render_template("sell.html", purchases=purchases)
