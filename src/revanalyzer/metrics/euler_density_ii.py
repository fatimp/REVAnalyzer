# -*- coding: utf-8 -*-
"""
Definition of Euler Density II metric. The Euler density here is extracted from PNM characteristics, it is computed as the difference between pore and throat numbers, normalized over subcube volume.
"""

import numpy as np
import os
from .basic_metric import BasicMetric
from .basic_pnm_metric import BasicPNMMetric


class EulerDensityII(BasicPNMMetric):
    """
    Class describing Euler density II metric.
    """     
    def __init__(self, n_threads = 1, resolution = 1., show_time = False):
        """
        **Input:**
            n_threads (int): number of CPU cores used for data generation, default: 1;
        
            resolution (float): resolution of studied sample (micrometers), default: 1;
            
            show_time (bool): Added to monitor time cost for large images,  default: False. 
        """
        super().__init__(vectorizer=None, n_threads = n_threads, resolution = resolution, show_time = show_time)
        self.metric_type = 's'

    def generate(self, cut, cut_name, outputdir, gendatadir):
        """
        Generates throat number for a specific subcube.
        
        **Input:**
        
        	cut (numpy.ndarray): subcube;
        	
        	cut_name (str): name of subcube;
        	
        	outputdir (str): output folder;
        	
        	gendatadir (str): folder with generated fdmss data output.    
        """
        df = super().generate(cut_name, gendatadir)
        L = cut.shape[0]
        euler_number = (df['throat.phases[0]'].isna().sum()-df['pore.phase'].isna().sum())/L**3
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(euler_number))
