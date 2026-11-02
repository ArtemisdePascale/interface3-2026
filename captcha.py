import requests
from icecream import ic
from bs4 import BeautifulSoup
import base64
from PIL import Image
import pytesseract
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
cookies = {
    'PHPSESSID': 'b92cf867315f6da9ec33e77933e49d22',
    '_ga_SRYSKX09J7': 'GS2.1.s1793610434$o27$g1$t1793613321$j43$l0$h0',
    '_ga': 'GA1.1.1978729830.1790084736',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://challenge01.root-me.org',
    'Connection': 'keep-alive',
    'Referer': 'http://challenge01.root-me.org/programmation/ch8/',
    'Upgrade-Insecure-Requests': '1',
    'Priority': 'u=0, i',
}

captchas = []

for i in range(100):
    r = requests.get('http://challenge01.root-me.org/programmation/ch8/')
    soup = BeautifulSoup(r.text, 'html.parser')
    image = soup.find('img')
    src = image.get('src')
    captchas.append(src)
    pic = Image.open(BytesIO(base64.b64decode(src.split(',')[1])))
    text = pytesseract.image_to_string(pic)
    text = text.strip()
    ic(text)
    data = {'cametu': text}
    response = requests.post('http://challenge01.root-me.org/programmation/ch8/', cookies=cookies, headers=headers, data=data)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find('p').text
    if 'Failed, Try again.' not in result:
        ic(soup)
        break 
