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
async def get_pk_data(pk):
	return await requests.get(f'https://pokeapi.co/api/v2/pokemon/{pk}').json()

@app.route('/')
def index():
	pokemon = []
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	check = False
	pk_id = 1
	while check:
		try:
			loop.run_until_complete(get_pk_data(pk_id))
			pk_id += 1
			print(pk_id)
		except: 
			print("excepted")
			check = False
	loop.close()
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
	sprites = req['sprites']
	name = req['name']
	weight = req['weight']
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
	