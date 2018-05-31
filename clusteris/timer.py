# -*- coding: utf-8 -*-

from timeit import default_timer as timer

class Timer(object):

    def __init__(self):
        self.times = []
        self.start = 0
        self.end = 0

    def AddTime(self, description):
        t = timer()
        self.times.append((description, t))

        if (description.lower() == "start"):
            self.start = t

        if (description.lower() == "end"):
            self.end = t

    def PrintTimes(self):
        for t in range(len(self.times) - 1):
            time = self.times[t+1][1] - self.times[t][1]
            print("Time for %s: %s" % (self.times[t+1][0], time))

        print("Total time: %s" % (self.end - self.start))
