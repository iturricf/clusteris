# -*- coding: utf-8 -*-

from sklearn.cluster import KMeans as K

from timer import Timer

class KMeans(object):

    def __init__(self, params):
        self.NClusters = params['n_clusters']
        self.kmeans = K(self.NClusters)

    def SetListener(self, listener):
        pass

    def Fit(self, dataset):
        t = Timer()
        t.AddTime("Start")
        self.dataset = dataset

        self.kmeans.fit(dataset)

        print('DEBUG - KMeans Centroids:')
        print(self.kmeans.cluster_centers_)

        t.AddTime("End")

        t.PrintTimes()

    def GetCentroids(self):
        return self.kmeans.cluster_centers_

    def GetLabels(self):
        return self.kmeans.labels_
