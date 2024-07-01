# -*- coding: utf-8 -*-
"""Module for the generation of PNM characteristics using SNOW algorithm."""

import time
import os
import multiprocessing
from itertools import repeat
import porespy as ps
import openpnm as op
from .utils import _subcube_ids, make_cut


def generate_PNM(image, cut_step, sREV_max_size, outputdir, n_threads = 1, resolution=1., show_time=False):
    """
    Running PNM extractor for all the selected subcubes.
    
    **Input:**

     	image (numpy.ndarray): 3D array representing the image;
     	
     	cut_step (int): increment step of subcube size;
     	
     	sREV_max_size (int): maximal subcube size for which sREV analysis is performed;
     	
     	outputdir (str): path to the output folder containing generated data;
     	
        n_threads (int): number of CPU cores used for data generation, default: 1;
        
     	resolution (float): resolution of studied sample, default: 1;
        
     	show_time (bool): Added to monitor time cost for large images,  default: False. 
    """
    start_time = time.time()
    L = image.shape[0]
    ids = _subcube_ids(L, cut_step, sREV_max_size)
    print(ids)
    pool = multiprocessing.Pool(processes=n_threads)
    print('aaa')
    #results = pool.starmap(_pnm_for_subcube, zip(ids, repeat(image), repeat(L), repeat(outputdir), repeat(resolution)))
    for elem in ids:
        pool.apply_async(_pnm_for_subcube, args = (elem, image, L, outputdir, resolution))
    print('bbb')
    pool.close()
    pool.join()
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
    cut = cut.astype(bool)
    print(cut)
    print('get_pn_csv: ', cut_name, outputdir, resolution)
    snow_output = ps.networks.snow2(cut, voxel_size = resolution)
    print('snow passed')
    pn = op.io.network_from_porespy(snow_output.network)
    print('pn passed')
    cut_name = os.path.join(outputdir, cut_name)
    op.io.network_to_csv(pn, filename = cut_name)
    print(cut_name, ' passed')


def _pnm_for_subcube(ids, image, L, outputdir, resolution):
    l = ids[0]
    idx = ids[1]
    if l  == 0 and idx == 0:
        get_pn_csv(image, 'cut0.csv', outputdir, resolution)
    else:
        cut = make_cut(image, L, l, idx)
        cut_name = 'cut'+str(idx)+'_'+str(l) + '.csv'
        get_pn_csv(cut, cut_name, outputdir, resolution)


