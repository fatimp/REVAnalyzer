# -*- coding: utf-8 -*-
"""Definition of Mean Connectivity metric"""

import numpy as np
import pandas as pd
import os
from .basic_metric import BasicMetric
from .basic_pnm_metric import BasicPNMMetric


class MeanConnectivity(BasicPNMMetric):
    """
    Class describing mean connectivity metric.
    """     
    def __init__(self, exe_path, n_threads = 1, resolution = 1., length_unit_type = 'M', direction = 'z', show_time = False):
        """
        **Input:**
            n_threads (int): number of CPU cores used for data generation, default: 1;
        
            resolution (float): resolution of studied sample (micrometers), default: 1;
            
            show_time (bool): Added to monitor time cost for large images,  default: False. 
        """
        super().__init__(vectorizer=None, exe_path = exe_path, n_threads = n_threads, resolution = resolution, length_unit_type = length_unit_type, direction = direction, show_time = show_time)
        self.metric_type = 's'

    def generate(self, cut, cut_name, outputdir, gendatadir):
        """
        Generates mean connectivity for a specific subcube.
        
        **Input:**
        
        	cut (numpy.ndarray): subcube;
        	
        	cut_name (str): name of subcube;
        	
        	outputdir (str): output folder;
        	
        	gendatadir (str): folder with generated fdmss data output.    
        """
        pore_number = super().generate(cut, cut_name, gendatadir)
        if pore_number > 0:
            filein = os.path.join(gendatadir, cut_name) + "_" + self.direction + '_link2.dat'
            mean_con = _read_mean_connectivity(filein)
        else:
            mean_con = 0
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(mean_con))

def _read_mean_connectivity(filein):
    with open(filein, mode='r') as f:
        link = pd.read_table(filepath_or_buffer=f,
                             header=None,
                             sep='\s+',
                             skipinitialspace=True,
                             index_col=0)
    link.columns = ['throat.pore1', 'throat.pore2',
                    'throat.pore1_length', 'throat.pore2_length',
                    'throat.length', 'throat.volume',
                    'throat.clay_volume']
    con = np.vstack((link['throat.pore1']-1,
                     link['throat.pore2']-1)).T
    con1 = con.reshape(-1)
    (unique, counts) = np.unique(con1, return_counts=True)
    return np.mean(counts)