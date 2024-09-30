# -*- coding: utf-8 -*-
"""Definition of Pore Number metric"""

import numpy as np
import os
from .basic_metric import BasicMetric
from .basic_pnm_metric import BasicPNMMetric


class PoreNumber(BasicPNMMetric):
    """
    Class describing pore number metric.
    """ 
    def __init__(self, n_threads = 1, resolution = 1., show_time = False):
        """
        **Input:**
        
            n_threads (int): number of threads used for data generation, default: 1;
        
            resolution (float): resolution of studied sample, default: 1;
            
            show_time (bool): Added to monitor time cost for large images,  default: False.             
        """
        super().__init__(vectorizer=None, n_threads = n_threads, resolution = resolution, show_time = show_time)
        self.metric_type = 's'

    def generate(self, cut, cut_name, outputdir, gendatadir):
        """
        Generates pore number for a specific subsample.
        
        **Input:**
        
            cut (numpy.ndarray): 3D array representing a subsample;
        
            cut_name (str): name of subsample;
            
            outputdir (str): output folder;
        	
        	gendatadir (str): folder with generated PNM data.  
        """    
        df = super().generate(cut_name, gendatadir)
        dimx = cut.shape[0]
        dimy = cut.shape[1]
        dimz = cut.shape[2]
        volume = dimx*dimy*dimz
        pore_number = (df.shape[0] - df['pore.phase'].isna().sum())/volume
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(pore_number))
