from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

phonebook=Flask(__name__)
phonebook.config.from_object(Config)

db = SQLAlchemy(phonebook)
migrate = Migrate(phonebook, db)

login = LoginManager(phonebook)
login.login_view = 'login'
from . import routes,models