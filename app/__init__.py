from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app=app)
migrate = Migrate(app=app, db=db)
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from .views import albums
from .models import album, user