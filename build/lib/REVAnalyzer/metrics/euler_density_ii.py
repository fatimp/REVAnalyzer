import numpy as np
import os
from .basic_metric import BasicMetric
from .basic_pnm_metric import BasicPNMMetric


class EulerDensityII(BasicPNMMetric):
    def __init__(self,  statoildir, resolution=1., length_unit_type='M', direction='z'):
        super().__init__(statoildir, resolution, length_unit_type, direction, vectorizer=None)
        self.metric_type = 's'

    def generate(self, inputdir, cut_name, l, outputdir):
        filein = os.path.join(inputdir, cut_name) + "_" + \
            self.direction + '_node1.dat'
        with open(filein, "r") as f:
            str_0 = f.readline().split()
            pore_number = int(str_0[0])/l**3
        filein2 = os.path.join(inputdir, cut_name) + "_" + \
            self.direction + '_link1.dat'
        with open(filein2, "r") as f:
            str_0 = f.readline().split()
            throat_number = int(str_0[0])/l**3
        cut_name_out = cut_name + ".txt"
        euler_number = pore_number - throat_number
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(euler_number))
        return cut_name_out
