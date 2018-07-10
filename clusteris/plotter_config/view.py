# -*- coding: utf-8 -*-

import wx

class PlotterConfigView(wx.Dialog):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = u"Graficar...", pos = wx.DefaultPosition, size = wx.Size(500,300), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        self.sizerMain = wx.BoxSizer(wx.VERTICAL)

        self.panelMain = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizerPlotter = wx.BoxSizer(wx.VERTICAL)

        self.BuildPlotterOptionsUI(bSizerPlotter)


        self.panelMain.SetSizer(bSizerPlotter)
        self.panelMain.Layout()
        bSizerPlotter.Fit(self.panelMain)
        self.sizerMain.Add(self.panelMain, 0, wx.EXPAND |wx.ALL, 0)

        self.panelAction = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizerActionContainer = wx.BoxSizer(wx.VERTICAL)

        self.BuildActionUI(bSizerActionContainer)

        self.panelAction.SetSizer(bSizerActionContainer)
        self.panelAction.Layout()
        bSizerActionContainer.Fit(self.panelAction)

        self.sizerMain.Add(self.panelAction, 0, wx.ALL|wx.EXPAND, 0)


        self.SetSizer(self.sizerMain)
        self.Layout()

        self.Centre(wx.BOTH)

    def BuildPlotterOptionsUI(self, container):
        """Builds the plotter parameters UI."""
        sbSizerPlotter = wx.StaticBoxSizer(wx.StaticBox(self.panelMain, wx.ID_ANY, u"Graficador"), wx.VERTICAL)

        bSizerDimension = wx.BoxSizer(wx.HORIZONTAL)

        self.radioBtn2D = wx.RadioButton(sbSizerPlotter.GetStaticBox(), wx.ID_ANY, u"2 Dimensiones", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerDimension.Add(self.radioBtn2D, 0, wx.ALL, 5)

        self.radioBtn3D = wx.RadioButton(sbSizerPlotter.GetStaticBox(), wx.ID_ANY, u"3 Dimensiones", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerDimension.Add(self.radioBtn3D, 0, wx.ALL, 5)


        sbSizerPlotter.Add(bSizerDimension, 0, wx.ALIGN_CENTER, 0)

        bSizerTitle = wx.BoxSizer(wx.VERTICAL)

        self.labelDescription = wx.StaticText(sbSizerPlotter.GetStaticBox(), wx.ID_ANY, u"Seleccionar atributos para cada Eje:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.labelDescription.Wrap(-1)
        bSizerTitle.Add(self.labelDescription, 0, wx.LEFT, 10)


        sbSizerPlotter.Add(bSizerTitle, 0, wx.ALL, 0)

        bSizerXAxe = wx.BoxSizer(wx.HORIZONTAL)

        self.labelXAxe = wx.StaticText(sbSizerPlotter.GetStaticBox(), wx.ID_ANY, u"Eje X", wx.DefaultPosition, wx.DefaultSize, 0)
        self.labelXAxe.Wrap(-1)
        bSizerXAxe.Add(self.labelXAxe, 1, wx.ALL|wx.EXPAND, 10)


        self.choiceXAxe = wx.Choice(sbSizerPlotter.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [], 0)
        self.choiceXAxe.SetSelection(0)
        bSizerXAxe.Add(self.choiceXAxe, 1, wx.ALL, 5)


        sbSizerPlotter.Add(bSizerXAxe, 1, wx.EXPAND, 0)

        bSizerYAxe = wx.BoxSizer(wx.HORIZONTAL)

        self.labelYAxe = wx.StaticText(sbSizerPlotter.GetStaticBox(), wx.ID_ANY, u"Eje Y", wx.DefaultPosition, wx.DefaultSize, 0)
        self.labelYAxe.Wrap(-1)
        bSizerYAxe.Add(self.labelYAxe, 1, wx.ALL|wx.EXPAND, 10)

        self.choiceYAxe = wx.Choice(sbSizerPlotter.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [], 0)
        self.choiceYAxe.SetSelection(0)
        bSizerYAxe.Add(self.choiceYAxe, 1, wx.ALL, 5)


        sbSizerPlotter.Add(bSizerYAxe, 1, wx.EXPAND, 0)

        bSizerZAxe = wx.BoxSizer(wx.HORIZONTAL)

        self.labelZAxe = wx.StaticText(sbSizerPlotter.GetStaticBox(), wx.ID_ANY, u"Eje Z", wx.DefaultPosition, wx.DefaultSize, 0)
        self.labelZAxe.Wrap(-1)
        bSizerZAxe.Add(self.labelZAxe, 1, wx.ALL|wx.EXPAND, 10)

        self.choiceZAxe = wx.Choice(sbSizerPlotter.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [], 0)
        self.choiceZAxe.SetSelection(0)
        bSizerZAxe.Add(self.choiceZAxe, 1, wx.ALL, 5)

        sbSizerPlotter.Add(bSizerZAxe, 1, wx.EXPAND, 0)

        container.Add(sbSizerPlotter, 1, wx.ALL|wx.EXPAND, 5)

    def BuildActionUI(self, container):
        """The action button UI. Start processing the dataset."""
        bSizerAction = wx.BoxSizer(wx.HORIZONTAL)

        self.buttonCancel = wx.Button(self.panelAction, wx.ID_ANY, u"Ca&ncelar", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerAction.Add(self.buttonCancel, 0, wx.ALIGN_CENTER, 5)

        self.buttonProcess = wx.Button(self.panelAction, wx.ID_ANY, u"P&rocesar", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerAction.Add(self.buttonProcess, 0, wx.ALIGN_CENTER, 5)

        container.Add(bSizerAction, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

    def Disable2DRadio(self):
        self.radioBtn2D.Disable()

    def Disable3DRadio(self):
        self.radioBtn3D.Disable()

    def Enable2DRadio(self):
        self.radioBtn2D.Enable()

    def Enable3DRadio(self):
        self.radioBtn3D.Enable()

    def DisableXAxeChoice(self):
        self.choiceXAxe.Disable()

    def DisableYAxeChoice(self):
        self.choiceYAxe.Disable()

    def DisableZAxeChoice(self):
        self.choiceZAxe.Disable()

    def EnableXAxeChoice(self):
        self.choiceXAxe.Enable()

    def EnableYAxeChoice(self):
        self.choiceYAxe.Enable()

    def EnableZAxeChoice(self):
        self.choiceZAxe.Enable()

    def SetXAxeList(self, value):
        self.choiceXAxe.SetItems(value)

    def SetXAxeSelection(self, value):
        self.choiceXAxe.SetSelection(value)

    def SetYAxeList(self, value):
        self.choiceYAxe.SetItems(value)

    def SetYAxeSelection(self, value):
        self.choiceYAxe.SetSelection(value)

    def SetZAxeList(self, value):
        self.choiceZAxe.SetItems(value)

    def SetZAxeSelection(self, value):
        self.choiceZAxe.SetSelection(value)

    def Set3DSelected(self):
        self.radioBtn3D.SetValue(True)

    def Set2DSelected(self):
        self.radioBtn2D.SetValue(True)

    def DisableProcessButton(self):
        self.buttonProcess.Disable()

    def EnableProcessButton(self):
        self.buttonProcess.Enable()

    def ShowErrorMessage(self, message):
        wx.LogError(message)

    def Start(self):
        self.sizerMain.Fit(self)
        self.Centre(wx.BOTH)
        return self.ShowModal()

    def __del__(self):
        pass


