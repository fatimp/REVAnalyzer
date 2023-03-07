import numpy as np
from .basic_vectorizer import BasicVectorizer


class CFVectorizer(BasicVectorizer):
    def __init__(self, norm=2, mode='max'):
        super().__init__(norm)
        self.mode = mode

    def vectorize(self, v1, v2):
        assert (self.mode == 'max' or self.mode ==
                'all'), "Mode should be 'max' or 'all'"
        n = min(len(v1[0]), len(v2[0]))
        if self.mode == 'max':
            v_res1 = []
            v_res2 = []
            deltas = []
            for i in range(3):
                v_norm1 = np.linalg.norm(v1[i], ord=self.norm)
                v_norm2 = np.linalg.norm(v2[i], ord=self.norm)
                d = np.linalg.norm(np.array(v1[i][:n]) -
                                   np.array(v2[i][:n]), ord=self.norm)
                deltas.append(2 * d/(v_norm1 + v_norm2))
                vi1 = np.array(v1[i][:n])/v_norm1
                vi2 = np.array(v2[i][:n])/v_norm2
                v_res1.append(vi1.tolist())
                v_res2.append(vi2.tolist())
        if self.mode == 'all':
            v_res1 = np.concatenate([v1[0][:n], v1[1][:n], v1[2][:n]]).tolist()
            v_res2 = np.concatenate([v2[0][:n], v2[1][:n], v2[2][:n]]).tolist()
            v_norm1 = np.linalg.norm(np.array(v_res1), ord=self.norm)
            v_norm2 = np.linalg.norm(np.array(v_res2), ord=self.norm)
            deltas = 2 * \
                np.linalg.norm(np.array(v_res1) - np.array(v_res2),
                               ord=self.norm)/(v_norm1 + v_norm2)
        return v_res1, v_res2, deltas
