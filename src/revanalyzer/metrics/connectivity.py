# -*- coding: utf-8 -*-
"""Definition of Connectivity metric"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from .basic_metric import BasicMetric
from .basic_pnm_metric import BasicPNMMetric


class Connectivity(BasicPNMMetric):
    """
    Class describing connectivity metric.
    """     
    def __init__(self,  vectorizer, statoildir, resolution=1., length_unit_type='M', direction='z'):
        """
        **Input:**
        
        	vectorizer (PNMVectorizer object): vectorizer to be used for Pore Radius metric;
        
        	statoildir (str): path to the folder containing generated data for subcubes in statoil format;
        
        	resolution (float): resolution of studied sample (unitless), default: 1;
        
        	length_unit_type (str): units of resolution. Can be 'NM', 'UM', 'MM' and 'M', default: 'M';
        
        	direction (str): flow direction, could be 'x', 'y' or 'z', default: 'z'. 
        """        
        super().__init__(statoildir, resolution, length_unit_type, direction, vectorizer)
        self.metric_type = 'v'

    def generate(self, inputdir, cut_name, l, outputdir):
        """
        Generates the connectivity distribution for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated data for subcubes in statoil format;
        	
        	cut_name (str): name of subcube;
        	
        	l (int): linear size of subcube.
        
        **Output:**
        
        	name of file (str), in which connectivity distribution, normalized over subcube volume, is written.
        """        
        pore_number = super().generate(inputdir, cut_name, l)
        if pore_number > 0:
            filein = os.path.join(inputdir, cut_name) + "_" + \
                self.direction + '_link2.dat'
            connectivity = _read_connectivity(filein)
        else:
            connectivity = []
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        np.savetxt(fileout, connectivity, delimiter='\t')
        return cut_name_out

    def show(self, inputdir, name, cut_size, cut_id, nbins):
        """
        Vizualize the connectivity distribution for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated metric data for subcubes;
        	 
        	name (str): name of binary ('uint8') file representing the image;
        	
        	cut_size (int): size of subcube;
        	
        	cut_id (int: 0,..8): cut index;
        	
        	nbins (int): number of bins in histogram. 
        """        
        x, hist = super().show(inputdir, name, cut_size, cut_id, nbins)
        fig, ax = plt.subplots(figsize=(10, 8))
        title = self.__class__.__name__ + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        ax.set_title(title)
        ax.bar(x, hist, width=0.5, color='r')
        ax.set_xlabel('connectivity')
        ax.set_ylabel('density')
        plt.show()


def _read_connectivity(filein):
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
    return np.array(counts)
