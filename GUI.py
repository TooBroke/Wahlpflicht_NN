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
        self.bgc = wx.GREEN
        self.w, self.h = 4,4
        self.labels, self.panels = self.doElements()
        self.game = Game(self, self.w, self.h)
        
        self.doBindings()
        self.doLayout()
        self.CenterOnScreen()
        
    def doElements(self):
        labels = []
        panels = []
        for i in range(self.w*self.h):
            p = wx.Panel(self)
            p.SetBackgroundColour(self.bgc)
            panels.append(p)
            t = wx.StaticText(p, label="0", style=wx.ALIGN_CENTER)
            t.SetBackgroundColour(wx.RED)
            labels.append(t)
        return labels, panels

    def doBindings(self):
        self.Bind(wx.EVT_KEY_DOWN, self.game.handleInput)
        for i in range(self.w*self.h):
            self.panels[i].Bind(wx.EVT_KEY_DOWN, self.game.handleInput)
            self.labels[i].Bind(wx.EVT_KEY_DOWN, self.game.handleInput)

    def doLayout(self):
        vboxGf = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self)
        for n in range(self.h):
            hbox = wx.StaticBoxSizer(wx.VERTICAL, panel)
            for i in range(n*self.h, n*self.h+self.w):
                #pbox = wx.BoxSizer(wx.HORIZONTAL)
                #pbox.Add(self.labels[i], 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
                #self.panels[i].SetSizer(pbox)
                hbox.Add(self.labels[i], 1, wx.ALIGN_CENTER)
            vboxGf.Add(hbox, 1, wx.EXPAND)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(vboxGf, 1, wx.EXPAND)
        self.SetSizer(hbox)
        self.Layout()

    def view_on_key(self, event):
        if (event.GetKeyCode() == wx.WXK_UP):
            self.refresh()

    def on_size(self, event):
        event.Skip()
        self.refresh()

    def refresh(self, gamefield):
        for x in range(self.w):
            for y in range(self.h):
                if gamefield[x][y] == 0:
                    self.labels[x*self.w+y].SetLabel("halp")
                else:
                    self.labels[x*self.w+y].SetLabel(str(2**gamefield[x][y]))

    def on_start(self, event):
        pass
    def on_reset(self, event):
        self.refresh()



app = wx.App()
top = Frame()
top.Show()
app.MainLoop()