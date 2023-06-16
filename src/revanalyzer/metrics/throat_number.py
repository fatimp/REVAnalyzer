# -*- coding: utf-8 -*-
"""Definition of Throat Number metric"""

import numpy as np
import os
from .basic_metric import BasicMetric
from .basic_pnm_metric import BasicPNMMetric


class ThroatNumber(BasicPNMMetric):
    """
    Class describing throat number metric.
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
        Generates throat number for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated data for subcubes in statoil format;
        	
        	cut_name (str): name of subcube;
        	
        	l (int): linear size of subcube.
        
        **Output:**
        
        	name of file (str), in which throat number, normalized over subcube volume, is written.
        """        
        pore_number = super().generate(inputdir, cut_name, l)
        if pore_number > 0:
            filein = os.path.join(inputdir, cut_name) + "_" + \
                self.direction + '_link1.dat'
            with open(filein, "r") as f:
                str_0 = f.readline().split()
                throat_number = int(str_0[0])/l**3
        else:
            throat_number = 0
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(throat_number))
        return cut_name_out
