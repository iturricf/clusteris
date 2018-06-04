# -*- coding: utf-8 -*-

import threading
import wx

class ProgressListener(object):

    def __init__(self, parent):
        print('DEBUG - Create listener')
        self.progress = wx.ProgressDialog("Procesando dataset", "por favor espere", maximum=100, parent=parent, style=wx.PD_SMOOTH|wx.PD_AUTO_HIDE)

    def Start(self):
        print('DEBUG - Start with thread')

        self.progress.ShowModal()
        self.progress.Update(10)

        # self.progressThread = threading.Thread(name='Progress', target=self._ActualStart)
        # self.progressThread.setDaemon(True)
        # self.progressThread.start()

    def Update(self, taskProgress):
        self.progress.Update(taskProgress)

    def Finish(self):
        self.progress.Destroy()

    # def _ActualStart(self):
    #     self.progress.ShowModal()
    #     self.progress.Update(10)
