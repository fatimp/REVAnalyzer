import numpy as np
import os
from .basic_metric import BasicMetric
from .basic_pnm_metric import BasicPNMMetric


class ThroatNumber(BasicPNMMetric):
    def __init__(self,  statoildir, resolution=1., length_unit_type='M', direction='z'):
        super().__init__(statoildir, resolution, length_unit_type, direction, vectorizer=None)
        self.metric_type = 's'

    def generate(self, inputdir, cut_name, l, outputdir):
        pore_number = super().generate(inputdir, cut_name, l)
        if pore_number > 0:
            filein = os.path.join(inputdir, cut_name) + "_" + \
                self.direction + '_link1.dat'
            with open(filein, "r") as f:
                str_0 = f.readline().split()
                throat_number = int(str_0[0])/l**3
        else:
            throat_number = 0
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(throat_number))
        return cut_name_out
