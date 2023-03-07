import numpy as np
from .basic_vectorizer import BasicVectorizer


class PNMVectorizer(BasicVectorizer):
    def __init__(self, factor=1, norm=2):
        super().__init__(norm)
        self.factor = factor

    def vectorize(self, v1, v2):
        rmax1 = np.ceil(max(v1))
        r1 = [0, rmax1]
        bins = int(self.factor*rmax1)
        hist1, bin_edges1 = np.histogram(v1, bins=bins, range=r1, density=True)
        hist2, bin_edges2 = np.histogram(v2, bins=bins, range=r1, density=True)
        n1 = np.linalg.norm(np.array(hist1), ord=self.norm)
        n2 = np.linalg.norm(np.array(hist2), ord=self.norm)
        delta = 2*np.linalg.norm(np.array(hist1) -
                                 np.array(hist2), ord=self.norm)/(n1 + n2)
        return hist1.tolist(), hist2.tolist(), delta
