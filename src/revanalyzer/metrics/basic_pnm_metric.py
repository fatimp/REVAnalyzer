# -*- coding: utf-8 -*-
"""Definition of basic PNM metric"""

import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from .basic_metric import BasicMetric
from revanalyzer.vectorizers import HistVectorizer


class BasicPNMMetric(BasicMetric):
    """
    Base class of PNM-based metrics. (Don't use it directly but derive from it).
    """  
    def __init__(self, vectorizer, exe_path, n_threads, resolution, length_unit_type, direction, show_time):
        """
        **Input:**
        	vectorizer (PNMVectorizer object): vectorizer to be used for a vector metric.
            
            n_threads (int): number of CPU cores used for data generation, default: 1;
                    
            resolution (float): resolution of studied sample (micrometers), default: 1;
            
            show_time (bool): Added to monitor time cost for large images,  default: False. 
        """
        if not (isinstance(vectorizer, HistVectorizer) or (vectorizer is None)):
            raise TypeError("Vectorizer should be None or an object of HistVectorizer class.")
        super().__init__(vectorizer, n_threads = n_threads)
        self.resolution = resolution
        self.length_unit_type = length_unit_type
        self.direction = direction
        self.show_time = show_time
        self.exe_path = exe_path

    def generate(self, cut, cut_name, gendatadir):
        """
        Generates PNM metric for a specific subcube.
        
        **Input:**
            cut_name (str): name of subcube;
        	
        	outputdir (str): output folder;
        	
        	gendatadir (str): folder with generated fdmss data output.    
        """
        dimx = cut.shape[0]
        dimy = cut.shape[1]
        dimz = cut.shape[2]
        volume = dimx*dimy*dimz
        filein = os.path.join(gendatadir, cut_name) + "_" + self.direction + '_node1.dat'
        with open(filein, "r") as f:
            str_0 = f.readline().split()
            pore_number = (int(str_0[0])-1)/volume
        return pore_number 
        
        
    def show(self, inputdir, step, cut_id, nbins):
        """
        Vizualize the vector metric for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated metric data for subcubes;
        	
        	cut_size (int): size of subcube;
        	
        	cut_id (int: 0,..8): cut index;
        	
        	nbins (int): number of bins in histogram. 
        
        **Output:**
        
        	(list(dtype = int), list(dtype = float)) : 'x' and 'y' coordinate values for a plot.
        """
        data = self.read(inputdir, step, cut_id)
        data = data/self.resolution 
        max_value = max(data)
        range_data = [0, max_value]
        hist, bin_edges = np.histogram(
            data, bins=nbins, range=range_data, density=True)
        step1 = max_value/nbins
        x = [i*step1 for i in range(nbins)]
        plt.rcParams.update({'font.size': 16})
        plt.rcParams['figure.dpi'] = 300
        return x, hist

    def vectorize(self, v1, v2):
        """
        Vectorize the vector metric values for a given pair of subcubes. Makes normalization to voxels and calls the
        vectorizer function.
        
        **Input:**
        
        	v1 (list(dtype = float)): data for the first cubcube;
        	
        	v2 (list(dtype = float)): data for the second cubcube.
        
        **Output:**
        
        	(list(dtype = float), list(dtype = float), float) - a tuple, in which the first two elements are vectorized metric values for a given pair of subcubes, and the last one is the normalized distance between these vectors. 
        """
        if not self.metric_type == 'v':
            raise TypeError("Metric type should be vector")
        v1 = v1/self.resolution
        v2 = v2/self.resolution
        res = self.vectorizer.vectorize(v1, v2)
        return res
