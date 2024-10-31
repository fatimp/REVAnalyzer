# -*- coding: utf-8 -*-
"""
Function for image comparison with vector metrics.
"""

def _delta(a, b):
    if (a+b != 0):
        return 2*abs((a-b)/((a+b)))
    else:
        return 0


def get_sREV_size(sigmas_n, threshold):
    """
    sREV size calculation (can be applied both for scalar and vector metrics).
    
    **Input:**
         
    	sigmas_n (dict, int[float]): dictionary, in which a key is a subcube linear size, and a value is a normailzed std for this subcube;
    
    	threshold (float, <1): threshold to estimate sREV size.
    
    **Output:**
    
    	sREV size (int): sREV size.
    """
    sigmas_n = {key: val for key, val in sigmas_n.items() if val != 0.0}
    sizes = list(sigmas_n.keys())
    sizes.sort(reverse=True)
    for i, l in enumerate(sizes):
        if sigmas_n[l] > threshold:
            if i == 0:
                return None
            else:
                return sizes[i-1]
    return sizes[-1]


def get_dREV_size_1_scalar(values, threshold):
    """
    dREV size calculation for scalar metric using formula (dREV_size_1). See the documentation.
    
    **Input:**
    
    	values (dict, int[float]): dictionary, in which a key is a subcube linear size, and a value is a difference of metric values this and neighbour subcuces;
      
    	threshold (float, <1): threshold to estimate sREV size.
    
    **Output:**
    
    	dREV size (int): dREV size.
    """
    sizes = list(values.keys())
    sizes.sort(reverse=True)
    for i in range(len(sizes)-1):
        if _delta(values[sizes[i]], values[sizes[i+1]]) > threshold:
            if i == 0:
                return None
            else:
                return sizes[i]
    return sizes[-1]


def get_dREV_size_1_scalar_dimensional(values, threshold):
    """
    dREV size calculation for scalar metric defined i 'x', 'y' an 'z' directions using formula (dREV_size_1).
    Returns maximal sREV size over all the directions.
    
    **Input:**
    
    	values (dict, int[list(dtype=float)]): dictionary, in which a key is a subcube linear size, and a value are the differences of metric values for this and neighbour subcuces computed in all directions;
    	  
    	threshold (float, <1): threshold to estimate sREV size.
    
    **Output:**
    
    	dREV size (int): dREV size.
    """
    sizes = list(values.keys())
    sizes.sort(reverse=True)
    result = []
    for k in range(3):
        label = 0
        for i in range(len(sizes)-1):
            if _delta(values[sizes[i]][k], values[sizes[i+1]][k]) > threshold:
                if i == 0:
                    return None
                else:
                    result.append(sizes[i])
                    label = 1
        if (label == 0):
            result.append(sizes[-1])
    return max(result)


def get_dREV_size_2_scalar(values, threshold):
    """
    dREV size calculation for scalar metric using formula (dREV_size_2). See the documentation.
    
    **Input:**
    
    	values (dict, int[float]): dictionary, in which a key is a subcube linear size, and a value is a difference of metric values for this and neighbour subcuces.;
     
    	threshold (float, <1): threshold to estimate dREV size.
    
    **Output:**
    
    	dREV size (int): dREV size.
    """
    sizes = list(values.keys())
    sizes.sort(reverse=True)
    value0 = values[sizes[0]]
    for i in range(1, len(sizes)):
        if _delta(values[sizes[i]], value0) > threshold:
            if i == 1:
                return None
            else:
                return sizes[i-1]
    return sizes[-1]


def get_dREV_size_2_scalar_dimensional(values, threshold):
    """
    dREV size calculation for scalar metric defined i 'x', 'y' an 'z' directions using formula (dREV_size_2).
    Returns maximal sREV size over all the directions.
    
    **Input:**
    
    	values (dict, int[list(dtype=float)]): dictionary, in which a key is a subcube linear size, and a value are the differences of metric values for this and neighbour subcuces computed in all directions;
    	  
    	threshold (float, <1): threshold to estimate dREV size.
    
    **Output:**
    
    	dREV size (int): dREV size.
    """
    sizes = list(values.keys())
    sizes.sort(reverse=True)
    result = []
    for k in range(3):
        value0 = values[sizes[0]][k]
        label = 0
        for i in range(len(sizes)-1):
            if _delta(values[sizes[i]][k], value0) > threshold:
                if i == 0:
                    return None
                else:
                    result.append(sizes[i])
                    label = 1
        if label == 0:
            result.append(sizes[-1])
    return max(result)


def get_dREV_size_1_vector(values, threshold):
    """
    dREV size calculation for vector metric. 
    
    **Input:**
    
    	values (dict, int[float]): dictionary, in which a key is a subcube linear size, and a value is a difference distances between vectors describing this and neighbour subcuces;
    	  
    	threshold (float, <1): threshold to estimate dREV size.
    
    **Output:**
    
    	dREV size (int): dREV size.
    """
    sizes = list(values.keys())
    sizes.sort(reverse=True)
    for i in range(len(sizes)):
        if values[sizes[i]] > threshold:
            if i == 0:
                return None
            else:
                return sizes[i-1]
    return sizes[-1]
