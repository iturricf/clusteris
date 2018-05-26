# -*- coding: utf-8 -*-

import numpy as np
from random import randint

# from genetic.individual import Individual

class Genetic(object):
    INITIAL_POPULATION = 15
    MAX_ITERATIONS = 50


    def __init__(self, params):
        self.NClusters = params['n_clusters']

    def Fit(self, dataset):
        self.dataset = dataset
        self.datasetLen, self.datasetDimension = list(dataset.shape)

        initialPop = self._GetInitialPop()

        self.fitness = [i.Fitness() for i in initialPop]

        exit()

        print('DEBUG - Genetic Fit.')

    def GetCentroids(self):
        print('DEBUG - Genetic Centroids.')

    def GetLabels(self):
        print('DEBUG - Genetic Labels.')


    def _GetInitialPop(self):
        population = []
        for i in range(self.INITIAL_POPULATION):
            tempDataset = self.dataset

            individual = []

            for k in range(self.NClusters):
                index = randint(0, len(tempDataset)-1)
                individual.append(tempDataset[index])
                tempDataset = np.delete(tempDataset, index, 0)

            population.append(Individual(individual, self.dataset))

        return population

class Individual(object):

    def __init__(self, centroids, dataset):
        self.dataset = dataset
        self.centroids = centroids
        self.clusters = len(centroids)
        self.elements = []
        self.classElements = [[] for i in range(self.clusters)]

        for p in dataset:
            distance = []
            points = []
            for k in range(self.clusters):
                centroid = np.array(centroids[k])
                d = np.linalg.norm(centroid - p) # distance
                distance.append(d)
                points.append(p)

            classNo = np.argmin(distance) # Class Number

            self.elements.append(classNo)
            self.classElements[classNo].append(points[classNo])

        print(self.classElements)

    def Fitness(self):
        # print('DEBUG - Individual Genetic Fitness.')
        intercluster = self._Intercluster()
        intracluster = self._Intracluster()

        fitness = min(intercluster) / max(intracluster)

        print("Fitness: %f" % fitness)

        return fitness

    def _Intercluster(self):
        # print('DEBUG - Individual Genetic Intercluster.')
        intercluster = []

        for i in range(self.clusters):
            for j in range(i+1, self.clusters):
                c1 = self.centroids[i]
                c2 = self.centroids[j]
                intercluster.append(np.linalg.norm(c1 - c2))

        return intercluster

    def _Intracluster(self):
        # print('DEBUG - Individual Genetic Intracluster.')
        intracluster = []

        for i in range(self.clusters):
            distance = []
            for m in range(len(self.classElements[i])):
                for n in range(m+1, len(self.classElements[i])):
                    element1 = self.classElements[i][m]
                    element2 = self.classElements[i][n]
                    d = np.linalg.norm(element1 - element2) # distance

                    distance.append(d)

            intracluster.append(distance[np.argmax(distance)])

        return intracluster
