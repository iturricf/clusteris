# -*- coding: utf-8 -*-

import wx

class Interactor(object):
    """Connects the UI events with the Presenter class."""

    def Connect(self, presenter, view):
        """Listens to UI evens and asigns an event handler on the Presenter."""
        self.presenter = presenter
        self.view = view

        view.buttonSelectDataset.Bind(wx.EVT_BUTTON, self.OnFileSelectorClicked)
        view.checkParseFeatures.Bind(wx.EVT_CHECKBOX, self.OnParseAttributesToggle)
        view.buttonProcess.Bind(wx.EVT_BUTTON, self.OnProcessClicked)
        view.choiceAlgorithm.Bind(wx.EVT_CHOICE, self.OnAlgorithmSelected)
        view.spinCentroidsParam.Bind(wx.EVT_SPINCTRL, self.OnCentroidSpinCtrl)

        view.radioBtn2D.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton2DClicked)
        view.radioBtn3D.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton3DClicked)

        view.choiceXAxe.Bind(wx.EVT_CHOICE, self.OnXAxeSelected)
        view.choiceYAxe.Bind(wx.EVT_CHOICE, self.OnYAxeSelected)
        view.choiceZAxe.Bind(wx.EVT_CHOICE, self.OnZAxeSelected)

        view.Bind(view.EVT_FILE_SELECTED, self.OnFileSelected)

    def OnFileSelectorClicked(self, evt):
        self.presenter.ShowFileDialog()

    def OnFileSelected(self, evt):
        self.presenter.SetSelectedFile(evt.path)

    def OnParseAttributesToggle(self, evt):
        self.presenter.ToggleParseAttributes(evt.IsChecked())

    def OnAlgorithmSelected(self, evt):
        self.presenter.SetAlgorithm(evt.GetSelection(), evt.GetString())

    def OnCentroidSpinCtrl(self, evt):
        self.presenter.SetCentroidParam(evt.GetPosition())

    def OnRadioButton2DClicked(self, evt):
        self.presenter.Radio2DClicked(evt.IsChecked())

    def OnRadioButton3DClicked(self, evt):
        self.presenter.Radio3DClicked(evt.IsChecked())

    def OnXAxeSelected(self, evt):
        self.presenter.SetSelectedAxe(0, evt.GetSelection())

    def OnYAxeSelected(self, evt):
        self.presenter.SetSelectedAxe(1, evt.GetSelection())

    def OnZAxeSelected(self, evt):
        self.presenter.SetSelectedAxe(2, evt.GetSelection())

    def OnProcessClicked(self, evt):
        self.presenter.Process()

