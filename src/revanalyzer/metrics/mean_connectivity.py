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
        Generates mean connectivity for a specific subsample.
        
        **Input:**
        
            cut (numpy.ndarray): 3D array representing a subsample;
        
            cut_name (str): name of subsample;
            
            outputdir (str): output folder;
        	
        	gendatadir (str): folder with generated PNM data.    
        """
        df = super().generate(cut_name, gendatadir)
        pore_number = df.shape[0] - df['pore.phase'].isna().sum()
        con1 = df['throat.conns[0]'].dropna().tolist()
        con2 = df['throat.conns[1]'].dropna().tolist()
        con = con1 +con2
        (unique, counts) = np.unique(con, return_counts=True)
        counts0 = [0 for i in range(pore_number) if i not in unique]
        counts = counts.tolist() + counts0
        mean_con = np.mean(counts)

        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(mean_con))

