import numpy as np
from gudhi.representations.vector_methods import Landscape
from .basic_vectorizer import BasicVectorizer


class LandscapeVectorizer(BasicVectorizer):
    def __init__(self, resolution, num_landcapes=1., norm=2):
        super().__init__(norm)
        self.resolution = resolution
        self.num_landscapes = num_landcapes

    def vectorize(self, v1, v2):
        L1 = Landscape(self.num_landscapes, self.resolution)
        L1.fit([v1])
        range1 = L1.sample_range
        v1 = L1.transform([v1])
        L2 = Landscape(self.num_landscapes,
                       self.resolution, sample_range=range1)
        L2.fit([v2])
        v2 = L2.transform([v2])
        n1 = np.linalg.norm(v1, ord=self.norm)
        n2 = np.linalg.norm(v2, ord=self.norm)
        delta = 2*np.linalg.norm(np.array(v1) -
                                 np.array(v2), ord=self.norm)/(n1 + n2)
        return v1.tolist(), v2.tolist(), delta
