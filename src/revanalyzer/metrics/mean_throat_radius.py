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
        Generates mean throat radius for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated data for subcubes in statoil format;
        	
        	cut_name (str): name of subcube;
        	
        	l (int): linear size of subcube.
        
        **Output:**
        
        	name of file (str), in which mean throat radius, normalized over subcube volume, is written.
        """        
        pore_number = super().generate(inputdir, cut_name, l)
        if pore_number > 0:
            filein = os.path.join(inputdir, cut_name) + "_" + \
                self.direction + '_link1.dat'
            throat_radius = _read_mean_throat_radius(filein)
        else:
            throat_radius = 0
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(throat_radius))
        return cut_name_out


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
