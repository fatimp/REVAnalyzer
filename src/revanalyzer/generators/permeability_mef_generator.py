# -*- coding: utf-8 -*-
"""Module for the computation of permeability using MEF."""

import os
import subprocess
import json
import shutil
import numpy as np
from .utils import make_cuts
from .pnm_generator import generate_PNM

mef_output = "mef_output"


def generate_permeability_mef(image, directions, size, cut_step, sREV_max_size, exe_path_ccm, exe_path_mef, exe_mef, n_threads=1, resolution=1., length_unit_type='UM', inputdir ='data', outputdir='output', show_time=False):
    """
    Running PNM-extractor and MEF module for all the selected subcubes.
    
    **Input:**

     	image (str): name of binary ('uint8') file representing the image;
     	
     	directions (str): 'x', 'y', 'z' or 'all'. If label of this parameter is 'all', permeability values are generated for all 3 possible flow directions;
     	
     	size (int): image linear size. Note, that only cubical images can be analyzed;
     	 
     	cut_step (int): increment step of subcube size;
     	
     	sREV_max_size (int): maximal subcube size for which sREV analysis is performed;
     	
     	exe_path_ccm (str): path to PNM-extractor;
     	
     	exe_path_mef (str): path to the folder with MEF exe file;
     	
     	exe_mef (str): path to exe file of MEF;
     	
     	n_threads (int): number of CPU cores used by FDMSS, default: 1;
     	
     	resolution (float): resolution of studied sample (unitless), default: 1;
     	
     	length_unit_type (str): units of resolution. Can be 'NM', 'UM', 'MM' and 'M', default: 'UM';
     	
     	inputdir (str): path to the folder containing image, default: 'data';
     	
     	outputdir (str): path to the output folder containing generated data, default: 'output';
     	
     	show_time (bool): Added to monitor time cost for large images,  default: False. 
     
     **Output:**
     	path to MEF output folder (str)
    """
    assert (directions == 'x' or directions == 'y' or directions ==
            'z' or directions == 'all'), "Direction should be 'x', 'y', 'z' or 'all'"
    if directions == 'all':
        directions_list = ['x', 'y', 'z']
    else:
        directions_list = [directions]
    glob_path = os.getcwd()
    outputdir_cuts_values = os.path.join(
        outputdir, image, 'Permeability', 'cuts_values')
    os.makedirs(outputdir_cuts_values, exist_ok=True)
    os.makedirs(os.path.join(glob_path, outputdir,
                image, mef_output), exist_ok=True)
    for direction in directions_list:
        statoildir = generate_PNM(image, size, cut_step, sREV_max_size, exe_path_ccm,
                                  n_threads, resolution, length_unit_type, direction, inputdir, outputdir, show_time)
        outputdir1 = os.path.join(outputdir, image)
        mef_output_name = _make_mef_config(
            statoildir, image, direction, outputdir1)
        config_path = os.path.join(glob_path, 'mef_config', image + ".json")
        os.chdir(exe_path_mef)
        code = subprocess.call([exe_mef, config_path])
        if (code != 0):
            raise RuntimeError("Error in PNM extractor run occured!")
        os.chdir(glob_path)
        perm_name = os.path.join(
            outputdir_cuts_values, image)
        if directions == 'all':
            perm_name = perm_name + "_" + direction
        _get_permeability(mef_output_name, perm_name)
        n_steps = int(np.ceil(size/cut_step))
        cut_sizes = [cut_step*(i+1) for i in range(n_steps-1)]
        for l in cut_sizes:
            cuts_data = 'cuts_data'
            os.makedirs(cuts_data, exist_ok=True)
            if (l <= sREV_max_size):
                cut_names = make_cuts(
                    inputdir, image, cuts_data, size, l, total=True)
                for cut_name in cut_names:
                    mef_output_name = _make_mef_config(
                        statoildir, cut_name, direction, outputdir1)
                    config_path = os.path.join(
                        glob_path, 'mef_config', cut_name + ".json")
                    os.chdir(exe_path_mef)
                    code = subprocess.call([exe_mef, config_path])
                    if (code != 0):
                        raise RuntimeError(
                            "Error in PNM extractor run occured!")
                    os.chdir(glob_path)
                    perm_name = os.path.join(
                        outputdir_cuts_values, cut_name)
                    if directions == 'all':
                        perm_name = perm_name + "_" + direction
                    _get_permeability(mef_output_name, perm_name)
                shutil.rmtree(cuts_data)
            else:
                cut_name = make_cuts(
                    inputdir, image, cuts_data, size, l, total=False)
                mef_output_name = _make_mef_config(
                    statoildir, cut_name, direction, outputdir1)
                config_path = os.path.join(
                    glob_path, 'mef_config', cut_name + ".json")
                os.chdir(exe_path_mef)
                code = subprocess.call([exe_mef, config_path])
                if (code != 0):
                    raise RuntimeError("Error in MEF run occured!")
                os.chdir(glob_path)
                perm_name = os.path.join(
                    outputdir_cuts_values, cut_name)
                if directions == 'all':
                    perm_name = perm_name + "_" + direction
                _get_permeability(mef_output_name, perm_name)
                shutil.rmtree(cuts_data)
    shutil.rmtree('mef_config')
    return os.path.join(outputdir1, mef_output)


def _make_mef_config(statoildir, name, direction, outputdir):
    json_string = """
    {
  "init_inlet_pressure": 0,
  "init_outlet_pressure": 1.2e6,
  "use_new_pbf_algorithm": false,
  "new_pbf_pressure_weight": 0.0,
  "possible_intrinsic_models": [
    "constant",
    "weibull"
  ],
  "fill_inlets": false,
  "possible_angle_models": [
    "uniform",
    "fixed",
    "MorrowII",
    "MorrowIII"
  ],
  "contact_angle_models": [
    {
      "fluid_from": "water",
      "fluid_to": "oil",
      "wetting_fluid": "water",
      "intrinsic_type": "constant",
      "intrinsic_constant_model_angle": 90,
      "weibull_gamma": 1,
      "weibull_delta": 1,
      "weibull_theta_min": 40,
      "weibull_theta_max": 150,
      "angle_type": "uniform",
      "uniform_min_angle": 0,
      "uniform_max_angle": 90,
      "MorrowII_angle": 35
    },
    {
      "fluid_from": "water",
      "fluid_to": "oil",
      "wetting_fluid": "oil",
      "intrinsic_type": "constant",
      "intrinsic_constant_model_angle": 90,
      "weibull_gamma": 1,
      "weibull_delta": 1,
      "weibull_theta_min": 40,
      "weibull_theta_max": 150,
      "angle_type": "uniform",
      "uniform_min_angle": 0,
      "uniform_max_angle": 90,
      "MorrowII_angle": 35
    }
  ],
  "statoil_prefix_path": "data/example/sandstone_x",
  "result_filename": "result.txt",
  "fluids": [
    {
      "name": "water",
      "change_wettability": false,
      "viscosity": 0.001,
      "bounded": 0.2,
      "surface_tension": {
        "oil": 0.03
      }
    },
    {
      "name": "oil",
      "change_wettability": false,
      "viscosity": 0.001,
      "bounded": 0.0,
      "surface_tension": {
        "water": 0.03
      }
    }
  ],
  "init_contained_fluid_name": "water",
  "init_wetting_fluid_name": "water",
  "flow_processes": [
 {
      "from_inlet_to_outlet": true,
      "final_pressure": -1e10,
      "final_saturation": 1,
      "pressure_step": 1e5,
      "saturation_step": 0.01,
      "inlet_fluid_name": "oil"
    }
  ],
  "flow_direction": "x",
  "has_preprocessing": false
}
    """
    mef_config = json.loads(json_string)
    glob_path = os.getcwd()
    mef_config["statoil_prefix_path"] = os.path.join(
        glob_path, statoildir, name + "_" + direction)
    mef_config["flow_direction"] = direction
    mef_output_name = os.path.join(
        glob_path, outputdir, mef_output, name + "_" + direction)
    mef_config["result_filename"] = mef_output_name
    configdir = 'mef_config'
    os.makedirs(configdir, exist_ok=True)
    with open(os.path.join(glob_path, configdir, name + ".json"), "w") as f:
        json.dump(mef_config, f, indent=4)
    return mef_output_name


def _get_permeability(filein, fileout):
    with open(filein, "r") as f:
        lines = f.readlines()
    s_perm = lines[17]
    perm = float(s_perm[20:])
    fileout = fileout + ".txt"
    with open(fileout, "w") as f:
        f.write(str(perm))
