import wx
from wx import xrc

class App(wx.App):
    a = 5

    def OnInit(self):
        self.res = xrc.XmlResource('gui.xrc')
        self.initFrame()
        return True
    
    def initFrame(self):
        self.frame = self.res.LoadFrame(None, 'mainFrame')
        self.frame.Bind(wx.EVT_BUTTON, self.calculate, id=xrc.XRCID('button'))
        self.frame.Show()

    def calculate(self, event):
        a = 5

if __name__ == '__main__':
    app = App(0)
    app.MainLoop()
