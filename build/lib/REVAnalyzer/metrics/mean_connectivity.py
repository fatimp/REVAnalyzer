import numpy as np
import pandas as pd
import os
from .basic_metric import BasicMetric
from .basic_pnm_metric import BasicPNMMetric


class MeanConnectivity(BasicPNMMetric):
    def __init__(self,  statoildir, resolution=1., length_unit_type='M', direction='z'):
        super().__init__(statoildir, resolution, length_unit_type, direction, vectorizer=None)
        self.metric_type = 's'

    def generate(self, inputdir, cut_name, l, outputdir):
        pore_number = super().generate(inputdir, cut_name, l)
        if pore_number > 0:
            filein = os.path.join(inputdir, cut_name) + "_" + \
                self.direction + '_link2.dat'
            connectivity = _read_mean_connectivity(filein)
        else:
            connectivity = 0
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        with open(fileout, "w") as f:
            f.write(str(connectivity))
        return cut_name_out


def _read_mean_connectivity(filein):
    with open(filein, mode='r') as f:
        link = pd.read_table(filepath_or_buffer=f,
                             header=None,
                             sep='\s+',
                             skipinitialspace=True,
                             index_col=0)
    link.columns = ['throat.pore1', 'throat.pore2',
                    'throat.pore1_length', 'throat.pore2_length',
                    'throat.length', 'throat.volume',
                    'throat.clay_volume']
    con = np.vstack((link['throat.pore1']-1,
                     link['throat.pore2']-1)).T
    con1 = con.reshape(-1)
    (unique, counts) = np.unique(con1, return_counts=True)
    return np.mean(counts)
