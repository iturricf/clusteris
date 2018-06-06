# -*- coding: utf-8 -*-

import csv
import importlib
import threading
import time

from os.path import basename, splitext

import numpy as np
import pandas as pd
import wx

from config.view import ConfigView
from config.interactor import Interactor as ConfigInteractor
from config.presenter import Presenter as ConfigPresenter

from model import Results
from plotter import Plotter

class Presenter(object):
    """
    Process UI events and updates view with results.
    """

    def __init__(self, view, interactor, model, params):
        self.view = view
        self.interactor = interactor
        self.model = model
        self.params = params

        interactor.Connect(self, view)

        self.InitView()

    def InitView(self):
        self.view.SetStatusBarText("Archivo dataset: No seleccionado", 0)
        self.view.SetStatusBarText("--", 1)
        self.view.SetStatusBarText("--", 2)
        self.view.SetStatusBarText("--", 3)

        self.view.DisableExportMenus()
        self.view.DisableProcess()
        # self.view.DisablePlotMenu()

    def ShowFileDialog(self):
        self.view.ShowFileDialog()

    def SetSelectedFile(self, path):
        print('DEBUG - Selected path: %s' % path)
        self.datasetPath = path
        self.model.datasetPath = path

        self.ParseDatasetFile()

    def ParseDatasetFile(self):
        try:
            delimiter = self._DetectDelimiter(self.model.datasetPath)

            parseHeader = None

            print('DEBUG - CSV Delimiter: %s' % delimiter)

            # Reads CSV file as Pandas DataFrame
            self.model.dataset = pd.read_csv(self.model.datasetPath, header=parseHeader, sep=delimiter)

            self.model.datasetRows, self.model.datasetCols = list(self.model.dataset.shape)
            self.model.datasetColsNames = ["Column %s" % str(c) for c in self.model.dataset.columns]

            attributes = ", ".join(str(c) for c in self.model.dataset.columns)

            print('DEBUG - Dataset samples: %d' % self.model.datasetRows)
            print('DEBUG - Dataset attributes: %s' % self.model.datasetCols)
            print('DEBUG - Dataset attributes names: %s' % attributes)

            self.view.SetStatusBarText("Archivo dataset: %s" % self.model.datasetPath, 0)
            self.view.SetStatusBarText("FILAS: %d" % self.model.datasetRows, 1)
            self.view.SetStatusBarText("COLS: %d" % self.model.datasetCols, 2)
            self.view.SetStatusBarText("HEADERS: %s" % ("NO" if parseHeader is None else "SI"), 3)

            self.view.EnableProcess()

            self.model.colsForAxes = range(3)
            self.model.clusters = 1

            ## Dataset Processing

            samples = []

            # Split Pandas DataFrame into columns
            for i in self.model.dataset.columns:
                samples.append(self.model.dataset[i].values)

            # Convert DataFrame columns into Numpy Array
            self.model.dataset = np.array(list(zip(*samples)))
            self._ShowDatasetAsTable()

        except IOError:
            self.view.ShowErrorMessage("Error al abrir el archivo '%s'." % self.model.datasetPath)

    def _DetectDelimiter(self, path):
        """Tries to infer the delimiter symbol in a CSV file using csv Sniffer class."""
        sniffer = csv.Sniffer()
        sniffer.preferred = ['|', ';', ',', '\t', ' ']
        with open(path, 'r') as file:
            line = file.readline()
            dialect = sniffer.sniff(line)
            return dialect.delimiter

    def _ShowDatasetAsTable(self):
        self.view.ShowDataset(self.model.dataset, self.model.datasetColsNames)

    def ShowExportImageDialog(self):
        print('DEBUG - ShowExportImageDialog')
        exportFilename, extension = splitext(basename(self.model.datasetPath))
        self.view.ShowSavePngFileDialog("%s-plot.png" % exportFilename)

    def ShowExportCsvDialog(self):
        print('DEBUG - ShowExportCsvDialog')
        exportFilename, extension = splitext(basename(self.model.datasetPath))
        self.view.ShowSaveCsvFileDialog("%s-result%s" % (exportFilename, extension))

    def ShowDatasetConfigDialog(self):
        print('DEBUG - ShowDatasetConfigDialog')

        view = ConfigView(self.view)
        interactor = ConfigInteractor()
        presenter = ConfigPresenter(view, interactor, self.model, self.params)

        if (presenter.Start()):
            self.Process()
        else:
            print('DEBUG - CANCELLED')

    def SetMaxRange(self, maxRange):
        print('DEBUG - Seteando rango')
        self.view.AdjustProgressRange(maxRange)

    def UpdateProgress(self, taskProgress):
        print('DEBUG - Update progress')
        self.view.UpdateProgress(taskProgress)

    def FinishProgress(self):
        print('DEBUG - Terminar')
        self.view.DestroyProgressDialog()

    def Process(self):
        self.result = Results()

        threadProcess = threading.Thread(name="Clustering", target=self._ProcessThread)
        threadProcess.start()

        self.view.ShowProgressDialog()

        threadProcess.join()
        print('DEBUG - Thread process detenido')
        self.Plot()

    def _ProcessThread(self):
        className = self.params.CLUSTERING_PROCESSORS[self.model.clusteringAlgorithm]

        procModule = []

        procModule.append(importlib.import_module('processor.dummy'))
        procModule.append(importlib.import_module('processor.kmeans'))
        procModule.append(importlib.import_module('processor.genetic_plus'))

        procClass = getattr(procModule[self.model.clusteringAlgorithm], className)

        processor = procClass({
            'n_clusters': self.model.clusters,
            'n_population': self.model.maxPopulation,
            'n_iterations': self.model.maxIterations
        })

        time.sleep(0.2)
        processor.SetListener(self)

        processor.Fit(self.model.dataset)

        self.result.labels = processor.GetLabels()
        self.result.centroids = processor.GetCentroids()

        wx.CallAfter(self.view.ShowDataset, self.model.dataset, self.model.datasetColsNames, self.result.labels)
        wx.CallAfter(self.view.EnableExportMenus)
        # wx.CallAfter(self.view.EnablePlotMenu)
        wx.CallAfter(self.FinishProgress)

    def Plot(self):
        print('DEBUG - Plot')

        self._PlotThread()

        # Se deshabilita el thread separado para el graficador debido a que causa
        # problemas cuando la aplicación corre en Windows

        # threadPlotter = threading.Thread(name="Plotter", target=self._PlotThread)
        # threadPlotter.start()
        # threadPlotter.join()

    def _PlotThread(self):
        plot = self.CreatePlot()
        print('DEBUG - Antes de imprimir!!')
        plot.Show()

    def CreatePlot(self):
        clusters = 1 if self.model.clusteringAlgorithm == 0 else self.model.clusters

        print('DEBUG - Clusters a graficar: %d' % clusters)
        plotter = Plotter()

        if (self.model.selectedAxes < 3):
            plotter.PlotSamples2D(self.model.dataset, axes=self.model.colsForAxes, labels=self.result.labels, clusters=clusters)

            if (len(self.result.centroids)):
                plotter.PlotCentroids2D(self.result.centroids, axes=self.model.colsForAxes)

        else:
            plotter.PlotSamples3D(self.model.dataset, axes=self.model.colsForAxes, labels=self.result.labels, clusters=clusters)

            if (len(self.result.centroids)):
                plotter.PlotCentroids3D(self.result.centroids, axes=self.model.colsForAxes)

        return plotter

    def ExportPngFile(self, path):
        plot = self.CreatePlot()
        plot.SaveTo(path)

    def ExportCsvFile(self, path):
        print('DEBUG - Export CSV to: %s' % path)

        rows = self.result.labels.shape

        reshaped = self.result.labels.reshape(rows[0], 1)

        toExport = np.append(self.model.dataset, reshaped, axis=1)
        df = pd.DataFrame(toExport)
        df.to_csv(path, header=None, index=None, sep=" ")

    def Close(self):
        print('DEBUG - Exiting program...')
        self.view.Destroy()

    def Start(self):
        self.view.Start()
