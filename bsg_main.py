# FOR NOTE: request.form[name] = value

from flask import *
import sqlite3
import json
import os
import pickle
from datetime import datetime

import world
from modules import events, fleets
import modules.galaxy_gen as galaxy


def to_json(obj):
	return obj.__dict__


player_world = world.World(galaxy.Galaxy(), events.EventHandler(), fleets.FleetHandler())

# The Flask initialization.
app = Flask(__name__)
app.config.from_object('flask_config')

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'player_database.db')
))


def connect_db():
	# Connects to the specific database.
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv


def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()


@app.cli.command('initdb')
def initdb_command():
	# Initializes the DB
	init_db()
	print('Initialized the database.')


def get_db():
	# Opens a new database connection if there is none for the current app context.
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()


# The code that happens for a page load for the base page. Contains the Main Menu HTML render as well as the core game.
@app.route('/', methods=['GET', 'POST'])
def index():
	if not player_world.world_initiated:
		if request.method == 'POST':
			seed = request.form.get('seed', None)
			if request.form.get('seed', None) == '':
				seed = False
			# POST's for new game
			if request.form.get('start_new_game', None) == 'default':
				player_world.initial_galaxy_generation(seed)
			elif request.form.get('start_new_game', None) == 'random':
				player_world.initial_galaxy_generation(seed, False)
		else:
			return render_template('index.html', trim_blocks=True, lstrip_blocks=True)

	db = get_db()
	cur = db.execute('SELECT * FROM saves')
	saves = cur.fetchall()

	if request.method == 'POST':
		pass
	return render_template('main.html', player_world=json.dumps(player_world, default=to_json), saves=saves, trim_blocks=True, lstrip_blocks=True)


# To create a save game or modify it. Is done in main.html
@app.route('/save_game', methods=['POST'])
def save_game():
	jquery_data = request.get_json()

	time = datetime.now()
	time = str(time.day) + '/' + str(time.month) + '/' + str(time.year) + ' ' + str(time.hour) + ':' + str(time.minute)

	db = get_db()
	cur = db.execute('SELECT save_name FROM saves')
	saves = cur.fetchall()

	for save in saves:
		if jquery_data['save_name'] == save['save_name']:
			db.execute('UPDATE saves SET pickle=?, modified_time=? WHERE save_name=?', (pickle.dumps(player_world), time, jquery_data['save_name']))
			db.commit()
			return jsonify(time=time)
	db.execute('INSERT INTO saves (save_name, pickle, create_time, modified_time, save_settings) VALUES (?, ?, ?, ?, ?)',
			  (jquery_data['save_name'], pickle.dumps(player_world), time, time, '{"seed": ' + player_world.seed + '}') )
	db.commit()
	return jsonify(time=time)


# Code to check if a save is valid. Is done in index.html
@app.route('/validate_save', methods=['POST'])
def validate_save():
	global player_world
	jquery_data = request.get_json()

	db = get_db()
	cur = db.execute('SELECT pickle FROM saves WHERE save_name=?', [jquery_data['save_name']])
	player_save = cur.fetchone()

	if player_save:
		player_world = pickle.loads(player_save['pickle'])
		return jsonify(valid=True)
	return jsonify(valid=False)


# Code for a AJAX call for the next turn functions.
@app.route('/next_turn', methods=['POST'])
def next_turn():
	jquery_data = request.get_json()
	print(jquery_data['save_name'])

	player_world.next_turn(jquery_data)

	return jsonify(success=True)


if __name__ == '__main__':
	app.run()
