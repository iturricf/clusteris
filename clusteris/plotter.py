# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

        self.fig = plt.figure()
        self.ax = Axes3D(self.fig)

    def PlotSamples(self, X, Y, Z, size, color):
        print('DEBUG - Plotter3D PlotSamples.')
        self.ax.scatter(X, Y, Z, c=color, s=size)

    def PlotCentroids(self, X, Y, Z, size, color):
        print('DEBUG - Plotter3D PlotCentroids.')
        self.ax.scatter(X, Y, Z, marker='*', c=color, s=size)

    def Show(self):
        plt.show()
