import requests
import json

def jsload(x):
    '''json.loads if possible, else return x as is.'''
    try:
        return json.loads(x)
    except:
        return x

class Client:
    def __init__(self, name, password, url):
        '''Create a new client object. name and password are strings, url is the base url of the server.'''
        self.name = name
        self._password = password
        self.url = url

    def signup(self):
        '''
        Sign up with the given name and password. Returns 'ok' if successful, an error message otherwise.
        '''
        url = self.url + '/signup'
        obj = {'name': self.name, 'password': self._password}
        return jsload(self._post(url, obj))
    
    def login(self):
        '''
        Log in with the given name and password. Returns 'ok' if successful, an error message otherwise.
        '''
        url = self.url + '/login'
        obj = {'name': self.name, 'password': self._password}
        return jsload(self._post(url, obj))

    def logout(self):
        '''
        Log out. Returns 'ok' if successful, an error message otherwise.
        '''
        url = self.url + '/logout'
        obj = {'name': self.name, 'password': self._password}
        return jsload(self._post(url, obj))
    
    def changePassword(self, newPassword):
        '''
        Change the password. New password is required. Returns 'ok' if successful, an error message otherwise.
        '''
        url = self.url + '/changePassword'
        obj = {'name': self.name, 'password': self._password, 'newPassword': newPassword}
        return jsload(self._post(url, obj))

    def players(self):
        '''
        List all players. Returns a list of player names.
        '''
        url = self.url + '/players'
        return jsload(self._get(url))

    def send(self, receiver, message):
        '''
        Send to given receiver a message. Returns 'ok' if successful, an error message otherwise.
        '''
        url = self.url + '/send'
        obj = {'name': self.name, 'password': self._password, 'receiver': receiver, 'message': message}
        return jsload(self._post(url, obj))

    def read(self):
        '''
        Read all unread messages. Returns a list of unread messages.
        '''
        url = self.url + '/read'
        obj = {'name': self.name, 'password': self._password}
        return jsload(self._post(url, obj))

    def invite(self, receiver, title, gridsize):
        '''
        Invite the given receiver to a game. Title and gridsize are required. Returns 'ok' if successful, an error message otherwise.
        '''
        url = self.url + '/invite'
        obj = {'name': self.name, 'password': self._password, 'receiver': receiver, 'title': title, 'gridsize': gridsize}
        return jsload(self._post(url, obj))

    def listInvites(self):
        '''
        List all invites sent to you. Returns a list of invites.
        '''
        url = self.url + '/listInvites'
        obj = {'name': self.name, 'password': self._password}
        return jsload(self._post(url, obj))
    

    def accept(self, id):
        '''
        Accept the invite with the given id. Returns 'ok' if successful, an error message otherwise.
        '''
        url = self.url + '/acceptInvite'
        obj = {'name': self.name, 'password': self._password, 'id': id}
        return jsload(self._post(url, obj))

    def decline(self, id):
        '''
        Decline the invite with the given id. Returns 'ok' if successful, an error message otherwise.
        '''
        url = self.url + '/declineInvite'
        obj = {'name': self.name, 'password': self._password, 'id': id}
        return jsload(self._post(url, obj))

    def listGames(self):
        '''
        List all games you are in. Returns a list of games.
        '''
        url = self.url + '/listGames'
        obj = {'name': self.name, 'password': self._password}
        return jsload(self._post(url, obj))
    
    def listFinishedGames(self):
        '''
        List all finished games you were in. Returns a list of games.
        '''
        url = self.url + '/listFinishedGames'
        obj = {'name': self.name, 'password': self._password}
        return jsload(self._post(url, obj))
    
    def play(self, id, move):
        '''
        Make a move in the game with the given id. Move is required. Returns 'ok' if successful, an error message otherwise.
        '''
        url = self.url + '/makeMove'
        obj = {'name': self.name, 'password': self._password, 'id': id, 'move': move}
        return jsload(self._post(url, obj))

    def resign(self, id):
        '''
        Resign from the game with the given id. Returns 'ok' if successful, an error message otherwise.
        '''
        url = self.url + '/resign'
        obj = {'name': self.name, 'password': self._password, 'id': id}
        return jsload(self._post(url, obj))
    
    def gameState(self, id):
        '''
        Get the game state of the game with the given id. Returns the game state if successful, an error message otherwise.
        '''
        url = self.url + '/gameState'
        obj = {'name': self.name, 'password': self._password, 'id': id}
        return jsload(self._post(url, obj))

    def _post(self, url, obj):
        '''
        Send a post request to the given url with the given object. Returns the response text.
        '''
        x = requests.post(url, json=obj)
        return x.text
    
    def _get(self, url):
        '''
        Send a get request to the given url. Returns the response text.
        '''
        x = requests.get(url)
        return x.text
