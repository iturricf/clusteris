# -*- coding: utf-8 -*-

import wx

class MainView (wx.Frame):

    def __init__(self, parent):

        self.app = wx.App(0)

        self.BuildMainUI(parent)

    ## Initialize main UI
    def BuildMainUI(self, parent):
        wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = u"ClusteRIS", pos = wx.DefaultPosition, size = wx.Size(-1,-1), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        sizerMain = wx.BoxSizer(wx.VERTICAL)

        self.panelMain = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        bSizerPanel = wx.BoxSizer(wx.VERTICAL)
        bSizerLeft = wx.BoxSizer(wx.VERTICAL)

        self.BuildDatasetUI(bSizerLeft)
        self.BuildProcessUI(bSizerLeft)
        self.BuildActionUI(bSizerLeft)

        bSizerPanel.Add(bSizerLeft, 1, wx.ALL, 1)

        self.panelMain.SetSizer(bSizerPanel)
        self.panelMain.Layout()
        bSizerPanel.Fit(self.panelMain)
        sizerMain.Add(self.panelMain, 1, wx.EXPAND|wx.ALL, 0)

        self.SetSizer(sizerMain)
        self.Layout()

        sizerMain.Fit(self)

        ## Add status bar
        self.statusBar = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)

        self.Centre(wx.BOTH)
        self.Show(True)

    def BuildDatasetUI(self, container):
        sbSizerDataset = wx.StaticBoxSizer(wx.StaticBox(self.panelMain, wx.ID_ANY, u"Dataset"), wx.VERTICAL)

        self.BuildFileSelectionUI(sbSizerDataset)
        self.BuildDatasetFormatUI(sbSizerDataset)
        self.BuildDatasetStatsUI(sbSizerDataset)

        container.Add(sbSizerDataset, 0, wx.ALL|wx.EXPAND, 5)

    def BuildProcessUI(self, container):
        sbSizerProcess = wx.StaticBoxSizer(wx.StaticBox(self.panelMain, wx.ID_ANY, u"Procesamiento"), wx.VERTICAL)

        bSizerAlgorithm = wx.BoxSizer(wx.HORIZONTAL)

        self.labelAlgorithm = wx.StaticText(sbSizerProcess.GetStaticBox(), wx.ID_ANY, u"Algoritmo", wx.DefaultPosition, wx.DefaultSize, 0)
        self.labelAlgorithm.Wrap(-1)
        bSizerAlgorithm.Add(self.labelAlgorithm, 1, wx.ALL|wx.EXPAND, 10)

        m_choiceAlgorithmChoices = [ u"Ninguno", u"K-means", u"Algoritmo Genético" ]
        self.choiceAlgorithm = wx.Choice(sbSizerProcess.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceAlgorithmChoices, 0)
        self.choiceAlgorithm.SetSelection(0)
        bSizerAlgorithm.Add(self.choiceAlgorithm, 1, wx.ALL, 5)

        sbSizerProcess.Add(bSizerAlgorithm, 1, wx.ALL|wx.EXPAND, 0)

        self.BuildParamsUI(sbSizerProcess)

        container.Add(sbSizerProcess, 1, wx.ALL|wx.EXPAND, 5)

    def BuildActionUI(self, container):
        bSizerAction = wx.BoxSizer(wx.VERTICAL)

        self.buttonProcess = wx.Button(self.panelMain, wx.ID_ANY, u"P&rocesar", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerAction.Add(self.buttonProcess, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        container.Add(bSizerAction, 0, wx.EXPAND, 0)

    def BuildFileSelectionUI(self, container):
        bSizerDatasetFileSelection = wx.BoxSizer(wx.HORIZONTAL)

        self.labelSelectDataset = wx.StaticText(container.GetStaticBox(), wx.ID_ANY, u"Seleccionar archivo", wx.DefaultPosition, wx.DefaultSize, 0)
        self.labelSelectDataset.Wrap(-1)
        bSizerDatasetFileSelection.Add(self.labelSelectDataset, 2, wx.ALL, 10)

        self.buttonSelectDataset = wx.Button(container.GetStaticBox(), wx.ID_ANY, u"E&xaminar", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerDatasetFileSelection.Add(self.buttonSelectDataset, 1, wx.ALL, 5)

        container.Add(bSizerDatasetFileSelection, 0, wx.EXPAND, 0)

    def BuildDatasetFormatUI(self, container):
        bSizerSizerColumns = wx.BoxSizer(wx.HORIZONTAL)

        self.checkParseFeatures = wx.CheckBox(container.GetStaticBox(), wx.ID_ANY, u"Procesar primera fila como títulos de atributos", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerSizerColumns.Add(self.checkParseFeatures, 0, wx.ALL, 5)

        container.Add(bSizerSizerColumns, 0, wx.ALL, 0)

    def BuildDatasetStatsUI(self, container):
        bSizerDatasetStats = wx.BoxSizer(wx.VERTICAL)

        self.labelSamplesCount = wx.StaticText(container.GetStaticBox(), wx.ID_ANY, u"Cantidad de muestras: {#}", wx.DefaultPosition, wx.DefaultSize, 0)
        self.labelSamplesCount.Wrap(-1)
        bSizerDatasetStats.Add(self.labelSamplesCount, 0, wx.ALL, 5)

        self.labelFeaturesCount = wx.StaticText(container.GetStaticBox(), wx.ID_ANY, u"Cantidad de atributos: {#}", wx.DefaultPosition, wx.DefaultSize, 0)
        self.labelFeaturesCount.Wrap(-1)
        bSizerDatasetStats.Add(self.labelFeaturesCount, 0, wx.ALL, 5)

        container.Add(bSizerDatasetStats, 0, wx.ALL, 0)

    def BuildParamsUI(self, container):
        bSizerParamK = wx.BoxSizer(wx.HORIZONTAL)

        self.labelCentroids = wx.StaticText(container.GetStaticBox(), wx.ID_ANY, u"Centroides", wx.DefaultPosition, wx.DefaultSize, 0)
        self.labelCentroids.Wrap(-1)
        bSizerParamK.Add(self.labelCentroids, 1, wx.ALL, 10)

        self.spinCentroidsParam = wx.SpinCtrl(container.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 2, 10, 0)
        bSizerParamK.Add(self.spinCentroidsParam, 1, wx.ALL, 5)

        container.Add(bSizerParamK, 1, wx.ALL|wx.EXPAND, 0)

    def SetParseFeaturesCheckbox(self, value):
        self.checkParseFeatures.SetValue(value)

    def SetLabelSamplesCountText(self, value):
        self.labelSamplesCount.SetLabel(value)

    def SetLabelFeaturesCountText(self, value):
        self.labelFeaturesCount.SetLabel(value)

    def SetStatusBarText(self, value):
        self.statusBar.SetStatusText(value)

    def SetCentroidSpinValue(self, value):
        self.spinCentroidsParam.SetValue(value)

    def SetAlgorithmSelection(self, value):
        self.choiceAlgorithm.SetSelection(value)

    def Start(self):
        self.app.MainLoop()

    def __del__(self):
        pass
