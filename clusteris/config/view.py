# -*- coding: utf-8 -*-

import wx

class ConfigView(wx.Dialog):
    """
    ConfigView is the config UI responsible. Shows dataset, processor and params
    related info.

    Provides public methods for asigning UI values from Presenter and dispatches
    user related actions events to be processed by associated Presenter class.
    """

    def __init__(self, parent):
        """Constructor. Initializes the wxPython app and Builds main UI."""
        self.app = wx.App(0)

        self.BuildMainUI(parent)

    def BuildMainUI(self, parent):
        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = u"Dataset configuration", pos = wx.DefaultPosition, size = wx.Size(-1,-1), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        self.sizerMain = wx.BoxSizer(wx.VERTICAL)

        self.panelMain = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        bSizerPanel = wx.BoxSizer(wx.HORIZONTAL)
        bSizerLeft = wx.BoxSizer(wx.VERTICAL)

        self.BuildProcessUI(bSizerLeft)
        self.BuildClassesUI(bSizerLeft)
        self.BuildPlotterOptionsUI(bSizerLeft)

        bSizerPanel.Add(bSizerLeft, 1, wx.ALL, 1)

        self.panelMain.SetSizer(bSizerPanel)
        self.panelMain.Layout()
        bSizerPanel.Fit(self.panelMain)

        self.sizerMain.Add(self.panelMain, 0, wx.ALL|wx.EXPAND, 0)

        self.panelAction = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizerActionContainer = wx.BoxSizer(wx.VERTICAL)

        self.BuildActionUI(bSizerActionContainer)

        self.panelAction.SetSizer(bSizerActionContainer)
        self.panelAction.Layout()
        bSizerActionContainer.Fit(self.panelAction)

        self.sizerMain.Add(self.panelAction, 0, wx.ALL|wx.EXPAND, 0)

        self.SetSizer(self.sizerMain)
        self.Layout()

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

    def BuildProcessUI(self, container):
        """Builds cluster processing parameters UI."""
        self.sbSizerProcess = wx.StaticBoxSizer(wx.StaticBox(self.panelMain, wx.ID_ANY, u"Procesamiento"), wx.VERTICAL)

        bSizerAlgorithm = wx.BoxSizer(wx.HORIZONTAL)

        self.labelAlgorithm = wx.StaticText(self.sbSizerProcess.GetStaticBox(), wx.ID_ANY, u"Algoritmo", wx.DefaultPosition, wx.DefaultSize, 0)
        self.labelAlgorithm.Wrap(-1)
        bSizerAlgorithm.Add(self.labelAlgorithm, 1, wx.ALL|wx.EXPAND, 10)

        self.choiceAlgorithm = wx.Choice(self.sbSizerProcess.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [], 0)
        bSizerAlgorithm.Add(self.choiceAlgorithm, 1, wx.ALL, 5)

        self.sbSizerProcess.Add(bSizerAlgorithm, 1, wx.ALL|wx.EXPAND, 0)

        self.BuildParamsUI(self.sbSizerProcess)

        self.BuildPopulationUI(self.sbSizerProcess)

        self.BuildIterationUI(self.sbSizerProcess)

        container.Add(self.sbSizerProcess, 1, wx.ALL|wx.EXPAND, 5)

    def BuildClassesUI(self, container):
        """Builds cluster processing parameters UI."""
        self.sbSizerClasses = wx.StaticBoxSizer(wx.StaticBox(self.panelMain, wx.ID_ANY, u"Número de Clases"), wx.VERTICAL)

        bSizerParamK = wx.BoxSizer(wx.HORIZONTAL)

        self.radioFixedClassParam = wx.RadioButton(self.sbSizerClasses.GetStaticBox(), wx.ID_ANY, u"Fijo", wx.DefaultPosition, wx.DefaultSize, 0)
        self.radioFixedClassParam.SetValue(1)
        bSizerParamK.Add(self.radioFixedClassParam, 1, wx.ALL, 10)

        self.spinFixedClassParam = wx.SpinCtrl(self.sbSizerClasses.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS)
        bSizerParamK.Add(self.spinFixedClassParam, 1, wx.ALL, 5)

        bSizerParamVarK = wx.BoxSizer(wx.HORIZONTAL)

        self.radioVarClassParam = wx.RadioButton(self.sbSizerClasses.GetStaticBox(), wx.ID_ANY, u"Optimizado desde", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerParamVarK.Add(self.radioVarClassParam, 1, wx.ALL, 10)

        self.spinVarClassParamFrom = wx.SpinCtrl(self.sbSizerClasses.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS)
        bSizerParamVarK.Add(self.spinVarClassParamFrom, 1, wx.ALL, 5)

        self.labelVarClassTo = wx.StaticText(self.sbSizerClasses.GetStaticBox(), wx.ID_ANY, u"hasta", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerParamVarK.Add(self.labelVarClassTo, 0, wx.ALL, 10)

        self.spinVarClassParamTo = wx.SpinCtrl(self.sbSizerClasses.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS)
        bSizerParamVarK.Add(self.spinVarClassParamTo, 1, wx.ALL, 5)

        self.sbSizerClasses.Add(bSizerParamK, 0, wx.ALL|wx.EXPAND, 0)
        self.sbSizerClasses.Add(bSizerParamVarK, 0, wx.ALL|wx.EXPAND, 0)

        container.Add(self.sbSizerClasses, 0, wx.ALL|wx.EXPAND, 5)

    def BuildActionUI(self, container):
        """The action button UI. Start processing the dataset."""
        bSizerAction = wx.BoxSizer(wx.HORIZONTAL)

        self.buttonGraphic = wx.Button(self.panelAction, wx.ID_ANY, u"Graficar", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerAction.Add(self.buttonGraphic, 0, wx.ALIGN_CENTER, 5)

        self.buttonProcess = wx.Button(self.panelAction, wx.ID_ANY, u"P&rocesar", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerAction.Add(self.buttonProcess, 0, wx.ALIGN_CENTER, 5)

        container.Add(bSizerAction, 0, wx.ALIGN_CENTER|wx.ALL, 5)

    def BuildParamsUI(self, container):
        """Processing params."""
        bSizerParamK = wx.BoxSizer(wx.HORIZONTAL)

        self.labelCentroids = wx.StaticText(container.GetStaticBox(), wx.ID_ANY, u"Cantidad de Clases", wx.DefaultPosition, wx.DefaultSize, 0)
        self.labelCentroids.Wrap(-1)
        bSizerParamK.Add(self.labelCentroids, 1, wx.ALL, 10)

        self.spinCentroidsParam = wx.SpinCtrl(container.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS)
        bSizerParamK.Add(self.spinCentroidsParam, 1, wx.ALL, 5)

        container.Add(bSizerParamK, 1, wx.ALL|wx.EXPAND, 0)

    def BuildPopulationUI(self, container):
        """Processing params."""
        bSizerParamK = wx.BoxSizer(wx.HORIZONTAL)

        self.labelPopulation = wx.StaticText(container.GetStaticBox(), wx.ID_ANY, u"Cantidad de Individuos", wx.DefaultPosition, wx.DefaultSize, 0)
        self.labelPopulation.Wrap(-1)
        bSizerParamK.Add(self.labelPopulation, 1, wx.ALL, 10)

        self.spinPopulationParam = wx.SpinCtrl(container.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS)
        bSizerParamK.Add(self.spinPopulationParam, 1, wx.ALL, 5)

        container.Add(bSizerParamK, 1, wx.ALL|wx.EXPAND, 0)

    def BuildIterationUI(self, container):
        """Processing params."""
        bSizerParamK = wx.BoxSizer(wx.HORIZONTAL)

        self.labelIteration = wx.StaticText(container.GetStaticBox(), wx.ID_ANY, u"N° de Iteraciones", wx.DefaultPosition, wx.DefaultSize, 0)
        self.labelIteration.Wrap(-1)
        bSizerParamK.Add(self.labelIteration, 1, wx.ALL, 10)

        self.spinIterationParam = wx.SpinCtrl(container.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS)
        bSizerParamK.Add(self.spinIterationParam, 1, wx.ALL, 5)

        container.Add(bSizerParamK, 1, wx.ALL|wx.EXPAND, 0)

    def SetCentroidSpinRange(self, min, max):
        self.spinCentroidsParam.SetRange(min, max)

    def SetCentroidSpinValue(self, value):
        self.spinCentroidsParam.SetValue(value)

    def SetLabelPopulationText(self, value):
        self.labelPopulation.SetLabel(value)

    def SetPopulationSpinRange(self, min, max):
        self.spinPopulationParam.SetRange(min, max)

    def SetPopulationSpinValue(self, value):
        self.spinPopulationParam.SetValue(value)

    def SetLabelIterationText(self, value):
        self.labelIteration.SetLabel(value)

    def SetIterationSpinRange(self, min, max):
        self.spinIterationParam.SetRange(min, max)

    def SetIterationSpinValue(self, value):
        self.spinIterationParam.SetValue(value)

    def HideGeneticParameters(self):
        self.spinIterationParam.Disable()
        self.spinPopulationParam.Disable()
        self.labelPopulation.Disable()
        self.labelIteration.Disable()

    def ShowGeneticParameters(self):
        self.spinIterationParam.Enable()
        self.spinPopulationParam.Enable()
        self.labelPopulation.Enable()
        self.labelIteration.Enable()

    def HideVarClassesParameter(self):
        self.spinVarClassParamFrom.Disable()
        self.spinVarClassParamTo.Disable()

    def ShowVarClassesParameter(self):
        self.spinVarClassParamFrom.Enable()
        self.spinVarClassParamTo.Enable()

    def HideFixedClassesParameter(self):
        self.spinFixedClassParam.Disable()

    def ShowFixedClassesParameter(self):
        self.spinFixedClassParam.Enable()

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

    def Set3DSelected(self):
        self.radioBtn3D.SetValue(True)

    def Set2DSelected(self):
        self.radioBtn2D.SetValue(True)

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
