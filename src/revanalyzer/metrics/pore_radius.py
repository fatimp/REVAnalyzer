# -*- coding: utf-8 -*-
"""Definition of Pore Radius metric"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from .basic_metric import BasicMetric
from .basic_pnm_metric import BasicPNMMetric


class PoreRadius(BasicPNMMetric):
    """
    Class describing pore radius metric.
    """ 
    def __init__(self, vectorizer, n_threads = 1, resolution = 1., show_time = False):
        """
        **Input:**
            n_threads (int): number of CPU cores used for data generation, default: 1;
        
            resolution (float): resolution of studied sample (micrometers), default: 1;
            
            show_time (bool): Added to monitor time cost for large images,  default: False. 
        """
        super().__init__(vectorizer, n_threads = n_threads, resolution = resolution, show_time = show_time)
        self.metric_type = 'v'

    def generate(self, cut, cut_name, outputdir, gendatadir):
        """
        Generates pore radius distribution for a specific subcube.
        
        **Input:**
        
        	cut (numpy.ndarray): subcube;
        	
        	cut_name (str): name of subcube;
        	
        	outputdir (str): output folder;
        	
        	gendatadir (str): folder with generated fdmss data output.    
        """
        df = super().generate(cut_name, gendatadir)
        pore_radius = np.array(df['pore.inscribed_diameter'].dropna().tolist())/2
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        np.savetxt(fileout, pore_radius, delimiter='\t')

    def show(self, inputdir, cut_size, cut_id, nbins):
        """
        Vizualize pore radius distribution for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated metric data for subcubes;
        	 
        	cut_size (int): size of subcube;
        	
        	cut_id (int: 0,..8): cut index;
        	
        	nbins (int): number of bins in histogram. 
        """        
        x, hist = super().show(inputdir, cut_size, cut_id, nbins)
        fig, ax = plt.subplots(figsize=(10, 8))
        title = self.__class__.__name__ + ", "  + "cut size = " + str(cut_size) + ", id = " + str(cut_id)
        ax.set_title(title)
        ax.bar(x, hist, width=0.5, color='r')
        ax.set_xlabel('pore radius')
        ax.set_ylabel('density')
        plt.show()
