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
        self.localModel.maxPopulation = self.params.POPULATION_DEFAULT_VALUE
        self.localModel.maxIterations = self.params.ITERATION_DEFAULT_VALUE

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
        self.view.HideGeneticParameters()

        self._DisablePlotterOptions()

        if (self.localModel.datasetCols == 2):
            self.view.Enable2DRadio()

            self.Radio2DClicked(True)

        if (self.localModel.datasetCols >= 3):
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
        self.localModel.clusteringAlgorithm = index

    def SetCentroidParam(self, value):
        print("DEBUG - Selected value: %d" % value)
        self.localModel.clusters = value

    def SetPopulationParam(self, value):
        print("DEBUG - Population value: %d" % value)
        self.localModel.maxPopulation = value

    def SetIterationParam(self, value):
        print("DEBUG - Iteration value: %d" % value)
        self.localModel.maxIterations = value

    def Radio2DClicked(self, value):
        print('DEBUG - Plotter 2D: %s' % value)
        if value:
            self.localModel.selectedAxes = 2
            self._SetAllAxesList(self.localModel.datasetColsNames)
            self.view.SetZAxeList([])
            self.view.DisableZAxeChoice()

            self.view.SetXAxeSelection(0)
            self.SetSelectedAxe(0, 0)
            self.view.SetYAxeSelection(1)
            self.SetSelectedAxe(1, 1)

            if (self.localModel.datasetCols > 2):
                self.view.EnableXAxeChoice()
                self.view.EnableYAxeChoice()

    def Radio3DClicked(self, value):
        print('DEBUG - Plotter 3D: %s' % value)
        if value:
            self.localModel.selectedAxes = 3
            self._SetAllAxesList(self.localModel.datasetColsNames)

            self._DisableAllLists()

            self.view.SetXAxeSelection(0)
            self.SetSelectedAxe(0, 0)
            self.view.SetYAxeSelection(1)
            self.SetSelectedAxe(1, 1)
            self.view.SetZAxeSelection(2)
            self.SetSelectedAxe(2, 2)

            if (self.localModel.datasetCols > 3):
                self.view.EnableXAxeChoice()
                self.view.EnableYAxeChoice()
                self.view.EnableZAxeChoice()

    def SetSelectedAxe(self, axe, value):
        print('DEBUG - Selected axe value: %d - %d' % (axe, value))
        self.localModel.colsForAxes[axe] = value
        print("Axes:: %s" % self.localModel.colsForAxes)

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
        self.view.SetXAxeList(self.localModel.datasetColsNames)
        self.view.SetYAxeList(self.localModel.datasetColsNames)
        self.view.SetZAxeList(self.localModel.datasetColsNames)

    def _DisableAllLists(self):
        self.view.DisableXAxeChoice()
        self.view.DisableYAxeChoice()
        self.view.DisableZAxeChoice()

    def _IsPlotterConfigValid(self):
        for i in range(self.localModel.selectedAxes - 1):
            if self.localModel.colsForAxes[i] == self.localModel.colsForAxes[i+1]:
                return False

        return True

    def Cancel(self):
        self.view.EndModal(False)

    def Process(self):
        if not self._IsPlotterConfigValid():
            self.view.ShowErrorMessage("Las columnas para los ejes seleccionados debe ser distinta para cada uno.")
            return False

        # Copio los parametros modificados al modelo global
        for k, v in self.localModel.__dict__.items():
            setattr(self.model, k, v)

        self.view.EndModal(True)

    def Start(self):
        return self.view.Start()
