from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
