# -*- coding: utf-8 -*-

class Params():
    """Default parameters for UI."""

    CENTROID_MIN_VALUE = 2
    CENTROID_MAX_VALUE = 10
    CENTROID_DEFAULT_VALUE = 2
    CENTROID_FIXED_DEFAULT_VALUE = True
    CENTROID_RANGE_MIN_VALUE = 2
    CENTROID_RANGE_MAX_VALUE = 10

    POPULATION_MIN_VALUE = 5
    POPULATION_MAX_VALUE = 50
    POPULATION_DEFAULT_VALUE = 10

    ITERATION_MIN_VALUE = 10
    ITERATION_MAX_VALUE = 40
    ITERATION_DEFAULT_VALUE = 20

    DATASET_PARSE_FEATURES_DEFAULT_VALUE = False

    CLUSTERING_ALGORITHMS = [u"Elegir", u"K-means", u"Algoritmo Genético"]
    CLUSTERING_PROCESSORS = ['Dummy', 'KMeans', 'Genetic']

    CLUSTERING_ALGORITHM_DEFAULT = 0

class Processing():
    """
    Processing model contiene los parametros mediante los cuales se va a
    ejecutar toda la corrida del proceso de clustering.
    """

    def __init__(self):
        self.clusteringAlgorithm = None
        self.dataset = None
        self.datasetPath = None
        self.datasetRows = None
        self.datasetCols = None
        self.datasetColsNames = None
        self.selectedAxes = None
        self.colsForAxes = None
        self.clusters = None
        self.clustersFixed = None
        self.clusters_range_min = None
        self.clusters_range_max = None


        self.parseAttributes = None

        self.maxPopulation = None
        self.maxIterations = None
        self.selectionRatio = None
        self.crossRatio = None
        self.mutationRatio = None

class Results():

    def __init__(self):
        self.centroids = None
        self.labels = None
