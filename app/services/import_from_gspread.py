import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app import app, db
from app.models.album import Album, Artist


class Importer:
    def importer(self):
        albums = self._read_from_gspread()
        new_albums = []

        for album in albums:
            a = Album(title=album['title'], personal_note=album['personal_notes'], wish_list=album['wish_list'])
            if not self._album_already_exists(album=a):
                artists = self._extract_artists_from_album(album_artists=album['artists'])
                for artist in artists:
                    a.artists.append(artist)
                db.session.add(a)
                db.session.commit()
                new_albums.append(a)

        return new_albums

    def _album_already_exists(self, album):
        return Album.query.filter_by(title=album.title).first()

    def _extract_artists_from_album(self, album_artists):
        artists_names = album_artists.split(";")
        artists = []
        for artist_name in artists_names:
            artist = Artist.query.filter_by(name=artist_name).first()
            if not artist:
                a = Artist(name=artist_name)
                artists.append(a)
                db.session.add(a)
            else:
                artists.append(artist)

        return artists

    def _read_from_gspread(self):
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(app.config['GSPREAD_API_CERT'], scope)
        client = gspread.authorize(creds)

        sheet = client.open(app.config['GSPREAD_TITLE']).sheet1

        values = sheet.get_all_records()
        return values
