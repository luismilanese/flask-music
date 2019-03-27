from urllib import request

from flask import render_template
from app import app
from app.forms.album_form import AlbumForm
from app.models.album import Album, Artist
from app.services import album_handling
from app import db

@app.route("/")
def index():
    return render_template("albums/index.html")


@app.route("/add-new", methods=["GET", "POST"])
def add_album():
    form = AlbumForm()
    form.artists.choices = [(a.id, a.name) for a in Artist.query.order_by('name')]

    if form.validate_on_submit():
        try:
            album_handling.insert(form)
        except Exception as e:
            print(str(e))

    return render_template("albums/form.html", form=form)
