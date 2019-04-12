import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app import app
from app.models.album import Album


class Importer:
    def importer(self):
        albums = self._read_from_gspread()
        for album in albums:
            a = Album(title=album['title'], personal_note=album['personal_notes'], wish_list=album['wish_list'])
            if not self._check_album_already_exists(album=a):
                print('Não existe!')
            else:
                print('Já existe')

    def _check_album_already_exists(self, album):
        return Album.query.filter_by(title=album.title).first()

    def _read_from_gspread(self):
        scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(app.config['GSPREAD_API_CERT'], scope)
        client = gspread.authorize(creds)

        sheet = client.open(app.config['GSPREAD_TITLE']).sheet1

        values = sheet.get_all_records()
        return values
