import sys
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ua = UserAgent()

url = 'https://www.metal-archives.com/bands/Farscape/7041'
header = {'User-Agent': str(ua.chrome)}

try:
    page = requests.get(url, headers=header)
    soup = BeautifulSoup(markup=page.text, features='html.parser')
    photo_div = soup.find('div', {'class': 'band_img'})
    photo = photo_div.findChild("img")
    print(photo['src'])
except Exception as e:
    sys.exit(str(e))
