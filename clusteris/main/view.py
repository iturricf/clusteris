# -*- coding: utf-8 -*-

import wx
import wx.lib.newevent

class MainView (wx.Frame):
    """
    MainView is the main UI responsible. Shows dataset, processor and params
    related info.

    Provides public methods for asigning UI values from Presenter and dispatches
    user related actions events to be processed by associated Presenter class.
    """

    # Custom Events for dataset file selection
    FileSelectedEvent, EVT_FILE_SELECTED = wx.lib.newevent.NewEvent()

    def __init__(self, parent):
        """Constructor. Initializes the wxPython app and Builds main UI."""
        self.app = wx.App(0)

        self.BuildMainUI(parent)

    def BuildMainUI(self, parent):
        wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = u"ClusteRIS", pos = wx.DefaultPosition, size = wx.Size(-1,-1), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        self.sizerMain = wx.BoxSizer(wx.VERTICAL)

        self.panelMain = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        bSizerPanel = wx.BoxSizer(wx.HORIZONTAL)
        bSizerLeft = wx.BoxSizer(wx.VERTICAL)

        self.BuildDatasetUI(bSizerLeft)
        self.BuildProcessUI(bSizerLeft)

        bSizerPanel.Add(bSizerLeft, 1, wx.ALL, 1)

        bSizerRight = wx.BoxSizer(wx.VERTICAL)

        self.BuildPlotterOptionsUI(bSizerRight)

        bSizerPanel.Add(bSizerRight, 1, wx.ALL, 1)

        self.panelMain.SetSizer(bSizerPanel)
        self.panelMain.Layout()
        bSizerPanel.Fit(self.panelMain)
        self.sizerMain.Add(self.panelMain, 1, wx.ALL|wx.EXPAND, 0)

        self.BuildActionUI(self.sizerMain)

        self.SetSizer(self.sizerMain)
        self.Layout()

        # Add status bar
        self.statusBar = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)

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

    def BuildDatasetUI(self, container):
        """Builds dataset file selection UI."""
        sbSizerDataset = wx.StaticBoxSizer(wx.StaticBox(self.panelMain, wx.ID_ANY, u"Dataset"), wx.VERTICAL)

        self.BuildFileSelectionUI(sbSizerDataset)
        self.BuildDatasetFormatUI(sbSizerDataset)
        self.BuildDatasetStatsUI(sbSizerDataset)

        container.Add(sbSizerDataset, 0, wx.ALL|wx.EXPAND, 5)

    def BuildProcessUI(self, container):
        """Builds cluster processing parameters UI."""
        sbSizerProcess = wx.StaticBoxSizer(wx.StaticBox(self.panelMain, wx.ID_ANY, u"Procesamiento"), wx.VERTICAL)

        bSizerAlgorithm = wx.BoxSizer(wx.HORIZONTAL)

        self.labelAlgorithm = wx.StaticText(sbSizerProcess.GetStaticBox(), wx.ID_ANY, u"Algoritmo", wx.DefaultPosition, wx.DefaultSize, 0)
        self.labelAlgorithm.Wrap(-1)
        bSizerAlgorithm.Add(self.labelAlgorithm, 1, wx.ALL|wx.EXPAND, 10)

        self.choiceAlgorithm = wx.Choice(sbSizerProcess.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [], 0)
        bSizerAlgorithm.Add(self.choiceAlgorithm, 1, wx.ALL, 5)

        sbSizerProcess.Add(bSizerAlgorithm, 1, wx.ALL|wx.EXPAND, 0)

        self.BuildParamsUI(sbSizerProcess)

        container.Add(sbSizerProcess, 1, wx.ALL|wx.EXPAND, 5)

    def BuildActionUI(self, container):
        """The action button UI. Start processing the dataset."""
        bSizerAction = wx.BoxSizer(wx.VERTICAL)

        self.buttonProcess = wx.Button(self, wx.ID_ANY, u"P&rocesar", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerAction.Add(self.buttonProcess, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        container.Add(bSizerAction, 0, wx.EXPAND, 0)

    def BuildFileSelectionUI(self, container):
        """Dataset file select."""
        bSizerDatasetFileSelection = wx.BoxSizer(wx.HORIZONTAL)

        self.labelSelectDataset = wx.StaticText(container.GetStaticBox(), wx.ID_ANY, u"Seleccionar archivo", wx.DefaultPosition, wx.DefaultSize, 0)
        self.labelSelectDataset.Wrap(-1)
        bSizerDatasetFileSelection.Add(self.labelSelectDataset, 2, wx.ALL, 10)

        self.buttonSelectDataset = wx.Button(container.GetStaticBox(), wx.ID_ANY, u"E&xaminar", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerDatasetFileSelection.Add(self.buttonSelectDataset, 1, wx.ALL, 5)

        container.Add(bSizerDatasetFileSelection, 0, wx.EXPAND, 0)

    def BuildDatasetFormatUI(self, container):
        """Dataset file options."""
        bSizerSizerColumns = wx.BoxSizer(wx.HORIZONTAL)

        self.checkParseFeatures = wx.CheckBox(container.GetStaticBox(), wx.ID_ANY, u"Procesar primera fila como títulos de atributos", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerSizerColumns.Add(self.checkParseFeatures, 0, wx.ALL, 5)

        container.Add(bSizerSizerColumns, 0, wx.ALL, 0)

    def BuildDatasetStatsUI(self, container):
        """Dataset file stats."""
        bSizerDatasetStats = wx.BoxSizer(wx.VERTICAL)

        self.labelSamplesCount = wx.StaticText(container.GetStaticBox(), wx.ID_ANY, u"Cantidad de muestras: {#}", wx.DefaultPosition, wx.DefaultSize, 0)
        self.labelSamplesCount.Wrap(-1)
        bSizerDatasetStats.Add(self.labelSamplesCount, 0, wx.ALL, 5)

        self.labelFeaturesCount = wx.StaticText(container.GetStaticBox(), wx.ID_ANY, u"Cantidad de atributos: {#}", wx.DefaultPosition, wx.DefaultSize, 0)
        self.labelFeaturesCount.Wrap(-1)
        bSizerDatasetStats.Add(self.labelFeaturesCount, 0, wx.ALL, 5)

        container.Add(bSizerDatasetStats, 0, wx.ALL, 0)

    def BuildParamsUI(self, container):
        """Processing params."""
        bSizerParamK = wx.BoxSizer(wx.HORIZONTAL)

        self.labelCentroids = wx.StaticText(container.GetStaticBox(), wx.ID_ANY, u"Cantidad de Clases", wx.DefaultPosition, wx.DefaultSize, 0)
        self.labelCentroids.Wrap(-1)
        bSizerParamK.Add(self.labelCentroids, 1, wx.ALL, 10)

        self.spinCentroidsParam = wx.SpinCtrl(container.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS)
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

    def SetCentroidSpinRange(self, min, max):
        self.spinCentroidsParam.SetRange(min, max)

    def SetCentroidSpinValue(self, value):
        self.spinCentroidsParam.SetValue(value)

    def SetAlgorithmList(self, value):
        self.choiceAlgorithm.SetItems(value)

    def SetAlgorithmSelection(self, value):
        self.choiceAlgorithm.SetSelection(value)

    def DisableProcessButton(self):
        self.buttonProcess.Disable()

    def EnableProcessButton(self):
        self.buttonProcess.Enable()

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

    def ShowFileDialog(self):
        """Shows file dialog and dispatch custom event after dataset file is selected."""

        wildcard = "Text files (*.txt)|*.txt|" \
                   "Comma separated values files (*.csv)|*.csv|" \
                   "All files (*.*)|*.*"

        with  wx.FileDialog(
            self,
            message='Please select a dataset file...',
            wildcard=wildcard,
            defaultDir="../samples",
            style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST|wx.FD_CHANGE_DIR|
                  wx.FD_PREVIEW
           ) as fileDialog:


            if fileDialog.ShowModal() == wx.ID_CANCEL:
                print ("DEBUG - Open Dataset cancelled by user.")
                return

            # Notify FileDialog custom FileSelectedEvent with corresponding path
            wx.PostEvent(self, self.FileSelectedEvent(path=fileDialog.GetPath()))

    def ShowErrorMessage(self, message):
        wx.LogError(message)

    def Start(self):
        """ Initializes the main loop for this UI. Starts listening events."""
        self.sizerMain.Fit(self)
        self.Centre(wx.BOTH)
        self.Show(True)

        self.app.MainLoop()

    def __del__(self):
        pass
