import requests
from bs4 import BeautifulSoup
import re
import smtplib
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
load_dotenv()

shops = [
                        'Albert Heijn',
                        'Gall En Gall',
                        'Coop Supermarkt',
                        'JUMBO'
                        ]

base_url = 'https://www.biernet.nl/bier/aanbiedingen/'
brands_url = [
                        'grolsch-premium-pilsener/krat-van-24-flesjes-a-030-liter',
                        'grolsch-premium-pilsener/krat-van-16-flesjes-a-045-liter',
                        'hertog-jan-pilsener/krat-van-24-flesjes-a-030-liter',
                        'warsteiner-premium-pilsener/krat-van-24-flesjes-a-030-liter'
                        ]
beer_discount = []

for brand in brands_url:
        r = requests.get(base_url+brand)
        c = r.content
        soup = BeautifulSoup(c, "lxml")

        discount = soup.find('ul', {"class":"aanbiedingen"})
        textdiscount = discount.find_all('div', {"class":"textaanbieding"})
        for shop in textdiscount:
                if shop.find('p', {"class":"Kratten"}) is not None and shop.find('img')['title'].title() in shops:
                        shop_info = {}
                        shop_info['name'] = shop.find('img')['title'].title()
                        shop_info['price'] = shop.find('span', {"class":"prijs"}).text
                        shop_info['brand'] = shop.find('span', {"class":"merke"}).text
                        shop_info['product'] = shop.find('p', {"class":"Kratten"}).text
                        shop_info['valid'] = re.sub(r"\s+", " ", shop.find('p', {"style":"margin:0;"}).text.strip())
                        beer_discount.append(shop_info)

beer_discount = sorted(beer_discount, key=lambda k: k['price'], reverse=True)

def generatebody():
        body = []
        for i in range(0,len(beer_discount)):
                body.append('Winkel:\t'+beer_discount[i]['name']+'<br/>')
                body.append('Merk:\t'+beer_discount[i]['brand']+'<br/>')
                body.append('Prijs:\t'+(beer_discount[i]['price'])+' - '+beer_discount[i]['product']+'<br/>')
                body.append('Geldig:\t'+beer_discount[i]['valid']+'<br/>')
                body.append('<br/>')
        return ''.join(body)

message = Mail(
    from_email=os.getenv('FROM'),
    to_emails=os.getenv('TO'),
    subject='Bier aanbiedingen - Daily',
    html_content=generatebody())
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)