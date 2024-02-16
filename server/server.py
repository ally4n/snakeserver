from flask import Flask, request, jsonify
from playerClass import Player
from gameManager import GameManager
from messengerDaemon import Communicator, Message
import json


from functools import wraps
from flask import request, jsonify

players = []

app = Flask(__name__)

gmanager = GameManager()
communicator = Communicator(gmanager=gmanager)

# checks if a player is present
def checkPresent(name):
    for p in players:
        if p.name == name:
            return p
    return False

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json()
        name = data.get('name')
        password = data.get('password')

        player = checkPresent(name)
        # Check if the user is present
        if not player:
            return returner(f'{name} does not exist or is not logged in currently.')

        if player.validator(name, password) != 'ok':
            return returner('Wrong username or password.')

        return f(player, *args, **kwargs)

    return decorated_function

def returner(info):
    if type(info) == str:
        return info
    return json.dumps(info)    

@app.route("/signup", methods=["POST"])
# signup function, conditions are checked in playerClass.py
def signup():
    data = request.get_json()
    player = Player()
    x = player.signup(data['name'], data['password'])

    if x == 'ok':
        players.append(player)
        return returner('Signed up successfully.')
    return returner(x)

@app.route("/login", methods=["POST"])
# login function, conditions are checked in playerClass.py
def login():
    data = request.get_json()
    player = Player()

    x = player.login(data['name'], data['password'])

    if x == 'ok':

        if checkPresent(data['name']):
            return returner('User already logged in.')

        players.append(player)
        return returner('Logged in successfully.')

    return returner(x)

@app.route("/logout", methods=["POST"])
@authorize
# logout function, presence and the password are checked in playerClass.py
def logout(player):
    data = request.get_json()
    players.remove(player)
    return returner('Logged out successfully.')

@app.route('/changePassword', methods=["POST"])
@authorize
# changePassword function, presence and the password are checked in playerClass.py
def changePassword(player):
    data = request.get_json()
    return returner(player.changePassword(data['password'], data['newPassword']))

@app.route('/players', methods=["GET"])
def getPlayers():
    return returner([p.name for p in players])

@app.route('/send', methods=["POST"])
@authorize
# send function, checks if the sender is present, and sends the message
def send(player):
    data = request.get_json()
    receiver = checkPresent(data['receiver'])

    if receiver == False:
        return returner(f'{data["receiver"]} does not exist or is not logged in currently.')

    return returner(communicator.send(player, receiver, data['message'])
)

@app.route('/read', methods=["POST"])
@authorize
# read function, checks if the player is present, and reads the message
def read(player):
    data = request.get_json()
    
    m = communicator.read(player)
    if m:
        return returner(m)
    return returner('ok')

@app.route('/invite', methods=["POST"])
@authorize
# invite function, checks if the sender is present, and sends the invite
def invite(player):
    data = request.get_json()
    receiver = checkPresent(data['receiver'])

    if receiver == False:
        return returner(f'{data["receiver"]} does not exist or is not logged in currently.')

    communicator.invite(player, receiver, data['title'], data['gridsize'])
    return returner('ok')

@app.route('/listInvites', methods=["POST"])
@authorize
def listInvites(player):
    data = request.get_json()
    
    return returner(communicator.listInvites(player))

@app.route('/acceptInvite', methods=["POST"])
@authorize
def acceptInvite(player):
    data = request.get_json()
    
    return returner(communicator.acceptInvite(player, data['id']))

@app.route('/declineInvite', methods=["POST"])
@authorize
def declineInvite(player):
    data = request.get_json()

    return returner(communicator.declineInvite(player, data['id']))

@app.route('/listGames', methods=["POST"])
@authorize
def listGames(player):
    data = request.get_json()

    return returner(communicator.listGames(player))

@app.route('/listFinishedGames', methods=["POST"])
@authorize
def listFinishedGames(player):
    data = request.get_json()

    return returner(communicator.listFinishedGames(player))

@app.route('/makeMove', methods=["POST"])
@authorize
def makeMove(player):
    data = request.get_json()

    return returner(communicator.makeMove(player, data['id'], data['move']))

@app.route('/resign', methods=["POST"])
@authorize
def resign(player):
    data = request.get_json()

    return returner(communicator.resign(player, data['id']))

@app.route('/gameState', methods=["POST"])
@authorize
def gameState(player):
    data = request.get_json()

    return returner(communicator.gameState(player, data['id']))

