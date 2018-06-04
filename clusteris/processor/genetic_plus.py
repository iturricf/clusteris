# -*- coding: utf-8 -*-

import math
from copy import deepcopy
from random import randint, uniform
from timer import Timer

import numpy as np
from sklearn.metrics import calinski_harabaz_score

class Genetic(object):
    INITIAL_POPULATION = 20 # Cantidad de individuos en la población inicial
    MAX_ITERATIONS = 10 # Cantidad de iteraciones
    FITNESS_THRESHOLD = 0.1

    SELECTION_RATIO = 0.2 # Porcentaje de selección
    CROSSING_RATIO = 0.6 # Porcentaje de cruza
    MUTATION_RATIO = 0.2 # Porcentaje de mutación

    MUTATION_PROBABILITY = 0.1 # Probabilidad de mutación para individuo seleccionado
    MUTATION_RETRY = 10 # Reintentos del proceso de mutación


    def __init__(self, params):
        """ Se inicializan los parametros del procesador genético."""
        self.NClusters = params['n_clusters']

    def SetListener(self, listener):
        self.listener = listener

    def Fit(self, dataset):
        """ Calcula la mejor distribución de los puntos del dataset, según los parámetros elegidos."""
        t = Timer()

        # self.listener.Start()

        t.AddTime("Start")
        self.dataset = dataset
        self.datasetLen, self.datasetDimension = list(dataset.shape)

        self.population = self._GetInitialPop() # 1. Generación de población inicial

        t.AddTime("Initial pop")

        self.bestIndividual = None

        for it in range(self.MAX_ITERATIONS):
            self.fitness = [i.Fitness() for i in self.population] # 2. Calculo de aptitud de la población

            minFit = np.argmax(self.fitness)
            print('DEBUG - Min fit key %d - value: %f' % (minFit, self.fitness[minFit]))

            # if (self.fitness[minFit] <= self.FITNESS_THRESHOLD): # 3. Primera condición de parada
            #     self.bestIndividual = self.population[minFit]
            #     break

            newPop = [] # Construcción de la nueva población

            # 4. Selección de individuos. Elitista + Ruleta

            # Aseguro al mejor miembro de la población
            eliteInd = self._ElitistSelection()
            newPop.append(eliteInd)

            # Selecciona el resto por ruleta

            selectionAmount = int(len(self.population) * self.SELECTION_RATIO)

            print('DEBUG - Selection amount: %s' % selectionAmount)

            selected = self._WheelSelection(selectionAmount - 1) # Porque ya tengo uno de elite
            newPop.extend(selected)

            # 5. Cruza pares de individuos seleccionados al azar

            crossAmount = int(len(self.population) * self.CROSSING_RATIO) # Cantidad de individuos resultados de la cruza

            print('DEBUG - Crossing amount: %s' % crossAmount)

            crossOverflow = crossAmount % 2.0
            crossAmount = int(math.ceil(crossAmount / 2.0)) # Se usa la mitad de pares para generar 2 hijos

            print('DEBUG - Overflow: %s' % crossOverflow)
            print('DEBUG - Cross: %s' % crossAmount)

            toCross = self._GetCrossingPairs(crossAmount) # Selección de pares

            for pair in toCross:
                child1, child2 = pair[0].CrossWith(pair[1]) # Cruza
                newPop.append(child1)
                newPop.append(child2)

            # 6. Mutación de individuos seleccionados al azar

            mutationAmount = int(len(self.population) * self.MUTATION_RATIO)

            # Si se obtuvo un individuo extra en la cruza resto uno para mutar
            if crossOverflow > 0:
                mutationAmount -= 1

            print('DEBUG - Mutation amount: %s' % mutationAmount)

            mutated = self._GetMutated(mutationAmount)

            newPop.extend(mutated)

            # El método anterior no asegura individuos mutados por lo tanto
            # se completa la población con nuevas cruzas si es necesario
            if (len(newPop) < len(self.population)):
                missingPop = len(self.population) - len(newPop)

                toCross = self._GetCrossingPairs(missingPop)

                for pair in toCross:
                    child1, child2 = pair[0].CrossWith(pair[1])

                    newPop.append(child1)

                    if (len(newPop) == len(self.population)):
                        break

                    newPop.append(child2)

                    if (len(newPop) == len(self.population)):
                        break

            print("New pop lenght: %d" % len(newPop))

            self.population = newPop

            t.AddTime("Iteration %d" % it)

            self.listener.Update(it+10)

        # 7. Ultima condición de parada, fin de las iteraciones
        # Si no encontré una solución antes, uso la mejor despues del proceso
        if self.bestIndividual is None:
            minFit = np.argmax(self.fitness)
            self.bestIndividual = self.population[minFit]

        t.AddTime("End")

        t.PrintTimes()

        print('DEBUG - Fitness: %s' % self.fitness[minFit])
        # self.listener.Finish()

    def GetCentroids(self):
        """ Devuelve los centroides calculados."""
        return self.bestIndividual.centroids

    def GetLabels(self):
        """ Devuelve un array de etiquetas asociadas a cada punto."""
        return self.bestIndividual.elements

    def _GetMutated(self, quantity=1):
        """ Intenta devolver mutaciones de los individuos de la población, en la cantidad especificada."""
        toMutate = []

        for i in range(self.MUTATION_RETRY):
            tryMutation = [deepcopy(individual) for individual in self._RandomSelection(quantity) if uniform(0, 1) < self.MUTATION_PROBABILITY]

            for m in tryMutation:
                toMutate.append(m)
                if len(toMutate) >= quantity:
                    break

            if (len(toMutate) >= quantity):
                break

        print('DEBUG - Actual mutations: %s' % len(toMutate))
        for i in toMutate:
            i.Mutate()

        return toMutate

    def _GetCrossingPairs(self, quantity=1):
        """ Selecciona pares de individuos para ser cruzados."""
        pairs = []

        for i in range(quantity):
            pairs.append(self._RandomSelection(2))

        return pairs

    def _WheelSelection(self, quantity=1):
        """ Selección de individuos por método de ruleta."""

        # Aptitud total de la población
        sumF = sum(self.fitness)
        # Probabilidades acumuladas asociadas a cada individuo
        prob = [(value + sum(self.fitness[:key])) / sumF for key, value in enumerate(self.fitness)]
        # Ruleta
        p = []
        for i in range(quantity):
            p.append(uniform(0, 1))

        # Elegir individuo de acuerdo a probabilidad calculada
        positions = np.searchsorted(prob, p)

        return [self.population[key] for key in positions]

    def _RandomSelection(self, quantity=1):
        """ Selección aleatoria de individuos."""
        positions = []

        for i in range(quantity):
            positions.append(randint(0, len(self.population) - 1))

        return [self.population[key] for key in positions]

    def _ElitistSelection(self):
        """ Selección elitista del mejor individuo."""
        return self.population[np.argmax(self.fitness)]

    def _GetInitialPop(self):
        """ Generación de población inicial aleatoria basada en puntos existentes."""
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
    """
    Representa un individuo potencial solución al problema de clustering.

     - El individuo conoce su aptitud,
     - tiene capacidad de mutar sus genes y actualizar su clasificación
       interna de los puntos al cambiar su estructura.
     - Además tiene la capacidad de realizar la cruza de sí mismo con otro
       individuo
    """

    def __init__(self, centroids, dataset):
        """
        Inicializa la estructura del individuo con los centroides y el dataset.
        Luego actualiza la asignación de puntos del dataset al centroide
        correspondiente.
        """
        self.dataset = dataset
        self.centroids = np.array(centroids)
        self.clusters = len(centroids)

        self.datasetLen, self.datasetDimension = list(dataset.shape)

        self.CalcRanges()

        self.Update()

    def CalcRanges(self):
        self.datasetRanges = []

        for i in range(self.datasetDimension):
            minValue = min(self.dataset[:, i])
            maxValue = max(self.dataset[:, i])

            self.datasetRanges.append((minValue, maxValue))

    def Update(self):
        """ Actualiza la asignación de puntos del dataset al centroide correspondiente."""

        self.fitness = None
        self.elements = []
        self.classElements = [[] for i in range(self.clusters)]

        for key, value in enumerate(self.dataset):
            distance = []
            points = []
            for c in self.centroids:
                d = np.linalg.norm(c - value) # distancia
                distance.append(d)
                points.append(value)

            classNo = np.argmin(distance) # La clase del punto

            self.elements.append(classNo) # Array clases para cada punto
            self.classElements[classNo].append(points[classNo]) # Tabla de clases y puntos por clases

    def Mutate(self):
        c = randint(0, self.clusters - 1) # Centroide aleatorio
        component = randint(0, self.datasetDimension - 1) # Componente del centroide

        genMutation = uniform(self.datasetRanges[component][0], self.datasetRanges[component][1])

        self.centroids[c][component] = genMutation # Mutación del centroide

        self.Update() # Actualización luego de modificar la estructura

    def CrossWith(self, parent2):
        """ Realiza la cruza del individuo actual con el parent2 y devuelve una tupla con los 2 hijos resultantes."""
        p1Genes = self.centroids.flatten()
        p2Genes = parent2.centroids.flatten()

        crossPoint = randint(1, len(p1Genes) -2)

        child1Genes = p1Genes[:crossPoint].tolist() + p2Genes[crossPoint:].tolist()
        child2Genes = p2Genes[:crossPoint].tolist() + p1Genes[crossPoint:].tolist()

        child1 = Individual(np.reshape(child1Genes, (self.clusters, self.datasetDimension)), self.dataset)
        child2 = Individual(np.reshape(child2Genes, (parent2.clusters, self.datasetDimension)), self.dataset)

        return child1, child2

    def Fitness(self):
        """ Calcula la aptitud del individuo."""
        # intercluster = self._Intercluster()
        # intracluster = self._Intracluster()

        # fitness = 1.0 / (min(intercluster) / max(intracluster))

        # print("Fitness: %f" % fitness)

        # return fitness

        if self.fitness is None:
            for pointClass in self.classElements:
                if len(pointClass) == 0:
                    print("Cluster VACIO!!!")
                    self.fitness = 0
                    return self.fitness

            self.fitness = calinski_harabaz_score(self.dataset, self.elements)
            print("Fitness: %f" % self.fitness)

            return self.fitness
        else:
            return self.fitness

    def _Intercluster(self):
        intercluster = []

        for i in range(self.clusters):
            for j in range(i+1, self.clusters):
                c1 = self.centroids[i]
                c2 = self.centroids[j]
                intercluster.append(np.linalg.norm(c1 - c2))

        return intercluster

    def _Intracluster(self):
        intracluster = []

        for i in range(self.clusters):
            distance = []
            for m, point1 in enumerate(self.classElements[i]):
                for point2 in self.classElements[m+1:]:
                    try:
                        d = np.linalg.norm(point2 - point1) # distance
                        distance.append(d)
                    except ValueError, e:
                        for c in self.centroids:
                            print(c)
                        print(point2)
                        print(point1)
                        print(e)


            intracluster.append(distance[np.argmax(distance)])

        return intracluster
