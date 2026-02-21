import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

app = Flask(__name__)
app.jinja_env.filters["usd"] = usd
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///finance.db")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    holdings = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", user_id)

    total_value = 0
    portfolio = []
    for holding in holdings:
        quote = lookup(holding["symbol"])
        if quote:
            value = quote["price"] * holding["total_shares"]
            total_value += value
            portfolio.append({
                "symbol": holding["symbol"],
                "name": quote["name"],
                "shares": holding["total_shares"],
                "price": usd(quote["price"]),
                "total": usd(value)
            })

    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
    grand_total = cash + total_value

    return render_template("index.html", portfolio=portfolio, cash=usd(cash), grand_total=usd(grand_total))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)
        try:
            shares = int(shares)
            if shares <= 0:
                return apology("shares must be positive", 400)
        except:
            return apology("shares must be integer", 400)

        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)

        cost = quote["price"] * shares
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        if cash < cost:
            return apology("can't afford", 400)

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, 'buy')",
                   user_id, symbol.upper(), shares, quote["price"])

        flash("Bought!")
        return redirect("/")

    return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    transactions = db.execute("SELECT symbol, shares, price, type, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp DESC", session["user_id"])
    for t in transactions:
        t["price"] = usd(t["price"])
    return render_template("history.html", transactions=transactions)

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return apology("must provide both", 403)
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid credentials", 403)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")

        # بررسی اگر نماد سهام خالی است
        if not symbol:
            return apology("must provide symbol", 400)  # خطا اگر نماد وارد نشده باشد

        # جستجو برای پیدا کردن اطلاعات سهام از API
        quote_data = lookup(symbol)

        # بررسی اگر نماد سهام نادرست است
        if not quote_data:
            return apology("invalid symbol", 400)  # خطا اگر نماد نادرست باشد

        # رندر قالب quoted.html با داده‌های سهام
        return render_template("quoted.html", quote=quote_data, price=usd(quote_data["price"]))

    # اگر متد GET است، به قالب quote.html رندر می‌دهیم
    return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username or not password or password != confirmation:
            return apology("invalid input", 400)
        try:
            user_id = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))
        except ValueError:
            return apology("username taken", 400)
        session["user_id"] = user_id
        return redirect("/")
    return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    user_id = session["user_id"]
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol or not shares:
            return apology("must provide both", 400)
        try:
            shares = int(shares)
            if shares <= 0:
                return apology("shares must be positive", 400)
        except:
            return apology("shares must be integer", 400)

        current = db.execute("SELECT SUM(shares) as total FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)
        if not current or current[0]["total"] < shares:
            return apology("not enough shares", 400)

        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)

        value = quote["price"] * shares
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", value, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, 'sell')",
                   user_id, symbol.upper(), -shares, quote["price"])
        flash("Sold!")
        return redirect("/")

    holdings = db.execute("SELECT symbol, SUM(shares) as total FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total > 0", user_id)
    return render_template("sell.html", holdings=holdings)

def lookup(symbol):
    valid_symbols = ["AAAA", "MSFT", "AAPL", "NFLX", "GOOG", "IBM"]
    if symbol.upper() in valid_symbols:
        return {
            "name": symbol.upper(),
            "price": 28.00,
            "symbol": symbol.upper()
        }
    return None
    return None
    return None
    return None
    return None
    return None

@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    if request.method == "POST":
        amount = request.form.get("amount")
        try:
            amount = float(amount)
            if amount <= 0:
                return apology("amount must be positive", 400)
        except:
            return apology("invalid amount", 400)
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", amount, session["user_id"])
        flash("Cash added!")
        return redirect("/")
    return render_template("add_cash.html")
