import numpy as np
from .basic_vectorizer import BasicVectorizer


class SimpleBinningVectorizer(BasicVectorizer):
    def __init__(self, bins, skip_zeros=True, norm=2):
        super().__init__(norm)
        self.bins = bins
        self.skip_zeros = skip_zeros

    def vectorize(self, v1, v2):
        r1 = _range_pd(v1)
        v1 = _hist_pd(v1, self.bins, r1)
        v2 = _hist_pd(v2, self.bins, r1)
        if self.skip_zeros:
            v12 = _skip_zeros12(v1, v2)
            v1 = v12[0]
            v2 = v12[1]
        n1 = np.linalg.norm(v1, ord=self.norm)
        n2 = np.linalg.norm(v2, ord=self.norm)
        delta = 2*np.linalg.norm(np.array(v1) -
                                 np.array(v2), ord=self.norm)/(n1 + n2)
        return v1, v2, delta


def _hist_pd(v, bins, r):
    v = [i for i in zip(*v)]
    b = np.array(v[0])
    d = np.array(v[1])
    d = d - b
    hist = np.histogram2d(b, d, bins=bins, range=r)
    norm = len(b)
    return np.ravel(hist[0])/norm


def _range_pd(v):
    v = [i for i in zip(*v)]
    b = np.array(v[0])
    d = np.array(v[1])
    d = np.array(d) - np.array(b)
    xmin = min(b)
    xmax = max(b)
    ymin = min(d)
    ymax = max(d)
    r = [[xmin, xmax], [ymin, ymax]]
    return r


def _skip_zeros12(v1, v2):
    v1_new = []
    v2_new = []
    zeroes_ids = []
    for count, elem in enumerate(zip(v1, v2)):
        if (elem[0] > 0 or elem[1] > 0):
            v1_new.append(elem[0])
            v2_new.append(elem[1])
        else:
            zeroes_ids.append(count)
    return (v1_new, v2_new, zeroes_ids)
