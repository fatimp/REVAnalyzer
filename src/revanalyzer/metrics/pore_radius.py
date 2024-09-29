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
    def __init__(self, vectorizer, exe_path, n_threads = 1, resolution = 1., length_unit_type = 'M', direction = 'z', show_time = False):
        """
        **Input:**
        
            vectorizer (HistVectorizer object): vectorizer to be used for a vector metric;
            
            exe_path (str): path to PNM extractor exe-file;
        
            n_threads (int): number of threads used for data generation, default: 1;
        
            resolution (float): resolution of studied sample, default: 1;
            
            length_unit_type (str): units of resolution. Can be 'NM', 'UM', 'MM' and 'M', default: 'M'.
            
            direction (str): 'x', 'y' or 'z', default: 'z';
            
            show_time (bool): Added to monitor time cost for large images,  default: False. 
        """
        super().__init__(vectorizer, exe_path = exe_path, n_threads = n_threads, resolution = resolution, length_unit_type = length_unit_type, direction = direction, show_time = show_time)
        self.metric_type = 'v'

    def generate(self, cut, cut_name, outputdir, gendatadir):
        """
        Generates pore radius distribution for a specific subsample.
        
        **Input:**
        
        	cut (numpy.ndarray): 3D array representing a subsample;
        	
        	cut_name (str): name of subsample;
        	
        	outputdir (str): output folder;
        	
        	gendatadir (str): folder with generated PNM data.  
        """
        pore_number = super().generate(cut, cut_name, gendatadir)
        if pore_number > 0:
            filein = os.path.join(gendatadir, cut_name) + "_" + self.direction + '_node2.dat'
            pore_radius = _read_pore_radius(filein)
        else:
            pore_radius = []
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        np.savetxt(fileout, pore_radius, delimiter='\t')

    def show(self, inputdir, step, cut_id, nbins):
        """
        Vizualize pore radius distribution for a specific subsample.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated metric data for subsamples;
        	 
        	step (int): subsamples selection step;
        	
        	cut_id (int: 0,..8): cut index;
        	
        	nbins (int): number of bins in histogram.  
        """        
        x, hist = super().show(inputdir, step, cut_id, nbins)
        fig, ax = plt.subplots(figsize=(10, 8))
        title = self.__class__.__name__ + ", "  + "cut size = " + str(step) + ", id = " + str(cut_id)
        ax.set_title(title)
        ax.bar(x, hist, width=0.5, color='r')
        ax.set_xlabel('pore radius')
        ax.set_ylabel('density')
        plt.show()

def _read_pore_radius(filein):
    with open(filein, mode='r') as f:
        node = pd.read_table(filepath_or_buffer=f,
                             header=None,
                             sep='\s+',
                             skipinitialspace=True,
                             index_col=0)
    node.columns = ['pore.volume', 'pore.radius', 'pore.shape_factor',
                    'pore.clay_volume']
    return np.array(node['pore.radius'])