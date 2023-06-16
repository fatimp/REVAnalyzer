# -*- coding: utf-8 -*-
"""Definition of basic PNM metric"""

import numpy as np
import matplotlib.pyplot as plt
import os
from .basic_metric import BasicMetric
from revanalyzer.vectorizers import PNMVectorizer

units = {'M': 1, 'MM': 1e-3, 'UM': 1e-6, 'NN': 1e-9}


class BasicPNMMetric(BasicMetric):
    """
    Base class of PNM-based metrics. (Don't use it directly but derive from it).
    """  
    def __init__(self, statoildir, resolution, length_unit_type, direction, vectorizer):
        """
        **Input:**
        
        	statoildir (str): path to the folder containing generated data for subcubes in statoil format;
        	
        	resolution (float): resolution of studied sample (unitless);
        	
        	length_unit_type (str): units of resolution. Can be 'NM', 'UM', 'MM' and 'M';
        	
        	direction (str): flow direction, could be 'x', 'y' or 'z';
        	 
        	vectorizer (PNMVectorizer object): vectorizer to be used for a vector metric.
        """
        assert (isinstance(
            vectorizer, PNMVectorizer) or (vectorizer is None)), "Vectorizer should be None or an object of PNMVectorizer class"
        super().__init__(vectorizer)
        self.statoildir = statoildir
        self.resolution = resolution
        self.length_unit_type = length_unit_type
        self.resolution_value = resolution * units[length_unit_type]
        self.direction = direction

    def generate(self, statoildir, cut_name, l):
        """
        Generator of a metric value for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated data for subcubes in statoil format;
        	
        	cut_name (str): name of subcube;
        	
        	l (int): linear size of subcube.
        
        **Output:**
        
        	pore number (float). Used for all PNM-based metrics exception handling. 
        """
        filein = os.path.join(statoildir, cut_name) + "_" + \
            self.direction + '_node1.dat'
        with open(filein, "r") as f:
            str_0 = f.readline().split()
            pore_number = (int(str_0[0])-1)/l**3
        return pore_number

    def show(self, inputdir, name, cut_size, cut_id, nbins):
        """
        Vizualize the vector metric for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated metric data for subcubes;
        	
        	name (str): name of binary ('uint8') file representing the image;
        	
        	cut_size (int): size of subcube;
        	
        	cut_id (int: 0,..8): cut index;
        	
        	nbins (int): number of bins in histogram. 
        
        **Output:**
        
        	(list(dtype = int), list(dtype = float)) : 'x' and 'y' coordinate values for a plot.
        """
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
        """
        Vectorize the vector metric values for a given pair of subcubes. Makes normalization to voxels and calls the
        vectorizer function.
        
        **Input:**
        
        	v1 (list(dtype = float)): data for the first cubcube;
        	
        	v2 (list(dtype = float)): data for the second cubcube.
        
        **Output:**
        
        	(list(dtype = float), list(dtype = float), float) - a tuple, in which the first two elements are vectorized metric values for a given pair of subcubes, and the last one is the normalized distance between these vectors. 
        """
        assert self.metric_type == 'v', "Metric type should be vector"
        coef_to_voxels = self.resolution * units[self.length_unit_type]
        v1 = v1/coef_to_voxels
        v2 = v2/coef_to_voxels
        res = self.vectorizer.vectorize(v1, v2)
        return res
