from random import randint, uniform
from copy import deepcopy
from sys import argv
from sklearn import metrics
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabaz_score
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
            for i in range(0, k):
                # obtenemos un punto al azar y pasa a ser un centroide
                punto = puntos[randint(0, len(puntos)-1)]
                for coordenada in punto:
                    self.centroides.append(coordenada)
            self.dimension = len(puntos[0])
            self.labels = self.asignar(puntos)
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
    def fitness(self, puntos):
        return min(self.intercluster()) / max(self.intracluster(puntos))

    def fitness2(self, puntos):
        return silhouette_score(puntos, self.labels)

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
    individuos = [Individuo(puntos, k, []) for i in range(0, numpob)]
    return individuos

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
    pop = poblacionInicial(npop, puntos, k)

    #nro de iteraciones
    iter = 1

    #Flag para verificar que todos los clusters tengan al menos un punto
    cluster_no_asignados = False

    #for i in range(0, maxit):
    while iter <= maxit or cluster_no_asignados:
        new = []
        fit = [indiv.fitness3(puntos) for indiv in pop]
        #fit2 = [indiv.fitness2(puntos) for indiv in pop]

        #seleccion elitista, se preserva el mejor individuo
        if (iter <= maxit):
            new.append(pop[np.argmax(fit)])

        while len(new) < len(pop):
            # genetic operators
            # seleccion por ruleta
            parent1 = ruleta(pop, fit)
            p = uniform(0, 1)
            # probabilidad de seleccion 20%
            if p <= 0.2:
                new.append(parent1)
            else:
                # cruza 65%
                if p <= pcros:
                    parent2 = ruleta(pop, fit)
                    while parent2 == parent1:
                        parent2 = ruleta(pop, fit)
                    child1, child2 = cruza(parent1, parent2)
                    new.append(child1)
                    if len(new) < len(pop):
                        new.append(child2)
                # mutacion 15% de los cuales mutan solo el 0.05%
                else:
                    child = deepcopy(parent1)
                    child.mutacion()
                    new.append(child)
            # asignamos los puntos a un cluster
            for indiv in new:
                indiv.labels = indiv.asignar(puntos)
            # si algun individuo tiene algun cluster vacio, lo sacamos
            for indiv in new:
                if indiv.clusterVacio() == True:
                    new.remove(indiv)
        pop = deepcopy(new)

        iter += 1

        #en la ultima iteracion obtenemos el mejor
        if(iter > maxit):
            # obtenemos el mejor individuo
            fit = [indiv.fitness3(puntos) for indiv in pop]
            best = [pop[np.argmax(fit)], max(fit)]
            cluster_no_asignados = True in [i not in best[0].labels for i in range(0, k)]

    print('DEBUG - Genetic Centroids:')
    print "\nFitness = %s" % best[1]
    print best[0].centroides
    # return best cluster
    return best[0]

class Genetic(object):
    def __init__(self, params):
        self.NClusters = params['n_clusters']

    def Fit(self, path):
        self.best = GeneticAlg(self, 10, self.NClusters, 0.50, 0.25, 40, path)

    def GetCentroids(self):
        sal = []
        for j in range(0, self.best.k):
            sal.append(self.best.centroides[j * self.best.dimension:(j + 1) * self.best.dimension])
        self.best.centroides = np.array(sal)
        return self.best.centroides

    def GetLabels(self):
        return self.best.labels