from flask import request
import json
from copy import deepcopy

from __main__ import app, storage
import util


@app.route('/games', methods=['POST'])
def post_game():

	game = json.loads(request.data.decode('UTF-8'))
	# TODO: Verify format and data

	game['state'] = {
		'state': 'planned',
		'winner': None,
		'fen': game['settings']['initialFEN'],
		'timeBudgets': {
			'playerA': game['settings']['timeBudget'],
			'playerB': game['settings']['timeBudget']
		}
	}
	game['events'] = []


	"""
	# TODO: Check initial state with Ruleserver
	valid, condition = ruleServer.stateCheck(game['state'])
	if not valid:
		return ("Error: Initial board state invalid:\nCondition: " + condition), 400
	"""

	id = util.id()

	storage['games'][id] = game

	# DEBUG
	util.showDict(storage)

	return json.dumps({
		'id': id
	}, indent=4), 201


@app.route('/games', methods=['GET'])
def get_games():

	games = deepcopy(storage['games'])

	# Remove stuff not needed in listing and add player names
	for id in games:
		del games[id]['settings']
		del games[id]['events']
		del games[id]['state']['fen']
		del games[id]['state']['timeBudgets']
		games[id]['playerNames'] = {
			'playerNameA': storage['players'][games[id]['players']['playerA']]['name'],
			'playerNameB': storage['players'][games[id]['players']['playerB']]['name']
		}
		del games[id]['players']

	return json.dumps(games, indent=4)


@app.route('/game/<id>', methods = ['GET'])
def get_game(id):

	if not id in storage['games']:
		return 'Error: Not found', 404

	game = deepcopy(storage['games'][id])

	del game['events']

	return json.dumps(game, indent=4)
