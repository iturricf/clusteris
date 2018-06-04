# -*- coding: utf-8 -*-

import csv
import threading

import numpy as np
import pandas as pd
import wx

from config.view import ConfigView
from config.interactor import Interactor as ConfigInteractor
from config.presenter import Presenter as ConfigPresenter

from model import Results
from plotter import Plotter
from processor.genetic_plus import Genetic
from processor.kmeans import KMeans
from progress import ProgressListener

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

    def ShowDatasetConfigDialog(self):
        print('DEBUG - ShowDatasetConfigDialog')

        view = ConfigView(self.view)
        interactor = ConfigInteractor()
        presenter = ConfigPresenter(view, interactor, self.model, self.params)

        presenter.Start()
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

            # self.datasetSamplesCount, self.datasetFeaturesCount = list(self.dataset.shape)
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
        self.view.ResetGrid()
        self.view.ShowDataset(self.model.dataset, self.model.datasetColsNames)

    def ShowExportImageDialog(self):
        print('DEBUG - ShowExportImageDialog')

    def ShowExportCsvDialog(self):
        print('DEBUG - ShowExportCsvDialog')

    def Process(self):
        self.result = Results()

        self.listener = ProgressListener(self.view)



        e = threading.Event()

        threads = []

        threadProcess = threading.Thread(name="Clustering", target=self._ProcessThread, args=(e, self.listener))
        # threadPlotter = threading.Thread(name="Plotter", target=self._PlotThread, args=(e,))

        # threadProgress.setDaemon(True)
        # threadProcess.setDaemon(True)
        # threadPlotter.setDaemon(True)

        # threads.append(threadProgress)
        threads.append(threadProcess)
        # threads.append(threadPlotter)

        for k, v in enumerate(threads):
            print('DEBUG - Iniciando thread: %d' % k)
            v.start()

        self.listener.Start()

        # for k, v in enumerate(threads):
        #     v.join()
        #     print('DEBUG - Thread %d detenido.' % k)

        # threadProgress.start()
        # threadProcess.start()
        # threadPlotter.start()

        # threadProgress.join()
        # threadProcess.join()
        # threadPlotter.join()

    def _ProgressThread(self):
        self.listener.Start()

    def _ProcessThread(self, event, listener):
        # self.listener = ProgressListener(self.view)
        # threadProgress.start()

        processor = Genetic({'n_clusters': 3})

        processor.SetListener(listener)
        processor.Fit(self.model.dataset)

        self.result.labels = processor.GetLabels()
        self.result.centroids = processor.GetCentroids()

        self.view.ShowDataset(self.model.dataset, self.model.datasetColsNames, self.result.labels)

        self.view.EnableExportMenus()

        print("Event set!")

        wx.CallAfter(self.listener.Finish)
        event.set()

    def _PlotThread(self, event):
        event.wait()

        plotter = Plotter()

        plotter.PlotSamples2D(self.model.dataset, axes=self.model.colsForAxes, labels=self.result.labels, clusters=3)
        plotter.PlotCentroids2D(self.result.centroids, axes=self.model.colsForAxes)

        plotter.Show()

    def Close(self):
        print('DEBUG - Exiting program...')
        self.view.Destroy()

    def Start(self):
        self.view.Start()
