from urllib import request

from flask import render_template, redirect, url_for
from app import app
from app.forms.album_form import AlbumForm
from app.models.album import Album, Artist
from app.repositories import album_repository
from app import db
from app.repositories.artist_repository import get_all_artists


@app.route("/")
def index():
    return render_template("albums/index.html")


@app.route("/add-new", methods=["GET", "POST"])
def add_album():
    form = AlbumForm()
    form.artists.choices = get_all_artists()

    if form.validate_on_submit():
        try:
            album_repository.insert_album(form)
            return redirect(url_for("all"))
        except Exception as e:
            print(str(e))

    return render_template("albums/form.html", form=form)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_album(id):
    album = album_repository.get_by_id(id)
    form = AlbumForm(obj=album)
    form.artists.choices = get_all_artists()

    if form.validate_on_submit():
        try:
            album_repository.update_album(id, form)
            return redirect(url_for("all"))
        except Exception as e:
            print(str(e))

    form.artists.data = [artist.id for artist in album.artists]

    return render_template("albums/form.html", form=form)


@app.route("/all")
def listing():
    albums = album_repository.list_albums()

    return render_template("albums/list.html", albums=albums)
