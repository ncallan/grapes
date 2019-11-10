import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SECRET_KEY"] = "ohgodnotinprod" # os.environ["SECRET_KEY"]

db = SQLAlchemy(app)

login = LoginManager()
login.init_app(app)
login.login_view = "signin"

from app.db_model import *
from app.routes import *
