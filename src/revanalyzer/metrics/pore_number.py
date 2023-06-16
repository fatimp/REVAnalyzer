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
    def __init__(self,  statoildir, resolution=1., length_unit_type='M', direction='z'):
        """
        **Input:**
        
        	statoildir (str): path to the folder containing generated data for subcubes in statoil format;
        	
        	resolution (float): resolution of studied sample (unitless), default: 1;
        	
        	length_unit_type (str): units of resolution. Can be 'NM', 'UM', 'MM' and 'M', default: 'M';
        	
        	direction (str): flow direction, could be 'x', 'y' or 'z', default: 'z'. 
        """
        super().__init__(statoildir, resolution, length_unit_type, direction, vectorizer=None)
        self.metric_type = 's'

    def generate(self, inputdir, cut_name, l, outputdir):
        """
        Generates pore number for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated data for subcubes in statoil format;
        	
        	cut_name (str): name of subcube;
        	
       		l (int): linear size of subcube.
        
        **Output:**
        
        	name of file (str), in which pore number, normalized over subcube volume, is written.
        """
        pore_number = super().generate(inputdir, cut_name, l)
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(pore_number))
        return cut_name_out
