from flask import Flask, render_template, url_for, request, redirect
import requests
import os
import asyncio
import aiohttp
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
import json

app = Flask(__name__)
Bootstrap(app)
fa = FontAwesome(app)

@app.route('/')
def index():
	pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/?limit=-1').json()["results"]
	return render_template('index.html', pokemon=pokemon)

@app.route('/<pokemon>')
def pokemon(pokemon):
	req = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}').json()
	for i in req['stats']:
		print(f"{i['stat']['name']}: {i['base_stat']}")
	for i in req['types']:
		print(f"type: {i['type']['name']}")
	for i in req['sprites']:
		print(f"{' '.join(i.split('_'))}: {req['sprites'][i]}")
	stats = req['stats']
	types = req['types']
	sprites = [req['sprites'][i] for i in req['sprites']]
	name = req['name']
	name = name.capitalize()
	weight = req['weight']
	sprites[0], sprites[1], sprites[2], sprites[3], sprites[4], sprites[5], sprites[6], sprites[7] = sprites[4], sprites[0], sprites[5], sprites[1], sprites[6], sprites[2], sprites[7], sprites[3]
	return render_template('pokemon.html', stats = stats, types = types, sprites = sprites, name = name, weight = weight)
	
@app.route('/get_pokemon', methods=['POST'])
def get_pokemon():
	try:
		pokemon = request.form['pokemon']
		return redirect(url_for('pokemon', pokemon=pokemon))
	except:
		return redirect(url_for('index'))

port = int(os.environ.get('PORT', 5000)) 
if __name__ == '__main__':
	app.run(threaded=True, port=port)
	