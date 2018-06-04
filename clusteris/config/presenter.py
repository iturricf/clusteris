# -*- coding: utf-8 -*-

import csv
import importlib

import numpy as np
import pandas as pd

import processor.genetic
from plotter import Plotter
from processor.dummy import Dummy
from processor.kmeans import KMeans
from processor.genetic_plus import Genetic

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
        self.populationNumber = self.params.POPULATION_DEFAULT_VALUE
        self.iterationsNumber = self.params.ITERATION_DEFAULT_VALUE
        self.samples = []

    def InitView(self):
        """Sets default values for the UI."""
        self.view.SetCentroidSpinRange(self.params.CENTROID_MIN_VALUE, self.params.CENTROID_MAX_VALUE)
        self.view.SetCentroidSpinValue(self.params.CENTROID_DEFAULT_VALUE)
        self.view.SetLabelPopulationText("Cantidad de individuos [" + str(self.params.POPULATION_MIN_VALUE) + " - " + str(self.params.POPULATION_MAX_VALUE) + "]")
        self.view.SetPopulationSpinRange(self.params.POPULATION_MIN_VALUE, self.params.POPULATION_MAX_VALUE)
        self.view.SetPopulationSpinValue(self.params.POPULATION_DEFAULT_VALUE)
        self.view.SetLabelIterationText("Cantidad de iteraciones [" + str(self.params.ITERATION_MIN_VALUE) + " - " + str(self.params.ITERATION_MAX_VALUE) + "]")
        self.view.SetIterationSpinRange(self.params.ITERATION_MIN_VALUE, self.params.ITERATION_MAX_VALUE)
        self.view.SetIterationSpinValue(self.params.ITERATION_DEFAULT_VALUE)
        self.view.SetAlgorithmList(self.params.CLUSTERING_ALGORITHMS)
        self.view.SetAlgorithmSelection(self.params.CLUSTERING_ALGORITHM_DEFAULT)

        self._DisablePlotterOptions()

        # self.view.DisableProcessButton()

        self.columnsForAxes = range(3)

        if (self.datasetFeaturesCount == 2):
            self.view.Enable2DRadio()

            self.Radio2DClicked(True)

        if (self.datasetFeaturesCount >= 3):
            self.view.Enable2DRadio()
            self.view.Enable3DRadio()
            self.view.Set3DSelected()

            self.Radio3DClicked(True)

    def SetAlgorithm(self, index, name):
        print("DEBUG - Selected index: %d; value: %s" % (index, name))
        if(index == 1):
            self.view.HideGeneticParameters()
        else:
            if(index == 2):
                self.view.ShowGeneticParameters()
        self.clusteringAlgorithm = index

    def SetCentroidParam(self, value):
        print("DEBUG - Selected value: %d" % value)
        self.centroidsNumber = value

    def SetPopulationParam(self, value):
        print("DEBUG - Population value: %d" % value)
        self.populationNumber = value

    def SetIterationParam(self, value):
        print("DEBUG - Iteration value: %d" % value)
        self.iterationsNumber = value

    def Radio2DClicked(self, value):
        print('DEBUG - Plotter 2D: %s' % value)
        if value:
            self.axesAvailable = 2
            self._SetAllAxesList(self.columnNames)
            self.view.SetZAxeList([])
            self.view.DisableZAxeChoice()

            self.view.SetXAxeSelection(0)
            self.SetSelectedAxe(0, 0)
            self.view.SetYAxeSelection(1)
            self.SetSelectedAxe(1, 1)

            if (self.datasetFeaturesCount > 2):
                self.view.EnableXAxeChoice()
                self.view.EnableYAxeChoice()

    def Radio3DClicked(self, value):
        print('DEBUG - Plotter 3D: %s' % value)
        if value:
            self.axesAvailable = 3
            self._SetAllAxesList(self.columnNames)

            self._DisableAllLists()

            self.view.SetXAxeSelection(0)
            self.SetSelectedAxe(0, 0)
            self.view.SetYAxeSelection(1)
            self.SetSelectedAxe(1, 1)
            self.view.SetZAxeSelection(2)
            self.SetSelectedAxe(2, 2)

            if (self.datasetFeaturesCount > 3):
                self.view.EnableXAxeChoice()
                self.view.EnableYAxeChoice()
                self.view.EnableZAxeChoice()

    def SetSelectedAxe(self, axe, value):
        print('DEBUG - Selected axe value: %d - %d' % (axe, value))
        self.columnsForAxes[axe] = value
        print("Axes:: %s" % self.columnsForAxes)

    def RadioFixedClassParamClicked(self, value):
        self.view.HideVarClassesParameter()
        self.view.ShowFixedClassesParameter()

    def RadioVarClassParamClicked(self, value):
        self.view.HideFixedClassesParameter()
        self.view.ShowVarClassesParameter()

    def _DisablePlotterOptions(self):
        self.view.Disable2DRadio()
        self.view.Disable3DRadio()

        self._DisableAllLists()

    def _SetAllAxesList(self, value):
        self.view.SetXAxeList(self.columnNames)
        self.view.SetYAxeList(self.columnNames)
        self.view.SetZAxeList(self.columnNames)

    def _DisableAllLists(self):
        self.view.DisableXAxeChoice()
        self.view.DisableYAxeChoice()
        self.view.DisableZAxeChoice()

    def _IsPlotterConfigValid(self):
        for i in range(self.axesAvailable - 1):
            if self.columnsForAxes[i] == self.columnsForAxes[i+1]:
                return False

        return True

    def Process(self, graphic):
        if self.dataset is None:
            self.view.ShowErrorMessage("No se ha seleccionado el dataset aún.")
            return False

        if not self._IsPlotterConfigValid():
            self.view.ShowErrorMessage("Las columnas para los ejes seleccionados debe ser distinta para cada uno.")
            return False

        if graphic:
            self.SetAlgorithm(0, "Graphic")
        else:
            if self.clusteringAlgorithm == 0:
                self.view.ShowErrorMessage("Debes seleccionar el algoritmo.")
                return False

        className = self.params.CLUSTERING_PROCESSORS[self.clusteringAlgorithm]

        procModule = []

        procModule.append(importlib.import_module('processor.dummy'))
        procModule.append(importlib.import_module('processor.kmeans'))
        procModule.append(importlib.import_module('processor.genetic_plus'))

        procClass = getattr(procModule[self.clusteringAlgorithm], className)

        processor = procClass({'n_clusters': self.centroidsNumber})
        if self.clusteringAlgorithm == 0:
            processor.Fit(Dataset)
        else:
            if self.clusteringAlgorithm == 1:
                processor.Fit(Dataset)
            if self.clusteringAlgorithm == 2:
                processor.Fit(Dataset, self.populationNumber, self.iterationsNumber)

        labels = processor.GetLabels()
        centroids = processor.GetCentroids()

        plotter = Plotter()

        clusters = self.centroidsNumber

        if (self.clusteringAlgorithm == 0):
            clusters = 1

        if (self.axesAvailable < 3):
            clusters = self.centroidsNumber
            if (self.clusteringAlgorithm == 0):
                clusters = 1
            plotter.PlotSamples2D(Dataset, axes=self.columnsForAxes, labels=labels, clusters=clusters)

            if (len(centroids)):
                plotter.PlotCentroids2D(centroids, axes=self.columnsForAxes)

        else:
            plotter.PlotSamples3D(Dataset, axes=self.columnsForAxes, labels=labels, clusters=clusters)

            if (len(centroids)):
                plotter.PlotCentroids3D(centroids, axes=self.columnsForAxes)

        plotter.Show()
