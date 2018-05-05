import wx
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class Mywin(wx.Frame): 
    def __init__(self, parent, title): 
      super(Mywin, self).__init__(parent, title = title,size = (500,500))
      panel = wx.Panel(self) 
      vbox = wx.BoxSizer(wx.VERTICAL) 

      self.dots = []

      # boton para abrir archivo
      self.btn2 = wx.Button(panel, 5, label='Abrir archivo .txt')
      vbox.Add(self.btn2,0,wx.ALIGN_CENTER) 
      self.btn2.Bind(wx.EVT_BUTTON, self.onOpen)

      #boton para mostrar grafico   
      self.btn = wx.Button(panel,-1,"Ver grafico") 
      vbox.Add(self.btn,0,wx.ALIGN_CENTER) 
      self.btn.Bind(wx.EVT_BUTTON,self.OnClicked)
         
      hbox = wx.BoxSizer(wx.HORIZONTAL)
         
      vbox.Add(hbox,1,wx.ALIGN_CENTER) 
      panel.SetSizer(vbox) 
        
      self.Centre() 
      self.Show() 
      self.Fit()

    # funcion para mostrar el grafico del dataset
    def graph(self, dots):
        matplotlib.rcParams['axes.unicode_minus'] = False
        eje_x = 0
        eje_y = 0
        for elem in dots:
            if float(elem[0]) > eje_x:
                eje_x = float(elem[0])
            if float(elem[1]) > eje_y:
                eje_y = float(elem[1])
            plt.plot(float(elem[0]), float(elem[1]), 'ro')
            # Ejes hasta +5 del mayor punto del dataset
            plt.axis([0, int(eje_x)+5, 0, int(eje_y)+5])
        plt.show()
	
    # manejador de eventos boton ver grafico
    def OnClicked(self, event): 
      btn = event.GetEventObject().GetLabel() 
      self.graph(self.dots)
      print "Label of pressed button = ",btn

    # boton open txt
    def onOpen(self, event):
        wildcard = "TXT files (*.txt)|*.txt"
        dialog = wx.FileDialog(self, "Open Text Files", wildcard=wildcard,
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_CANCEL:
            return

        path = dialog.GetPath()

        if os.path.exists(path):
            with open(path) as fobj:
                for line in fobj:
                    line = line.strip().split()
                    self.dots.append(line)

        

app = wx.App() 
Mywin(None, 'Clustering') 
app.MainLoop()