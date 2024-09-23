# -*- coding: utf-8 -*-
"""Module for the generation of PNM characteristics using PNM extractor."""
import numpy as np
import time
import os
import multiprocessing
from itertools import repeat
import subprocess
import json
from .utils import _subcube_ids, make_cut, _write_array


def generate_PNM(image, size, n_steps, sREV_max_step, outputdir, exe_path, n_threads = 1, resolution=1., length_unit_type='M', inout_axe='z', show_time=False):
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
    cut_step = (np.array(size)/n_steps).astype(int)
    cut_sizes = [(cut_step*(i+1)).tolist() for i in range(n_steps-1)]
    cut_sizes.append(size)
    ids = _subcube_ids(n_steps, sREV_max_step)
    for i in ids:
        _pnm_for_subcube(exe_path, n_threads, i, n_steps, image, cut_sizes, outputdir, resolution, length_unit_type, inout_axe)
    if show_time:
        print("---PNM extractor run time is %s seconds ---" % (time.time() - start_time))


def get_pn_csv(exe_path, n_threads, cut, cut_name, outputdir, resolution, length_unit_type, inout_axe):
    """
    Calculation of PNM statistics for a given subcube and writing the result to csv file.
    
    **Input:**

     	cut (numpy.ndarray): 3D array representing a subcube;
     	
     	cut_name (str): name of output file;
     	
     	outputdir (str): path to the output folder containing generated data;
        
     	resolution (float): resolution of studied sample, default: 1;
    """
    glob_path = os.getcwd()
    output_path = os.path.join(glob_path, outputdir)
    my_env = os.environ.copy()
    my_env["OMP_NUM_THREADS"] = str(n_threads)
    image_path = os.path.join(output_path, cut_name)
    _write_array(cut, image_path)
    dimx = cut.shape[2]
    dimy = cut.shape[1]
    dimz = cut.shape[0]
    config_path = _make_PN_config(cut_name, dimx, dimy, dimz, outputdir, resolution, length_unit_type, inout_axe)
    code = subprocess.call([exe_path, config_path], env=my_env)
    if (code != 0):
        raise RuntimeError("Error in PNM extractor run occured!")
    os.remove(image_path)
    os.remove(config_path)


def _pnm_for_subcube(exe_path, n_threads, ids, n_steps, image, cut_sizes, outputdir, resolution, length_unit_type, inout_axe):
    l = ids[0]
    idx = ids[1]
    cut_name = 'cut'+str(l)+'_'+str(idx)
    size = cut_sizes[-1]
    if l  == n_steps:
        get_pn_csv(exe_path, n_threads, image, cut_name, outputdir, resolution, length_unit_type, inout_axe)
    else:
        cut_size = cut_sizes[l-1]
        cut = make_cut(image, size, cut_size, idx)
        get_pn_csv(exe_path, n_threads, cut, cut_name, outputdir, resolution, length_unit_type, inout_axe)

def _make_PN_config(name, dimx, dimy, dimz, outputdir, resolution=1., length_unit_type='M', inout_axe='z'):
    json_string = """
    {
    "input_data": {
        "filename": "pathname_in",
        "size": {
            "x": 0,
            "y": 0,
            "z": 0
        }
    },
    "output_data": {
        "statoil_prefix": "pathname_out"
    },
    "extraction_parameters": {
        "resolution": 1,
        "partitioning_coeff": 0.67,
        "length_unit_type_options": [
            "NM",
            "UM",
            "MM",
            "M"
        ],
        "length_unit_type": "M",
        "axis_type_options": [
            "DEFAULT",
            "INOUT",
            "PERIODIC"
        ],
        "axes": {
            "x": "DEFAULT",
            "y": "DEFAULT",
            "z": "DEFAULT"
        },
        "persistence_limit": 1.0,
        "simplification_size_limit": 0.0
    }
    }
    """
    PN_config = json.loads(json_string)
    glob_path = os.getcwd()
    PN_config["input_data"]["filename"] = os.path.join(
        glob_path, outputdir, name)
    PN_config["input_data"]["size"]["x"] = dimx
    PN_config["input_data"]["size"]["y"] = dimy
    PN_config["input_data"]["size"]["z"] = dimz
    PN_config["output_data"]["statoil_prefix"] = os.path.join(
        glob_path, outputdir, name + "_" + inout_axe)
    PN_config["extraction_parameters"]["resolution"] = resolution
    PN_config["extraction_parameters"]["length_unit_type"] = length_unit_type
    directions = ['x', 'y', 'z']
    for i in directions:
        if i == inout_axe:
            PN_config["extraction_parameters"]["axes"][i] = "INOUT"
    config_path = os.path.join(glob_path, outputdir, name + '.json')
    with open(config_path, 'w') as f:
        json.dump(PN_config, f, indent=4)
    return config_path
