# -*- coding: utf-8 -*-

from model import Params, Processing

from config.view import ConfigView
from config.interactor import Interactor
from config.presenter import Presenter

from main.view import MainView
from main.interactor import Interactor as MainInteractor
from main.presenter import Presenter as MainPresenter

# Implements clusteris app based on the MVP pattern
#  - ConfigView is the config UI.
#  - Interactor connects events in the config UI to handlers on the Presenter.
#  - Presenter initializes the UI, process events from it and updates the view.
# view = ConfigView(None)
# interactor = Interactor()
# presenter = Presenter(view, interactor, Params)

model = Processing()
view = MainView(None)
interactor = MainInteractor()
presenter = MainPresenter(view, interactor, model, Params)

presenter.Start()
