# -*- coding: utf-8 -*-
"""Definition of PD-based metrics. For the definition of persistence diagrams (PD) see the documentation."""

from .basic_metric import BasicMetric
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import subprocess
from ..generators import _write_array
from ..vectorizers import SimpleBinningVectorizer, PersistenceImageVectorizer, LandscapeVectorizer, SilhouetteVectorizer


class BasicPDMetric(BasicMetric):
    """
    Base class of PD-based metrics. (Don't use it directly but derive from it).
    """ 
    def __init__(self, vectorizer, exe_path, n_threads, show_time):
        """
        **Input:**
        
        	vectorizer (SimpleBinningVectorizer, PersistenceImageVectorizer, LandscapeVectorizer or SilhouetteVectorizer object): vectorizer to be used for PD metric.
        	
        	show_time (bool): flag to monitor time cost for large images.
        """
        if not (isinstance(vectorizer, SimpleBinningVectorizer) or isinstance(vectorizer, PersistenceImageVectorizer) or isinstance(
            vectorizer, LandscapeVectorizer) or isinstance(vectorizer, SilhouetteVectorizer)):
            raise TypeError('Vectorizer should be an object of SimpleBinningVectorizer, PersistenceImageVectorizer, LandscapeVectorizer or SilhouetteVectorizer class')
        super().__init__(vectorizer, n_threads = n_threads)
        self.exe_path = exe_path
        self.show_time = show_time
        
    def generate(self, cut, cut_name, outputdir, gendatadir = None):
        """
        Generates PD metric for a specific subcube.
        
        **Input:**
        
        	cut (numpy.ndarray): subcube;
        	
        	cut_name (str): name of subcube;
        	
        	outputdir (str): output folder;
        	    
        	i (0,1,2): rank of generated PD.
        """ 
        start_time = time.time()
        glob_path = os.getcwd()
        my_env = os.environ.copy()
        my_env["OMP_NUM_THREADS"] = str(self.n_threads)
        output_path = os.path.join(glob_path, outputdir)
        image_path = os.path.join(output_path, cut_name) 
        dimx = cut.shape[2]
        dimy = cut.shape[1]
        dimz = cut.shape[0]
        pd0 = os.path.join(output_path, 'PD0', 'cuts_values')
        pd1 = os.path.join(output_path, 'PD1', 'cuts_values')
        pd2 = os.path.join(output_path, 'PD2', 'cuts_values')
        os.makedirs(pd0, exist_ok=True)
        os.makedirs(pd1, exist_ok=True)
        os.makedirs(pd2, exist_ok=True)
        _write_array(cut, image_path)
        code = subprocess.call([self.exe_path, str(dimx), str(dimy), str(dimz), output_path, cut_name, output_path], env=my_env)
        if (code != 0):
            raise RuntimeError("Error in PD generator occured!")
        os.remove(image_path)
        if self.show_time:
            print("cut ", cut_name, ", run time: ")
            print("--- %s seconds ---" % (time.time() - start_time))
        return cut_name + ".txt"
        

    def show(self, inputdir, step, cut_id):
        """
        Transforms generated PD data to the convenient fomat to the following visualization in subclasses.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated metric data for subcubes;
                	
        	cut_size (int): size of subcube;
        	
        	cut_id (int: 0,..8): cut index.
        
        **Output:**
        
        	(list(dtype = float), list(dtype = float)) -  a tuple, in which the first and the second elements are the vectors of birth and death values, respectively.
        """          
        data = self.read(inputdir, step, cut_id)
        b = [elem[0] for elem in data]
        d = [elem[1] for elem in data]
        plt.rcParams.update({'font.size': 16})
        plt.rcParams['figure.dpi'] = 300
        return b, d

    def vectorize(self, v1, v2):
        """
        Vectorize the vector metric values for a given pair of subcubes using the method of vectorizer. 
        
        **Input:**
        
        	v1 (list(dtype = float)): data for the first cubcube;
        	
        	v2 (list(dtype = float)): data for the second cubcube.
        
        **Output:**
        
        	(list(dtype = float), list(dtype = float), float) - a tuple, in which the first two elements are vectorized metric values for a given pair of subcubes, and the last one is the normalized distance between these vectors. 
        """
        return self.vectorizer.vectorize(v1, v2)


class PD0(BasicPDMetric):
    """
    Class describing metric PD of rank 0.
    """    
    def __init__(self, vectorizer, exe_path, n_threads = 1, show_time = False):
        """
        **Input:**
        
        	vectorizer (SimpleBinningVectorizer, PersistenceImageVectorizer, LandscapeVectorizer or SilhouetteVectorizer object): vectorizer to be used for PD metric.
        	
        	show_time (bool): flag to monitor time cost for large images.        
        """
        super().__init__(vectorizer, exe_path, n_threads, show_time)
        self.metric_type = 'v'
        
    def generate(self, cut, cut_name, outputdir, gendatadir = None):
        """
        Generates the PD of rank 0 for a specific subcube.
        
        **Input:**
        
        	cut (numpy.ndarray): subcube;
        	
        	cut_name (str): name of subcube;
        	
        	outputdir (str): output folder.
        """
        return super().generate(cut, cut_name, outputdir)

    def show(self, inputdir, step, cut_id):
        """
        Vizualize the PD of rank 0 for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated metric data for subcubes;
        	 
        	cut_size (int): size of subcube;
        	
        	cut_id (int: 0,..8): cut index.
        """  
        b, d = super().show(inputdir, step, cut_id)
        title = 'PD0' + ",  step = " + str(step) + ", id = " + str(cut_id)
        _show_pd(b, d, title)


class PD1(BasicPDMetric):
    """
    Class describing metric PD of rank 1.
    """ 
    def __init__(self, vectorizer, exe_path, n_threads = 1, show_time = False):
        """
        **Input:**
        
        	vectorizer (SimpleBinningVectorizer, PersistenceImageVectorizer, LandscapeVectorizer or SilhouetteVectorizer object): vectorizer to be used for PD metric.
        	
        	show_time (bool): flag to monitor time cost for large images.        
        """
        super().__init__(vectorizer, exe_path, n_threads, show_time)
        self.metric_type = 'v'

    def generate(self, cut, cut_name, outputdir, gendatadir = None):
        """
        Generates the PD of rank 1 for a specific subcube.
        
        **Input:**
        
        	cut (numpy.ndarray): subcube;
        	
        	cut_name (str): name of subcube;
        	
        	outputdir (str): output folder.
        """
        return super().generate(cut, cut_name, outputdir)

    def show(self, inputdir, step, cut_id):
        """
        Vizualize the PD of rank 0 for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated metric data for subcubes;
        	 
        	cut_size (int): size of subcube;
        	
        	cut_id (int: 0,..8): cut index.
        """  
        b, d = super().show(inputdir, step, cut_id)
        title = 'PD1' + ",  step = " + str(step) + ", id = " + str(cut_id)
        _show_pd(b, d, title)

class PD2(BasicPDMetric):
    """
    Class describing metric PD of rank 2.
    """ 
    def __init__(self, vectorizer, exe_path, n_threads = 1, show_time = False):
        """
        **Input:**
        
        	vectorizer (SimpleBinningVectorizer, PersistenceImageVectorizer, LandscapeVectorizer or SilhouetteVectorizer object): vectorizer to be used for PD metric.
        	
        	show_time (bool): flag to monitor time cost for large images.        
        """
        super().__init__(vectorizer, exe_path, n_threads, show_time)
        self.metric_type = 'v'

    def generate(self, cut, cut_name, outputdir, gendatadir = None):
        """
        Generates the PD of rank 2 for a specific subcube.
        
        **Input:**
        
        	cut (numpy.ndarray): subcube;
        	
        	cut_name (str): name of subcube;
        	
        	outputdir (str): output folder.
        """
        return super().generate(cut, cut_name, outputdir)

    def show(self, inputdir, step, cut_id):
        """
        Vizualize the PD of rank 0 for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated metric data for subcubes;
        	 
        	cut_size (int): size of subcube;
        	
        	cut_id (int: 0,..8): cut index.
        """  
        b, d = super().show(inputdir, step, cut_id)
        title = 'PD2' + ",  step = " + str(step) + ", id = " + str(cut_id)
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
