# -*- coding: utf-8 -*-
"""
Definition of Euler Density I metric. The Euler density here is calculated using the topological properties of considered voxel domain as in Vogel, H. J., Weller, U., & Schlüter, S. (2010). Quantification of soil structure based on Minkowski functions. Computers & Geosciences, 36(10), 1236-1245. See the details in documentation.
"""

from .basic_metric import BasicMetric
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import imp
from julia import Main
from julia.api import Julia
jl = Julia(compiled_modules=False)


class EulerDensityI(BasicMetric):
    """
    Class describing Euler density I metric.
    """     
    def __init__(self, show_time=False):
        """
        **Input:**
        
        	show_time (bool): flag to monitor time cost for large images, default: False.
        """
        super().__init__(vectorizer=None)
        self.metric_type = 's'
        self.show_time = show_time

    def generate(self, cut, cut_name, outputdir, gendatadir = None):
        """
        Generates Euler density for a specific subcube.
        
        **Input:**
        
        	cut (numpy.ndarray): subcube;
        	
        	cut_name (str): name of subcube;
        	
        	outputdir (str): output folder.
        """        
        start_time = time.time()
        path0 = imp.find_module('revanalyzer')[1]
        pathjl = os.path.join(path0, 'jl', 'euler_density.jl')
        pathjl = 'include("'+pathjl+'")'
        jl.eval(pathjl)
        length = cut.shape[0]
        v = cut.reshape(cut.size,)
        addr = v.ctypes.data
        euler_d = Main.euler_density(addr, length)
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(euler_d))
        if self.show_time:
            print("cut ", cut_name, ", run time: ")
            print("--- %s seconds ---" % (time.time() - start_time))
