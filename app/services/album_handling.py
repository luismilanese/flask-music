from app import db
from app.models.album import Album, Artist


def insert(form):
    title = form.title.data
    personal_note = form.personal_note.data

    new_album = Album(title=title, personal_note=personal_note)

    for artist_id in form.artists.data:
        new_album.artists.append(Artist.query.filter_by(id=artist_id).first())

    db.session.add(new_album)
    db.session.commit()
