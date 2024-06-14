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

    def generate(self, cut, cut_name, outputdir, gendatadir = None):
        """
        Generates porosity for a specific subcube.
        
        **Input:**
        
        	cut (numpy.ndarray): subcube;
        	
        	cut_name (str): name of subcube;
        	
        	outputdir (str): output folder.
        """
        dim = cut.shape[0]
        porosity = 1 - np.count_nonzero(cut)/(dim**3)
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(porosity))
