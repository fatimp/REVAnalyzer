
from .basic_metric import BasicMetric
import numpy as np
import matplotlib.pyplot as plt
from REV_analyzer.vectorizes import SimpleBinningVectorizer, PersistenceImageVectorizer, LandscapeVectorizer, SilhouetteVectorizer


class BasicPDMetric(BasicMetric):
    def __init__(self, vectorizer):
        assert isinstance(vectorizer, SimpleBinningVectorizer) or isinstance(vectorizer, PersistenceImageVectorizer) or isinstance(
            vectorizer, LandscapeVectorizer) or isinstance(vectorizer, SilhouetteVectorizer), "Vectorizer should be an object of SimpleBinningVectorizer, PersistenceImageVectorizer, LandscapeVectorizer or SilhouetteVectorizer class"
        super().__init__(vectorizer)

    def show(self, inputdir, name, cut_size, cut_id):
        data = self.read(inputdir, name, cut_size, cut_id)
        b = [elem[0] for elem in data]
        d = [elem[1] for elem in data]
        plt.rcParams.update({'font.size': 16})
        plt.rcParams['figure.dpi'] = 300
        return b, d

    def vectorize(self, v1, v2):
        return self.vectorizer.vectorize(v1, v2)


class PD0(BasicPDMetric):
    def __init__(self, vectorizer):
        super().__init__(vectorizer)
        self.metric_type = 'v'

    def show(self, inputdir, name, cut_size, cut_id):
        b, d = super().show(inputdir, name, cut_size, cut_id)
        title = 'PD0' + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        _show_pd(b, d, title)


class PD1(BasicPDMetric):
    def __init__(self, vectorizer):
        super().__init__(vectorizer)
        self.metric_type = 'v'

    def show(self, inputdir, name, cut_size, cut_id):
        b, d = super().show(inputdir, name, cut_size, cut_id)
        title = 'PD1' + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        _show_pd(b, d, title)


class PD2(BasicPDMetric):
    def __init__(self, vectorizer):
        super().__init__(vectorizer)
        self.metric_type = 'v'

    def show(self, inputdir, name, cut_size, cut_id):
        b, d = super().show(inputdir, name, cut_size, cut_id)
        title = 'PD2' + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        _show_pd(b, d, title)


def _show_pd(b, d, title):
    fig, ax = plt.subplots()
    plt.title(title)
    plt.plot(b, d, "ro")
    plt.axhline(y=0, color='black', linestyle='-')
    plt.axvline(x=0, color='black', linestyle='-')
    plt.xlabel("birth")
    plt.ylabel("death")
    plt.show()
