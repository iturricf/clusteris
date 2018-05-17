# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

class Plotter2D(object):

    def __init__(self):
        plt.rcParams['figure.figsize'] = (16, 9)
        plt.rcParams['axes.unicode_minus'] = False
        plt.style.use('ggplot')

    def PlotSamples(self, X, Y, size, color):
        print('DEBUG - Plotter2D PlotSamples.')
        plt.scatter(X, Y, s=size, c=color)

    def PlotCentroids(self, X, Y, size, color):
        print('DEBUG - Plotter2D PlotCentroids.')
        plt.scatter(X, Y, marker='*', c=color, s=size)

    def Show(self):
        plt.show()

class Plotter3D(object):

    def __init__(self):
        plt.rcParams['figure.figsize'] = (16, 9)
        plt.rcParams['axes.unicode_minus'] = False
        plt.style.use('ggplot')

    def PlotSamples(self, X, Y, Z, size, color):
        print('DEBUG - Plotter3D PlotSamples.')

    def PlotCentroids(self, X, Y, Z, size, color):
        print('DEBUG - Plotter3D PlotCentroids.')

    def Show(self):
        plt.show()
