import os
import subprocess
import json
import shutil
import numpy as np
import time
from .utils import make_cuts

statoildir = 'PN_data'


def generate_PNM(inputdir, image, size, cut_step, sREV_max_size, exe_path, n_threads=1, resolution=1., length_unit_type='M', direction='z', outputdir='output', show_time=False):
    start_time = time.time()
    glob_path = os.getcwd()
    outputdir = os.path.join(outputdir, image)
    _make_PN_config(inputdir, image, size, outputdir,
                    resolution=resolution, length_unit_type=length_unit_type, inout_axe=direction)
    config_path = os.path.join(glob_path, 'PN_config', image)
    my_env = os.environ.copy()
    my_env["OMP_NUM_THREADS"] = str(n_threads)
    code = subprocess.call([exe_path, config_path], env=my_env)
    if (code != 0):
        raise RuntimeError("Error in PNM extractor run occured!")
    if show_time:
        print("Size ", size, ", run time: ")
        print("--- %s seconds ---" % (time.time() - start_time))

    n_steps = int(np.ceil(size/cut_step))
    cut_sizes = [cut_step*(i+1) for i in range(n_steps-1)]
    for l in cut_sizes:
        start_time_l = time.time()
        cuts_data = 'cuts_data'
        os.makedirs(cuts_data, exist_ok=True)
        if (l <= sREV_max_size):
            cut_names = make_cuts(
                inputdir, image, cuts_data, size, l, total=True)
            for cut_name in cut_names:
                _make_PN_config(cuts_data, cut_name, l, outputdir,
                                resolution=resolution, length_unit_type=length_unit_type, inout_axe=direction)
                config_path = os.path.join(glob_path, 'PN_config', cut_name)
                code = subprocess.call([exe_path, config_path], env=my_env)
                if (code != 0):
                    raise RuntimeError("Error in PNM extractor run occured!")
            shutil.rmtree(cuts_data)
        else:
            cut_name = make_cuts(
                inputdir, image, cuts_data, size, l, total=False)
            _make_PN_config(cuts_data, cut_name, l, outputdir,
                            resolution=resolution, length_unit_type=length_unit_type, inout_axe=direction)
            config_path = os.path.join(glob_path, 'PN_config', cut_name)
            code = subprocess.call([exe_path, config_path], env=my_env)
            if (code != 0):
                raise RuntimeError("Error in PNM extractor run occured!")
            shutil.rmtree(cuts_data)
        if show_time:
            print("Size ", l, ", run time: ")
            print("--- %s seconds ---" % (time.time() - start_time_l))
    shutil.rmtree('PN_config')
    return os.path.join(outputdir, statoildir)


def _make_PN_config(inputdir, name, size, outputdir, resolution=1., length_unit_type='M', inout_axe='z', persistence_limit=1.):
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
        glob_path, inputdir, name)
    PN_config["input_data"]["size"]["x"] = size
    PN_config["input_data"]["size"]["y"] = size
    PN_config["input_data"]["size"]["z"] = size
    os.makedirs(os.path.join(glob_path, outputdir, statoildir), exist_ok=True)
    PN_config["output_data"]["statoil_prefix"] = os.path.join(
        glob_path, outputdir, statoildir, name + "_" + inout_axe)
    PN_config["extraction_parameters"]["resolution"] = resolution
    PN_config["extraction_parameters"]["length_unit_type"] = length_unit_type
    directions = ['x', 'y', 'z']
    for i in directions:
        if i == inout_axe:
            PN_config["extraction_parameters"]["axes"][i] = "INOUT"
    PN_config["extraction_parameters"]["resolution"] = persistence_limit
    configdir = 'PN_config'
    os.makedirs(configdir, exist_ok=True)
    with open(os.path.join(glob_path, configdir, name), 'w') as f:
        json.dump(PN_config, f, indent=4)
