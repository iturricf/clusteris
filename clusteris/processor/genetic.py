from random import randint, uniform
from copy import deepcopy
from sys import argv
from sklearn import metrics
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabaz_score
from sklearn.metrics import pairwise_distances_argmin
import numpy as np

def ProcessDataset(arqStr):
    arq = open(arqStr, "r")
    x, y = [], []
    for line in arq:
        lin = line.strip().split()
        x.append(map(float, lin))
    return x

class Individuo (object):
    # constructor
    def __init__(self, puntos, k, centroides):
        self.centroides = centroides
        self.k = k
        if puntos != None:
            self.dimension = len(puntos[0])
            #evitamos que elija al mismo punto como centroides
            puntosDisponibles = deepcopy(puntos)
            while (len(self.centroides)/self.dimension) < k:
                valor = randint(0, len(puntosDisponibles)-1)
                # obtenemos un punto al azar y pasa a ser un centroide
                punto = puntosDisponibles[valor]
                for coordenada in punto:
                    self.centroides.append(coordenada)
                #sacamos el punto de los puntos disponibles
                puntosDisponibles.pop(valor)
            self.labels = self.asignarPuntos(puntos)
        else:
            self.dimension = len(centroides)/k

    # asignar cada punto a un cluster
    def asignar(self, puntos):
        salida = []
        # calculamos la distancia de cada punto con cada centroide
        for punto in puntos:
            distancia = []
            for index in range(0, self.k):
                centroide = np.array(self.centroides[index*self.dimension:(index+1)*self.dimension])
                distancia.append(np.linalg.norm(np.array(punto) - centroide))
            salida.append(np.argmin(distancia))
        return salida

    def asignarPuntos(self, puntos):
        arrpoint = np.array(puntos)
        arrcentr = []
        for index in range(0, self.k):
            elem = self.centroides[index*self.dimension:(index+1)*self.dimension]
            arrcentr.append(elem)
        arrcentr = np.array(arrcentr)
        return pairwise_distances_argmin(arrpoint, arrcentr)

    # devuelve True si hay un cluster vacio y False si todos los clusters estan no vacios
    def clusterVacio(self):
        return True in [i not in self.labels for i in range(0, self.k)]

    # devuelve los elementos que pertenecen a un cluster
    def elements(self, cluster, salida):
        return np.where(np.array(salida) == cluster)[0]

    # actualizar los centroides en base a la asignacion de los puntos
    def actualizar(self, puntos, salida):
        for index in range(0, self.k):
            xi = self.elements(index, salida)
            for d in range(index*self.dimension, (index+1)*self.dimension):
                self.centroides[d] = sum(puntos[item][d%self.dimension] for item in xi)/len(xi) if len(xi) != 0 else self.centroides[d]

    # intracluster distance
    def intracluster(self, puntos):
        intra = []
        for index in range(0, self.k):
            # xi tiene los puntos que pertenecen a ese cluster (index)
            xi = self.elements(index, self.labels)
            dmax = 0
            for m, punto1 in enumerate(xi):
                for punto2 in xi[m+1:]:
                    d = np.linalg.norm(np.array(puntos[punto1])-np.array(puntos[punto2]))
                    if d > dmax:
                        dmax = d
            intra.append(dmax)
        return intra

    # intercluster distancia entre todos los clusters
    def intercluster(self):
        inter = []
        for index in range(0, self.k):
            for j in range(index+1, self.k):
                inicio = np.array(self.centroides[index*self.dimension:(index+1)*self.dimension])
                fin = np.array(self.centroides[j*self.dimension:(j+1)*self.dimension])
                inter.append(np.linalg.norm(inicio-fin))
        return inter

    # funcion de aptitud
    def fitness1(self, puntos):
        return min(self.intercluster()) / max(self.intracluster(puntos))

    # funcion de aptitud usando indice de Silhouette
    def fitness2(self, puntos):
        return silhouette_score(puntos, self.labels)

    # funcion de aptitud usando indice de Calinski
    def fitness3(self, puntos):
        return calinski_harabaz_score(puntos, self.labels)

    # operacion de mutacion
    def mutacion(self):
        for c, centroid in enumerate(self.centroides):
            delta = uniform(0,1)
            if uniform(0,1) <= 0.5:
                valor = centroid - delta*centroid
                self.centroides[c] = valor if valor >= 0 else 0
            else:
                self.centroides[c] = centroid + delta*centroid if centroid!=0 else delta

def poblacionInicial(numpob, puntos, k):
    pob = []
    while(len(pob) < numpob):
        indiv = Individuo(puntos, k, [])
        indiv.asignarPuntos(puntos)
        if not indiv.clusterVacio():
            pob.append(indiv)
    return pob
# cruza por punto simple
def cruza(padre1, padre2):
    puntoCruza = randint(1, len(padre1.centroides)-2)
    # se genera un par de nuevos individuos
    individuo1 = Individuo(None, padre1.k, padre1.centroides[:puntoCruza]+padre2.centroides[puntoCruza:])
    individuo2 = Individuo(None, padre1.k, padre2.centroides[:puntoCruza]+padre1.centroides[puntoCruza:])
    nuevosIndividuos = individuo1, individuo2
    return nuevosIndividuos

# seleccion por ruleta
def ruleta(pop, fit):
    sumf = sum(fit)
    # probabilidades asociadas a cada individuo
    prob = [(item + sum(fit[:index])) / sumf for index, item in enumerate(fit)]
    p = uniform(0, 1)
    # vemos que posicion de individuo fue seleccionado en base a la probabilidad
    position = np.searchsorted(np.asarray(prob), p)
    return pop[position]

def GeneticAlg(self, npop, k, pcros, pmut, maxit, arqStr):
    puntos = ProcessDataset(arqStr)
    #generamos la poblacion inicial
    pop = poblacionInicial(npop, puntos, k)

    for i in range(0, maxit):
        new = []
        fit = [indiv.fitness3(puntos) for indiv in pop]

        # seleccion elitista, se preserva el mejor individuo para la siguiente poblacion
        new.append(pop[np.argmax(fit)])

        while len(new) < len(pop):
            # genetic operators
            # seleccion por ruleta
            parent1 = ruleta(pop, fit)
            p = uniform(0, 1)
            # seleccion por ranking
            if p <= 0.2:
                parent1.labels = parent1.asignarPuntos(puntos)
                # si este individuo tiene todos los cluster no vacios, lo incluimos a la nueva poblacion
                if not parent1.clusterVacio():
                    new.append(parent1)
            else:
                # cruza simple en un punto
                if p <= pcros:
                    parent2 = ruleta(pop, fit)
                    while parent2 == parent1:
                        parent2 = ruleta(pop, fit)
                    child1, child2 = cruza(parent1, parent2)
                    child1.labels = child1.asignarPuntos(puntos)
                    if not child1.clusterVacio():
                        new.append(child1)
                    if len(new) < len(pop):
                        child2.labels = child2.asignarPuntos(puntos)
                        if not child2.clusterVacio():
                            new.append(child2)
                # mutacion
                else:
                    child = deepcopy(parent1)
                    child.mutacion()
                    child.labels = child.asignarPuntos(puntos)
                    if not child.clusterVacio():
                        new.append(child)
        # actualizamos la nueva poblacion
        pop = deepcopy(new)
    # obtenemos el mejor individuo de la ultima poblacion generada
    fit = [indiv.fitness3(puntos) for indiv in pop]
    best = [pop[np.argmax(fit)], max(fit)]

    print('DEBUG - Genetic Centroids:')
    print "\nFitness = %s" % best[1]
    print best[0].centroides
    # return best cluster
    return best[0]

class Genetic(object):
    def __init__(self, params):
        self.NClusters = params['n_clusters']

    def Fit(self, path):
        self.best = GeneticAlg(self, 40, self.NClusters, 0.50, 0.25, 50, path)

    def GetCentroids(self):
        sal = []
        for j in range(0, self.best.k):
            sal.append(self.best.centroides[j * self.best.dimension:(j + 1) * self.best.dimension])
        self.best.centroides = np.array(sal)
        return self.best.centroides

    def GetLabels(self):
        return self.best.labels