# -*- coding: utf-8 -*-

import numpy as np

class Dummy(object):

    def __init__(self, params):
        self.NClusters = params['n_clusters']

    def SetListener(self, listener):
        pass

    def Fit(self, dataset):
        self.dataset = dataset
        self.rows, self.cols = list(dataset.shape)
        print('DEBUG - Rows #: %d' % self.rows)
        print('DEBUG - Cols #: %d' % self.cols)

    def GetCentroids(self):
        return []

    def GetLabels(self):
        return np.zeros(self.rows, dtype=int)
