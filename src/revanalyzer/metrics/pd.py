# -*- coding: utf-8 -*-
"""Definition of PD-based metrics. For the definition of persistence diagrams (PD) see the documentation."""

from .basic_metric import BasicMetric
import numpy as np
import matplotlib.pyplot as plt
from revanalyzer.vectorizers import SimpleBinningVectorizer, PersistenceImageVectorizer, LandscapeVectorizer, SilhouetteVectorizer


class BasicPDMetric(BasicMetric):
    """
    Base class of PD-based metrics. (Don't use it directly but derive from it).
    """ 
    def __init__(self, vectorizer):
        """
        **Input:**
        
        vectorizer (SimpleBinningVectorizer, PersistenceImageVectorizer, LandscapeVectorizer or SilhouetteVectorizer 
                   object):vectorizer to be used for PD metric.
        """
        assert isinstance(vectorizer, SimpleBinningVectorizer) or isinstance(vectorizer, PersistenceImageVectorizer) or isinstance(
            vectorizer, LandscapeVectorizer) or isinstance(vectorizer, SilhouetteVectorizer), 'Vectorizer should be an object of SimpleBinningVectorizer, PersistenceImageVectorizer, LandscapeVectorizer or SilhouetteVectorizer class'
        super().__init__(vectorizer)

    def show(self, inputdir, name, cut_size, cut_id):
        """
        Transforms generated PD data to the convenient fomat to the following visualization in subclasses.
        
        **Input:**
        
        inputdir (str): path to the folder containing generated metric data for subcubes. 
        name (str): name of binary ('uint8') file representing the image.
        cut_size (int): size of subcube.
        cut_id (int: 0,..8): cut index.
        
        **Output:**
        
        (list(dtype = float), list(dtype = float)) -  a tuple, in which the first and the second elements are the vectors of 
        birth and death values, respectively.
        """          
        data = self.read(inputdir, name, cut_size, cut_id)
        b = [elem[0] for elem in data]
        d = [elem[1] for elem in data]
        plt.rcParams.update({'font.size': 16})
        plt.rcParams['figure.dpi'] = 300
        return b, d

    def vectorize(self, v1, v2):
        """
        Vectorize the vector metric values for a given pair of subcubes using the method of vectorizer. 
        
        **Input:**
        
        v1 (list(dtype = float)): data for the first cubcube.
        v2 (list(dtype = float)): data for the second cubcube.
        
        **Output:**
        
        (list(dtype = float), list(dtype = float), float) - a tuple, in which the first two elements are vectorized metric values
        for a given pair of subcubes, and the last one is the normalized distance between these vectors. 
        """
        return self.vectorizer.vectorize(v1, v2)
        

class PD0(BasicPDMetric):
    """
    Class describing metric PD of rank 0.
    """    
    def __init__(self, vectorizer):
        """
        **Input:**
        
        vectorizer (SimpleBinningVectorizer, PersistenceImageVectorizer, LandscapeVectorizer or SilhouetteVectorizer 
                   object):vectorizer to be used for PD metric.
        """
        super().__init__(vectorizer)
        self.metric_type = 'v'

    def show(self, inputdir, name, cut_size, cut_id):
        """
        Vizualize the PD of rank 0 for a specific subcube.
        
        **Input:**
        
        inputdir (str): path to the folder containing generated metric data for subcubes. 
        name (str): name of binary ('uint8') file representing the image.
        cut_size (int): size of subcube.
        cut_id (int: 0,..8): cut index.
        """  
        b, d = super().show(inputdir, name, cut_size, cut_id)
        title = 'PD0' + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        _show_pd(b, d, title)


class PD1(BasicPDMetric):
    """
    Class describing metric PD of rank 1.
    """ 
    def __init__(self, vectorizer):
        """
        **Input:**
        
        vectorizer (SimpleBinningVectorizer, PersistenceImageVectorizer, LandscapeVectorizer or SilhouetteVectorizer 
                   object):vectorizer to be used for PD metric.
        """
        super().__init__(vectorizer)
        self.metric_type = 'v'

    def show(self, inputdir, name, cut_size, cut_id):
        """
        Vizualize the PD of rank 1 for a specific subcube.
        
        **Input:**
        
        inputdir (str): path to the folder containing generated metric data for subcubes. 
        name (str): name of binary ('uint8') file representing the image.
        cut_size (int): size of subcube.
        cut_id (int: 0,..8): cut index.
        """  
        b, d = super().show(inputdir, name, cut_size, cut_id)
        title = 'PD1' + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        _show_pd(b, d, title)


class PD2(BasicPDMetric):
    """
    Class describing metric PD of rank 2.
    """ 
    def __init__(self, vectorizer):
        """
        **Input:**
        
        vectorizer (SimpleBinningVectorizer, PersistenceImageVectorizer, LandscapeVectorizer or SilhouetteVectorizer 
                   object):vectorizer to be used for PD metric.
        """
        super().__init__(vectorizer)
        self.metric_type = 'v'

    def show(self, inputdir, name, cut_size, cut_id):
        """
        Vizualize the PD of rank 2 for a specific subcube.
        
        **Input:**
        
        inputdir (str): path to the folder containing generated metric data for subcubes. 
        name (str): name of binary ('uint8') file representing the image.
        cut_size (int): size of subcube.
        cut_id (int: 0,..8): cut index.
        """  
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
