# -*- coding: utf-8 -*-

import wx
import wx.xrc

class frameMain (wx.Frame):

    def __init__( self, parent ):

        self.dataset = None
        self.datasetPath = ""
        self.firstLineFeatures = False
        self.datasetLines = 0
        self.datasetAttributes = 0

        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"ClusteRIS", pos = wx.DefaultPosition, size = wx.Size( 800,560 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        sizerMain = wx.BoxSizer( wx.VERTICAL )

        self.panelMain = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizerPanel = wx.BoxSizer( wx.VERTICAL )

        bSizerLeft = wx.BoxSizer( wx.VERTICAL )

        sbSizerDataset = wx.StaticBoxSizer( wx.StaticBox( self.panelMain, wx.ID_ANY, u"Dataset" ), wx.VERTICAL )

        bSizerDatasetInner2 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticTextDatasetPath = wx.StaticText( sbSizerDataset.GetStaticBox(), wx.ID_ANY, u"Seleccionar archivo", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticTextDatasetPath.Wrap( -1 )
        bSizerDatasetInner2.Add( self.m_staticTextDatasetPath, 0, wx.ALL, 10 )

        self.m_buttonDataset = wx.Button( sbSizerDataset.GetStaticBox(), wx.ID_ANY, u"E&xaminar", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizerDatasetInner2.Add( self.m_buttonDataset, 0, wx.ALL, 5 )

        self.Bind(wx.EVT_BUTTON, self.ShowFileDialog, self.m_buttonDataset)


        sbSizerDataset.Add( bSizerDatasetInner2, 1, wx.EXPAND, 0 )

        bSizerSizerColumns = wx.BoxSizer( wx.HORIZONTAL )

        self.m_checkBoxColumns = wx.CheckBox( sbSizerDataset.GetStaticBox(), wx.ID_ANY, u"Procesar primera fila como nombres", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizerSizerColumns.Add( self.m_checkBoxColumns, 0, 0, 5 )

        self.Bind(wx.EVT_CHECKBOX, self.ToggleFirstLineFeatures)


        sbSizerDataset.Add( bSizerSizerColumns, 1, wx.ALL, 0 )

        bSizerDatasetInnerPath = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticTextSelectedPath = wx.StaticText( sbSizerDataset.GetStaticBox(), wx.ID_ANY, u"{Selected Path}", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticTextSelectedPath.Wrap( -1 )
        bSizerDatasetInnerPath.Add( self.m_staticTextSelectedPath, 0, wx.ALL, 10 )

        self.m_buttonDatasetSelected = wx.Button( sbSizerDataset.GetStaticBox(), wx.ID_ANY, u"Validar", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizerDatasetInnerPath.Add( self.m_buttonDatasetSelected, 0, wx.ALL, 5 )


        sbSizerDataset.Add( bSizerDatasetInnerPath, 1, 0, 0 )

        bSizerDatasetStats = wx.BoxSizer( wx.VERTICAL )

        self.m_staticTextRows = wx.StaticText( sbSizerDataset.GetStaticBox(), wx.ID_ANY, u"Cantidad de muestras: {#}", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticTextRows.Wrap( -1 )
        bSizerDatasetStats.Add( self.m_staticTextRows, 0, wx.ALL, 5 )

        self.m_staticTextFeatures = wx.StaticText( sbSizerDataset.GetStaticBox(), wx.ID_ANY, u"Cantidad de atributos: {#}", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticTextFeatures.Wrap( -1 )
        bSizerDatasetStats.Add( self.m_staticTextFeatures, 0, wx.ALL, 5 )


        sbSizerDataset.Add( bSizerDatasetStats, 1, wx.ALL, 0 )


        bSizerLeft.Add( sbSizerDataset, 1, wx.ALL, 5 )

        sbSizerProcess = wx.StaticBoxSizer( wx.StaticBox( self.panelMain, wx.ID_ANY, u"Procesamiento" ), wx.VERTICAL )


        bSizerLeft.Add( sbSizerProcess, 1, wx.ALL, 5 )


        bSizerPanel.Add( bSizerLeft, 1, wx.ALL, 1 )


        self.panelMain.SetSizer( bSizerPanel )
        self.panelMain.Layout()
        bSizerPanel.Fit( self.panelMain )
        sizerMain.Add( self.panelMain, 1, wx.EXPAND |wx.ALL, 0 )


        self.SetSizer( sizerMain )
        self.Layout()

        self.Centre( wx.BOTH )
        self.Show(True)

    def ShowFileDialog(self, evt):

        wildcard = "Comma separated values files (*.csv)|*.csv|" \
                   "Text files (*.txt)|*.txt|" \
                   "All files (*.*)|*.*"

        fileDialog = wx.FileDialog(
            self,
            message='Please select a dataset file...',
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_CHANGE_DIR |
                  wx.FD_PREVIEW
            )

        if fileDialog.ShowModal() == wx.ID_CANCEL:
            print ("Open Dataset: Cancelled by user")
            return

        self.ParseDatasetPath(fileDialog.GetPath())

        fileDialog.Destroy()

    def ParseDatasetPath(self, path):
        print(path)

        self.datasetPath = path
        self.m_staticTextSelectedPath.SetLabel(path)

        self.dataset = open(path, 'r')

        lines = self.dataset.readlines()

        self.datasetLines = len(lines) - int(self.firstLineFeatures)
        self.datasetAttributes = self.GetDatesetFeaturesAmount(lines[0].strip())

        print('Dataset lines: %d' % self.datasetLines)
        print('Dataset attributes: %d' % self.datasetAttributes)

        self.dataset.close()

    def ToggleFirstLineFeatures(self, evt):
        if (evt.IsChecked()):
            print('firstLineFeatures: Checked')
        else:
            print('firstLineFeatures: Unchecked')

        self.firstLineFeatures = evt.IsChecked()

    def GetDatesetFeaturesAmount(self, line):
        print(line)
        fields = line.split(',')

        if (not self.HasValidFeatures(fields, line)):
            fields = line.split(';')

            if (not self.HasValidFeatures(fields, line)):
                fields = line.split(' ')

                if (not self.HasValidFeatures(fields, line)):
                    return 0

        return len(fields)

    def HasValidFeatures(self, fields, line):
        return not (len(fields) == 1 and fields[0] == line)

    def __del__( self ):
        pass

def main():
    app = wx.App()
    frameMain(None)
    app.MainLoop()

main()
