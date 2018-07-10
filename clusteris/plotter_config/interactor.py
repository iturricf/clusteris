# -*- coding: utf-8 -*-

import wx

class PlotterConfigInteractor(object):
    """Connects the UI events with the Presenter class."""

    def Connect(self, presenter, view):
        """Listens to UI evens and asigns an event handler on the Presenter."""
        self.presenter = presenter
        self.view = view

        view.radioBtn2D.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton2DClicked)
        view.radioBtn3D.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton3DClicked)
        view.choiceXAxe.Bind(wx.EVT_CHOICE, self.OnXAxeSelected)
        view.choiceYAxe.Bind(wx.EVT_CHOICE, self.OnYAxeSelected)
        view.choiceZAxe.Bind(wx.EVT_CHOICE, self.OnZAxeSelected)

        view.buttonCancel.Bind(wx.EVT_BUTTON, self.OnCancelClicked)
        view.buttonProcess.Bind(wx.EVT_BUTTON, self.OnProcessClicked)

        view.Bind(wx.EVT_CLOSE, self.OnCancelClicked)

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

    def OnCancelClicked(self, evt):
        self.presenter.Cancel()
