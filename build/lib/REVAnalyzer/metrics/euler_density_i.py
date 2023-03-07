
from .basic_metric import BasicMetric
import numpy as np
import matplotlib.pyplot as plt
import os
import time
from julia import Main
from julia.api import Julia
jl = Julia(compiled_modules=False)


class EulerDensityI(BasicMetric):
    def __init__(self, show_time=False):
        super().__init__(vectorizer=None)
        self.metric_type = 's'
        self.show_time = show_time

    def generate(self, inputdir, cut_name, l, outputdir):
        start_time = time.time()
        if inputdir is not None:
            filein = os.path.join(inputdir, cut_name)
        else:
            filein = cut_name
        jl.eval('include("./REVAnalyzer/jl/euler_density.jl")')
        Main.data = [filein, str(l)]
        euler_d = jl.eval("euler_density(data)")
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(euler_d))
        if self.show_time:
            print("cut ", cut_name, ", run time: ")
            print("--- %s seconds ---" % (time.time() - start_time))
        return cut_name_out
