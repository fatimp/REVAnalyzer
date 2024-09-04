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
    def __init__(self, vectorizer, exe_path, n_threads = 1, resolution = 1., length_unit_type = 'M', direction = 'z', show_time = False):
        """
        **Input:**
            n_threads (int): number of CPU cores used for data generation, default: 1;
        
            resolution (float): resolution of studied sample (micrometers), default: 1;
            
            show_time (bool): Added to monitor time cost for large images,  default: False. 
        """
        super().__init__(vectorizer, exe_path = exe_path, n_threads = n_threads, resolution = resolution, length_unit_type = length_unit_type, direction = direction, show_time = show_time)
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
        pore_number = super().generate(cut, cut_name, gendatadir)
        if pore_number > 0:
            filein = os.path.join(gendatadir, cut_name) + "_" + self.direction + '_link1.dat'
            throat_radius = _read_throat_radius(filein)
        else:
            throat_radius = []
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

def _read_throat_radius(filein):
    with open(filein, mode='r') as f:
        link = pd.read_table(filepath_or_buffer=f,
                             header=None,
                             skiprows=1,
                             sep='\s+',
                             skipinitialspace=True,
                             index_col=0)
    link.columns = ['throat.pore1', 'throat.pore2', 'throat.radius',
                    'throat.shape_factor', 'throat.total_length']
    return np.array(link['throat.radius'])