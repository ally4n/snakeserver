import json
import os
from gameManager import GameManager

class Player():

    def __init__(self):
        self.name = ''
        self._password = ''

    def _loadFile(self, name, mode='r'):
        return open(f'players/{name}.json', mode) 

    def signup(self, name, password):

        if self.name != '':
            return 'There already exits a logged in user for this player object.'

        if os.path.isfile(f'players/{name}.json'):
            return 'The username is in use.'

        if name == '' or password == '':
            return 'Username or password cannot be empty.'

        self.name = name
        self._password = password

        f = self._loadFile(name, 'w')
        json.dump({'name': name, 'password': password}, f)

        return 'ok'

    def validator(self, name, password):
        if self.name == '' and self._password == '':
            if os.path.isfile(f'players/{name}.json'):
                f = self._loadFile(name, 'r')
                try:
                    data = json.load(f)
                except:
                    return 'There exists a corrupted file for this player.'
                self.name = data['name']
                self._password = data['password']
            else:
                return 'There is no such user.'

        if name != self.name or password != self._password:
            return 'Wrong username or password·.'

        return 'ok'

    def login(self, name, password):
        return self.validator(name, password)      

    def changePassword(self, name, newPassword):

        f = self._loadFile(name, 'w')
        json.dump({'name': self.name, 'password': self.newPassword}, f)
        self._password = newPassword

        return 'ok'
         
 
