import numpy as np
import pandas as pd
import os
from .basic_metric import BasicMetric
from .basic_pnm_metric import BasicPNMMetric


class MeanPoreRadius(BasicPNMMetric):
    def __init__(self,  statoildir, resolution=1., length_unit_type='M', direction='z'):
        super().__init__(statoildir, resolution, length_unit_type, direction, vectorizer=None)
        self.metric_type = 's'

    def generate(self, inputdir, cut_name, l, outputdir):
        pore_number = super().generate(inputdir, cut_name, l)
        if pore_number > 0:
            filein = os.path.join(inputdir, cut_name) + "_" + \
                self.direction + '_node2.dat'
            pore_radius = _read_mean_pore_radius(filein)
        else:
            pore_radius = 0
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(pore_radius))
        return cut_name_out


def _read_mean_pore_radius(filein):
    with open(filein, mode='r') as f:
        node = pd.read_table(filepath_or_buffer=f,
                             header=None,
                             sep='\s+',
                             skipinitialspace=True,
                             index_col=0)
    node.columns = ['pore.volume', 'pore.radius', 'pore.shape_factor',
                    'pore.clay_volume']
    return np.mean(node['pore.radius'])
