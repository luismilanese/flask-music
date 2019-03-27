from app import db
from app.models.album import Album, Artist


def insert_artists(names_string):
    names_list = names_string.split(";")
    new_artists_id = []

    for name in names_list:
        artist = Artist(name=name.strip())
        db.session.add(artist)
        db.session.flush()
        new_artists_id.append(artist.id)
    db.session.commit()

    return new_artists_id
