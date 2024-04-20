# -*- coding: utf-8 -*-
"""Main module of the library, ensures the complete pipeline for REV analysis.
"""
import numpy as np
import os
import json
import shutil
import matplotlib.pyplot as plt
import itertools
from .generators import make_cuts, run_fdmss
from .metrics import BasicMetric, BasicPNMMetric, BasicPDMetric, Permeability, ChordLength, PoreSize
from .REV_formulas import _delta, get_sREV_size, get_dREV_size_1_scalar, get_dREV_size_2_scalar, get_dREV_size_1_vector, get_dREV_size_1_scalar_dimensional, get_dREV_size_2_scalar_dimensional


class REVAnalyzer:
    """
    analysis of representativity of a given image for a given scalar or vector metric.
    """
    def __init__(self, metric, image, size, cut_step, sREV_max_size, datadir='data', outputdir='output'):
        """
        **Input:**

        	metric (subclass of BasicMetric): metric to be analyzed;
        
        	image (str): name of binary ('uint8') file representing the image;
        
        	size (int): image linear size. Note, that only cubical images can be analyzed;
         
        	cut_step (int): increment step of subcube size;
        
        	sREV_max_size (int): maximal subcube size for which sREV analysis is performed;
        
        	datadir (str): path to the folder containing image, default: 'data';
        
        	outputdir (str): path to the output folder containing generated data, default: 'output'.
        """
        if not issubclass(metric.__class__, BasicMetric):
            raise TypeError("Metric should be an object of a class derived from BasicMetric.")
        self.metric = metric
        self.image = image
        self.size = size
        self.cut_step = cut_step
        self.sREV_max_size = sREV_max_size
        self.datadir = datadir
        self.outputdir = outputdir
        self._outputdir_cut_values = os.path.join(
            self.outputdir, self.image, self.metric.__class__.__name__, 'cuts_values')
        self._outputdir_vectorized_cut_values = None
        os.makedirs(self.outputdir, exist_ok=True)
        os.makedirs(self._outputdir_cut_values, exist_ok=True)
        self.n_steps = int(np.ceil(size/cut_step))
        self.cut_sizes = [cut_step*(i+1) for i in range(self.n_steps-1)]
        self._metric_cut_names = []
        self.metric_mean = {}
        self.metric_std = {}
        self.metric_normed_std = {}
        self.metric_normed_std_1 = {}
        self.metric_normed_std_2 = {}
        self.dREV_threshold = None
        self.sREV_threshold = None
        self.sREV_size_1 = None
        self.sREV_size_2 = None
        self.dREV_size_1 = None
        self.dREV_size_2 = None
        self.is_fdmss_data = False
        if isinstance(self.metric, Permeability):
            fdmss_input=os.path.join(self.outputdir, self.image, 'fdmss_data', 'fdmss_input.txt')
            if os.path.isfile(fdmss_input):
                with open(fdmss_input) as f:
                    lines = [line.rstrip('\n') for line in f]
                    if lines[0] == self.metric.direction and lines[1] == str(self.metric.resolution):                        
                        self.is_fdmss_data = True
                    

    def generate(self):
        """
        Generator of metric values for all selected subcubes.
        """
        if isinstance(self.metric, Permeability) and not self.is_fdmss_data:
            fdmss_data=os.path.join(self.outputdir, self.image, 'fdmss_data')
            os.makedirs(fdmss_data, exist_ok=True)
            run_fdmss(self.image, self.metric.direction, self.datadir, fdmss_data, self.metric.n_threads, self.metric.resolution, self.metric.show_time)
            fdmss_input = os.path.join(fdmss_data, 'fdmss_input.txt')            
            with open(fdmss_input, 'w') as f:
                lines = [self.metric.direction, str(self.metric.resolution)]
                f.write('\n'.join(lines))
        if issubclass(self.metric.__class__, BasicPNMMetric):
            for l in self.cut_sizes:
                if (l <= self.sREV_max_size):
                    cut_names = [
                        'cut'+str(i)+'_'+str(l)+'_'+self.image for i in range(9)]
                    for cut_name in cut_names:
                        metric_cut_name = self.metric.generate(
                            self.metric.statoildir, cut_name, l, self._outputdir_cut_values)
                        self._metric_cut_names.append(metric_cut_name)
                else:
                    cut_name = 'cut'+str(0)+'_'+str(l)+'_'+self.image
                    metric_cut_name = self.metric.generate(
                        self.metric.statoildir, cut_name, l, self._outputdir_cut_values)
                    self._metric_cut_names.append(metric_cut_name)
                metric_cut_name = self.metric.generate(
                    self.metric.statoildir, self.image, self.size, self._outputdir_cut_values)
        else:
            for l in self.cut_sizes:
                cuts_data = 'cuts_data'
                os.makedirs(cuts_data, exist_ok=True)
                if (l <= self.sREV_max_size):
                    cut_names = make_cuts(self.datadir,
                                          self.image, cuts_data, self.size, l, total=True)
                    for cut_name in cut_names:
                        metric_cut_name = self.metric.generate(
                            cuts_data, cut_name, l, self._outputdir_cut_values)
                        self._metric_cut_names.append(metric_cut_name)
                    shutil.rmtree(cuts_data)
                else:
                    cut_name = make_cuts(self.datadir, self.image, cuts_data,
                                         self.size, l, total=False)
                    metric_cut_name = self.metric.generate(
                        cuts_data, cut_name, l, self._outputdir_cut_values)
                    self._metric_cut_names.append(metric_cut_name)
                    shutil.rmtree(cuts_data)
            metric_cut_name = self.metric.generate(
                self.datadir, self.image, self.size, self._outputdir_cut_values)
            self._metric_cut_names.append(metric_cut_name)

    def read(self, cut_size, cut_id=0): 
        """
        Read the generated metric value for a given subcube. analyzer.read(0) returns the metric value for the uncut image.
        
        **Input:**
        
        	cut_size (int): size of subcube;
        	
        	cut_id (int: 0,..8): cut index .   
        
        **Output**
        
        	metric value (float or np.array(dtype='float')).       
        """
        return self.metric.read(
            self._outputdir_cut_values, self.image, cut_size, cut_id)
    
    def show(self, cut_size, cut_id = 0, nbins = None):
        """
        Vizualize the vector metric for a specific subcube.
        
        **Input:**
         
        	cut_size (int): size of subcube;
        
        	cut_id (int: 0,..8): cut index;
        	
        	nbins (int): number of bins in histogram. For PNM-based metric only.
        """
        if not self.metric.metric_type == 'v':
            raise TypeError("Metric type should be vector")
        if issubclass(self.metric.__class__, BasicPNMMetric) or isinstance(self.metric, ChordLength) or isinstance(self.metric, PoreSize):
            if nbins is None:
                raise ValueError("Number of bins in histogram should be defined for the visualization of this metric")
            self.metric.show(self._outputdir_cut_values, self.image, cut_size, cut_id, nbins)
        else:
            self.metric.show(self._outputdir_cut_values, self.image, cut_size, cut_id)
        

    def vectorize(self):
        """
        Vectorization of generated metric data using vetorizer. For vector metric only.
        """
        if not self.metric.metric_type == 'v':
            raise TypeError("Metric type should be vector")
        cut_sizes = [x for x in self.cut_sizes]
        self._outputdir_vectorized_cut_values = os.path.join(
            self.outputdir, self.image, self.metric.__class__.__name__, 'vectorized_cuts_values')
        os.makedirs(self._outputdir_vectorized_cut_values, exist_ok=True)
        x = np.arange(9)
        y = [0]
        for i in range(len(self.cut_sizes)-1):
            d = {}
            if (self.cut_sizes[i] < self.sREV_max_size and self.cut_sizes[i+1] <= self.sREV_max_size):
                idx = itertools.product(x, repeat=2)
            else:
                if (self.cut_sizes[i] <= self.sREV_max_size and self.cut_sizes[i+1] > self.sREV_max_size):
                    idx = itertools.product(x, y)
                else:
                    idx = itertools.product(y, repeat=2)
            for elem in idx:
                v1 = self.read(self.cut_sizes[i], elem[0])
                if self.metric.directional:
                    v0 = v1[0]
                else:
                    v0 = v1
                if len(v0) == 0:
                    print("Metric is not defined at l = ",
                          self.cut_sizes[i], " for cut = ", elem[0])
                    cut_sizes.remove(self.cut_sizes[i])
                    break
                v2 = self.read(self.cut_sizes[i+1], elem[1])
                str_elem = str(elem[0]) + ', ' + str(elem[1])
                result = self.metric.vectorize(v1, v2)
                if (type(result[2]) is list and (np.nan in result[2])) or (type(result[2]) is not list and np.isnan(result[2])):
                    print("Metric is not defined at l = ",
                          self.cut_sizes[i], " for cut = ", elem[0])
                    cut_sizes.remove(self.cut_sizes[i])
                    break
                d[str_elem] = result

            jsonname = 'cut_' + str(self.cut_sizes[i])
            with open(os.path.join(self._outputdir_vectorized_cut_values, jsonname), 'w') as f:
                json.dump(d, f, indent=4)
        if (self.cut_sizes[-1] <= self.sREV_max_size):
            idx = itertools.product(x, y)
        else:
            idx = itertools.product(y, repeat=2)
        d = {}
        for elem in idx:
            v1 = self.read(self.cut_sizes[-1], elem[0])
            if self.metric.directional:
                v0 = v1[0]
            else:
                v0 = v1
            if len(v0) == 0:
                print("Metric is not defined at l = ",
                      self.cut_sizes[-1], " for cut = ", elem[0])
                cut_sizes.remove(self.cut_sizes[-1])
                break
            v2 = self.read(0)
            str_elem = str(elem[0]) + ', ' + str(elem[1])
            result = self.metric.vectorize(v1, v2)
            if (type(result[2]) is list and (np.nan in result[2])) or (type(result[2]) is not list and np.isnan(result[2])):
                print("Metric is not defined at l = ",
                      self.cut_sizes[i], " for cut = ", elem[0])
                cut_sizes.remove(self.cut_sizes[i])
                break
            d[str_elem] = result
        jsonname = 'cut_' + str(self.cut_sizes[-1])
        with open(os.path.join(self._outputdir_vectorized_cut_values, jsonname), 'w') as f:
            json.dump(d, f, indent=4)
        self.cut_sizes = cut_sizes

    def analyze(self, dREV_threshold, sREV_threshold):
        """
        Perform the analysis of representativity.
        
        **Input:**
        
        	dREV_threshold (float, <1): threshold to estimate dREV size;
        	
        	sREV_threshold (float, <1): threshold to estimate sREV size.
        """
        self.dREV_threshold = dREV_threshold
        self.sREV_threshold = sREV_threshold
        if self.metric.metric_type == 's':
            if self.metric.directional:
                self.metric_mean[self.size] = self.read(0)
            else:
                self.metric_mean[self.size] = self.read(0).item()
            for l in self.cut_sizes:
                if (l <= self.sREV_max_size):
                    data = [self.read(l, i) for i in range(9)]
                    if self.metric.directional:
                        self.metric_mean[l] = [
                            np.mean(list(i)) for i in zip(*data)]
                        self.metric_std[l] = [
                            np.std(list(i)) for i in zip(*data)]
                        self.metric_normed_std[l] = max(
                            [np.std(list(i))/abs(np.mean(list(i))) for i in zip(*data)])
                    else:
                        self.metric_mean[l] = np.mean(data)
                        self.metric_std[l] = np.std(data)
                        self.metric_normed_std[l] = self.metric_std[l] / \
                            abs(self.metric_mean[l])
                else:
                    if self.metric.directional:
                        self.metric_mean[l] = self.read(l, 0)
                    else:
                        self.metric_mean[l] = self.read(l, 0).item()
            self.sREV_size_1 = get_sREV_size(
                self.metric_normed_std, self.sREV_threshold)
            if self.metric.directional:
                self.dREV_size_1 = get_dREV_size_1_scalar_dimensional(
                    self.metric_mean, self.dREV_threshold)
                self.dREV_size_2 = get_dREV_size_2_scalar_dimensional(
                    self.metric_mean, self.dREV_threshold)
            else:
                self.dREV_size_1 = get_dREV_size_1_scalar(
                    self.metric_mean, self.dREV_threshold)
                self.dREV_size_2 = get_dREV_size_2_scalar(
                    self.metric_mean, self.dREV_threshold)
        if self.metric.metric_type == 'v':
            for l in self.cut_sizes:
                if l == self.cut_sizes[-1]:
                    l1 = self.size
                else:
                    l1 = l + self.cut_step
                jsonname = 'cut_' + str(l)
                with open(os.path.join(self._outputdir_vectorized_cut_values, jsonname), 'r') as f:
                    d = json.load(f)
                deltas = [elem[2] for elem in d.values()]
                n = deltas[0]
                if (type(n) is list):
                    self.metric_mean[l1] = max(
                        [np.mean(list(i)) for i in zip(*deltas)])
                else:
                    self.metric_mean[l1] = np.mean(deltas)
                if (l <= self.sREV_max_size):
                    if (type(n) is list):
                        self.metric_std[l1] = max(
                            [np.std(list(i)) for i in zip(*deltas)])
                        self.metric_normed_std[l1] = max(
                            [np.std(list(i))/np.mean(list(i)) for i in zip(*deltas)])
                    else:
                        self.metric_std[l1] = np.std(deltas)
                        self.metric_normed_std[l1] = self.metric_std[l1] / \
                            self.metric_mean[l1]
                    self.metric_normed_std_1[l1] = self.metric_std[l1] / \
                        self.dREV_threshold
                    if (self.dREV_threshold is None or self.metric_mean[l1] > self.dREV_threshold):
                        self.metric_normed_std_2[l1] = self.metric_normed_std[l1]
                    else:
                        self.metric_normed_std_2[l1] = self.metric_normed_std_1[l1]
            self.dREV_size_1 = get_dREV_size_1_vector(
                self.metric_mean, self.dREV_threshold)
            self.sREV_size_1 = get_sREV_size(
                self.metric_normed_std_1, self.sREV_threshold)
            self.sREV_size_2 = get_sREV_size(
                self.metric_normed_std_2, self.sREV_threshold)

    def show_results(self, figdir='figs'):
        """
        Visualization of REV analysis results.
        
        **Input:**
        
        	figdir (str): path to the folder for saving figures.
        """
        figdir = os.path.join(self.outputdir, self.image, figdir)
        os.makedirs(figdir, exist_ok=True)
        plt.rcParams.update({'font.size': 16})
        plt.rcParams['figure.dpi'] = 300
        x = list(self.metric_mean.keys())
        x.sort()
        xerr = list(self.metric_std.keys())
        xerr.sort()
        nzeros = len(x) - len(xerr)
        fig, ax = plt.subplots()
        title = self.metric.__class__.__name__ + ", " + self.image
        plt.title(title)
        if self.metric.metric_type == 's' and self.metric.directional:
            y = [self.metric_mean[l] for l in x]
            y1 = [i for i in zip(*y)]
            yerr = [self.metric_std[l] for l in xerr]
            for i in range(nzeros):
                yerr.append([0, 0, 0])
            yerr1 = [i for i in zip(*yerr)]
            x1 = np.array(x)-2
            x2 = np.array(x)+2
            plt.errorbar(x1, y1[0], yerr=yerr1[0], label='x')
            plt.errorbar(x, y1[1], yerr=yerr1[1], label='y')
            plt.errorbar(x2, y1[2], yerr=yerr1[2], label='z')
            plt.legend()
        else:
            y = [self.metric_mean[l] for l in x]
            yerr = [self.metric_std[l] for l in xerr]
            for i in range(nzeros):
                yerr.append(0)
            plt.errorbar(x, y, yerr=yerr)
        plt.xlabel("linear size of subcube, voxels")
        if self.metric.metric_type == 's':
            plt.ylabel(self.metric.__class__.__name__)
        if self.metric.metric_type == 'v':
            plt.ylabel("difference in distance")
            ax.axhline(y=self.dREV_threshold, color='k',
                       linestyle='-', label="dREV threshold")
            plt.legend()
        fig_name = "fig_REV_" + self.image + "_" + self.metric.__class__.__name__
        plt.savefig(os.path.join(figdir, fig_name), bbox_inches='tight')
        plt.show()

        fig, ax = plt.subplots()
        plt.title(title)
        xdrev = x[:-1]
        xsrev = list(self.metric_normed_std.keys())
        if self.metric.metric_type == 's':
            if self.metric.directional:
                y1 = np.array(y1)
                ydrev1 = [max([_delta(y1[k][i], y1[k][i+1])
                              for k in range(3)]) for i in range(len(xdrev))]
                ydrev2 = [max([_delta(y1[k][i], y1[k][-1])
                              for k in range(3)]) for i in range(len(xdrev))]
            else:
                ydrev1 = [_delta(self.metric_mean[x[i]], self.metric_mean[x[i+1]])
                          for i in range(len(xdrev))]
                y0 = self.metric_mean[x[-1]]
                ydrev2 = [_delta(self.metric_mean[x[i]], y0)
                          for i in range(len(xdrev))]
            ysrev = [self.metric_normed_std[l] for l in xsrev]
            ax.plot(xsrev, ysrev, "r--", label='sREV, $\sigma_{norm}$')
            ax.plot(xdrev, ydrev1, "b-", label='dREV, $\delta_1$')
            ax.plot(xdrev, ydrev2, "g-", label='dREV, $\delta_2$')
            ax.axhline(y=self.dREV_threshold, color='k',
                       linestyle='-', label="dREV threshold")
            plt.ylabel('$\sigma_{norm}$, $\delta_1$, $\delta_2$')
        if self.metric.metric_type == 'v':
            ysrev1 = [self.metric_normed_std_1[l] for l in xsrev]
            ysrev2 = [self.metric_normed_std_2[l] for l in xsrev]
            ax.plot(xsrev, ysrev1, "r-", label='sREV, $\sigma_{norm1}$')
            ax.plot(xsrev, ysrev2, "r--", label='sREV, $\sigma_{norm2}$')
            plt.ylabel("$\sigma_{norm1}$, $\sigma_{norm2}$")
        ax.axhline(y=self.sREV_threshold, color='k',
                   linestyle='--', label="sREV threshold")
        plt.xlabel("linear size of subcube, voxels")

        plt.legend()
        fig_name = "fig_threshold_" + self.image + "_" + self.metric.__class__.__name__
        plt.savefig(os.path.join(figdir, fig_name), bbox_inches='tight')
        plt.show()
