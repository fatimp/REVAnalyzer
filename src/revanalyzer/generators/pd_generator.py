import os
import subprocess
import shutil
import numpy as np
import time
import pandas as pd
from .utils import make_cuts


def generate_PD(image, size, cut_step, sREV_max_size, exe_path, n_threads=1, p_limit=0, inputdir = 'data', outputdir='output', show_time=False):
    start_time = time.time()
    glob_path = os.getcwd()
    outputdir = os.path.join(outputdir, image)
    my_env = os.environ.copy()
    my_env["OMP_NUM_THREADS"] = str(n_threads)
    input_path = os.path.join(
        glob_path, inputdir)
    output_path = os.path.join(
        glob_path, outputdir)

    code = subprocess.call(
        [exe_path, str(size), str(p_limit), input_path, image, output_path], env=my_env)
    if (code != 0):
        raise RuntimeError("Error in persistent pairs generator run occured!")
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
                input_path = os.path.join(glob_path, cuts_data)
                code = subprocess.call(
                    [exe_path, str(l), str(p_limit), input_path, cut_name, output_path], env=my_env)
                if (code != 0):
                    raise RuntimeError(
                        "Error in persistent pairs generator run occured!")
            shutil.rmtree(cuts_data)
        else:
            cut_name = make_cuts(
                inputdir, image, cuts_data, size, l, total=False)
            input_path = os.path.join(glob_path, cuts_data)
            code = subprocess.call(
                [exe_path, str(l), str(p_limit), input_path, cut_name, output_path], env=my_env)
            if (code != 0):
                raise RuntimeError(
                    "Error in persistent pairs generator run occured!")
            shutil.rmtree(cuts_data)
        if show_time:
            print("Size ", l, ", run time: ")
            print("--- %s seconds ---" % (time.time() - start_time_l))
    return os.path.join(outputdir)
