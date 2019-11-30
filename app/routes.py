"""Define the views for your application here."""
from uuid import UUID, uuid4

from flask import render_template, request, url_for, redirect, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import DataError

from app import app, db
from app.db_model import *
from app.forms import LoginForm

# Credit to https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-worlds
# Splash screen:


@app.route("/index")
@app.route("/")
def index():
    return render_template("splash.html")

# Create alias to from /static/pwa/sw.js to /sw.js in order to allow for full-site service worker scope:


@app.route("/sw.js")
def serviceworker():
    return app.send_static_file("pwa/sw.js")

# User auth/deauth/register routes:


@app.route("/auth", methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("signin"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("home"))
    return render_template("auth.html", title="Sign In", form=form)


@app.route("/deauth")
def signout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register")
def register():
    return render_template("register.html")

# Error handlers:


@app.errorhandler(404)
def notfound(error=None):
    return render_template("errors/404.html", error=error)

# Actual app views:


@app.route("/account")
@login_required
def account():
    return render_template("account.html")


@app.route("/home")
@login_required
def home():
    return render_template("home.html", events=current_user.events)


@app.route("/events/<eventID>")
@login_required
def events(eventID=None):
    if eventID is None:
        abort(404)

    try:
        event = Event.query.filter_by(owner=current_user, id=eventID).first()
    except DataError:
        event = None

    if event is None:
        abort(404)
    return render_template("showevent.html", event=event)
