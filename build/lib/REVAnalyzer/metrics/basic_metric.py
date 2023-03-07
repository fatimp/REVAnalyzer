import numpy as np
import os


class BasicMetric:
    def __init__(self, vectorizer):
        self.vectorizer = vectorizer
        self.directional = False
        self.metric_type = None

    def read(self, inputdir, name, cut_size, cut_id):
        if self.directional:
            directions = ('_x', '_y', '_z')
            if cut_size == 0:
                cut_names = [name + direction +
                             ".txt" for direction in directions]
            else:
                cut_names = ["cut" + str(cut_id) + "_" + str(cut_size) +
                             "_" + name + direction + ".txt" for direction in directions]
            data = []
            for cut_name in cut_names:
                if inputdir is not None:
                    filein = os.path.join(inputdir, cut_name)
                else:
                    filein = cut_name
                d = np.loadtxt(filein, delimiter=" ", dtype=np.float)
                if self.metric_type == 'v':
                    data.append(d)
                if self.metric_type == 's':
                    if np.isnan(d) or np.isinf(d):
                        data.append(0)
                    else:
                        data.append(d.item())
            return data
        else:
            if cut_size == 0:
                cut_name = name + ".txt"
            else:
                cut_name = "cut" + str(cut_id) + "_" + \
                    str(cut_size) + "_" + name + ".txt"
            if inputdir is not None:
                filein = os.path.join(inputdir, cut_name)
            else:
                filein = cut_name
            data = np.loadtxt(filein, delimiter=" ", dtype=np.float)
            if self.metric_type == 's' and np.isnan(data):
                data = np.array(0)
            return data
