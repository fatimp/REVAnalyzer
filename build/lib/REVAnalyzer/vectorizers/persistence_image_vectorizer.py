import numpy as np
from gudhi.representations.vector_methods import PersistenceImage
from .basic_vectorizer import BasicVectorizer


class PersistenceImageVectorizer(BasicVectorizer):
    def __init__(self, resolution, bandwidth=1., norm=2):
        super().__init__(norm)
        self.resolution = resolution
        self.bandwidth = bandwidth

    def vectorize(self, v1, v2):
        n1 = len(v1)
        n2 = len(v2)
        C1 = PersistenceImage(bandwidth=self.bandwidth, weight=lambda x: np.arctan(0.5*(x[1] - x[0])),
                              resolution=self.resolution)
        C1.fit([v1])
        range1 = C1.im_range
        v1 = C1.transform([v1])
        v1 = v1/n1
        C2 = PersistenceImage(bandwidth=self.bandwidth, weight=lambda x: np.arctan(0.5*(x[1] - x[0])),
                              resolution=self.resolution, im_range=range1)
        C2.fit([v2])
        v2 = C2.transform([v2])
        v2 = v2/n2
        n1 = np.linalg.norm(v1, ord=self.norm)
        n2 = np.linalg.norm(v2, ord=self.norm)
        delta = 2*np.linalg.norm(np.array(v1) -
                                 np.array(v2), ord=self.norm)/(n1 + n2)
        return v1.tolist(), v2.tolist(), delta
