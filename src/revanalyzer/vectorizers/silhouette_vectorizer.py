import numpy as np
from gudhi.representations.vector_methods import Silhouette
from .basic_vectorizer import BasicVectorizer


class SilhouetteVectorizer(BasicVectorizer):
    def __init__(self, resolution, n=1, norm=2):
        super().__init__(norm)
        self.resolution = resolution
        self.n = n

    def vectorize(self, v1, v2):
        S1 = Silhouette(weight=lambda x: (
            x[1] - x[0])**self.n, resolution=self.resolution)
        S1.fit([v1])
        range1 = S1.sample_range
        v1 = S1.transform([v1])
        S2 = Silhouette(weight=lambda x: (
            x[1] - x[0])**self.n, resolution=self.resolution,  sample_range=range1)
        S2.fit([v2])
        v2 = S2.transform([v2])
        n1 = np.linalg.norm(v1, ord=self.norm)
        n2 = np.linalg.norm(v2, ord=self.norm)
        delta = 2*np.linalg.norm(np.array(v1) -
                                 np.array(v2), ord=self.norm)/(n1 + n2)
        return v1.tolist(), v2.tolist(), delta
