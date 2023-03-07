
from .basic_metric import BasicMetric
from revanalyzer.vectorizers  import CFVectorizer
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import imp
from julia import Main
from julia.api import Julia
jl = Julia(compiled_modules=False)


class BasicCFMetric(BasicMetric):
    def __init__(self, vectorizer, show_time, normalize):
        assert isinstance(
            vectorizer, CFVectorizer), "Vectorizer should be an object of CFVectorizer class"
        super().__init__(vectorizer)
        self.directional = True
        self.show_time = show_time
        if normalize == True:
            self.normalize = str(1)
        else:
            self.normalize = str(0)

    def generate(self, inputdir, cut_name, l, outputdir, method):
        start_time = time.time()
        if inputdir is not None:
            filein = os.path.join(inputdir, cut_name)
        else:
            filein = cut_name
        path0 = imp.find_module('revanalyzer')[1]
        pathjl = os.path.join(path0, 'jl', 'corfunction_xyz.jl')
        pathjl = 'include("'+pathjl+'")'
        jl.eval(pathjl)
        Main.data = [filein, method, str(l), self.normalize]
        cf = jl.eval("vectorize(data)")
        cf0 = np.concatenate(cf)
        for elem in cf0:
            if np.isnan(elem) or np.isinf(elem):
                cf = np.array(([], [], []))
                break
        directions = ('_x', '_y', '_z')
        for i, direction in enumerate(directions):
            cut_name_out = cut_name + direction + ".txt"
            fileout = os.path.join(outputdir, cut_name_out)
            np.savetxt(fileout, cf[i])
        if self.show_time:
            print("cut ", cut_name, ", run time: ")
            print("--- %s seconds ---" % (time.time() - start_time))
        return cut_name + ".txt"

    def show(self, inputdir, name, cut_size, cut_id):
        data = self.read(inputdir, name, cut_size, cut_id)
        x = np.arange(len(data[0]))
        plt.rcParams.update({'font.size': 16})
        plt.rcParams['figure.dpi'] = 300
        return x, data[0], data[1], data[2]

    def vectorize(self, v1, v2):
        return self.vectorizer.vectorize(v1, v2)


class C2(BasicCFMetric):
    def __init__(self,  vectorizer, show_time=False, normalize=True):
        super().__init__(vectorizer, show_time, normalize)
        self.metric_type = 'v'

    def generate(self, inputdir, cut_name, l, outputdir):
        return super().generate(inputdir, cut_name, l, outputdir, method='c2')

    def show(self, inputdir, name, cut_size, cut_id):
        x, vx, vy, vz = super().show(inputdir, name, cut_size, cut_id)
        fig, ax = plt.subplots(figsize=(10, 8))
        title = self.__class__.__name__ + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        ax.set_title(title)
        ax.plot(x, vx, "r-", label='x')
        ax.plot(x, vy, "b-", label='y')
        ax.plot(x, vz, "g-", label='z')
        ax.legend()
        ax.set_xlabel("voxels")
        ax.set_ylabel("CF value")
        plt.show()


class L2(BasicCFMetric):
    def __init__(self,  vectorizer, show_time=False, normalize=True):
        super().__init__(vectorizer, show_time, normalize)
        self.metric_type = 'v'

    def generate(self, inputdir, cut_name, l, outputdir):
        return super().generate(inputdir, cut_name, l, outputdir, method='l2')

    def show(self, inputdir, name, cut_size, cut_id):
        x, vx, vy, vz = super().show(inputdir, name, cut_size, cut_id)
        fig, ax = plt.subplots(figsize=(10, 8))
        title = self.__class__.__name__ + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        ax.set_title(title)
        ax.plot(x, vx, "r-", label='x')
        ax.plot(x, vy, "b-", label='y')
        ax.plot(x, vz, "g-", label='z')
        ax.legend()
        ax.set_xlabel("voxels")
        ax.set_ylabel("CF value")
        plt.show()


class S2(BasicCFMetric):
    def __init__(self,  vectorizer, show_time=False, normalize=True):
        super().__init__(vectorizer, show_time, normalize)
        self.metric_type = 'v'

    def generate(self, inputdir, cut_name, l, outputdir):
        return super().generate(inputdir, cut_name, l, outputdir, method='s2')

    def show(self, inputdir, name, cut_size, cut_id):
        x, vx, vy, vz = super().show(inputdir, name, cut_size, cut_id)
        fig, ax = plt.subplots(figsize=(10, 8))
        title = self.__class__.__name__ + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        ax.set_title(title)
        ax.plot(x, vx, "r-", label='x')
        ax.plot(x, vy, "b-", label='y')
        ax.plot(x, vz, "g-", label='z')
        ax.legend()
        ax.set_xlabel("voxels")
        ax.set_ylabel("CF value")
        plt.show()


class SS2(BasicCFMetric):
    def __init__(self,  vectorizer, show_time=False, normalize=True):
        super().__init__(vectorizer, show_time, normalize)
        self.metric_type = 'v'

    def generate(self, inputdir, cut_name, l, outputdir):
        return super().generate(inputdir, cut_name, l, outputdir, method='ss')

    def show(self, inputdir, name, cut_size, cut_id):
        x, vx, vy, vz = super().show(inputdir, name, cut_size, cut_id)
        fig, ax = plt.subplots(figsize=(10, 8))
        title = self.__class__.__name__ + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        ax.set_title(title)
        ax.plot(x, vx, "r-", label='x')
        ax.plot(x, vy, "b-", label='y')
        ax.plot(x, vz, "g-", label='z')
        ax.legend()
        ax.set_xlabel("voxels")
        ax.set_ylabel("CF value")
        plt.show()
