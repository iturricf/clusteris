# -*- coding: utf-8 -*-

from params import Params

from config.view import MainView
from config.interactor import Interactor
from config.presenter import Presenter

# Implements clusteris app based on the MVP pattern
#  - MainView is the config UI.
#  - Interactor connects events in the config UI to handlers on the Presenter.
#  - Presenter initializes the UI, process events from it and updates the view.
view = MainView(None)
interactor = Interactor()
presenter = Presenter(view, interactor, Params)
