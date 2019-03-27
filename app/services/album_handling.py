from app import db
from app.models.album import Album, Artist
from app.services.artist_handling import insert_artists


def insert_album(form):
    title = form.title.data
    personal_note = form.personal_note.data

    new_album = Album(title=title, personal_note=personal_note)

    artists = form.artists.data

    if form.new_artists.data:
        new_artists = insert_artists(form.new_artists.data)
        for artist_id in new_artists:
            artists.append(artist_id)

    for artist_id in artists:
        new_album.artists.append(Artist.query.filter_by(id=artist_id).first())

    db.session.add(new_album)
    db.session.commit()
