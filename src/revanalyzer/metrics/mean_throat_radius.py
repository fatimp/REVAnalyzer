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
    def __init__(self, resolution = 1., show_time = False):
        """
        **Input:**          
            resolution (float): resolution of studied sample (micrometers), default: 1;
            
            show_time (bool): Added to monitor time cost for large images,  default: False. 
        """
        super().__init__(vectorizer=None, resolution = resolution, show_time = show_time)
        self.metric_type = 's'

    def generate(self, cut, cut_name, outputdir, gendatadir):
        """
        Generates throat radius for a specific subcube.
        
        **Input:**
        
        	cut (numpy.ndarray): subcube;
        	
        	cut_name (str): name of subcube;
        	
        	outputdir (str): output folder;
        	
        	gendatadir (str): folder with generated fdmss data output.    
        """
        df = super().generate(cut_name, gendatadir)
        L = cut.shape[0]
        mean_throat_radius = np.mean(df['throat.inscribed_diameter'].dropna().tolist())/2
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(mean_throat_radius))
