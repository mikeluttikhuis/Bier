from flask import Flask, render_template
#from flask_caching import Cache
import requests
import json

app = Flask(__name__)
#cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
#@cache.cached(timeout=14400)
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
	discount_all = []
	for dc in r_discount:
		if dc["soort_uid"] in brands and dc["winkel_uid"] in shops:
			discount = []
			discount.append(shops[dc["winkel_uid"]])
			discount.append(dc["aantal"])
			discount.append(brands[dc["soort_uid"]])
			discount.append(dc["voorprijs"])
			discount.append(dc["einddatum"])
			discount_all.append(discount)
	return render_template('index.html',data=discount_all)
