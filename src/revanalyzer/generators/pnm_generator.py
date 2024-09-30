# -*- coding: utf-8 -*-
"""Module for the generation of PNM characteristics using PNM extractor."""
import numpy as np
import time
import os
import porespy as ps
import openpnm as op
import multiprocessing
from .utils import _subcube_ids, make_cut


def generate_PNM(image, size, n_steps, sREV_max_step, outputdir, n_threads = 1, resolution=1., show_time=False):
    """
    Running PNM extractor for all the selected subcubes.
    
    **Input:**

     	image (numpy.ndarray): 3D array representing the image;
     	
        size (tuple (int, int, int)): linear image sizes in x, y and z directions;
        
     	n_steps (int): number of subsamples selection steps;
     	
     	sREV_max_step (int): maximal step for which sREV and stationarity analysis can be performed;
     	
     	outputdir (str): path to the output folder containing generated data;
     	
        n_threads (int): number of threads used for data generation, default: 1;
        
     	resolution (float): resolution of studied sample, default: 1; 
        
     	show_time (bool): Added to monitor time cost for large images,  default: False. 
    """
    cut_step = (np.array(size)/n_steps).astype(int)
    cut_sizes = [(cut_step*(i+1)).tolist() for i in range(n_steps-1)]
    cut_sizes.append(size)
    ids = _subcube_ids(n_steps, sREV_max_step)
    #for i in ids:
    #    _pnm_for_subcube(n_threads, i, n_steps, image, cut_sizes, outputdir, resolution, show_time)
    pool = multiprocessing.Pool(processes=n_threads)
    for elem in ids:
        pool.apply_async(_pnm_for_subcube, args = (elem, n_steps, image, cut_sizes, outputdir, resolution, show_time))
    pool.close()
    pool.join()

#def get_pn_csv(n_threads, cut, cut_name, outputdir, resolution, show_time):
def get_pn_csv(cut, cut_name, outputdir, resolution, show_time):
    """
    Calculation of PNM statistics for a given subcube and writing the result to csv file.
    
    **Input:**
    
        n_threads (int): number of threads used for data generation;

     	cut (numpy.ndarray): 3D array representing a subsample;
     	
     	cut_name (str): name of output file;
     	
     	outputdir (str): path to the output folder containing generated data;
        
     	resolution (float): resolution of studied subsample;
        
        show_time (bool): Added to monitor time cost for large images.
    """
    start_time = time.time()
    cut = cut.astype(bool)
    cut = ~cut
    #parallelization = {'cores':n_threads}
    parallelization = {'cores':1}
    snow_output = ps.networks.snow2(cut, voxel_size = resolution, parallelization = parallelization)
    pn = op.io.network_from_porespy(snow_output.network)
    cut_name1 = os.path.join(outputdir, cut_name)
    op.io.network_to_csv(pn, filename = cut_name1)
    if show_time:
        print(cut_name)
        print("---PNM extractor run time is %s seconds ---" % (time.time() - start_time))

"""
def _pnm_for_subcube(n_threads, ids, n_steps, image, cut_sizes, outputdir, resolution, show_time):
    l = ids[0]
    idx = ids[1]
    cut_name = 'cut'+str(l)+'_'+str(idx)
    size = cut_sizes[-1]
    if l  == n_steps:
        get_pn_csv(n_threads, image, cut_name, outputdir, resolution, show_time)
    else:
        cut_size = cut_sizes[l-1]
        cut = make_cut(image, size, cut_size, idx)
        get_pn_csv(n_threads, cut, cut_name, outputdir, resolution, show_time)
"""

def _pnm_for_subcube(ids, n_steps, image, cut_sizes, outputdir, resolution, show_time):
    l = ids[0]
    idx = ids[1]
    cut_name = 'cut'+str(l)+'_'+str(idx)
    size = cut_sizes[-1]
    if l  == n_steps:
        get_pn_csv(image, cut_name, outputdir, resolution, show_time)
    else:
        cut_size = cut_sizes[l-1]
        cut = make_cut(image, size, cut_size, idx)
        get_pn_csv(cut, cut_name, outputdir, resolution, show_time)