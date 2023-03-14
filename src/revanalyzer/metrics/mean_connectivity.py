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
    def __init__(self,  statoildir, resolution=1., length_unit_type='M', direction='z'):
        """
        **Input:**
        
        statoildir (str): path to the folder containing generated data for subcubes in statoil format.
        resolution (float): resolution of studied sample (unitless), default: 1.
        length_unit_type (str): units of resolution. Can be 'NM', 'UM', 'MM' and 'M', default: 'M'.
        direction (str): flow direction, could be 'x', 'y' or 'z', default: 'z'. 
        """        
        super().__init__(statoildir, resolution, length_unit_type, direction, vectorizer=None)
        self.metric_type = 's'

    def generate(self, inputdir, cut_name, l, outputdir):
        """
        Generates mean connectivity for a specific subcube.
        
        **Input:**
        
        inputdir (str): path to the folder containing generated data for subcubes in statoil format.
        cut_name (str): name of subcube.
        l (int): linear size of subcube.
        
        **Output:**
        
        name of file (str), in which mean connectivity, normalized over subcube volume, is written.
        """         
        pore_number = super().generate(inputdir, cut_name, l)
        if pore_number > 0:
            filein = os.path.join(inputdir, cut_name) + "_" + \
                self.direction + '_link2.dat'
            connectivity = _read_mean_connectivity(filein)
        else:
            connectivity = 0
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(connectivity))
        return cut_name_out


def _read_mean_connectivity(filein):
    with open(filein, mode='r') as f:
        link = pd.read_table(filepath_or_buffer=f,
                             header=None,
                             sep='\s+',
                             skipinitialspace=True,
                             index_col=0)
    link.columns = ['throat.pore1', 'throat.pore2',
                    'throat.pore1_length', 'throat.pore2_length',
                    'throat.length', 'throat.volume',
                    'throat.clay_volume']
    con = np.vstack((link['throat.pore1']-1,
                     link['throat.pore2']-1)).T
    con1 = con.reshape(-1)
    (unique, counts) = np.unique(con1, return_counts=True)
    return np.mean(counts)
