import wx
from random import randint
from time import sleep
import time
class Dir():
    NORTH = 0,
    EAST = 1,
    SOUTH = 2,
    WEST = 3

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
        gamefield = []
        for i in range(self.w):
            gamefield.append([0 for n in range(self.h)])
        self.gamefield = gamefield
        
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
            if self.moveGamefield(direction):
                self.spawnNewElement()
                self.failures = 0
                self.update()
            else:
                self.failures += 1
            if self.failures > 10:
                self.running = False
            self.lastGameUpdate = time.clock()
            print(self.score)
        
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
                if self.gamefield[x][y] != 0:
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
                if self.gamefield[xcur+xdir][ycur+ydir] == 0:
                    xcur += xdir
                    ycur += ydir
                elif self.gamefield[xcur+xdir][ycur+ydir] == self.gamefield[x][y]:
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
            cur = self.gamefield[xcur][ycur]
            if cur == 0:
                self.gamefield[xcur][ycur] = self.gamefield[x][y]
                self.gamefield[x][y] = 0
            elif cur == self.gamefield[x][y]:
                self.gamefield[xcur][ycur] += 1
                self.gamefield[x][y] = 0
                self.score += 2**self.gamefield[xcur][ycur]
            return True
        
    def hasFreeSpace(self):
        for x in range(self.w):
            for y in range(self.h):
                if self.gamefield[x][y] == 0:
                    return True
        return False
    
    def spawnNewElement(self):
        val = 1
        if randint(0,100) > 90:
            val = 2
        if self.hasFreeSpace():
            x,y = randint(0,self.w-1), randint(0,self.h-1)
            while(self.gamefield[x][y] != 0):
                x,y = randint(0,self.w-1), randint(0,self.h-1)
            self.gamefield[x][y] = val;
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
        values = [0,0,0,0]
        for x in range(self.w):
            for y in range(self.h):
                nei = self.getNeighbor(x, y)
                for i in range(4):
                    values[i] += nei[i]
        result = values.index(max(values))
        if result == 0:
            return Dir.NORTH
        elif result == 1:
            return Dir.EAST
        elif result == 2:
            return Dir.SOUTH
        else:
            return Dir.WEST
    
    def test(self):
        return Dir.SOUTH
    
    def getNeighbor(self, x, y):
        result = []
        #NORTH
        for i in range(y,0,-1):
            if self.gamefield[x][i] != 0:
                result.append(1)
                break
        if len(result) == 0:
            result.append(0)
        #EAST
        for i in range(x,self.w):
            if self.gamefield[i][y] != 0:
                result.append(1)
                break
        if len(result) == 1:
            result.append(0)
        #SOUTH
        for i in range(y,self.h):
            if self.gamefield[x][i] != 0:
                result.append(1)
                break
        if len(result) == 2:
            result.append(0)
        #WEST
        for i in range(x,0,-1):
            if self.gamefield[i][y] != 0:
                result.append(1)
                break
        if len(result) == 3:
            result.append(0)
        return result
        
        
    def handleInput(self, event):
        key = event.GetKeyCode()
        if self.running:
            if key == ord('W'):
                self.move(Dir.NORTH)
            elif key == ord('A'):
                self.move(Dir.WEST)
            elif key == ord('S'):
                self.move(Dir.SOUTH)
            elif key == ord('D'):
                self.move(Dir.EAST)
            self.update()
        if key == ord('R'):
            self.restart()
        if key == ord('G'):
            print(self.runGame(self.easy))
            self.update()
        event.Skip()