'''
Created on 06.04.2017

@author: Broke
'''

class Dir():
    NORTH = 0,
    EAST = 1,
    SOUTH = 2,
    WEST = 3

class Gamefield:
    
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.upperLeft = Segment()
        self.initGamefield()
        
    def initGamefield(self):
        current = self.upperLeft
        for i in range(self.height-1):
            current.south = Segment()
            current.south.north = current
            current = current.south
        for y in range(self.height):
            current = self.upperLeft.getSouthern(y)
            for x in range(self.width-1):
                current.east = Segment()
                current.east.west = current
                if current.north != None:
                    current.north.east.south = current.east
                    current.east.north = current.north.east
                current = current.east
                
    def isEmpty(self):
        if self.upperLeft.north == None and self.upperLeft.east == None and self.upperLeft.south == None and self.upperLeft.west == None:
            return True
        else:
            return False
        
    def hasFreeSpace(self):
        segList = self.getListOfAllSegments()
        for i in segList:
            if i.value == 0:
                return True
        return False
        
    def getListOfAllSegments(self):
        result = []
        current = self.upperLeft
        while current != None:
            extendList = current.getListOfDir(Dir.SOUTH)
            if extendList != None:
                result.extend(extendList)
            current = current.getInDir(Dir.EAST)
        return result
    
    def get(self, x, y):
        return self.upperLeft.getSouthern(y).getEastern(x)
    
    def getValue(self, x, y):
        return self.get(x,y).value
    
    def getComplementListOfDirection(self, direction):
        if direction == Dir.SOUTH:
            return self.upperLeft.getSouthern(self.height).getListOfDir(Dir.EAST)
        elif direction == Dir.NORTH:
            return self.upperLeft.getListOfDir(Dir.EAST)
        elif direction == Dir.WEST:
            return self.upperLeft.getListOfDir(Dir.SOUTH)
        else:
            return self.upperLeft.getEastern(self.height).getListOfDir(Dir.SOUTH)
        
    def getComplementDirection(self, direction):
        if direction == Dir.SOUTH:
            return Dir.NORTH
        elif direction == Dir.NORTH:
            return Dir.SOUTH
        elif direction == Dir.WEST:
            return Dir.EAST
        else:
            return Dir.WEST
        
    def moveInDir(self, direction):
        moved = False
        score = 0
        segList = self.getComplementListOfDirection(direction)
        comDir = self.getComplementDirection(direction)
        for seg in segList:
            current = seg
            #Add sums together
            while current != None:
                tempSeg = current.getInDir(comDir)
                while tempSeg != None and tempSeg.value == 0:
                    tempSeg = tempSeg.getInDir(comDir)
                if tempSeg != None:
                    if tempSeg.value == current.value:
                        current.value += 1
                        tempSeg.value = 0
                        score += 2**current.value
                        moved = True
                current = current.getInDir(comDir)
            #Move Segments
            current = seg
            while current != None:
                tempSeg = current
                while tempSeg != None and tempSeg.value == 0:
                    tempSeg = tempSeg.getInDir(comDir)
                if tempSeg != None:
                    if tempSeg != current:
                        moved = True
                    a = tempSeg.value
                    tempSeg.value = 0
                    current.value = a
                current = current.getInDir(comDir)
        return moved, score

                
    def moveToDir(self, segment, direction):
        current = segment
        next = segment.getInDir(direction)
        while next != None and next.value == 0:
            next.value = current.value
            current.value = 0
            current = next
            next = next.getInDir(direction)
            
    def getAs2DArray(self):
        segList = self.upperLeft.getListOfDir(Dir.SOUTH)
        result = []
        for line in range(self.height):
            result.append([])
            current = segList[line]
            for seg in current.getListOfDir(Dir.EAST):
                result[line].append(seg.value)
        return result
    
    def getAs1DArray(self):
        segList = self.upperLeft.getListOfDir(Dir.SOUTH)
        result = []
        for line in range(self.height):
            current = segList[line]
            for seg in current.getListOfDir(Dir.EAST):
                result.append(seg.value)
        return result
    
    
    
class Segment:
    
    def __init__(self):
        self.value = 0
        self.north = None
        self.south = None
        self.west = None
        self.east = None
        
    def getInDir(self, direction):
        if direction == Dir.NORTH:
            return self.north
        elif direction == Dir.SOUTH:
            return self.south
        elif direction == Dir.EAST:
            return self.east
        else:
            return self.west
        
    def getNeighbors(self):
        result = []
        if self.north != None:
            result.append(self.north)
        if self.south != None:
            result.append(self.south)
        if self.east != None:
            result.append(self.east)
        if self.west != None:
            result.append(self.west)
        return result
        
    def getListOfDir(self, direction):
        """
        Returns a list of all elements in this direction.
        Includes this object
        """
        result = []
        result.append(self)
        current = self
        while current.getInDir(direction) != None:
            result.append(current.getInDir(direction))
            current = current.getInDir(direction)
        return result
            
    def getSouthern(self, index):
        current = self
        for i in range(index):
            if current.south != None:
                current = current.south
        return current
    
    def getWestern(self, index):
        current = self
        for i in range(index):
            if current.west != None:
                current = current.west
        return current
    
    def getEastern(self, index):
        current = self
        for i in range(index):
            if current.east != None:
                current = current.east
        return current
    
    def getNorthern(self, index):
        current = self
        for i in range(index):
            if current.north != None:
                current = current.north
        return current

