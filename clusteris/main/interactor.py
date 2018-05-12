# -*- coding: utf-8 -*-

import wx

class Interactor(object):

    def Install(self, presenter, view):
        self.presenter = presenter
        self.view = view

        view.buttonSelectDataset.Bind(wx.EVT_BUTTON, self.OnFileSelectorClicked)
        view.checkParseFeatures.Bind(wx.EVT_CHECKBOX, self.OnParseAttributesToggle)
        view.buttonProcess.Bind(wx.EVT_BUTTON, self.OnProcessClicked)
        view.choiceAlgorithm.Bind(wx.EVT_CHOICE, self.OnAlgorithmSelected)
        view.spinCentroidsParam.Bind(wx.EVT_SPINCTRL, self.OnCentroidSpinCtrl)

    def OnFileSelectorClicked(self, evt):
        wildcard = "Comma separated values files (*.csv)|*.csv|" \
                   "Text files (*.txt)|*.txt|" \
                   "All files (*.*)|*.*"

        fileDialog = wx.FileDialog(
            self.view,
            message='Please select a dataset file...',
            wildcard=wildcard,
            style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST|wx.FD_CHANGE_DIR|
                  wx.FD_PREVIEW
           )

        if fileDialog.ShowModal() == wx.ID_CANCEL:
            print ("DEBUG - Open Dataset cancelled by user.")
            return

        self.OnFileSelected(fileDialog.GetPath())

        fileDialog.Destroy()

    def OnFileSelected(self, path):
        self.presenter.SetSelectedFile(path)

    def OnParseAttributesToggle(self, evt):
        self.presenter.ToggleParseAttributes(evt.IsChecked())

    def OnAlgorithmSelected(self, evt):
        print("DEBUG - Selected value: %s; index: %d" % (evt.GetString(), evt.GetSelection()))

    def OnCentroidSpinCtrl(self, evt):
        print("DEBUG - Selected value: %d" % evt.GetPosition())

    def OnProcessClicked(self, evt):
        self.presenter.Process()
