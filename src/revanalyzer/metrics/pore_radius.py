import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from .basic_metric import BasicMetric
from .basic_pnm_metric import BasicPNMMetric


class PoreRadius(BasicPNMMetric):
    def __init__(self,  vectorizer, statoildir, resolution=1., length_unit_type='M', direction='z'):
        super().__init__(statoildir, resolution, length_unit_type, direction, vectorizer)
        self.metric_type = 'v'

    def generate(self, inputdir, cut_name, l, outputdir):
        pore_number = super().generate(inputdir, cut_name, l)
        if pore_number > 0:
            filein = os.path.join(inputdir, cut_name) + "_" + \
                self.direction + '_node2.dat'
            pore_radius = _read_pore_radius(filein)
        else:
            pore_radius = []
        cut_name_out = cut_name + ".txt"
        fileout = os.path.join(outputdir, cut_name_out)
        np.savetxt(fileout, pore_radius, delimiter='\t')
        return cut_name_out

    def show(self, inputdir, name, cut_size, cut_id, nbins):
        x, hist = super().show(inputdir, name, cut_size, cut_id, nbins)
        fig, ax = plt.subplots(figsize=(10, 8))
        title = self.__class__.__name__ + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        ax.set_title(title)
        ax.bar(x, hist, width=0.5, color='r')
        ax.set_xlabel('$R_p$')
        ax.set_ylabel('density')
        plt.show()


def _read_pore_radius(filein):
    with open(filein, mode='r') as f:
        node = pd.read_table(filepath_or_buffer=f,
                             header=None,
                             sep='\s+',
                             skipinitialspace=True,
                             index_col=0)
    node.columns = ['pore.volume', 'pore.radius', 'pore.shape_factor',
                    'pore.clay_volume']
    return np.array(node['pore.radius'])
