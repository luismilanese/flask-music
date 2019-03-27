from datetime import datetime
from app import db


class TimestampMixin(object):
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow())
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow())


albums_artists = db.Table('albums_artists',
                          db.Column('album_id', db.Integer, db.ForeignKey('albums.id'), primary_key=True),
                          db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True))


class Album(TimestampMixin, db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    personal_note = db.Column(db.String(250), nullable=True)
    wish_list = db.Column(db.Boolean())
    artists = db.relationship("Artist", secondary=albums_artists, lazy="subquery",
                              backref=db.backref('albums', lazy=True))

    def __init__(self, title, personal_note=None, wish_list=False):
        self.title = title
        self.wish_list = wish_list
        if personal_note is not None:
            self.personal_note = personal_note

    def __repr__(self):
        return "Album {}".format(self.title)


class Artist(TimestampMixin, db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
