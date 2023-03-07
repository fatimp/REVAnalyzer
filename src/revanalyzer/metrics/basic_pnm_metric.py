import numpy as np
import matplotlib.pyplot as plt
import os
from .basic_metric import BasicMetric
from revanalyzer.vectorizers import PNMVectorizer

units = {'M': 1, 'MM': 1e-3, 'UM': 1e-6, 'NN': 1e-9}


class BasicPNMMetric(BasicMetric):
    def __init__(self, statoildir, resolution, length_unit_type, direction, vectorizer):
        assert (isinstance(
            vectorizer, PNMVectorizer) or (vectorizer is None)), "Vectorizer should be None or an object of PNMVectorizer class"
        super().__init__(vectorizer)
        self.statoildir = statoildir
        self.resolution = resolution
        self.length_unit_type = length_unit_type
        self.resolution_value = resolution * units[length_unit_type]
        self.direction = direction

    def generate(self, inputdir, cut_name, l):
        filein = os.path.join(inputdir, cut_name) + "_" + \
            self.direction + '_node1.dat'
        with open(filein, "r") as f:
            str_0 = f.readline().split()
            pore_number = (int(str_0[0])-1)/l**3
        return pore_number

    def show(self, inputdir, name, cut_size, cut_id, nbins):
        data = self.read(inputdir, name, cut_size, cut_id)
        max_value = max(data)
        range_data = [0, max_value]
        hist, bin_edges = np.histogram(
            data, bins=nbins, range=range_data, density=True)
        step = max_value/nbins
        x = [i*step for i in range(nbins)]
        plt.rcParams.update({'font.size': 16})
        plt.rcParams['figure.dpi'] = 300
        return x, hist

    def vectorize(self, v1, v2):
        assert self.metric_type == 'v', "Metric type should be vector"
        coef_to_voxels = self.resolution * units[self.length_unit_type]
        v1 = v1/coef_to_voxels
        v2 = v2/coef_to_voxels
        res = self.vectorizer.vectorize(v1, v2)
        return res
