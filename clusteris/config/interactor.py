# -*- coding: utf-8 -*-

import wx

class Interactor(object):
    """Connects the UI events with the Presenter class."""

    def Connect(self, presenter, view):
        """Listens to UI evens and asigns an event handler on the Presenter."""
        self.presenter = presenter
        self.view = view

        view.choiceAlgorithm.Bind(wx.EVT_CHOICE, self.OnAlgorithmSelected)
        view.spinFixedClassParam.Bind(wx.EVT_SPINCTRL, self.OnCentroidSpinCtrl)
        view.spinVarClassParamFrom.Bind(wx.EVT_SPINCTRL, self.OnCentroidRangeMinSpinCtrl)
        view.spinVarClassParamTo.Bind(wx.EVT_SPINCTRL, self.OnCentroidRangeMaxSpinCtrl)
        view.spinPopulationParam.Bind(wx.EVT_SPINCTRL, self.OnPopulationSpinCtrl)
        view.spinIterationParam.Bind(wx.EVT_SPINCTRL, self.OnIterationsSpinCtrl)
        view.radioFixedClassParam.Bind(wx.EVT_RADIOBUTTON, self.OnRadioFixedClassParamClicked)
        view.radioVarClassParam.Bind(wx.EVT_RADIOBUTTON, self.OnRadioVarClassParamClicked)

        view.buttonCancel.Bind(wx.EVT_BUTTON, self.OnCancelClicked)
        view.buttonProcess.Bind(wx.EVT_BUTTON, self.OnProcessClicked)

        view.Bind(wx.EVT_CLOSE, self.OnCancelClicked)

    def OnAlgorithmSelected(self, evt):
        self.presenter.SetAlgorithm(evt.GetSelection(), evt.GetString())

    def OnCentroidSpinCtrl(self, evt):
        self.presenter.SetCentroidParam(evt.GetPosition())

    def OnCentroidRangeMinSpinCtrl(self, evt):
        self.presenter.SetCentroidRangeMinParam(evt.GetPosition())

    def OnCentroidRangeMaxSpinCtrl(self, evt):
        self.presenter.SetCentroidRangeMaxParam(evt.GetPosition())

    def OnPopulationSpinCtrl(self, evt):
        self.presenter.SetPopulationParam(evt.GetPosition())

    def OnIterationsSpinCtrl(self, evt):
        self.presenter.SetIterationParam(evt.GetPosition())

    def OnRadioFixedClassParamClicked(self, evt):
        self.presenter.RadioFixedClassParamClicked(evt.IsChecked())

    def OnRadioVarClassParamClicked(self, evt):
        self.presenter.RadioVarClassParamClicked(evt.IsChecked())

    def OnProcessClicked(self, evt):
        self.presenter.Process()

    def OnCancelClicked(self, evt):
        self.presenter.Cancel()
