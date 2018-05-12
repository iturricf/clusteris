# -*- coding: utf-8 -*-

from params import Params

from main.view import MainView
from main.interactor import Interactor
from main.presenter import Presenter

view = MainView(None)
interactor = Interactor()
presenter = Presenter(view, interactor, Params)
