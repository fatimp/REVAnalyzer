# -*- coding: utf-8 -*-
"""Definition of Mean Throat Radius metric"""

import numpy as np
import pandas as pd
import os
from .basic_metric import BasicMetric
from .basic_pnm_metric import BasicPNMMetric


class MeanThroatRadius(BasicPNMMetric):
    """
    Class describing mean throat radius metric.
    """     
    def __init__(self, exe_path, n_threads = 1, resolution = 1., length_unit_type = 'M', direction = 'z', show_time = False):
        """
        **Input:**
            
            exe_path (str): path to PNM extractor exe-file;
        
            n_threads (int): number of threads used for data generation, default: 1;
        
            resolution (float): resolution of studied sample, default: 1;
            
            length_unit_type (str): units of resolution. Can be 'NM', 'UM', 'MM' and 'M', default: 'M'.
            
            direction (str): 'x', 'y' or 'z', default: 'z';
            
            show_time (bool): Added to monitor time cost for large images,  default: False. 
        """
        super().__init__(vectorizer=None, exe_path = exe_path, n_threads = n_threads, resolution = resolution, length_unit_type = length_unit_type, direction = direction, show_time = show_time)
        self.metric_type = 's'

    def generate(self, cut, cut_name, outputdir, gendatadir):
        """
        Generates throat radius for a specific subsample.
        
        **Input:**
        
            cut (numpy.ndarray): 3D array representing a subsample;
        
            cut_name (str): name of subsample;
            
            outputdir (str): output folder;
        	
        	gendatadir (str): folder with generated PNM data.    
        """
        pore_number = super().generate(cut, cut_name, gendatadir)
        if pore_number > 0:
            filein = os.path.join(gendatadir, cut_name) + "_" + self.direction + '_link1.dat'
            mean_throat_radius = _read_mean_throat_radius(filein)
        else:
            mean_throat_radius = 0
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(mean_throat_radius))

def _read_mean_throat_radius(filein):
    with open(filein, mode='r') as f:
        link = pd.read_table(filepath_or_buffer=f,
                             header=None,
                             skiprows=1,
                             sep='\s+',
                             skipinitialspace=True,
                             index_col=0)
    link.columns = ['throat.pore1', 'throat.pore2', 'throat.radius',
                    'throat.shape_factor', 'throat.total_length']
    return np.mean(link['throat.radius'])