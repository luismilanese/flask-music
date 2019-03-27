from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError


class AlbumForm(FlaskForm):
    title = StringField("title", validators=[DataRequired(), Length(min=1, max=100)])
    personal_note = StringField("personal_note", validators=[Length(min=0, max=250)])
    artists = SelectMultipleField("artists", coerce=int)
    new_artists = StringField("new_artists")
    wish_list = BooleanField("wish_list")

    def validate_artists(form, field):
        if len(form.artists.data) == 0 and len(form.new_artists.data) == 0:
            raise ValidationError("There should be a least one artist!")
