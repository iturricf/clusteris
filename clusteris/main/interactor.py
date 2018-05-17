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
        view.Bind(view.EVT_FILE_SELECTED, self.OnFileSelected)

    def OnFileSelectorClicked(self, evt):
        self.presenter.ShowFileDialog()

    def OnFileSelected(self, evt):
        self.presenter.SetSelectedFile(evt.path)

    def OnParseAttributesToggle(self, evt):
        self.presenter.ToggleParseAttributes(evt.IsChecked())

    def OnAlgorithmSelected(self, evt):
        print("DEBUG - Selected value: %s; index: %d" % (evt.GetString(), evt.GetSelection()))

    def OnCentroidSpinCtrl(self, evt):
        self.presenter.SetCentroidParam(evt.GetPosition())
        print("DEBUG - Selected value: %d" % evt.GetPosition())

    def OnProcessClicked(self, evt):
        self.presenter.Process()
