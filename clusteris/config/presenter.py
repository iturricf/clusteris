# -*- coding: utf-8 -*-

from copy import deepcopy

class Presenter(object):
    """
    Process UI events and updates view with results.
    """

    def __init__(self, view, interactor, model, params):
        self.view = view
        self.interactor = interactor
        self.params = params
        self.model = model
        self.localModel = deepcopy(self.model)

        interactor.Connect(self, view)

        self.InitModel()
        self.InitView()

    def InitModel(self):
        print('DEBUG - INIT presenter')

        self.localModel.clusteringAlgorithm = self.params.CLUSTERING_ALGORITHM_DEFAULT
        self.localModel.clusters = self.params.CENTROID_DEFAULT_VALUE
        self.localModel.clustersFixed = self.params.CENTROID_FIXED_DEFAULT_VALUE
        self.localModel.clusters_range_min = self.params.CENTROID_RANGE_MIN_VALUE
        self.localModel.clusters_range_max = self.params.CENTROID_RANGE_MAX_VALUE
        self.localModel.maxPopulation = self.params.POPULATION_DEFAULT_VALUE
        self.localModel.maxIterations = self.params.ITERATION_DEFAULT_VALUE

    def InitView(self):
        """Sets default values for the UI."""
        self.view.SetCentroidSpinRange(self.params.CENTROID_MIN_VALUE, self.params.CENTROID_MAX_VALUE)
        self.view.SetCentroidSpinValue(self.params.CENTROID_DEFAULT_VALUE)
        self.view.SetCentroidParamFromRange(self.params.CENTROID_MIN_VALUE, self.params.CENTROID_MAX_VALUE)
        self.view.SetCentroidParamFrom(self.params.CENTROID_MIN_VALUE)
        self.view.SetCentroidParamToRange(self.params.CENTROID_MIN_VALUE, self.params.CENTROID_MAX_VALUE)
        self.view.SetCentroidParamTo(self.params.CENTROID_MAX_VALUE)
        self.view.SetLabelPopulationText("Cantidad de individuos [" + str(self.params.POPULATION_MIN_VALUE) + " - " + str(self.params.POPULATION_MAX_VALUE) + "]")
        self.view.SetPopulationSpinRange(self.params.POPULATION_MIN_VALUE, self.params.POPULATION_MAX_VALUE)
        self.view.SetPopulationSpinValue(self.params.POPULATION_DEFAULT_VALUE)
        self.view.SetLabelIterationText("Cantidad de iteraciones [" + str(self.params.ITERATION_MIN_VALUE) + " - " + str(self.params.ITERATION_MAX_VALUE) + "]")
        self.view.SetIterationSpinRange(self.params.ITERATION_MIN_VALUE, self.params.ITERATION_MAX_VALUE)
        self.view.SetIterationSpinValue(self.params.ITERATION_DEFAULT_VALUE)
        self.view.SetAlgorithmList(self.params.CLUSTERING_ALGORITHMS)
        self.view.SetAlgorithmSelection(self.params.CLUSTERING_ALGORITHM_DEFAULT)
        self.view.HideGeneticParameters()

    def SetAlgorithm(self, index, name):
        print("DEBUG - Selected index: %d; value: %s" % (index, name))
        if(index == 1):
            self.view.HideGeneticParameters()
        else:
            if(index == 2):
                self.view.ShowGeneticParameters()
        self.localModel.clusteringAlgorithm = index

    def SetCentroidParam(self, value):
        print("DEBUG - Selected value: %d" % value)
        self.localModel.clusters = value

    def SetCentroidRangeMinParam(self, value):
        print("DEBUG - Selected value: %d" % value)
        self.localModel.clusters_range_min = value

    def SetCentroidRangeMaxParam(self, value):
        print("DEBUG - Selected value: %d" % value)
        self.localModel.clusters_range_max = value

    def SetPopulationParam(self, value):
        print("DEBUG - Population value: %d" % value)
        self.localModel.maxPopulation = value

    def SetIterationParam(self, value):
        print("DEBUG - Iteration value: %d" % value)
        self.localModel.maxIterations = value

    def RadioFixedClassParamClicked(self, value):
        self.localModel.clustersFixed = True
        self.view.HideVarClassesParameter()
        self.view.ShowFixedClassesParameter()

    def RadioVarClassParamClicked(self, value):
        self.localModel.clustersFixed = False
        self.view.HideFixedClassesParameter()
        self.view.ShowVarClassesParameter()

    def Cancel(self):
        self.view.EndModal(False)

    def Process(self):
        # Si eligio rango de clases, verificamos que el rango sea valido
        if self.view.getRadioFixedClassParam() is False:
            if self.view.getspinVarClassParamFrom() >= self.view.getspinVarClassParamTo():
                self.view.ShowErrorMessage("El rango de clases para optimizar no es valido.")
                return False

        # Copio los parametros modificados al modelo global
        for k, v in self.localModel.__dict__.items():
            setattr(self.model, k, v)

        self.view.EndModal(True)

    def Start(self):
        return self.view.Start()
