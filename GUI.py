import wx
from wx.lib.intctrl import IntCtrl
import threading
import time
from GAMELOGIC import Dir, Game

aiEvent = wx.NewEventType()
EVT_AI = wx.PyEventBinder(aiEvent, 1)

class AIThread(threading.Thread):
    def __init__(self, parent, games, func):
        threading.Thread.__init__(self)
        self.parent=parent
        self.gameCount = games
        self.calcMove = func
        self.working = True
        
    def run(self):
        loops = int(self.parent.menu.runCountCtrl.GetValue())
        i = -1
        while i < loops and self.working:
            if self.parent.game.isFinished():
                self.parent.restartGame(ai=True)
            while not self.parent.game.isFinished():
                sleepTime = int(self.parent.menu.aiSpeedCtrl.GetValue())
                if sleepTime != 0:
                    time.sleep(sleepTime/1000.0)
                if self.working:
                    evt = MoveEvent(aiEvent, -1, self.calcMove(self.parent.game.gamefield))
                    wx.PostEvent(self.parent, evt)
                else:
                    break
            if loops == 0:
                i-=1
            else:
                i+=1
        self.parent.update(forced=True)
        
    def stop(self):
        self.working = False
        
class MoveEvent(wx.PyCommandEvent):
    
    def __init__(self, etype, eid, direction):
        wx.PyCommandEvent.__init__(self, etype, eid)
        self.direction = direction
        
    def GetValue(self):
        return self.direction
    
class MenuPanel(wx.Panel):
    
    width = 100
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        
        #Attributes
        self.scoreLabel = wx.StaticText(self, label="blub", size=(self.width,-1))
        self.scoreLabel.SetBackgroundColour(wx.WHITE)
        self.add(self.scoreLabel)
        self.aiSpeedLabel = wx.StaticText(self, label="AISpeed", size=(self.width/2,-1))
        self.add(self.aiSpeedLabel)
        self.aiSpeedCtrl = IntCtrl(self, size=(self.width/2,-1))
        self.add(self.aiSpeedCtrl)
        self.aiSelectLabel = wx.StaticText(self, label="AI", size=(self.width/4,-1))
        self.add(self.aiSelectLabel)
        self.aiSelectCB = wx.ComboBox(self, style=wx.CB_DROPDOWN | wx.CB_READONLY, choices=self.parent.aiList.keys(), size=(self.width/4*3,-1))
        self.aiSelectCB.SetSelection(3)
        self.add(self.aiSelectCB)
        self.runCountLabel = wx.StaticText(self, label="Runs", size=(self.width/2,-1))
        self.add(self.runCountLabel)
        self.runCountCtrl = IntCtrl(self, size=(self.width/2,-1))
        self.add(self.runCountCtrl)
        self.runAIButton = wx.Button(self, label="Run AI", size=(self.width,-1))
        self.add(self.runAIButton)
#         self.trainAIButton = wx.Button(self, label="Train AI", size=(self.width,-1))
#         self.add(self.trainAIButton)
        self.stopAIButton = wx.Button(self, label="Stop AI", size=(self.width,-1))
        self.add(self.stopAIButton)
        self.restartButton = wx.Button(self, label="Restart", size=(self.width,-1))
        self.add(self.restartButton)

        #Layout
        self.__doLayout()
        
        #Event Handlers
        self.restartButton.Bind(wx.EVT_BUTTON, self.parent.onRestart)
        self.runAIButton.Bind(wx.EVT_BUTTON, self.parent.onRunAI)
        self.stopAIButton.Bind(wx.EVT_BUTTON, self.parent.onStopAI)
        
        
    def __doLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        aiSpeedSizer = wx.BoxSizer(wx.HORIZONTAL)
        aiSpeedSizer.AddMany([(self.aiSpeedLabel), (self.aiSpeedCtrl, 1, wx.EXPAND)])
        aiSelectSizer = wx.BoxSizer(wx.HORIZONTAL)
        aiSelectSizer.AddMany([(self.aiSelectLabel),(self.aiSelectCB, 1, wx.EXPAND)])
        runCountSizer = wx.BoxSizer(wx.HORIZONTAL)
        runCountSizer.AddMany([(self.runCountLabel), (self.runCountCtrl, 1, wx.EXPAND)])
        
        sizer.AddMany([(self.scoreLabel, 1, wx.EXPAND),
                       (aiSpeedSizer),
                       (aiSelectSizer),
                       (runCountSizer),
                       (self.runAIButton),
#                        (self.trainAIButton),
                       (self.stopAIButton),
                       (self.restartButton)])
        self.SetSizer(sizer)
        
    
    def add(self, element):
        self.parent.guiElements.append(element)
        
    def getCB(self):
        return self.aiSelectCB.GetValue()
        
    
class Canvas(wx.Panel):
    def __init__(self, parent):
        super(Canvas, self).__init__(parent)
        self.parent = parent
        self.fontSize = 36
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.gamefield = []
        self.SetBackgroundColour(wx.WHITE)


    def on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        if self.gamefield.width > 0:
            sw, sh = self.GetSize()
            gfw, gfh = self.gamefield.width,self.gamefield.height
            divisor = sw if sw<sh else sh
            w, h = divisor//gfw, divisor//gfh
            cx = abs(sw-sh)/2 if sw>sh else 0
            cy = abs(sw-sh)/2 if sh>sw else 0
            border = 5
            for x in range(gfw):
                for y in range(gfh):
                    val = 2**self.gamefield.getValue(x,y)
                    if val == 1:
                        dc.SetPen(wx.Pen((100,100,100), border))
                    else:
                        dc.SetPen(wx.Pen(wx.BLACK, border))
                    dc.DrawRectangle(cx+x*w+border/2,cy+y*h+border/2,w-border,h-border)
                    dc.SetFont(wx.Font(self.fontSize, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
                    if val != 1:
                        xtxt = cx + x * w + (w/2 - dc.GetTextExtent(str(val))[0]/2)
                        ytxt =  cy + y * h + (h / 2 - dc.GetTextExtent(str(val))[1]/2)
                        dc.DrawText(str(val), xtxt, ytxt)
        else:
            pass

class Frame(wx.Frame):

    game = None
    worker = None
    nextGUIUpdate = time.clock()
    fps = 10
    gameNumber = 0
    average = []
    aiList = dict(randomAI="self.game.randomAI", 
                  simpleAI="self.game.simpleAI",
                  geneticNN="self.executeNN",
                  testAI="self.game.testAI")

    def __init__(self):
        super(Frame, self).__init__(None)
        self.SetTitle('2048')
        self.menuWidth = 100
        self.initElements()
        self.game = Game(self, 4)

        self.doBindings()
        self.doLayout()
        self.CenterOnScreen()
        self.SetBackgroundColour(wx.WHITE)
        self.update(self.game.gamefield, True)

    def initElements(self):
        self.guiElements = []
        self.view = Canvas(self)
        self.guiElements.append(self.view)
        self.menu = MenuPanel(self)

    def doBindings(self):
        for element in self.guiElements:
            element.Bind(wx.EVT_KEY_DOWN, self.handleInputEvent)
        self.Bind(wx.EVT_KEY_DOWN, self.handleInputEvent)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(EVT_AI, self.onMove)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        
    def onRestart(self, event):
        self.stopWorker()
        self.restartGame()
    
    def onRunAI(self, event):
        self.gameNumber = 0
        self.average = []
        self.worker = AIThread(self, 2, eval(self.aiList[self.menu.getCB()]))
        self.worker.start()
    
    def onTrainAI(self, event):
        pass
        
    def onMove(self, event):
        self.game.move(event.GetValue())
        
    def onStopAI(self, event):
        self.stopWorker()
        
    def restartGame(self, ai=False):
        if ai:
            self.gameNumber += 1
            self.average.append(self.game.score)
        else:
            self.gameNumber = 0
            self.average = []
        self.game.restart()
        
    def stopWorker(self):
        if self.worker != None and self.worker.is_alive() :
            self.worker.stop()
            self.update(forced=True)
        
    def doLayout(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.view, 1, wx.EXPAND)
        hbox.Add(self.menu, 0, wx.EXPAND)
        self.SetSizer(hbox)

    def onSize(self, event):
        w, h = event.GetSize()
        s = max([w-self.menuWidth,h])
        self.SetSize((s+self.menuWidth-15,s))
        self.update(self.view.gamefield)
        event.Skip()
        #self.Refresh()
        
    def onClose(self, event):
        self.stopWorker()
        self.Destroy()
        
    def executeNN(self, gamefield):
        from NN_GENETIC_FOR_GUI import moveNN
        return moveNN(gamefield)
        
    def update(self, gamefield=None, forced = False):
        if time.clock() >= self.nextGUIUpdate or forced:
            if gamefield != None:
                self.view.gamefield = gamefield
                self.view.Refresh()
            if self.game:
                if self.menu.scoreLabel.GetLabel() is not self.getScoreString():
                    self.menu.scoreLabel.SetLabel(self.getScoreString())
            self.nextGUIUpdate = time.clock() + 1.0/self.fps

    def getScoreString(self):
            s = "Score:\t"+self.getScoreAsString(self.game.getScore())
            s += "\nFailures: "+str(self.game.failures)
            s += "\nRunning: "+str(self.game.running)
            if self.gameNumber > 0:
                s += "\n Game "+str(self.gameNumber)
            if len(self.average)>0:
                s += "\n Avg Score: "+str(sum(self.average)/len(self.average))
            return s

    def getScoreAsString(self, score):
        r = str(score)
        return ("0"*(6-len(r)))+r
    
    def handleInputEvent(self, event):
        self.handleInput(event.GetKeyCode())
        event.Skip()
        
    def handleInput(self, c):
        if not self.game.isFinished():
            if c == ord('W'):
                self.game.move(Dir.NORTH)
            elif c == ord('A'):
                self.game.move(Dir.WEST)
            elif c == ord('S'):
                self.game.move(Dir.SOUTH)
            elif c == ord('D'):
                self.game.move(Dir.EAST)
        if c == ord('R'):
            self.stopWorker()
            self.restartGame()


app = wx.App()
top = Frame()
top.Show()
app.MainLoop()
