from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, Model
from flask_wtf import CSRFProtect
from sqlalchemy import Column, DateTime
import datetime


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app=app)
migrate = Migrate(app=app, db=db)

csrf = CSRFProtect(app)

from .views import albums
from .models import album