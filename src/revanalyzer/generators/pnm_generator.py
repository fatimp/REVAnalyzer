# -*- coding: utf-8 -*-
"""Module for the generation of PNM characteristics using PNM extractor."""

import time
import os
import multiprocessing
from itertools import repeat
import subprocess
import json
from .utils import _subcube_ids, make_cut, _write_array


def generate_PNM(image, cut_step, sREV_max_size, outputdir, exe_path, n_threads = 1, resolution=1., length_unit_type='M', inout_axe='z', show_time=False):
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
    for i in ids:
        _pnm_for_subcube(exe_path, n_threads, i, image, outputdir, resolution, length_unit_type, inout_axe)
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
    L = cut.shape[0]
    config_path = _make_PN_config(cut_name, L, outputdir, resolution, length_unit_type, inout_axe)
    code = subprocess.call([exe_path, config_path], env=my_env)
    if (code != 0):
        raise RuntimeError("Error in PNM extractor run occured!")
    os.remove(image_path)
    os.remove(config_path)


def _pnm_for_subcube(exe_path, n_threads, ids, image, outputdir, resolution, length_unit_type, inout_axe):
    l = ids[0]
    idx = ids[1]
    if l  == 0 and idx == 0:
        get_pn_csv(exe_path, n_threads, image, 'cut0', outputdir, resolution, length_unit_type, inout_axe)
    else:
        L = image.shape[0]
        cut = make_cut(image, L, l, idx)
        cut_name = 'cut'+str(idx)+'_'+str(l)
        get_pn_csv(exe_path, n_threads, cut, cut_name, outputdir, resolution, length_unit_type, inout_axe)

def _make_PN_config(name, size, outputdir, resolution=1., length_unit_type='M', inout_axe='z'):
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
    PN_config["input_data"]["size"]["x"] = size
    PN_config["input_data"]["size"]["y"] = size
    PN_config["input_data"]["size"]["z"] = size
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
