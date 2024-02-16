import json
import os
import time
from datetime import datetime


class Communicator():
    
    def __init__(self, gmanager):
        self.messages = []
        self.invites = []
        self.gameManager = gmanager

    def send(self, sender, receiver, message):
        message = Message(time.strftime('%Y-%m-%d %H:%M:%S'), sender.name, receiver.name, message)
        self.messages.append(message)

        if not os.path.isfile(f'messages/{receiver.name}.json'):
            json.dump([message.to_dict()], open(f'messages/{receiver.name}.json', 'w'))
            return 'ok'

        data = json.load(open(f'messages/{receiver.name}.json', 'r'))
        data.append(message.to_dict())
        json.dump(data, open(f'messages/{receiver.name}.json', 'w'))
        return 'ok'


    def read(self, player):
        msgs = []
        for m in self.messages:
            if m.receiver == player.name and not m.read:
                m.read = True
                msgs.append({'id':f'{m.id}', 'sender':f'{m.sender}','message':f'{m.message}'})
        return msgs 

    def listInvites(self, player):
        invites = []
        for i in self.invites:
            if i.receiver == player.name:
                if not i.accepted and not i.declined:
                    invites.append({'id':f'{i.id}', 'sender':f'{i.sender}', 'title':f'{i.title}', 'gridsize':f'{i.gridsize}'})
        return invites

    def invite(self, sender, receiver, title, gridsize):
        self.invites.append(Invite(int(datetime.now().strftime('%Y%m%d%H%M%S%f')), sender.name, receiver.name, title, gridsize))

    def acceptInvite(self, player, id):
        for i in self.invites:
            if i.id == id:
                
                if i.receiver != player.name:
                    return 'This invite is not sent for you.'
                
                if i.accepted or i.declined:
                    return 'This invite has already been accepted or declined.'

                i.accepted = True
                self.gameManager.createGame(id, gridsize=i.gridsize,title=i.title, players=[i.sender, i.receiver])
                return 'ok'
        return 'Invite could not have been found.'

    def declineInvite(self, player, id):
        for i in self.invites:
            if i.id == id:
                
                if i.receiver != player.name:
                    return 'This invite is not sent for you.'

                i.declined = True
                return 'ok'
        return 'Invite could not have been found.'

    def listGames(self, player):
        return self.gameManager.listGames(player)
    
    def listFinishedGames(self, player):
        return self.gameManager.listFinishedGames(player)

    def makeMove(self, player, id, move):
        game = self.gameManager.getGame(player, id)
        if game:
            return game.makeMove(player, move)
        return 'No such game exists or you are not a player of it.'
    
    def resign(self, player, id):
        game = self.gameManager.getGame(player, id)
        if game:
            return game.resign(player)
        return 'No such game exists or you are not a player of it.'

    def gameState(self, player, id):
        game = self.gameManager.getGame(player, id)
        if game:
            return game.gameState()
        return 'No such game exists or you are not a player of it.'

class Message():
    
    def __init__(self, id, sender, receiver, message):
        self.id = id
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.read = False

    def to_dict(self):
        return {'id':self.id, 'sender':self.sender, 'receiver':self.receiver, 'message':self.message}
    

class Invite():
    
    def __init__(self, id, sender, receiver, title, gridsize):
        self.id = id
        self.sender = sender
        self.receiver = receiver
        self.title = title
        self.gridsize = gridsize
        self.accepted = False
        self.declined = False