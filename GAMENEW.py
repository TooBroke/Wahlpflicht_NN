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
        self.update()

    def initGame(self):
        self.gamefield = Gamefield(self.w, self.h)
#         self.gamefield.upperLeft.value = 1
#         self.gamefield.upperLeft.getSouthern(self.h).value = 1
#         self.running = True
        
    def startGame(self):
        self.running = True
        self.spawnNewElement()
        self.spawnNewElement()

    def update(self, force = False):
        self.gui.refresh(self.gamefield)
        self.lastGUIUpdate = time.clock()

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
        
    def moveGamefield(self, direction):
        moved = False
        xr, yr = [],[]
        if direction == Dir.SOUTH:
            xr = range(self.w)
            yr = range(self.h-1,-1,-1)
        if direction == Dir.EAST:
            xr = range(self.w-1,-1,-1)
            yr = range(self.h)
        if direction in [Dir.NORTH, Dir.WEST]:
            xr = range(self.w)
            yr = range(self.h)
        for x in xr:
            for y in yr:
                if self.gamefield.getValue(x,y) != 0:
                    if self.moveElement(x,y,direction):
                        moved = True
        return moved
                        
    def moveElement(self, x, y, direction):
        xdir,ydir = 0,0
        if direction == Dir.NORTH:
            ydir = -1
        elif direction == Dir.SOUTH:
            ydir = 1
        elif direction == Dir.WEST:
            xdir = -1
        elif direction == Dir.EAST:
            xdir = 1
        xcur,ycur = x,y
        running = True
        while running:
            if(-1 < xcur+xdir < self.w and -1 < ycur+ydir < self.h):
                if self.gamefield.getValue(xcur+xdir,ycur+ydir) == 0:
                    xcur += xdir
                    ycur += ydir
                elif self.gamefield.getValue(xcur+xdir,ycur+ydir) == self.gamefield.getValue(x, y):
                    xcur += xdir
                    ycur += ydir
                    running = False                 
                else:
                    running = False
            else:
                running = False
        if xcur == x and ycur == y:
            return False
        else:
            cur = self.gamefield.getValue(xcur, ycur)
            if cur == 0:
                self.gamefield.get(xcur,ycur).value = self.gamefield.getValue(x,y)
                self.gamefield.get(x,y).value = 0
            elif cur == self.gamefield.getValue(x, y):
                self.gamefield.get(xcur,ycur).value += 1
                self.gamefield.get(x,y).value = 0
                self.score += 2**self.gamefield.getValue(xcur,ycur)
            return True
    
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
        self.running = True
        self.initGame()
        self.startGame()
        self.update()
        
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
        print(randint(0,3))
        return a[randint(0,3)]
        
    def handleInputEvent(self, event):
        self.handleInput(event.GetKeyCode())
        event.Skip()
        
    def handleInput(self, c):
        if self.running:
            if c == ord('W'):
                self.move(Dir.NORTH)
            elif c == ord('A'):
                self.move(Dir.WEST)
            elif c == ord('S'):
                self.move(Dir.SOUTH)
            elif c == ord('D'):
                self.move(Dir.EAST)
            self.update()
        if c == ord('R'):
            self.restart()
        if c == ord('G'):
            print(self.runGame(self.easy))
            self.update()