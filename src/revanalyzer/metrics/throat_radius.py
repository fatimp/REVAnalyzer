# -*- coding: utf-8 -*-
"""Definition of Throat Radius metric"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from .basic_metric import BasicMetric
from .basic_pnm_metric import BasicPNMMetric


class ThroatRadius(BasicPNMMetric):
    """
    Class describing throat radius metric.
    """ 
    def __init__(self, vectorizer, resolution = 1., show_time = False):
        """
        **Input:**
        	vectorizer (HistVectorizer object): vectorizer to be used for a vector metric.
            
            resolution (float): resolution of studied sample (micrometers), default: 1;
            
            show_time (bool): Added to monitor time cost for large images,  default: False. 
        """
        super().__init__(vectorizer, resolution = resolution, show_time = show_time)
        self.metric_type = 'v'

    def generate(self, cut, cut_name, outputdir, gendatadir):
        """
        Generates throat radius distribution for a specific subcube.
        
        **Input:**
        
        	cut (numpy.ndarray): subcube;
        	
        	cut_name (str): name of subcube;
        	
        	outputdir (str): output folder;
        	
        	gendatadir (str): folder with generated fdmss data output.    
        """
        df = super().generate(cut_name, gendatadir)
        throat_radius = np.array(df['throat.inscribed_diameter'].dropna().tolist())/2
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        np.savetxt(fileout, throat_radius, delimiter='\t')

    def show(self, inputdir, cut_size, cut_id, nbins):
        """
        Vizualize throat radius distribution for a specific subcube.
        
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
        ax.set_xlabel('throat radius')
        ax.set_ylabel('density')
        plt.show()
