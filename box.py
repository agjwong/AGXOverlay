import wx
import win32gui

def GetRoundBitmap( w, h, r ):
    maskColor = wx.Color(0,0,0)
    shownColor = wx.Color(5,5,5)
    b = wx.EmptyBitmap(w,h)
    dc = wx.MemoryDC(b)
    dc.SetBrush(wx.Brush(maskColor))
    dc.DrawRectangle(0,0,w,h)
    dc.SetBrush(wx.Brush(shownColor))
    dc.SetPen(wx.Pen(shownColor))
    dc.DrawRoundedRectangle(0,0,w,h,r)
    dc.SelectObject(wx.NullBitmap)
    b.SetMaskColour(maskColor)
    return b

def GetRoundShape( w, h, r ):
    return wx.RegionFromBitmap( GetRoundBitmap(w,h,r) )

def captureAuditionWindow(mainframe):
    win32gui.EnumWindows(_setMainFrame, mainFrame)

def setPositions(frame):
    win32gui.EnumWindows(_setPositions, frame)

def _setMainFrame(hwnd, mainFrame):
    if win32gui.GetWindowText(hwnd) == "Audition Galaxy": 
        mainFrame.AssociateHandle(hwnd)

def _setPositions(hwnd, f):
    
    if win32gui.GetWindowText(hwnd) == "Audition Galaxy": 
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y

        f.SetSize(w, h)
        f.SetPosition((x,y))

class FancyFrame(wx.Frame):
    def __init__(self, mainFrame):
        style = ( wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR |
                  wx.NO_BORDER | wx.FRAME_SHAPED  )
        wx.Frame.__init__(self, mainFrame, title='Fancy', style = style)

        self.SetTransparent( 220 )

        # self.Bind(wx.EVT_KEY_UP, self.OnKeyDown)
        # self.Bind(wx.EVT_SET_FOCUS, self.SetParentFocus)
        # self.Bind(wx.EVT_MOTION, self.OnMouse)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        # self.Disable()
        self.Show(True)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc = wx.GCDC(dc)
        w, h = self.GetSizeTuple()
        r = 10
        dc.SetPen( wx.Pen("#806666", width = 2 ) )
        dc.SetBrush( wx.Brush("#80A0B0") )
        dc.DrawRoundedRectangle( 0,0,w,h,r )

    # def OnParentMove(self, event):
    #     print("parent moves")
    #     rect = event.getRect()
    #     x = rect[0]
    #     y = rect[1]
    #     w = rect[2] - x
    #     h = rect[3] - y

    #     self.SetSize(w, h)
    #     self.SetPosition((x,y))

    def OnKeyDown(self, event):
        """quit if user press q or Esc"""
        print(event)
        if event.GetKeyCode() == 27 or event.GetKeyCode() == ord('Q'): #27 is Esc
            self.Close(force=True)
        elif event.GetKeyCode() == ord('A'):
            self.Show(True)
        else:
            event.Skip()

    def OnMouse(self, event):
        """implement dragging"""
        if not event.Dragging():
            self._dragPos = None
            return
        self.CaptureMouse()
        if not self._dragPos:
            self._dragPos = event.GetPosition()
        else:
            pos = event.GetPosition()
            displacement = self._dragPos - pos
            self.SetPosition( self.GetPosition() - displacement )

app = wx.App()
mainFrame = wx.Frame(None)
captureAuditionWindow(mainFrame)
f = FancyFrame(mainFrame)
setPositions(f)

# mainFrame.Bind(wx.EVT_MOVE, f.OnParentMove)
app.MainLoop()