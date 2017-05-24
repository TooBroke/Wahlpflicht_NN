from __future__ import print_function
from random import randint
from GAMEMODEL import Dir, Gamefield


class Game():
    def __init__(self, gui, s):
        self.gui = gui
        self.size = s
        self.score = 0
        self.running = False
        self.failures = 0
        self.initGame()
        self.startGame()
        self.update()

    def initGame(self):
        self.gamefield = Gamefield(self.size, self.size)
        
    def startGame(self):
        self.spawnNewElement()
        self.spawnNewElement()
        self.running = True

    def update(self, forced = False):
        if self.gui is not None:
            self.gui.update(self.gamefield, forced)

    def getMap(self):
        return self.gamefield
    
    def move(self, direction):
        moved, addScore = self.gamefield.moveInDir(direction)
        self.score += addScore
        if moved:
            self.spawnNewElement()
            self.failures = 0
        else:
            self.failures += 1
        if self.failures >= 2:
            self.running = False
        self.update()
        
    def spawnNewElement(self):
        if randint(0,100) > 90:
            value = 2
        else:
            value = 1
        if self.gamefield.hasFreeSpace():
            x,y = randint(0,self.size-1), randint(0,self.size-1)
            while(self.gamefield.get(x, y).value != 0):
                x,y = randint(0,self.size-1), randint(0,self.size-1)
            self.gamefield.get(x, y).value = value;
        else:
            self.running = False
            
    def restart(self):
        self.score = 0
        self.initGame()
        self.startGame()
        self.update()
        
    def getMaxNumber(self):
        return 2**max(self.gamefield.getAs1DArray())
        
    def getScore(self):
        return self.score
        
    def isFinished(self):
        return not self.running
    
    def runGame(self, func):
        self.restart()
        while(self.running):
            self.move(func())
            
        return self.score
    
    def simpleAI(self, gamefield):
        south = 0
        for i in gamefield.upperLeft.getListOfDir(Dir.EAST):
            last = 0
            current = i
            while current != None:
                if last != 0 and current.value != 0:
                    if last == current.value:
                        south += last
                if current.value != 0:
                    last = current.value
                current = current.getInDir(Dir.SOUTH)
        north = 0
        for i in gamefield.upperLeft.getSouthern(self.size).getListOfDir(Dir.EAST):
            last = 0
            current = i
            while current != None:
                if last != 0 and current.value != 0:
                    if last == current.value:
                        north += last
                if current.value != 0:
                    last = current.value
                current = current.getInDir(Dir.NORTH)
        east = 0
        for i in gamefield.upperLeft.getListOfDir(Dir.SOUTH):
            last = 0
            current = i
            while current != None:
                if last != 0 and current.value != 0:
                    if last == current.value:
                        east += last
                if current.value != 0:
                    last = current.value
                current = current.getInDir(Dir.EAST)
        west = 0
        for i in gamefield.upperLeft.getEastern(self.size).getListOfDir(Dir.SOUTH):
            last = 0
            current = i
            while current != None:
                if last != 0 and current.value != 0:
                    if last == current.value:
                        west += last
                if current.value != 0:
                    last = current.value
                current = current.getInDir(Dir.WEST)
        a = [north, south, east, west]
        if max(a) == south and south != 0:
            return Dir.SOUTH
        elif max(a) == east and east != 0:
            return Dir.EAST
        elif max(a) == west and west != 0:
            return Dir.WEST
        elif max(a) == north and north != 0:
            return Dir.NORTH
        else:
            if self.failures < 5:
                return Dir.SOUTH
            else:
                a=[Dir.EAST,Dir.WEST,Dir.SOUTH,Dir.NORTH]
                return a[randint(0,3)]
    
    def randomAI(self, gamefield):
        a=[Dir.EAST,Dir.WEST,Dir.SOUTH,Dir.NORTH]
        return a[randint(0,3)]
    
    def testAI(self, gamefield):
        return Dir.SOUTH
        