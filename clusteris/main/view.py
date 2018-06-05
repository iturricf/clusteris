# -*- coding: utf-8 -*-

import wx
import wx.grid
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

        wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = u"ClusteRIS", pos = wx.DefaultPosition, size = wx.Size(-1, -1), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.Size(850, 600), wx.DefaultSize)

        self.BuildMenubar()

        self.BuildMainUI()

        self.SetCustomIcon()

        # Add status bar
        self.statusBar = self.CreateStatusBar(1, wx.STB_SIZEGRIP|wx.STB_SHOW_TIPS|wx.STB_ELLIPSIZE_START, wx.ID_ANY)
        self.statusBar.SetFieldsCount(4, [-6, -1, -1, -2])
        self.statusBar.SetStatusStyles([wx.SB_RAISED, wx.SB_SUNKEN, wx.SB_SUNKEN, wx.SB_SUNKEN])

    def SetCustomIcon(self):
        iconPath = "resources/clusteris.ico"

        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.Bitmap(iconPath, wx.BITMAP_TYPE_ANY))

        self.SetIcon(icon)

    def BuildMenubar(self):
        self.menubarMain = wx.MenuBar(0)
        self.menuFile = wx.Menu()
        self.mItemDataset = wx.MenuItem(self.menuFile, wx.ID_ANY, u"&Abrir dataset"+ u"\t" + u"CTRL+a", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuFile.Append(self.mItemDataset)

        self.mItemExportImage = wx.MenuItem(self.menuFile, wx.ID_ANY, u"Exportar resultado como &imagen"+ u"\t" + u"CTRL+i", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuFile.Append(self.mItemExportImage)

        self.mItemExportCsv = wx.MenuItem(self.menuFile, wx.ID_ANY, u"Exportar resultado como archivo &CSV"+ u"\t" + u"CTRL+e", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuFile.Append(self.mItemExportCsv)

        self.menuFile.AppendSeparator()

        self.mItemExit = wx.MenuItem(self.menuFile, wx.ID_ANY, u"&Salir"+ u"\t" + u"CTRL+q", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuFile.Append(self.mItemExit)

        self.menubarMain.Append(self.menuFile, u"&Archivo")

        self.menuProcess = wx.Menu()
        self.mItemProcess = wx.MenuItem(self.menuProcess, wx.ID_ANY, u"P&rocesar dataset"+ u"\t" + u"CTRL+r", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuProcess.Append(self.mItemProcess)

        self.mItemPlot = wx.MenuItem(self.menuProcess, wx.ID_ANY, u"&Graficar" + u"\t" + u"CTRL+g", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuProcess.Append(self.mItemPlot)

        self.menubarMain.Append(self.menuProcess, u"&Procesamiento")

        self.menuHelp = wx.Menu()
        self.mItemHelp = wx.MenuItem(self.menuHelp, wx.ID_ANY, u"Obtener ayuda"+ u"\t" + u"F1", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuHelp.Append(self.mItemHelp)

        self.menuHelp.AppendSeparator()

        self.mItemAbout = wx.MenuItem(self.menuHelp, wx.ID_ANY, u"Acerca de ClusteRIS...", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuHelp.Append(self.mItemAbout)

        self.menubarMain.Append(self.menuHelp, u"A&yuda")

        self.SetMenuBar(self.menubarMain)

    def BuildMainUI(self):
        self.sizerMain = wx.BoxSizer(wx.VERTICAL)

        self.panelMain = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL)
        self.panelMain.SetScrollRate(5, 5)

        self.bSizerPanel = wx.BoxSizer(wx.VERTICAL)

        self.BuildGridUI(self.bSizerPanel)

        self.panelMain.SetSizer(self.bSizerPanel)
        self.panelMain.Layout()

        self.bSizerPanel.Fit(self.panelMain)
        self.sizerMain.Add(self.panelMain, 1, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(self.sizerMain)
        self.Layout()

    def BuildGridUI(self, container):
        self.gridResult = wx.grid.Grid(self.panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        self.gridResult.CreateGrid(20, 5)
        self.gridResult.EnableEditing(False)
        self.gridResult.EnableGridLines(True)
        self.gridResult.EnableDragGridSize(False)
        self.gridResult.SetMargins(0, 0)

        # Columns
        self.gridResult.EnableDragColMove(False)
        self.gridResult.EnableDragColSize(True)
        self.gridResult.SetColLabelSize(30)
        self.gridResult.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.gridResult.EnableDragRowSize(False)
        self.gridResult.SetRowLabelSize(80)
        self.gridResult.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance

        # Cell Defaults
        self.gridResult.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
        container.Add(self.gridResult, 0, wx.ALL, 5)

    def ShowDataset(self, dataset, colsNames, labels = False):
        rows, cols = dataset.shape

        table = self.gridResult.GetTable()
        self.gridResult.DeleteCols(numCols=table.GetColsCount())
        self.gridResult.DeleteRows(numRows=table.GetRowsCount())

        print(rows, cols)

        self.gridResult.AppendRows(rows)
        self.gridResult.AppendCols(cols)

        for i in xrange(cols):
            self.gridResult.SetColLabelValue(i, "Columna %d" % i)

        for i in xrange(rows):
            for j in xrange(cols):
                self.gridResult.SetCellValue(i, j, str(dataset[i][j]))

        if labels is not False:
            self.gridResult.AppendCols(1)
            self.gridResult.SetColLabelValue(cols, "Clases")

            for i in xrange(rows):
                self.gridResult.SetCellValue(i, cols, str(labels[i]))

        self.gridResult.AutoSize()
        self.gridResult.Layout()

        self.bSizerPanel.Layout()
        self.panelMain.Layout()
        self.sizerMain.Layout()
        self.Layout()

    def SetStatusBarText(self, value, field=0):
        self.statusBar.SetStatusText(value, field)

    def DisableExportMenus(self):
        self.mItemExportImage.Enable(False)
        self.mItemExportCsv.Enable(False)

    def EnableExportMenus(self):
        self.mItemExportImage.Enable(True)
        self.mItemExportCsv.Enable(True)

    def DisableProcess(self):
        self.mItemProcess.Enable(False)

    def EnableProcess(self):
        self.mItemProcess.Enable(True)

    def DisablePlotMenu(self):
        self.mItemPlot.Enable(False)

    def EnablePlotMenu(self):
        self.mItemPlot.Enable(True)

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

    def ShowProgressDialog(self):
        print('DEBUG - Show Progress')
        self.progress = wx.ProgressDialog("Procesando dataset", "por favor espere", maximum=100, parent=self, style=wx.PD_SMOOTH|wx.PD_AUTO_HIDE)
        self.progress.ShowModal()

    def AdjustProgressRange(self, maxRange):
        self.progress.SetRange(maxRange)

    def UpdateProgress(self, progress):
        self.progress.Update(progress)

    def DestroyProgressDialog(self):
        self.progress.EndModal(True)

    def Start(self):
        """ Initializes the main loop for this UI. Starts listening events."""
        self.sizerMain.Fit(self)
        self.Centre(wx.BOTH)
        self.Show(True)
        # self.Maximize(True)

        self.app.MainLoop()

    def __del__(self):
        pass
