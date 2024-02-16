import json
import time
import os

class GameManager():
    def __init__(self):
        self.games = []
        self.loadAllGames()

    def createGame(self, id, gridsize, title, players):
        game = SnakeGame(int(id), gridsize, title, players)
        self.games.append(game)
        return game

    def listGames(self, player):
        games = []
        for game in self.games:
            if player.name in game.players and not game.isGameOver:
                games.append(game.gameState())
        return games
    
    def listFinishedGames(self, player):
        games = []
        for game in self.games:
            if player.name in game.players and game.isGameOver:
                games.append(game.gameState())
        return games

    def getGame(self, player, id):
        for g in self.games:
            if id == g.id:
                if player.name in g.players:
                    return g
                return False
        return False
    
    def loadGame(self, id):
        jsfile = json.load(open(f'games/{id}.json', 'r'))

        if jsfile['isGameOver']:
            return
        
        game = SnakeGame(jsfile['id'], jsfile['gridsize'], jsfile['title'], jsfile['players'])
        game.loadGame(jsfile)

        self.games.append(game)
        return  

    def loadAllGames(self):
        for game in os.listdir('games'):
            print(game)
            f, ext = os.path.splitext(game)
            if ext == '.json':
                print(f'Loading game {f}.')
                self.loadGame(f)
    
class SnakeGame():

    def __init__(self, id, gridsize, title, players):

        self.id = id
        self.title = title
        self.gridsize = gridsize
        self.grid = Grid(gridsize)
        self.players = players
        self.turn = int(time.time() % 2)
        self.moves = []
        self.snakes = {players[0]: [[0,0]], players[1]: [[gridsize-1,gridsize-1]]}
        self.apple = [int(gridsize/2), int(gridsize/2)]
        self.isGameOver = False
        self.winner = None
          
        self.grid.write(self.apple[0], self.apple[1], 'a')
        self.grid.write(0, 0, players[0])
        self.grid.write(gridsize-1, gridsize-1, players[1])

        self.saveGame()

    def gameState(self):
        return {
            'id': self.id,
            'title': self.title,
            'gridsize': self.gridsize,
            'grid': self.grid.to_dict(),
            'players': self.players, 
            'turn': self.players[self.turn], 
            'moves': [m.to_dict() for m in self.moves],
            'snakes': self.snakes,
            'apple': self.apple,
            'isGameOver': self.isGameOver,
            'winner': self.winner
        }

    def loadGame(self, data):
        self.id = data['id']
        self.title = data['title']
        self.gridsize = data['gridsize']
        self.grid = Grid(data['gridsize'])
        self.grid.grid = data['grid']
        self.players = data['players']
        self.turn = data['players'].index(data['turn'])
        self.moves = [Move(m['player'], m['move']) for m in data['moves']]
        self.snakes = data['snakes']
        self.apple = data['apple']
        self.isGameOver = data['isGameOver']
        self.winner = data['winner']

    def saveGame(self):
        json.dump(self.gameState(), open(f'games/{self.id}.json', 'w'))

    def makeMove(self, player, move):
        
        if self.isGameOver:
            return 'The game is over.'
    
        if player.name != self.players[self.turn]:
            return 'It is not your turn.'
        
        self.moves.append(Move(player, move))
        self.gameCycle(self.moves[-1])

        self.turn = 1 - self.turn

        self.saveGame()
        return 'ok'
    
    def gameCycle(self, move):

        snake = self.snakes[move.player]
        head = snake[-1]        

        if move.move == 'up':
            snake.append([head[0]-1, head[1]])
        elif move.move == 'down':
            snake.append([head[0]+1, head[1]])
        elif move.move == 'left':
            snake.append([head[0], head[1]-1])
        elif move.move == 'right':
            snake.append([head[0], head[1]+1])
        else:
            return 'Invalid move.'
        
        if snake[-1] == self.apple:
            self.apple = self.newApple()
        else:
            snake.pop(0)
        
        if self.collision():
            self.isGameOver = True
            self.winner = self.players[1 - self.turn]
            return 'Game over.'
        
        self.grid.resetGrid()
        self.grid.write(self.apple[0], self.apple[1], 'a')

        for s in self.snakes:
            for x, y in self.snakes[s]:
                self.grid.write(x, y, s)

    def newApple(self):
        empty = self.grid.getEmpty()
        return empty[int(time.time() % len(empty))]

    def collision(self):
        head = self.snakes[self.players[self.turn]][-1]
        if head in self.snakes[self.players[1 - self.turn]]:
            return True
        if head[0] < 0 or head[0] >= self.gridsize or head[1] < 0 or head[1] >= self.gridsize:
            return True
        return False
    
    def resign(self, player):
        self.isGameOver = True
        self.winner = self.players[1 - self.players.index(player.name)]
        return 'ok'
    
class Move():
    def __init__(self, player, move):

        if type(player) == str:
            self.player = player
        else:
            self.player = player.name

        self.move = move
    
    def to_dict(self):
        return {
            'player': self.player,
            'move': self.move
        }

class Grid():
    def __init__(self, gridsize):
        self.gridsize = gridsize
        self.grid = [[0 for x in range(gridsize)] for y in range(gridsize)]

    def to_dict(self):
        return self.grid
    
    def write(self, x, y, value):
        self.grid[x][y] = value

    def getEmpty(self):
        empty = []
        for x in range(self.gridsize):
            for y in range(self.gridsize):
                if self.grid[x][y] == 0:
                    empty.append([x,y])
        return empty

    def read(self, x, y):
        return self.grid[x][y]

    def resetGrid(self):
        self.grid = [[0 for x in range(self.gridsize)] for y in range(self.gridsize)]