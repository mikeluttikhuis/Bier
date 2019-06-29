from flask import Flask
import requests
import json
import logging
import logging.handlers

app = Flask(__name__)

handler = logging.handlers.RotatingFileHandler(
        'log.txt',
        maxBytes=1024 * 1024)
logging.getLogger('werkzeug').setLevel(logging.DEBUG)
logging.getLogger('werkzeug').addHandler(handler)
app.logger.setLevel(logging.WARNING)
app.logger.addHandler(handler)

@app.route('/')
def index():
        r_shop = requests.get('https://www.biernet.nl/extra/app/V3_3.3.4/winkel.php')
        r_shop = json.loads(r_shop.text)
        r_discount = requests.get('https://www.biernet.nl/extra/app/V3_3.3.4/aanbieding.php')
        r_discount = json.loads(r_discount.text)
        r_kind = requests.get('https://www.biernet.nl/extra/app/V3_3.3.4/soort.php')
        r_kind = json.loads(r_kind.text)

        shops = {
                "1": "Albert Heijn",
                "9": "Coop",
                "14": "Gall en Gall",
                "5": "Jumbo"
        }

        brands = {
                "1141": "Grolsch Premium Pilsener Krat 24x0,3L",
                "13": "Grolsch Premium Pilsener Krat 16x0,45L",
                "19": "Hertog Jan Pilsener Krat 24x0,3L",
                "246": "Warsteiner Premium Pilsener Krat 24x0,33L",
                "26": "Warsteiner Premium Pilsener Krat 24x0,3L"
        }

        discounts = []
        for dc in r_discount:
                if dc["soort_uid"] in brands and dc["winkel_uid"] in shops:
                        discounts.append('Winkel: '+shops[dc["winkel_uid"]]+'</br>')
                        discounts.append('Merk: '+brands[dc["soort_uid"]]+'</br>')
                        discounts.append('Prijs: €'+dc["voorprijs"]+'</br>')
                        discounts.append('Geldig tot: '+dc["einddatum"]+'</br>')
                        discounts.append('</br>')
        return ''.join(discounts)