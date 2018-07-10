# -*- coding: utf-8 -*-

import wx

class Interactor(object):
    """Connects the UI events with the Presenter class."""

    def Connect(self, presenter, view):
        """Listens to UI evens and asigns an event handler on the Presenter."""
        self.presenter = presenter
        self.view = view

        # Menu Archivo
        view.Bind(wx.EVT_MENU, self.OnOpenDatasetClicked, view.mItemDataset)
        view.Bind(wx.EVT_MENU, self.OnExportImageClicked, view.mItemExportImage)
        view.Bind(wx.EVT_MENU, self.OnExportCsvClicked, view.mItemExportCsv)
        view.Bind(wx.EVT_MENU, self.OnExitClicked, view.mItemExit)

        # Menu Proceso
        view.Bind(wx.EVT_MENU, self.OnProcessDataset, view.mItemProcess)
        view.Bind(wx.EVT_MENU, self.OnPlotResults, view.mItemPlot)

        view.Bind(wx.EVT_CLOSE, self.OnExitClicked)

        view.Bind(view.EVT_FILE_SELECTED, self.OnFileSelected)
        view.Bind(view.EVT_EXPORT_CSV_FILE_SELECTED, self.OnExportCsvFileSelected)
        view.Bind(view.EVT_EXPORT_PNG_FILE_SELECTED, self.OnExportPngFileSelected)

    def OnOpenDatasetClicked(self, evt):
        self.presenter.ShowFileDialog()

    def OnExportImageClicked(self, evt):
        self.presenter.ShowExportImageDialog()

    def OnExportPngFileSelected(self, evt):
        self.presenter.ExportPngFile(evt.path)

    def OnExportCsvClicked(self, evt):
        self.presenter.ShowExportCsvDialog()

    def OnExportCsvFileSelected(self, evt):
        self.presenter.ExportCsvFile(evt.path)

    def OnFileSelected(self, evt):
        self.presenter.SetSelectedFile(evt.path)

    def OnProcessDataset(self, evt):
        self.presenter.ShowDatasetConfigDialog()
        # self.presenter.Process()

    def OnPlotResults(self, evt):
        self.presenter.ShowPlotConfigDialog()
        # self.presenter.Plot()

    def OnExitClicked(self, evt):
        self.presenter.Close()
