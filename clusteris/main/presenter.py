# -*- coding: utf-8 -*-

import csv
import importlib

import numpy as np
import pandas as pd

import processor.genetic
from plotter import Plotter
from processor.dummy import Dummy
from processor.kmeans import KMeans

import Genetic

class Presenter(object):
    """
    Process UI events and updates view with results.
    """

    def __init__(self, view, interactor, params):
        self.view = view
        self.interactor = interactor
        self.params = params

        interactor.Connect(self, view)

        self.InitModel()
        self.InitView()

        view.Start()

    def InitModel(self):
        self.dataset = None
        self.datasetPath = ""
        self.parseAttributes = False
        self.datasetSamplesCount = 0
        self.datasetFeaturesCount = 0
        self.clusteringAlgorithm = self.params.CLUSTERING_ALGORITHM_DEFAULT
        self.centroidsNumber = self.params.CENTROID_DEFAULT_VALUE
        self.samples = []

    def InitView(self):
        """Sets default values for the UI."""
        self.view.SetParseFeaturesCheckbox(self.params.DATASET_PARSE_FEATURES_DEFAULT_VALUE)
        self.view.SetLabelSamplesCountText('Cantidad de muestras: N/A')
        self.view.SetLabelFeaturesCountText('Cantidad de atributos: N/A')
        self.view.SetStatusBarText('Archivo dataset: No seleccionado.')
        self.view.SetCentroidSpinRange(self.params.CENTROID_MIN_VALUE, self.params.CENTROID_MAX_VALUE)
        self.view.SetCentroidSpinValue(self.params.CENTROID_DEFAULT_VALUE)
        self.view.SetAlgorithmList(self.params.CLUSTERING_ALGORITHMS)
        self.view.SetAlgorithmSelection(self.params.CLUSTERING_ALGORITHM_DEFAULT)

    def ShowFileDialog(self):
        self.view.ShowFileDialog()

    def SetAlgorithm(self, index, name):
        print("DEBUG - Selected index: %d; value: %s" % (index, name))
        self.clusteringAlgorithm = index

    def SetCentroidParam(self, value):
        print("DEBUG - Selected value: %d" % value)
        self.centroidsNumber = value

    def ToggleParseAttributes(self, isChecked):
        print('DEBUG - Parse attributes: %s' % isChecked)
        self.parseAttributes = isChecked
        self.ParseDatasetFile()

    def SetSelectedFile(self, path):
        print('DEBUG - Selected path: %s' % path)
        self.datasetPath = path

        self.ParseDatasetFile()

    def ParseDatasetFile(self):
        try:
            delimiter = self._DetectDelimiter(self.datasetPath)
            if (not self.parseAttributes):
                parseHeader = None
            else:
                parseHeader = 0

            print('DEBUG - CSV Delimiter: %s' % delimiter)

            # Reads CSV file as Pandas DataFrame
            self.dataset = pd.read_csv(self.datasetPath, header=parseHeader, sep=delimiter)

            self.datasetSamplesCount, self.datasetFeaturesCount = list(self.dataset.shape)

            attributes = ", ".join(str(c) for c in self.dataset.columns)

            print('DEBUG - Dataset samples: %d' % self.datasetSamplesCount)
            print('DEBUG - Dataset attributes: %s' % self.datasetFeaturesCount)
            print('DEBUG - Dataset attributes names: %s' % attributes)

            self.view.SetLabelSamplesCountText('Cantidad de muestras: %d' % self.datasetSamplesCount)
            self.view.SetLabelFeaturesCountText('Cantidad de atributos: %d' % self.datasetFeaturesCount)
            self.view.SetStatusText('Archivo dataset: %s' % self.datasetPath)

        except IOError:
            self.view.ShowErrorMessage("Error al abrir el archivo '%s'." % self.datasetPath)

    def _DetectDelimiter(self, path):
        """Tries to infer the delimiter symbol in a CSV file using csv Sniffer class."""
        sniffer = csv.Sniffer()
        sniffer.preferred = ['|', ';', ',', '\t', ' ']
        with open(path, 'r') as file:
            line = file.readline()
            dialect = sniffer.sniff(line)
            return dialect.delimiter

    def Process(self):
        samples = []

        # Split Pandas DataFrame into columns
        for i in self.dataset.columns:
            samples.append(self.dataset[i].values)

        # Convert DataFrame columns into Numpy Array
        Dataset = np.array(list(zip(*samples)))

        if (self.clusteringAlgorithm == 2):
            self._GenetycAlg(self.datasetPath)

        else:
            className = self.params.CLUSTERING_PROCESSORS[self.clusteringAlgorithm]

            procModule = []

            procModule.append(importlib.import_module('processor.dummy'))
            procModule.append(importlib.import_module('processor.kmeans'))

            procClass = getattr(procModule[self.clusteringAlgorithm], className)

            processor = procClass({'n_clusters': self.centroidsNumber})
            processor.Fit(Dataset)

            labels = processor.GetLabels()
            centroids = processor.GetCentroids()

            plotter = Plotter()

            if (self.datasetFeaturesCount < 3):
                plotter.PlotSamples2D(Dataset, labels=labels, clusters=self.centroidsNumber)

                if (len(centroids)):
                    plotter.PlotCentroids2D(centroids)

            else:
                plotter.PlotSamples3D(Dataset, labels=labels, clusters=self.centroidsNumber)

                if (len(centroids)):
                    plotter.PlotCentroids3D(centroids)

            plotter.Show()

    def _GenetycAlg(self, path):
        result = processor.genetic.GeneticAlg(self.datasetSamplesCount, self.centroidsNumber,float(0.85),float(0.05),int(10), path)
        print result
