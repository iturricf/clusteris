# -*- coding: utf-8 -*-

import math
from random import randint, uniform
from timer import Timer

import numpy as np

# from genetic.individual import Individual

class Genetic(object):
    INITIAL_POPULATION = 15
    MAX_ITERATIONS = 50
    FITNESS_THRESHOLD = 0.1

    SELECTION_RATIO = 0.2
    CROSSING_RATIO = 0.6
    MUTATION_RATIO = 0.2

    MUTATION_PROBABILITY = 0.1
    MUTATION_RETRY = 10


    def __init__(self, params):
        self.NClusters = params['n_clusters']

    def Fit(self, dataset):
        t = Timer()

        t.AddTime("Start")
        self.dataset = dataset
        self.datasetLen, self.datasetDimension = list(dataset.shape)

        self.population = self._GetInitialPop()

        t.AddTime("Initial pop")

        t.AddTime("Fitness")

        self.bestIndividual = None

        for it in range(self.MAX_ITERATIONS):
            self.fitness = [i.Fitness() for i in self.population]

            minFit = np.argmin(self.fitness)
            # print('DEBUG - Min fit key %d - value: %f' % (minFit, self.fitness[minFit]))

            if (self.fitness[minFit] <= self.FITNESS_THRESHOLD):
                self.bestIndividual = self.population[minFit]
                break

            newPop = []

            # Aseguro al mejor miembro de la población
            eliteInd = self._ElitistSelection()

            newPop.append(eliteInd)

            selectionAmount = len(self.population) * self.SELECTION_RATIO

            print('DEBUG - Selection amount: %s' % selectionAmount)
            # Selecciona cantidad de individuos de la población mediante ruleta
            selected = self._WheelSelection(selectionAmount - 1) # Porque ya tengo uno de elite

            newPop.extend(selected)

            crossAmount = len(self.population) * self.CROSSING_RATIO

            print('DEBUG - Crossing amount: %s' % crossAmount)

            crossOverflow = crossAmount % 2.0
            crossAmount = math.ceil(crossAmount / 2.0)

            print('DEBUG - Overflow: %s' % crossOverflow)
            print('DEBUG - Cross: %s' % crossAmount)

            toCross = self._GetCrossingPairs(crossAmount)

            for pair in toCross:
                child1, child2 = self._MakeCross(pair[0], pair[1])
                newPop.append(child1)
                newPop.append(child2)


            print(len(newPop))

            mutationAmount = int(len(self.population) * self.MUTATION_RATIO)

            print('DEBUG - Mutation amount: %s' % mutationAmount)

            if crossOverflow > 0:
                mutationAmount -= 1

            print('DEBUG - Mutation amount: %s' % mutationAmount)

            mutated = self._GetMutated(mutationAmount)

            newPop.extend(mutated)

            if (len(newPop) < len(self.population)):
                missingPop = len(self.population) - len(newPop)

                toCross = self._GetCrossingPairs(missingPop)

                for pair in toCross:
                    child1, child2 = self._MakeCross(pair[0], pair[1])

                    newPop.append(child1)

                    if (len(newPop) == len(self.population)):
                        break

                    newPop.append(child2)

                    if (len(newPop) == len(self.population)):
                        break

            print("New pop lenght: %d" % len(newPop))

            t.AddTime("Iteration %d" % it)

        if self.bestIndividual == None:
            minFit = np.argmin(self.fitness)
            self.bestIndividual = self.population[minFit]

        print('DEBUG - Genetic Fit.')
        t.AddTime("End")

        t.PrintTimes()

        print('DEBUG - Fitness: %s' % self.fitness[minFit])

    def GetCentroids(self):
        print('DEBUG - Genetic Centroids.')
        return self.bestIndividual.centroids

    def GetLabels(self):
        print('DEBUG - Genetic Labels.')
        return self.bestIndividual.elements

    def _GetMutated(self, quantity=1):
        toMutate = []

        for i in range(self.MUTATION_RETRY):
            tryMutation = [individual for individual in self._RandomSelection(quantity) if uniform(0, 1) < self.MUTATION_PROBABILITY]
            toMutate.extend(tryMutation)

            if (len(toMutate) >= quantity):
                break

        print(len(toMutate))
        for i in toMutate:
            i.Mutate()

        return toMutate

    def _MakeCross(self, parent1, parent2):
        p1Genes = parent1.centroids.flatten()
        p2Genes = parent2.centroids.flatten()

        crossPoint = randint(1, len(p1Genes) -2)

        child1Genes = p1Genes[:crossPoint].tolist() + p2Genes[crossPoint:].tolist()
        child2Genes = p2Genes[:crossPoint].tolist() + p1Genes[crossPoint:].tolist()

        child1 = Individual(np.reshape(child1Genes, (parent1.clusters, self.datasetDimension)), self.dataset)
        child2 = Individual(np.reshape(child2Genes, (parent2.clusters, self.datasetDimension)), self.dataset)

        return child1, child2

    def _GetCrossingPairs(self, quantity=1):
        pairs = []

        for i in range(int(quantity)):
            pairs.append(self._RandomSelection(2))

        return pairs

    def _WheelSelection(self, quantity=1):
        # Aptitud total de la población
        sumF = sum(self.fitness)
        # Probabilidades acumuladas asociadas a cada individuo
        prob = [(value + sum(self.fitness[:key])) / sumF for key, value in enumerate(self.fitness)]
        # Ruleta
        p = []
        for i in range(int(quantity)):
            p.append(uniform(0, 1))

        # Elegir individuo de acuerdo a probabilidad calculada
        positions = np.searchsorted(prob, p)

        return [self.population[key] for key in positions]

    def _RandomSelection(self, quantity=1):
        positions = []

        for i in range(int(quantity)):
            positions.append(randint(0, len(self.population) - 1))

        return [self.population[key] for key in positions]

    def _ElitistSelection(self):
        return self.population[np.argmin(self.fitness)]

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

    def _GetMinFitness(self):
        self.fitness

class Individual(object):

    def __init__(self, centroids, dataset):
        self.dataset = dataset
        self.centroids = np.array(centroids)
        self.clusters = len(centroids)
        self.elements = []
        self.classElements = [[] for i in range(self.clusters)]

        self.datasetLen, self.datasetDimension = list(dataset.shape)

        self.Update()

    def Update(self):
        for key, value in enumerate(self.dataset):
            distance = []
            points = []
            for c in self.centroids:
                # centroid = self.centroids[k]
                d = np.linalg.norm(c - value) # distance
                distance.append(d)
                points.append(value)

            classNo = np.argmin(distance) # Class Number

            self.elements.append(classNo)
            self.classElements[classNo].append(points[classNo])

    def Mutate(self):
        c = randint(0, self.clusters - 1) # Centroide aleatorio
        component = randint(0, self.datasetDimension - 1) # Componente del centroide

        delta = randint(1, 5)

        if uniform(0, 1) < 0.5:
            delta *= -1

        self.centroids[c][component] += delta

        self.Update()

    def Fitness(self):
        # print('DEBUG - Individual Genetic Fitness.')
        intercluster = self._Intercluster()
        intracluster = self._Intracluster()

        fitness = 1.0 / (min(intercluster) / max(intracluster))

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
            for m, point1 in enumerate(self.classElements[i]):
                for point2 in self.classElements[m+1:]:
                    try:
                        d = np.linalg.norm(point2 - point1) # distance
                        distance.append(d)
                    except ValueError, e:
                        print(point2)
                        print(point1)
                        print(e)


            intracluster.append(distance[np.argmax(distance)])

        return intracluster
