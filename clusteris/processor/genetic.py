from random import randint, uniform
from copy import deepcopy
from sys import argv
import numpy as np

def ProcessDataset(arqStr):
    arq = open(arqStr, "r")
    x, y = [], []
    for line in arq:
        lin = line.strip().split()
        x.append(map(float, lin))
    return x

def BinSearch(prob,p,imin,imax):
	imid = (imin+imax)/2
	if imid == len(prob)-1 or imid == 0:
		return imid
	if p > prob[imid] and p <= prob[imid+1]:
		return imid+1
	elif p < prob[imid]:
		imid = BinSearch(prob,p,imin,imid)
	else:
		imid = BinSearch(prob,p,imid,imax)
	return imid

class Individuo (object):
    # constructor
    def __init__(self, puntos, k, centroides):
        self.centroides = centroides
        self.puntos = puntos
        self.k = k
        if puntos != None:
            for i in range(0, k):
                # obtenemos un punto al azar y pasa a ser un centroide
                punto = puntos[randint(0, len(puntos)-1)]
                for coordenada in punto:
                    self.centroides.append(coordenada)
            self.dimension = len(puntos[0])
        else:
            self.dimension = len(centroides)/k

    # asignar cada punto a un cluster
    def asignar(self, puntos):
        salida = []
        # calculamos la distancia de cada punto con cada centroide
        for punto in puntos:
            distancia = []
            for index in range(0, self.k):
                centroide = np.array(self.centroides[ index*self.dimension:(index+1)*self.dimension])
                distancia.append(np.linalg.norm(np.array(punto) - centroide))
            salida.append(np.argmin(distancia))
        return salida

    #
    def elements(self, cluster, salida):
        return np.where(np.array(salida) == cluster)[0]

    # actualizar los centroides en base a la asignacion de los puntos
    def actualizar(self, puntos, salida):
        for index in range(0, self.k):
            xi = self.elements(index, salida)
            for d in range(index*self.dimension, (index+1)*self.dimension):
                self.centroides[d] = sum(puntos[item][d%self.dimension] for item in xi)/len(xi) if len(xi) != 0 else self.centroides[d]

    # intracluster distance
    def intracluster(self, puntos, salida):
        intra = []
        for index in range(0, self.k):
            xi = self.elements(index, salida)
            dmax = 0
            for m, punto1 in enumerate(xi):
                for punto2 in xi[m+1:]:
                    d = np.linalg.norm(np.array(puntos[punto1])-np.array(puntos[punto2]))
                    if d > dmax:
                        dmax = d
            intra.append(dmax)
        return intra

    # intercluster distancia para todos los clusters
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
        salida = self.asignar(puntos)
        self.actualizar(puntos, salida)
        return min(self.intercluster())/max(self.intracluster(puntos, self.asignar(puntos)))

    # operacion de mutacion
    def mutacion(self, probmut):
        for c,centroid in enumerate(self.centroides):
            if uniform(0,1) <= probmut:
                delta = uniform(0,1)
                if uniform(0,1) <= 0.5:
                    valor = centroid - 2*delta*centroid
                    self.centroides[c] = valor if valor >= 0 else 0
                else:
                    self.centroides[c] = centroid + 2*delta*centroid if centroid!=0 else 2*delta

def poblacionInicial(numpob, puntos, k):
    individuos = [Individuo(puntos, k, []) for i in range(0, numpob)]
    return individuos

# cruza por punto simple
def cruza(padre1, padre2, k):
    puntoCruza = randint(1, len(padre1.centroides)-2)
    # se genera un par de nuevos individuos
    individuo1 = Individuo(None, k, padre1.centroides[:puntoCruza]+padre2.centroides[puntoCruza:])
    individuo2 = Individuo(None, k, padre2.centroides[:puntoCruza]+padre1.centroides[puntoCruza:])
    nuevosIndividuos = individuo1, individuo2
    return nuevosIndividuos

# seleccion por ruleta
def ruleta(pop, fit):
    sumf = sum(fit)
    prob = [(item + sum(fit[:index])) / sumf for index, item in enumerate(fit)]
    return pop[BinSearch(prob, uniform(0, 1), 0, len(prob) - 1)]

def GeneticAlg(self, npop, k, pcros, pmut, maxit, arqStr):
    puntos = ProcessDataset(arqStr)
    pop = poblacionInicial(npop, puntos, k)
    fit = [indiv.fitness(puntos) for indiv in pop]
    verybest = [pop[np.argmax(fit)], max(fit)]
    for i in range(0, maxit):
        fit = [indiv.fitness(puntos) for indiv in pop]
        new = []
        while len(new) < len(pop):
            # selection
            parent1 = ruleta(pop, fit)
            p = uniform(0, 1)
            # genetic operators
            if p <= pcros:
                parent2 = ruleta(pop, fit)
                while parent2 == parent1:
                    parent2 = ruleta(pop, fit)
                child1, child2 = cruza(parent1, parent2, k)
                new.append(child1)
                if len(new) < len(pop):
                    new.append(child2)
            else:
                child = deepcopy(parent1)
                child.mutacion(pmut)
                new.append(child)
        pop = deepcopy(new)
        # elitism (but individual is kept outside population)
        if max(fit) > verybest[1]:
            verybest = [pop[np.argmax(fit)], max(fit)]
    verybest[0].cluster = indiv.asignar(puntos)
    print('DEBUG - Genetic Centroids:')
    print "\nFitness = %s" % verybest[1]
    print verybest[0].centroides
    # return best cluster
    return verybest[0]

class Genetic(object):

    def __init__(self, params):
        self.NClusters = params['n_clusters']

    def Fit(self, path):
        self.best = GeneticAlg(self, 10, self.NClusters, 0.85, 0.05, 15, path)

    def GetCentroids(self):
        sal = []
        for j in range(0, self.best.k):
            sal.append(self.best.centroides[j * self.best.dimension:(j + 1) * self.best.dimension])
        self.best.centroides = np.array(sal)
        return self.best.centroides

    def GetLabels(self):
        return self.best.cluster


# python Genetic.py n_individuals n_clusters p_crossover p_mutation iterations input_file
if __name__ == '__main__':
    print GeneticAlg(int(argv[1]),int(argv[2]),float(argv[3]),float(argv[4]),int(argv[5]),argv[6])