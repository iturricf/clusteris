# -*- coding: utf-8 -*-

from copy import deepcopy

class PlotterConfigPresenter(object):
    """
    Process UI events and updates view with results.
    """

    def __init__(self, view, interactor, model):
        self.view = view
        self.interactor = interactor
        self.model = model
        self.localModel = deepcopy(self.model)

        interactor.Connect(self, view)

        # self.InitModel()
        self.InitView()

    def InitView(self):
        """Sets default values for the UI."""

        self._DisablePlotterOptions()

        if (self.localModel.datasetCols == 2):
            self.view.Enable2DRadio()

            self.Radio2DClicked(True)

        if (self.localModel.datasetCols >= 3):
            self.view.Enable2DRadio()
            self.view.Enable3DRadio()
            self.view.Set3DSelected()

            self.Radio3DClicked(True)

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
