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
        # self.BuildPlotterOptionsUI(bSizerLeft)

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

        self.HideVarClassesParameter()

        self.SetSizer(self.sizerMain)
        self.Layout()

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

        self.buttonCancel = wx.Button(self.panelAction, wx.ID_ANY, u"Ca&ncelar", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerAction.Add(self.buttonCancel, 0, wx.ALIGN_CENTER, 5)

        self.buttonProcess = wx.Button(self.panelAction, wx.ID_ANY, u"P&rocesar", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerAction.Add(self.buttonProcess, 0, wx.ALIGN_CENTER, 5)

        container.Add(bSizerAction, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

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
        self.spinFixedClassParam.SetRange(min, max)

    def SetCentroidSpinValue(self, value):
        self.spinFixedClassParam.SetValue(value)

    def GetCentroidSpinValue(self):
        return self.spinFixedClassParam.GetValue()

    def SetCentroidParamFromRange(self, min, max):
        self.spinVarClassParamFrom.SetRange(min, max)

    def SetCentroidParamFrom(self, value):
        self.spinVarClassParamFrom.SetValue(value)

    def GetCentroidParamFrom(self):
        self.spinVarClassParamFrom.GetValue()

    def SetCentroidParamToRange(self, min, max):
        self.spinVarClassParamTo.SetRange(min, max)

    def SetCentroidParamTo(self, value):
        self.spinVarClassParamTo.SetValue(value)

    def GetCentroidParamTo(self):
        self.spinVarClassParamTo.GetValue()

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

    def getRadioFixedClassParam(self):
        return self.radioFixedClassParam.GetValue()

    def getspinVarClassParamFrom(self):
        return self.spinVarClassParamFrom.GetValue()

    def getspinVarClassParamTo(self):
        return self.spinVarClassParamTo.GetValue()

    def SetAlgorithmList(self, value):
        self.choiceAlgorithm.SetItems(value)

    def SetAlgorithmSelection(self, value):
        self.choiceAlgorithm.SetSelection(value)

    def getAlgorithmSelection(self):
        return self.choiceAlgorithm.GetSelection()

    def DisableProcessButton(self):
        self.buttonProcess.Disable()

    def EnableProcessButton(self):
        self.buttonProcess.Enable()

    def ShowErrorMessage(self, message):
        wx.LogError(message)

    def Start(self):
        """ Initializes the main loop for this UI. Starts listening events."""
        self.sizerMain.Fit(self)
        self.Centre(wx.BOTH)
        return self.ShowModal()

    def __del__(self):
        pass
