'''
Created on 23.02.2017

@author: Broke
'''
import wx
from GAMENEW import Game

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
    aiList = dict(test="self.game.test",
                  simple="self.game.easy")

    def __init__(self):
        super(Frame, self).__init__(None)
        self.SetTitle('2048')
        self.menuWidth = 100
        self.initElements()
        self.game = Game(self, 4,4)

        self.doBindings()
        self.doLayout()
        self.CenterOnScreen()
        self.SetBackgroundColour(wx.WHITE)

    def initElements(self):
        self.guiElements = []
        self.view = Canvas(self)
        self.guiElements.append(self.view)
        self.scoreLabel = wx.StaticText(self, label="blub", size=(self.menuWidth,-1))
        self.scoreLabel.SetBackgroundColour(wx.WHITE)
        self.guiElements.append(self.scoreLabel)
        self.restartButton = wx.Button(self, label="RESTART", size=(self.menuWidth,-1))
        self.guiElements.append(self.restartButton)
        self.runButton = wx.Button(self, label="run AI", size=(self.menuWidth,-1))
        self.guiElements.append(self.runButton)
        #Combobox
        self.comboboxAI = wx.ComboBox(self, style=wx.CB_DROPDOWN | wx.CB_READONLY, choices=self.aiList.keys(), size=(self.menuWidth, -1))
        self.comboboxAI.SetSelection(0)
        self.guiElements.append(self.comboboxAI)

    def doBindings(self):
        for element in self.guiElements:
            element.Bind(wx.EVT_KEY_DOWN, self.game.handleInputEvent)
        self.Bind(wx.EVT_KEY_DOWN, self.game.handleInputEvent)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.restartButton.Bind(wx.EVT_BUTTON, self.restart)
        self.runButton.Bind(wx.EVT_BUTTON, self.runAI)
        
    def restart(self, event):
        self.game.handleInput(ord('R'))
        
    def runAI(self, event):
        self.game.runGame(eval(self.aiList[self.comboboxAI.GetValue()]))
        self.game.update()

    def doLayout(self):
        menuBox = wx.BoxSizer(wx.VERTICAL)
        menuBox.Add(self.scoreLabel, 1, wx.EXPAND)
        menuBox.Add(self.restartButton)
        menuBox.Add(self.runButton)
        menuBox.Add(self.comboboxAI)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.view, 1, wx.EXPAND)
        hbox.Add(menuBox, 0, wx.EXPAND)

        self.SetSizer(hbox)

    def view_on_key(self, event):
        if (event.GetKeyCode() == wx.WXK_UP):
            self.refresh()

    def on_size(self, event):
        w, h = event.GetSize()
        s = max([w-self.menuWidth,h])
        self.SetSize((s+self.menuWidth-15,s))
        self.refresh(self.view.gamefield)
        event.Skip()
        #self.Refresh()

    def refresh(self, gamefield):
        self.view.gamefield = gamefield
        self.view.Refresh()
        if(self.game):
            a = "Score:\t"+self.getScoreAsString(self.game.getScore())
            a += "\nFailures: "+str(self.game.failures)
            a += "\nRunning: "+str(self.game.running)
            self.scoreLabel.SetLabel(a)

    def getScoreAsString(self, score):
        r = str(score)
        return ("0"*(6-len(r)))+r

    def on_start(self, event):
        pass
    def on_reset(self, event):
        self.refresh()



app = wx.App()
top = Frame()
top.Show()
app.MainLoop()
