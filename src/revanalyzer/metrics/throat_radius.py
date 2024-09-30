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
    def __init__(self, vectorizer, n_threads = 1, resolution = 1., show_time = False):
        """
        **Input:**
        
            vectorizer (HistVectorizer object): vectorizer to be used for a vector metric;
        
            n_threads (int): number of threads used for data generation, default: 1;
        
            resolution (float): resolution of studied sample, default: 1;
            
            show_time (bool): Added to monitor time cost for large images,  default: False. 
        """
        super().__init__(vectorizer, n_threads = n_threads, resolution = resolution, show_time = show_time)
        self.metric_type = 'v'

    def generate(self, cut, cut_name, outputdir, gendatadir):
        """
        Generates throat radius distribution for a specific subsample.
        
        **Input:**
        
        	cut (numpy.ndarray): 3D array representing a subsample;
        	
        	cut_name (str): name of subsample;
        	
        	outputdir (str): output folder;
        	
        	gendatadir (str): folder with generated PNM data.    
        """
        df = super().generate(cut_name, gendatadir)
        throat_radius = np.array(df['throat.inscribed_diameter'].dropna().tolist())/2
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        np.savetxt(fileout, throat_radius, delimiter='\t')

    def show(self, inputdir, step, cut_id, nbins):
        """
        Vizualize throat radius distribution for a specific subsample.
        
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