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
	payload = {'d': ''}
	headers = {'User-Agent': 'nl.Biernet.iOS.app/V3'}
	r_shop = requests.get('https://www.biernet.nl/extra/app/V3_3.3.4/winkel.php', params=payload, headers=headers)
	r_shop = json.loads(r_shop.text)
	r_discount = requests.get('https://www.biernet.nl/extra/app/V3_3.3.4/aanbieding.php', params=payload, headers=headers)
	r_discount = json.loads(r_discount.text)
	r_soort = requests.get('https://www.biernet.nl/extra/app/V3_3.3.4/soort.php', params=payload, headers=headers)
	r_soort = json.loads(r_soort.text)

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

	discounts.append('<div class="background">')
	discounts.append('<div class="container">')
	discounts.append('<div class="title">')
	discounts.append('<h1>Bier aanbiedingen</h1>')
	discounts.append('</div>')
	discounts.append('</div>')
	discounts.append('<div class="container">')

	for dc in r_discount:
		if dc["soort_uid"] in brands and dc["winkel_uid"] in shops:
			discounts.append('<div class="card">')
			discounts.append('<div class="card__shop">Winkel: %s</div>' % shops[dc["winkel_uid"]])
			discounts.append('<div class="card__brand">Merk: %s x %s</div>' % (dc["aantal"], brands[dc["soort_uid"]]))
			discounts.append('<div class="card__price">Prijs: %s</div>' % dc["voorprijs"])
			discounts.append('<div class="card__date">Geldig t/m: %s</div>' % dc["einddatum"])
			discounts.append('</div>')
	
	discounts.append('</div>')
	discounts.append('</div>')

	return ''.join(discounts)