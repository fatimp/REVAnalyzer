# -*- coding: utf-8 -*-
"""Module for the generation of PNM characteristics using SNOW algorithm."""

import time
import os
import numpy as np
import porespy as ps
import openpnm as op
from .utils import _read_array, make_cut


def generate_PNM(image, cut_step, sREV_max_size, outputdir, resolution=1., show_time=False):
    """
    Running PNM extractor for all the selected subcubes.
    
    **Input:**

     	image (numpy.ndarray): 3D array representing the image;
     	
     	cut_step (int): increment step of subcube size;
     	
     	sREV_max_size (int): maximal subcube size for which sREV analysis is performed;
     	
     	outputdir (str): path to the output folder containing generated data;
     	
     	resolution (float): resolution of studied sample, default: 1;
        
     	show_time (bool): Added to monitor time cost for large images,  default: False. 
    """
    start_time = time.time()
    L = image.shape[0]
    n_steps = int(np.ceil(L/cut_step))
    cut_sizes = [cut_step*(i+1) for i in range(n_steps-1)]
    for l in cut_sizes:
        if (l <= sREV_max_size):
            for idx in range(9):
                cut = make_cut(image, L, l, idx)
                cut_name = 'cut'+str(idx)+'_'+str(l) + '.csv'
                get_pn_csv(cut, cut_name, outputdir, resolution)
        else:
            cut = make_cut(image, L, l, 0)
            cut_name = 'cut0'+'_'+str(l)+ '.csv'
            get_pn_csv(cut, cut_name, outputdir, resolution)
    get_pn_csv(image, 'cut0.csv', outputdir, resolution)
    if show_time:
        print("---PNM extractor run time is %s seconds ---" % (time.time() - start_time))


def get_pn_csv(cut, cut_name, outputdir, resolution):
    """
    Calculation of PNM statistics for a given subcube and writing the result to csv file.
    
    **Input:**

     	cut (numpy.ndarray): 3D array representing a subcube;
     	
     	cut_name (str): name of output file;
     	
     	outputdir (str): path to the output folder containing generated data;
        
     	resolution (float): resolution of studied sample, default: 1;
    """
    snow_output = ps.networks.snow2(cut, voxel_size = resolution)
    pn = op.io.network_from_porespy(snow_output.network)
    cut_name = os.path.join(outputdir, cut_name)
    op.io.network_to_csv(pn, filename = cut_name)
