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

    def generate(self, inputdir, cut_name, l, outputdir):
        """
        Generates Euler density for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing subcubes;
        	
        	cut_name (str): name of subcube;
        	
        	l (int): linear size of subcube.
        
        **Output:**
        
        	name of file (str), in which Euler density is written.
        """         
        start_time = time.time()
        if inputdir is not None:
            filein = os.path.join(inputdir, cut_name)
        else:
            filein = cut_name
        path0 = imp.find_module('revanalyzer')[1]
        pathjl = os.path.join(path0, 'jl', 'euler_density.jl')
        pathjl = 'include("'+pathjl+'")'
        jl.eval(pathjl)
        Main.data = [filein, str(l)]
        euler_d = jl.eval("euler_density(data)")
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(euler_d))
        if self.show_time:
            print("cut ", cut_name, ", run time: ")
            print("--- %s seconds ---" % (time.time() - start_time))
        return cut_name_out
