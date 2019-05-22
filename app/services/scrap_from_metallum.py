import sys
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib.parse import urlencode


class MetallumScrapper:
    def __init__(self, term):
        ua = UserAgent()
        headers = {'User-Agent': str(ua.chrome)}
        self.headers = headers
        self.term = term

    def get_album_cover(self):
        album_url_from_google = self._search_google()
        album_cover = self._get_image_from_metallum(album_url_from_google)

        return album_cover

    def _search_google(self):
        search_term = {'q': 'site:www.metal-archives.com ' + self.term}
        url = 'https://www.google.com.br/search?' + urlencode(search_term)

        try:
            google_result = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(markup=google_result.text, features='html.parser')

            if soup.find("div", {"id": "imagebox_bigimages"}):
                return soup.find_all('h3')[1:2][0].find_parent('a')['href']

            return soup.find('h3').find_parent('a')['href']
        except Exception as e:
            sys.exit(str(e))

    def _get_image_from_metallum(self, url):
        try:
            page = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(markup=page.text, features='html.parser')
            image_div = soup.find('div', {'class': 'album_img'})
            image = image_div.findChild("img")

            return image['src']
        except Exception as e:
            sys.exit(str(e))

    def _download_image(self, image_src):
        pass


ms = MetallumScrapper("nervochaos to the death")
print(ms.get_album_cover())


