# -*- coding: utf-8 -*-

from params import Params

from main.view import MainView
from main.interactor import Interactor
from main.presenter import Presenter

# Implements clusteris app based on the MVP pattern
#  - MainView is the main UI.
#  - Interactor connects events in the main UI to handlers on the Presenter.
#  - Presenter initializes the UI, process events from it and updates the view.
view = MainView(None)
interactor = Interactor()
presenter = Presenter(view, interactor, Params)
