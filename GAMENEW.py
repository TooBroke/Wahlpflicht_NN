from __future__ import print_function
from random import randint
from time import sleep
import time
from GAMEMODEL import *


class Game():
    def __init__(self, gui, w,  h):
        self.gui = gui
        self.w, self.h = w, h
        self.score = 0
        self.running = False
        self.useFastMode = False
        self.GUIDelay  = 0
        self.GameDelay = 0
        self.failures = 0
        self.lastGUIUpdate = time.clock()
        self.lastGameUpdate = time.clock()
        self.initGame()
        self.startGame()
        self.update()

    def initGame(self):
        self.gamefield = Gamefield(self.w, self.h)
#         self.gamefield.upperLeft.value = 1
#         self.gamefield.upperLeft.getSouthern(self.h).value = 1
#         self.running = True
        
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
        if self.lastGameUpdate*1000+self.GameDelay < time.clock()*1000:
            moved, addScore = self.gamefield.moveInDir(direction)
            self.score += addScore
            if moved:
                self.spawnNewElement()
                self.failures = 0
                self.update()
            else:
                self.failures += 1
            if self.failures > 10:
                self.running = False
            self.lastGameUpdate = time.clock()
            self.update()
        
    def spawnNewElement(self):
        val = 1
        if randint(0,100) > 90:
            val = 2
        if self.gamefield.hasFreeSpace():
            x,y = randint(0,self.w-1), randint(0,self.h-1)
            while(self.gamefield.get(x, y).value != 0):
                x,y = randint(0,self.w-1), randint(0,self.h-1)
            self.gamefield.get(x, y).value = val;
        else:
            self.running = False
            
    def restart(self):
        self.score = 0
        self.initGame()
        self.startGame()
        self.update(forced=True)
        
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
    def easy(self):
        south = 0
        for i in self.gamefield.upperLeft.getListOfDir(Dir.EAST):
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
        for i in self.gamefield.upperLeft.getSouthern(self.h).getListOfDir(Dir.EAST):
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
        for i in self.gamefield.upperLeft.getListOfDir(Dir.SOUTH):
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
        for i in self.gamefield.upperLeft.getEastern(self.h).getListOfDir(Dir.SOUTH):
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
    
    def test(self):
        a=[Dir.EAST,Dir.WEST,Dir.SOUTH,Dir.NORTH]
        return a[randint(0,3)]
        