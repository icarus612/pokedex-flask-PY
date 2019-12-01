from flask import Flask, render_template, url_for, request, redirect
import requests
import os
from flask_bootstrap import Bootstrap
import json

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/<pokemon>')
def pokemon(pokemon):
	req = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}').json()
	for i in req['stats']:
		print(f"{i['stat']['name']}: {i['base_stat']}")
	
	for i in req['types']:
		print(f"type: {i['type']['name']}")
	for i in req['sprites']:
		print(f"{' '.join(i.split('_'))}: {req['sprites'][i]}")
	print(json.dumps(req['sprites'], indent=2))
	return render_template('pokemon.html', pokemon=pokemon, error=None)

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
	