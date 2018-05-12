# -*- coding: utf-8 -*-

import wx

# import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class Presenter(object):

    def __init__(self, view, interactor):
        self.view = view
        self.interactor = interactor

        interactor.Install(self, view)

        self.InitModel()
        self.InitView()

        view.Start()

    def InitModel(self):
        self.dataset = None
        self.datasetPath = ""
        self.parseAttributes = False
        self.datasetSamplesCount = 0
        self.datasetFeaturesCount = 0
        self.samples = []

    def InitView(self):
        self.view.checkParseFeatures.SetValue(False)
        self.view.labelSamplesCount.SetLabel('Cantidad de muestras: N/A')
        self.view.labelFeaturesCount.SetLabel('Cantidad de atributos: N/A')
        self.view.statusBar.SetStatusText('Archivo dataset: No seleccionado.')
        self.view.spinCentroidsParam.SetValue(5)
        self.view.choiceAlgorithm.SetSelection(0)

    def SetSelectedFile(self, path):
        print('DEBUG - Selected path: %s' % path)

        try:
            with open(path, 'r') as dataset:
                lines = dataset.readlines();

                self.datasetSamplesCount = len(lines) - int(self.parseAttributes)
                self.datasetFeaturesCount = self._GetDatesetFeaturesAmount(lines[0].strip())

                print('DEBUG - Dataset samples: %d' % self.datasetSamplesCount)
                print('DEBUG - Dataset attributes: %d' % self.datasetFeaturesCount)

                self.view.labelSamplesCount.SetLabel('Cantidad de muestras: %d' % self.datasetSamplesCount)
                self.view.labelFeaturesCount.SetLabel('Cantidad de atributos: %d' % self.datasetFeaturesCount)
                self.view.statusBar.SetStatusText('Archivo dataset: %s' % path)

                self.datasetPath = path
        except IOError:
            wx.LogError("Error al abrir el archivo '%s'." % path)

    def ToggleParseAttributes(self, isChecked):
        print('DEBUG - Parse attributes: %s' % isChecked)
        self.parseAttributes = isChecked

    def _GetDatesetFeaturesAmount(self, line):
        fields = line.split(',')

        if (not self._HasValidFeatures(fields, line)):
            fields = line.split(';')

            if (not self._HasValidFeatures(fields, line)):
                fields = line.split(' ')

                if (not self._HasValidFeatures(fields, line)):
                    return 0

        return len(fields)

    def _HasValidFeatures(self, fields, line):
        return not (len(fields) == 1 and fields[0] == line)

    def Process(self):
        try:
            with open(self.datasetPath) as dataset:
                for line in dataset:
                    sample = line.strip().split()
                    self.samples.append(sample)
        except IOError:
            wx.LogError("Error al abrir el archivo '%s'." % path)

        self._ShowDatasetPlot()

    def _ShowDatasetPlot(self):
        matplotlib.rcParams['axes.unicode_minus'] = False
        eje_x = 0
        eje_y = 0
        for sample in self.samples:
            if float(sample[0]) > eje_x:
                eje_x = float(sample[0])
            if float(sample[1]) > eje_y:
                eje_y = float(sample[1])
            plt.plot(float(sample[0]), float(sample[1]), 'ro')
            # Ejes hasta +5 del mayor punto del dataset
            plt.axis([0, int(eje_x)+5, 0, int(eje_y)+5])
        plt.show()
