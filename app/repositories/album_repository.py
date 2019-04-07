from datetime import datetime

from app import db
from app.models.album import Album, Artist
from app.repositories.artist_repository import insert_artists


def insert_album(form):
    title = form.title.data
    personal_note = form.personal_note.data
    wish_list = form.wish_list.data

    new_album = Album(title=title, personal_note=personal_note, wish_list=wish_list)

    artists = form.artists.data

    if form.new_artists.data:
        new_artists = insert_artists(form.new_artists.data)
        for artist_id in new_artists:
            artists.append(artist_id)

    for artist_id in artists:
        new_album.artists.append(Artist.query.filter_by(id=artist_id).first())

    db.session.add(new_album)
    db.session.commit()


def update_album(id, form):
    album = get_by_id(id)
    album.title = form.title.data
    album.personal_note = form.personal_note.data
    album.wish_list = form.wish_list.data

    # removing former relationship to create it again below
    album.artists = []

    artists = form.artists.data

    if form.new_artists.data:
        new_artists = insert_artists(form.new_artists.data)
        for artist_id in new_artists:
            artists.append(artist_id)

    for artist_id in artists:
        album.artists.append(Artist.query.filter_by(id=artist_id).first())

    db.session.commit()


def delete_album(album):
    album.deleted = datetime.now()
    db.session.commit()


def list_albums():
    return Album.query.filter_by(deleted=None).all()


def get_by_id(id):
    return Album.query.filter_by(id=id).first()

