# -*- coding: utf-8 -*-
"""Definition of CF-based metrics. For the definition of correlation functions (CF) see the documentation."""

from .basic_metric import BasicMetric
from revanalyzer.vectorizers  import CFVectorizer, HistVectorizer
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import imp
from julia import Main
from julia.api import Julia
jl = Julia(compiled_modules=False)


class BasicCFMetric(BasicMetric):
    """
    Base class of CF-based metrics. (Don't use it directly but derive from it).
    """ 
    def __init__(self, vectorizer, show_time, normalize):
        """
        **Input:**
        
        	vectorizer (CFVectorizer): vectorizer to be used for CF metric;
        	
        	show_time (bool): flag to monitor time cost for large images, default: False;
        	
        	normalize (bool): flag to control normalization of CF. If True, CF are normalized to satisfy the condition CF(0) = 1. See the details in Karsanina et al. (2021). Compressing soil structural information into parameterized correlation functions. European Journal of Soil Science, 72(2), 561-577. Default: True.
        """        
        super().__init__(vectorizer)
        self.show_time = show_time
        if normalize == True:
            self.normalize = str(1)
        else:
            self.normalize = str(0)

    def generate(self, inputdir, cut_name, l, outputdir, method):
        """
        Generates the CF for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated data for subcubes in statoil format;
        	
        	cut_name (str): name of subcube;
        
        	l (int): linear size of subcube;
        	
        	outputdir (str): path to the folder containing generated CF data;
        	
        	method (str): method for generation of cpecific CF. Different in differenent CF-based metrics.
        
        **Output:**
        
        	name of file (str), in which CF is written.
        """          
        start_time = time.time()
        if inputdir is not None:
            filein = os.path.join(inputdir, cut_name)
        else:
            filein = cut_name
        path0 = imp.find_module('revanalyzer')[1]
        pathjl = os.path.join(path0, 'jl', 'corfunction_xyz.jl')
        pathjl = 'include("'+pathjl+'")'
        jl.eval(pathjl)
        Main.data = [filein, method, str(l), self.normalize]
        cf = jl.eval("compute_cf(data)")
        if len(np.shape(cf)) > 1:
            cf0 = np.concatenate(cf)
            for elem in cf0:
                if np.isnan(elem) or np.isinf(elem):
                    cf = np.array(([], [], []))
                    break
            directions = ('_x', '_y', '_z')
            for i, direction in enumerate(directions):
                cut_name_out = cut_name + direction + ".txt"
                fileout = os.path.join(outputdir, cut_name_out)
                np.savetxt(fileout, cf[i])
        else:
            cut_name_out = cut_name + ".txt"
            fileout = os.path.join(outputdir, cut_name_out)
            np.savetxt(fileout, cf)           
        if self.show_time:
            print("cut ", cut_name, ", run time: ")
            print("--- %s seconds ---" % (time.time() - start_time))
        return cut_name + ".txt"

    def show(self, inputdir, name, cut_size, cut_id):
        """
        Vizualize CF for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated metric data for subcubes;
        	
        	name (str): name of binary ('uint8') file representing the image;
        	
        	cut_size (int): size of subcube;
        	
        	cut_id (int: 0,..8): cut index.
        
        **Output:**
        
        	(x, data) - a tuple, in which
        	
        		x (list(dtype = int)): 'x' coordinate values for a plot;
        		
        		data[0] (list(dtype = float)): 'y' coordinate values for a plot, corresponding of CF generated in 'x' direction;
        		
        		data[1] (list(dtype = float)): 'y' coordinate values for a plot, corresponding of CF generated in 'y' direction;
        		
        		data[2] (list(dtype = float)): 'y' coordinate values for a plot, corresponding of CF generated in 'z' direction.
        """        
        data = self.read(inputdir, name, cut_size, cut_id)
        x = np.arange(len(data[0]))
        plt.rcParams.update({'font.size': 16})
        plt.rcParams['figure.dpi'] = 300
        return x, data[0], data[1], data[2]

    def vectorize(self, v1, v2):
        """
        Vectorize the vector metric values for a given pair of subcubes. 
        
        **Input:**
        
        	v1 (list(dtype = float)): data for the first cubcube;
        	
        	v2 (list(dtype = float)): data for the second cubcube;
        
        **Output:**
        
        	Depends on the chosen mode in CFVectorizer.
        
        	If mode = 'all':
        
        		(list(dtype = float), list(dtype = float), float) - a tuple, in which the first two elements are vectorized metric values for a given pair of subcubes, and the last one is the normalized distance between these vectors. 
        
        	If mode = 'max:
        
 			(list(list(dtype = float)), list(list(dtype = float)), list(float)) - a tuple, in which in which the first two elements are vectorized metric values in 'x', 'y' and 'z' directions for a given pair of subcubes, and the last one is a list of normalized distances between these vectors.        
        """
        return self.vectorizer.vectorize(v1, v2)


class C2(BasicCFMetric):
    """
    Class describing metric C2. 
    """ 
    def __init__(self,  vectorizer, show_time=False, normalize=True):
        """
        **Input:**
        
        	vectorizer (CFVectorizer): vectorizer to be used for CF metric;
        	
        	show_time (bool): flag to monitor time cost for large images, default: False;
        	
        	normalize (bool): flag to control normalization of CF. If True, CF are normalized to satisfy the condition CF(0) = 1. See the details in Karsanina et al. (2021). Compressing soil structural information into parameterized correlation functions. European Journal of Soil Science, 72(2), 561-577. Default: True.
        """ 
        if not isinstance(vectorizer, CFVectorizer):
            raise TypeError("Vectorizer should be an object of CFVectorizer class")
        super().__init__(vectorizer, show_time, normalize)
        self.directional = True
        self.metric_type = 'v'

    def generate(self, inputdir, cut_name, l, outputdir):
        """
        Generates the correlation function C2 for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated data for subcubes in statoil format;
        	
        	cut_name (str): name of subcube;
        	
        	l (int): linear size of subcube;
        	
        	outputdir (str): path to the folder containing generated CF data;
        	        
        **Output:**
        
        	name of file (str), in which CF is written.
        """
        return super().generate(inputdir, cut_name, l, outputdir, method='c2')

    def show(self, inputdir, name, cut_size, cut_id):
        """
        Vizualize the correlation function C2 for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated metric data for subcubes;
        	
        	name (str): name of binary ('uint8') file representing the image;
        	
        	cut_size (int): size of subcube;
        	
        	cut_id (int: 0,..8): cut index.
        """
        x, vx, vy, vz = super().show(inputdir, name, cut_size, cut_id)
        fig, ax = plt.subplots(figsize=(10, 8))
        title = self.__class__.__name__ + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        ax.set_title(title)
        ax.plot(x, vx, "r-", label='x')
        ax.plot(x, vy, "b-", label='y')
        ax.plot(x, vz, "g-", label='z')
        ax.legend()
        ax.set_xlabel("voxels")
        ax.set_ylabel("CF value")
        plt.show()


class L2(BasicCFMetric):
    """
    Class describing metric L2. 
    """ 
    def __init__(self,  vectorizer, show_time=False, normalize=True):
        """
        **Input:**
        
        	vectorizer (CFVectorizer): vectorizer to be used for CF metric;
        	
        	show_time (bool): flag to monitor time cost for large images, default: False;
        	
        	normalize (bool): flag to control normalization of CF. If True, CF are normalized to satisfy the condition CF(0) = 1. See the details in Karsanina et al. (2021). Compressing soil structural information into parameterized correlation functions. European Journal of Soil Science, 72(2), 561-577. Default: True.
        """
        if not isinstance(vectorizer, CFVectorizer):
            raise TypeError("Vectorizer should be an object of CFVectorizer class")
        super().__init__(vectorizer, show_time, normalize)
        self.directional = True
        self.metric_type = 'v'

    def generate(self, inputdir, cut_name, l, outputdir):
        """
        Generates the correlation function L2 for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated data for subcubes in statoil format;
        	
        	cut_name (str): name of subcube;
        	
        	l (int): linear size of subcube;
        	
        	outputdir (str): path to the folder containing generated CF data;
        
        **Output:**
        
        	name of file (str), in which CF is written.
        """
        return super().generate(inputdir, cut_name, l, outputdir, method='l2')

    def show(self, inputdir, name, cut_size, cut_id):
        """
        Vizualize the correlation function L2 for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated metric data for subcubes;
        	
        	name (str): name of binary ('uint8') file representing the image;
        	
        	cut_size (int): size of subcube;
        	
        	cut_id (int: 0,..8): cut index.
        """
        x, vx, vy, vz = super().show(inputdir, name, cut_size, cut_id)
        fig, ax = plt.subplots(figsize=(10, 8))
        title = self.__class__.__name__ + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        ax.set_title(title)
        ax.plot(x, vx, "r-", label='x')
        ax.plot(x, vy, "b-", label='y')
        ax.plot(x, vz, "g-", label='z')
        ax.legend()
        ax.set_xlabel("voxels")
        ax.set_ylabel("CF value")
        plt.show()


class S2(BasicCFMetric): 
    """
    Class describing metric S2. 
    """
    def __init__(self,  vectorizer, show_time=False, normalize=True):
        """
        **Input:**
        
        	vectorizer (CFVectorizer): vectorizer to be used for CF metric;
        	
        	show_time (bool): flag to monitor time cost for large images, default: False;
        	
        	normalize (bool): flag to control normalization of CF. If True, CF are normalized to satisfy the condition CF(0) = 1. See the details in Karsanina et al. (2021). Compressing soil structural information into parameterized correlation functions. European Journal of Soil Science, 72(2), 561-577. Default: True.
        """
        if not isinstance(vectorizer, CFVectorizer):
            raise TypeError("Vectorizer should be an object of CFVectorizer class")
        super().__init__(vectorizer, show_time, normalize)
        self.directional = True
        self.metric_type = 'v'

    def generate(self, inputdir, cut_name, l, outputdir):
        """
        Generates the correlation function S2 for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated data for subcubes in statoil format;
        	
        	cut_name (str): name of subcube;
        	
        	l (int): linear size of subcube;
        	
        	outputdir (str): path to the folder containing generated CF data;
        
        **Output:**
        
        	name of file (str), in which CF is written.
        """
        return super().generate(inputdir, cut_name, l, outputdir, method='s2')

    def show(self, inputdir, name, cut_size, cut_id):
        """
        Vizualize the correlation function S2 for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated metric data for subcubes;
        	
        	name (str): name of binary ('uint8') file representing the image;
        	
        	cut_size (int): size of subcube;
        	
        	cut_id (int: 0,..8): cut index.
        """        
        x, vx, vy, vz = super().show(inputdir, name, cut_size, cut_id)
        fig, ax = plt.subplots(figsize=(10, 8))
        title = self.__class__.__name__ + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        ax.set_title(title)
        ax.plot(x, vx, "r-", label='x')
        ax.plot(x, vy, "b-", label='y')
        ax.plot(x, vz, "g-", label='z')
        ax.legend()
        ax.set_xlabel("voxels")
        ax.set_ylabel("CF value")
        plt.show()
        


class SS(BasicCFMetric):
    """
    Class describing metric SS. 
    """ 
    def __init__(self,  vectorizer, show_time=False, normalize=True):
        """
        **Input:**
        
        	vectorizer (CFVectorizer): vectorizer to be used for CF metric;
        	
        	show_time (bool): flag to monitor time cost for large images, default: False;
        	
        	normalize (bool): flag to control normalization of CF. If True, CF are normalized to satisfy the condition CF(0) = 1. See the details in Karsanina et al. (2021). Compressing soil structural information into parameterized correlation functions. European Journal of Soil Science, 72(2), 561-577. Default: True.
        """
        if not isinstance(vectorizer, CFVectorizer):
            raise TypeError("Vectorizer should be an object of CFVectorizer class")
        super().__init__(vectorizer, show_time, normalize)
        self.directional = True
        self.metric_type = 'v'

    def generate(self, inputdir, cut_name, l, outputdir):
        """
        Generates the correlation function SS for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated data for subcubes in statoil format;
        	
        	cut_name (str): name of subcube;
        	
        	l (int): linear size of subcube;
        	
        	outputdir (str): path to the folder containing generated CF data.
        
        **Output:**
        
        	name of file (str), in which CF is written.
        """
        return super().generate(inputdir, cut_name, l, outputdir, method='ss')

    def show(self, inputdir, name, cut_size, cut_id):
        """
        Vizualize the correlation function SS for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated metric data for subcubes;
        	
        	name (str): name of binary ('uint8') file representing the image;
        
        	cut_size (int): size of subcube;
        
        	cut_id (int: 0,..8): cut index.
        """
        x, vx, vy, vz = super().show(inputdir, name, cut_size, cut_id)
        fig, ax = plt.subplots(figsize=(10, 8))
        title = self.__class__.__name__ + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        ax.set_title(title)
        ax.plot(x, vx, "r-", label='x')
        ax.plot(x, vy, "b-", label='y')
        ax.plot(x, vz, "g-", label='z')
        ax.legend()
        ax.set_xlabel("voxels")
        ax.set_ylabel("CF value")
        plt.show()


class SV(BasicCFMetric):
    """
    Class describing metric SV. 
    """ 
    def __init__(self,  vectorizer, show_time=False, normalize=True):
        """
        **Input:**
        
        	vectorizer (CFVectorizer): vectorizer to be used for CF metric;
        	
        	show_time (bool): flag to monitor time cost for large images, default: False;
        	
        	normalize (bool): flag to control normalization of CF. If True, CF are normalized to satisfy the condition CF(0) = 1. See the details in Karsanina et al. (2021). Compressing soil structural information into parameterized correlation functions. European Journal of Soil Science, 72(2), 561-577. Default: True.
        """
        if not isinstance(vectorizer, CFVectorizer):
            raise TypeError("Vectorizer should be an object of CFVectorizer class")
        super().__init__(vectorizer, show_time, normalize)
        self.directional = True
        self.metric_type = 'v'

    def generate(self, inputdir, cut_name, l, outputdir):
        """
        Generates the correlation function SV for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated data for subcubes in statoil format;
        	
        	cut_name (str): name of subcube;
        	
        	l (int): linear size of subcube;
        	
        	outputdir (str): path to the folder containing generated CF data.
        
        **Output:**
        
        	name of file (str), in which CF is written.
        """
        return super().generate(inputdir, cut_name, l, outputdir, method='sv')

    def show(self, inputdir, name, cut_size, cut_id):
        """
        Vizualize the correlation function SV for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated metric data for subcubes;
        	
        	name (str): name of binary ('uint8') file representing the image;
        
        	cut_size (int): size of subcube;
        
        	cut_id (int: 0,..8): cut index.
        """
        x, vx, vy, vz = super().show(inputdir, name, cut_size, cut_id)
        fig, ax = plt.subplots(figsize=(10, 8))
        title = self.__class__.__name__ + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        ax.set_title(title)
        ax.plot(x, vx, "r-", label='x')
        ax.plot(x, vy, "b-", label='y')
        ax.plot(x, vz, "g-", label='z')
        ax.legend()
        ax.set_xlabel("voxels")
        ax.set_ylabel("CF value")
        plt.show()


class ChordLength(BasicCFMetric):
    """
    Class describing metric S2. 
    """
    def __init__(self,  vectorizer, show_time=False, normalize=True):
        """
        **Input:**
        
        	vectorizer (CFVectorizer): vectorizer to be used for CF metric;
        	
        	show_time (bool): flag to monitor time cost for large images, default: False;
        	
        	normalize (bool): flag to control normalization of CF. If True, CF are normalized to satisfy the condition CF(0) = 1. See the details in Karsanina et al. (2021). Compressing soil structural information into parameterized correlation functions. European Journal of Soil Science, 72(2), 561-577. Default: True.
        """
        if not isinstance(vectorizer, HistVectorizer):
            raise TypeError("Vectorizer should be an object of HistVectorizer class")
        super().__init__(vectorizer, show_time, normalize)
        self.directional = False
        self.metric_type = 'v'

    def generate(self, inputdir, cut_name, l, outputdir):
        """
        Generates the correlation function chord-length for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated data for subcubes in statoil format;
        	
        	cut_name (str): name of subcube;
        	
        	l (int): linear size of subcube;
        	
        	outputdir (str): path to the folder containing generated CF data.
        
        **Output:**
        
        	name of file (str), in which CF is written.
        """
        return super().generate(inputdir, cut_name, l, outputdir, method='cl')

    def show(self, inputdir, name, cut_size, cut_id, nbins):
        """
        Vizualize the correlation function chord-length for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated metric data for subcubes;
        	
        	name (str): name of binary ('uint8') file representing the image;
        
        	cut_size (int): size of subcube;
        
        	cut_id (int: 0,..8): cut index,
            
            nbins (int): number of bins in histrogram
        """
        data = self.read(inputdir, name, cut_size, cut_id)
        max_value = max(data)
        range_data = [0, max_value]
        hist, bin_edges = np.histogram(data, bins=nbins, range=range_data, density=True)
        step = max_value/nbins
        x = [i*step for i in range(nbins)]
        plt.rcParams.update({'font.size': 16})
        plt.rcParams['figure.dpi'] = 300
        fig, ax = plt.subplots(figsize=(10, 8))
        title = self.__class__.__name__ + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        ax.set_title(title)
        ax.bar(x, hist, width=0.5, color='r')
        ax.set_xlabel('chord-length')
        ax.set_ylabel('density')
        plt.show()


class PoreSize(BasicCFMetric):
    """
    Class describing metric pore-size. 
    """ 
    def __init__(self,  vectorizer, show_time=False, normalize=True):
        """
        **Input:**
        
        	vectorizer (CFVectorizer): vectorizer to be used for CF metric;
        	
        	show_time (bool): flag to monitor time cost for large images, default: False;
        	
        	normalize (bool): flag to control normalization of CF. If True, CF are normalized to satisfy the condition CF(0) = 1. See the details in Karsanina et al. (2021). Compressing soil structural information into parameterized correlation functions. European Journal of Soil Science, 72(2), 561-577. Default: True.
        """
        if not isinstance(vectorizer, HistVectorizer):
            raise TypeError("Vectorizer should be an object of HistVectorizer class")
        super().__init__(vectorizer, show_time, normalize)
        self.directional = False
        self.metric_type = 'v'

    def generate(self, inputdir, cut_name, l, outputdir):
        """
        Generates the correlation function pore-size for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated data for subcubes in statoil format;
        	
        	cut_name (str): name of subcube;
        	
        	l (int): linear size of subcube;
        	
        	outputdir (str): path to the folder containing generated CF data.
        
        **Output:**
        
        	name of file (str), in which CF is written.
        """
        return super().generate(inputdir, cut_name, l, outputdir, method='ps')

    def show(self, inputdir, name, cut_size, cut_id, nbins):
        """
        Vizualize the correlation function chord-length for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated metric data for subcubes;
        	
        	name (str): name of binary ('uint8') file representing the image;
        
        	cut_size (int): size of subcube;
        
        	cut_id (int: 0,..8): cut index,
            
            nbins (int): number of bins in histrogram
        """
        data = self.read(inputdir, name, cut_size, cut_id)
        max_value = max(data)
        range_data = [0, max_value]
        hist, bin_edges = np.histogram(data, bins=nbins, range=range_data, density=True)
        step = max_value/nbins
        x = [i*step for i in range(nbins)]
        plt.rcParams.update({'font.size': 16})
        plt.rcParams['figure.dpi'] = 300
        fig, ax = plt.subplots(figsize=(10, 8))
        title = self.__class__.__name__ + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        ax.set_title(title)
        ax.bar(x, hist, width=0.5, color='r')
        ax.set_xlabel('pore-size')
        ax.set_ylabel('density')
        plt.show()


class CrossCorrelation(BasicCFMetric):
    """
    Class describing metric cross-correlation. 
    """ 
    def __init__(self,  vectorizer, show_time=False, normalize=True):
        """
        **Input:**
        
        	vectorizer (CFVectorizer): vectorizer to be used for CF metric;
        	
        	show_time (bool): flag to monitor time cost for large images, default: False;
        	
        	normalize (bool): flag to control normalization of CF. If True, CF are normalized to satisfy the condition CF(0) = 1. See the details in Karsanina et al. (2021). Compressing soil structural information into parameterized correlation functions. European Journal of Soil Science, 72(2), 561-577. Default: True.
        """
        if not isinstance(vectorizer, CFVectorizer):
            raise TypeError("Vectorizer should be an object of CFVectorizer class")
        super().__init__(vectorizer, show_time, normalize)
        self.metric_type = 'v'

    def generate(self, inputdir, cut_name, l, outputdir):
        """
        Generates the correlation function cross-correlation for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated data for subcubes in statoil format;
        	
        	cut_name (str): name of subcube;
        	
        	l (int): linear size of subcube;
        	
        	outputdir (str): path to the folder containing generated CF data.
        
        **Output:**
        
        	name of file (str), in which CF is written.
        """
        return super().generate(inputdir, cut_name, l, outputdir, method='cc')

    def show(self, inputdir, name, cut_size, cut_id):
        """
        Vizualize the correlation function cross-correlation for a specific subcube.
        
        **Input:**
        
        	inputdir (str): path to the folder containing generated metric data for subcubes;
        	
        	name (str): name of binary ('uint8') file representing the image;
        
        	cut_size (int): size of subcube;
        
        	cut_id (int: 0,..8): cut index.
        """
        x, vx, vy, vz = super().show(inputdir, name, cut_size, cut_id)
        fig, ax = plt.subplots(figsize=(10, 8))
        title = self.__class__.__name__ + ", " + name + \
            ", cut size = " + str(cut_size) + ", id = " + str(cut_id)
        ax.set_title(title)
        ax.plot(x, vx, "r-", label='x')
        ax.plot(x, vy, "b-", label='y')
        ax.plot(x, vz, "g-", label='z')
        ax.legend()
        ax.set_xlabel("voxels")
        ax.set_ylabel("CF value")
        plt.show()
