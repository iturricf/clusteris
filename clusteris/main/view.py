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
        self.m_statusBar = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)

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

        self.m_staticTextAlgorithm = wx.StaticText(sbSizerProcess.GetStaticBox(), wx.ID_ANY, u"Algoritmo", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticTextAlgorithm.Wrap(-1)
        bSizerAlgorithm.Add(self.m_staticTextAlgorithm, 1, wx.ALL|wx.EXPAND, 10)

        m_choiceAlgorithmChoices = [ u"Ninguno", u"K-means", u"Algoritmo Genético" ]
        self.m_choiceAlgorithm = wx.Choice(sbSizerProcess.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceAlgorithmChoices, 0)
        self.m_choiceAlgorithm.SetSelection(0)
        bSizerAlgorithm.Add(self.m_choiceAlgorithm, 1, wx.ALL, 5)


        sbSizerProcess.Add(bSizerAlgorithm, 1, wx.ALL|wx.EXPAND, 0)

        self.BuildParamsUI(sbSizerProcess)

        container.Add(sbSizerProcess, 1, wx.ALL|wx.EXPAND, 5)

    def BuildActionUI(self, container):
        bSizerAction = wx.BoxSizer(wx.VERTICAL)

        self.m_buttonProcess = wx.Button(self.panelMain, wx.ID_ANY, u"P&rocesar", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerAction.Add(self.m_buttonProcess, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        container.Add(bSizerAction, 0, wx.EXPAND, 0)

    def BuildFileSelectionUI(self, container):
        bSizerDatasetFileSelection = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticTextDatasetPath = wx.StaticText(container.GetStaticBox(), wx.ID_ANY, u"Seleccionar archivo", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticTextDatasetPath.Wrap(-1)
        bSizerDatasetFileSelection.Add(self.m_staticTextDatasetPath, 2, wx.ALL, 10)

        self.m_buttonDataset = wx.Button(container.GetStaticBox(), wx.ID_ANY, u"E&xaminar", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerDatasetFileSelection.Add(self.m_buttonDataset, 1, wx.ALL, 5)

        container.Add(bSizerDatasetFileSelection, 0, wx.EXPAND, 0)

    def BuildDatasetFormatUI(self, container):
        bSizerSizerColumns = wx.BoxSizer(wx.HORIZONTAL)

        self.m_checkBoxColumns = wx.CheckBox(container.GetStaticBox(), wx.ID_ANY, u"Procesar primera fila como títulos de atributos", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerSizerColumns.Add(self.m_checkBoxColumns, 0, wx.ALL, 5)

        container.Add(bSizerSizerColumns, 0, wx.ALL, 0)

    def BuildDatasetStatsUI(self, container):
        bSizerDatasetStats = wx.BoxSizer(wx.VERTICAL)

        self.m_staticTextRows = wx.StaticText(container.GetStaticBox(), wx.ID_ANY, u"Cantidad de muestras: {#}", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticTextRows.Wrap(-1)
        bSizerDatasetStats.Add(self.m_staticTextRows, 0, wx.ALL, 5)

        self.m_staticTextFeatures = wx.StaticText(container.GetStaticBox(), wx.ID_ANY, u"Cantidad de atributos: {#}", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticTextFeatures.Wrap(-1)
        bSizerDatasetStats.Add(self.m_staticTextFeatures, 0, wx.ALL, 5)


        container.Add(bSizerDatasetStats, 0, wx.ALL, 0)

    def BuildParamsUI(self, container):
        bSizerParamK = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticTextParamK = wx.StaticText( container.GetStaticBox(), wx.ID_ANY, u"Centroides", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticTextParamK.Wrap( -1 )
        bSizerParamK.Add( self.m_staticTextParamK, 1, wx.ALL, 10 )

        self.m_spinCtrlParamK = wx.SpinCtrl( container.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 2, 10, 0 )
        bSizerParamK.Add( self.m_spinCtrlParamK, 1, wx.ALL, 5 )

        container.Add( bSizerParamK, 1, wx.ALL|wx.EXPAND, 0 )

    def Start(self):
        self.app.MainLoop()

    def __del__(self):
        pass
