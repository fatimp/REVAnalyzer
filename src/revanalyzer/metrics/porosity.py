# -*- coding: utf-8 -*-
"""Definition of Porosity metric."""

import numpy as np
import os
from .basic_metric import BasicMetric


class Porosity(BasicMetric):
    """
    Class describing porosity metric.
    """
    def __init__(self):
        super().__init__(vectorizer=None)
        self.metric_type = 's'

    def generate(self, inputdir, cut_name, l, outputdir):
        """
        Generates porosity for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing subcubes;
        	
        	cut_name (str): name of subcube;
        	
        	l (int): linear size of subcube.
        
        **Output:**
        
        	name of file (str), in which porosity is written.
        """  
        filein = os.path.join(inputdir, cut_name)
        v = np.fromfile(filein, dtype='uint8', sep="")
        n_zeros = v.size - np.count_nonzero(v)
        porosity = float(n_zeros)/(l**3)
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(porosity))
        return cut_name_out
