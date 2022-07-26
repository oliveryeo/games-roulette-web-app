import os

from random import randint
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime

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
db = SQL("sqlite:///gamesroulette.db")

@app.route("/")
@login_required
def index():
    """Show games homepage"""

    # Initiate user_id session
    user_id = session['user_id']

    # Pass admin variable into html -> Allows layout.html to display admin button
    admin = db.execute("SELECT admin FROM users WHERE id = ?", user_id)[0]["admin"]

    # Get all games from database
    games = db.execute("SELECT id, gamename, genre, website FROM games ORDER BY id DESC LIMIT 5")

    return render_template("index.html", admin=admin, games=games)


@app.route("/requests", methods=["GET", "POST"])
@login_required
def requests():
    """Show requests form"""
    user_id = session['user_id']

    if request.method == "POST":
        # Assign all relevant varaibles
        name = request.form.get("name")
        website = request.form.get("website")
        available_genres = ["action", "roleplaying", "strategy", "adventure", "simulation", "sports"]
        genres_list = []

        for i in available_genres:
            if request.form.get(f"{i}"):
                genres_list.append(request.form.get(f"{i}"))

        # Concatenate all genres
        genres = ", ".join(genres_list)
        status = "pending"

        # Update requests list database
        db.execute("INSERT INTO requests (gamename, genre, website, status) VALUES (?, ?, ?, ?)", name, genres, website, status)

        # Return to website
        return redirect("/")

    else:
        return render_template("requests.html")

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    """Approve requests"""
    user_id = session['user_id']

    # Check if user is admin
    admin = db.execute("SELECT admin FROM users WHERE id = ?", user_id)[0]["admin"]
    if not admin:
        return apology("You are not authorised", 400)

    if request.method == "POST":
        # Update database if approved
        if request.form.get("decision") == "approve":
            # Transfer data to actual database
            approved_request = db.execute("SELECT id, gamename, genre, website FROM requests ORDER BY id LIMIT 1")[0]
            db.execute("INSERT INTO games (gamename, genre, website) VALUES (?, ?, ?)", approved_request["gamename"], approved_request["genre"], approved_request["website"])

            # Delete data at request database
            db.execute("DELETE FROM requests WHERE id = ?", approved_request["id"])

        # Update database if denied
        elif request.form.get("decision") == "deny":
             approved_request = db.execute("SELECT id, gamename, genre, website FROM requests ORDER BY id LIMIT 1")[0]
             db.execute("DELETE FROM requests WHERE id = ?", approved_request["id"])

        return redirect("/")

    else:
        # Render requests to approve
        all_requests = db.execute("SELECT id, gamename, genre, website FROM requests ORDER BY id LIMIT 1")
        return render_template("admin.html", all_requests=all_requests)


@app.route("/categories")
@login_required
def categories():
    """Categories of games"""
    return render_template("categories.html")


@app.route("/action")
@login_required
def action():
    """Action games"""
    # Get data of all action games
    action_games = db.execute("SELECT id, gamename, genre, website FROM games WHERE genre LIKE '%action%'")
    return render_template("action.html", games=action_games)


@app.route("/roleplaying")
@login_required
def roleplaying():
    """Roleplaying games"""
    # Get data of all roleplaying games
    roleplaying_games = db.execute("SELECT id, gamename, genre, website FROM games WHERE genre LIKE '%roleplaying%'")
    return render_template("roleplaying.html", games=roleplaying_games)


@app.route("/strategy")
@login_required
def strategy():
    """Strategy games"""
    # Get data of all strategy games
    strategy_games = db.execute("SELECT id, gamename, genre, website FROM games WHERE genre LIKE '%strategy%'")
    return render_template("strategy.html", games=strategy_games)


@app.route("/adventure")
@login_required
def adventure():
    """Simulation games"""
    # Get data of all adventure games
    adventure_games = db.execute("SELECT id, gamename, genre, website FROM games WHERE genre LIKE '%adventure%'")
    return render_template("adventure.html", games=adventure_games)


@app.route("/simulation")
@login_required
def simulation():
    """Simulation games"""
    # Get data of all simulation games
    simulation_games = db.execute("SELECT id, gamename, genre, website FROM games WHERE genre LIKE '%simulation%'")
    return render_template("simulation.html", games=simulation_games)


@app.route("/sports")
@login_required
def sports():
    """Sports games"""
    # Get data of all sports games
    sports_games = db.execute("SELECT id, gamename, genre, website FROM games WHERE genre LIKE '%sports%'")
    return render_template("sports.html", games=sports_games)


@app.route("/roulette", methods=["GET", "POST"])
@login_required
def roulette():
    """Games roulette"""
    if request.method == "POST":
        # Get min and max id integer of games database
        min_id = int(db.execute("SELECT MIN(id) FROM games")[0]["MIN(id)"])
        max_id = int(db.execute("SELECT MAX(id) FROM games")[0]["MAX(id)"])

        # Randomize the id and return the selected game
        random_id = randint(min_id, max_id)
        selected_game = db.execute("SELECT id, gamename, genre, website FROM games WHERE id = ?", random_id)

        return render_template("roulette.html", games=selected_game)

    else:
        return render_template("roulette.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # Query database for username, check if username exists
        elif db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username")):
            return apology("username already exists", 400)

        # Add username and hashed password to database
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password)

        # Redirect to login page
        return redirect("/login")

    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
