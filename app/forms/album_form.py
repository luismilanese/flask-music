from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Length


class AlbumForm(FlaskForm):
    title = StringField("title", validators=[DataRequired(), Length(min=1, max=100)])
    personal_note = StringField("personal_note", validators=[Length(min=0, max=250)])
    artists = SelectMultipleField("artists", coerce=int, validators=[DataRequired()])
    wish_list = BooleanField("wish_list")
