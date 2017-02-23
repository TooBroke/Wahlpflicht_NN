'''
Created on 23.02.2017

@author: Broke
'''
import wx
from GAME import Game

class Canvas(wx.Panel):
    def __init__(self, parent):
        super(Canvas, self).__init__(parent)
        self.parent = parent
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.gamefield = []
        
    def on_size(self, event):
        event.Skip()
        self.Refresh()
        
    def on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        if len(self.gamefield) > 0:
            sw, sh = self.GetSize()
            gfw, gfh = len(self.gamefield[0]), len(self.gamefield)
            divisor = sw if sw<sh else sh
            w, h = divisor//gfw, divisor//gfh
            cx = abs(sw-sh)/2 if sw>sh else 0
            cy = abs(sw-sh)/2 if sh>sw else 0
            border = 5
            for x in range(gfw):
                for y in range(gfh):
                    val = 2**self.gamefield[x][y]
                    if val == 1:
                        dc.SetPen(wx.Pen((100,100,100), border))
                    else:
                        dc.SetPen(wx.Pen(wx.BLACK, border))
                    dc.DrawRectangle(cx+x*w+border/2,cy+y*h+border/2,w-border,h-border)
                    dc.SetFont(wx.Font(26, wx.SWISS, wx.NORMAL, wx.BOLD))
                    if val != 1:
                        dc.DrawText(str(val), cx + x * w + (w / 2 - 13), cy + y * h + (h / 2 - 13))
        else:
            pass

class Frame(wx.Frame):

    def __init__(self):
        super(Frame, self).__init__(None)
        self.SetTitle('2048')
        self.view = Canvas(self)
        self.game = Game(self, 4,4)
        
        self.doBindings()
        self.doLayout()
        self.CenterOnScreen()

    def doBindings(self):
        self.view.Bind(wx.EVT_KEY_DOWN, self.game.handleInput)

    def doLayout(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.view, 1, wx.EXPAND)
        self.SetSizer(hbox)

    def view_on_key(self, event):
        if (event.GetKeyCode() == wx.WXK_UP):
            self.refresh()

    def on_size(self, event):
        event.Skip()
        self.refresh()

    def refresh(self, gamefield):
        self.view.gamefield = gamefield
        self.view.Refresh()

    def on_start(self, event):
        pass
    def on_reset(self, event):
        self.refresh()



app = wx.App()
top = Frame()
top.Show()
app.MainLoop()