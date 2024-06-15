# -*- coding: utf-8 -*-
""" Utilities for metric generators."""

import numpy as np
import os


def make_cuts(datadir, image, outputdir, L, l, total=True):
    """
    Making subcube cuts from a given image. 
    
    **Input:**
     
     	datadir (str): path to the folder containing image;
     
     	image (str): name of binary ('uint8') file representing the image;
     
     	L (int): image linear size. Note, that only cubical images can be analyzed;
     	 
     	l (int): linear size of cut subcube;
     	
     	outputdir (str): path to the output folder in which cuts are located;
     	
     	total (bool): If 'True' 9 cuts are generated, 8 - from the corners of initial image, and 1 - from its centre. If 'False', only the centre cut is generated.
     	
    **Output:**
    
    	names of generated subcubes (list(dtype=str)).
    """    
    cut_names = []
    A = _read_array(os.path.join(datadir, image), L, 'uint8')
    A0 = A[int((L-l)/2):int((L+l)/2), int((L-l)/2)
               :int((L+l)/2), int((L-l)/2):int((L+l)/2)]
    cut_name0 = "cut0_" + str(l) + "_" + image
    cut_names.append(cut_name0)
    fout0 = os.path.join(outputdir, cut_name0)
    A0.astype('uint8').tofile(fout0)
    if (total):
        A1 = A[:l, :l, :l]
        A2 = A[:l, :l, L-l:]
        A3 = A[:l, L-l:, :l]
        A4 = A[L-l:, :l, :l]
        A5 = A[L-l:, L-l:, L-l:]
        A6 = A[:l, L-l:, L-l:]
        A7 = A[L-l:, :l, L-l:]
        A8 = A[L-l:, L-l:, :l]
        A = [A1, A2, A3, A4, A5, A6, A7, A8]
        for i in range(1, 9):
            cut_name = "cut" + str(i) + "_" + str(l) + "_" + image
            cut_names.append(cut_name)
            fout = os.path.join(outputdir, cut_name)
            A[i-1].astype('uint8').tofile(fout)
        return cut_names
    else:
        return cut_name0


def _read_array(image, dim, dtype):
    v = np.fromfile(image, dtype=dtype, sep="")
    return v.reshape([dim, dim, dim])


def _write_array(A, fileout):
    A.astype('uint8').tofile(fileout)


def _subcube_ids(L, cut_step, sREV_max_size):
    n_steps = int(np.ceil(L/cut_step))
    ids = [(0,0)]
    cut_sizes = [cut_step*(i+1) for i in range(n_steps-1)]
    for l in cut_sizes:
        if (l <= sREV_max_size):
            for idx in range(9):
                ids.append((l, idx))
        else:
            ids.append((l, 0))
    return ids


def make_cut(A, L, l, idx):
    """
    Making subcube cut for a given 3D array. 
    
    **Input:**
     
     	A(np.array): initial 3D array;
     
     	L (int): image linear size. Note, that only cubical images can be analyzed;
     	 
     	l (int): linear size of cut subcube;
     	
     	idx (int): index of subcube (0,1,..8). idx = 0 corresponds to the center subcube, idx = 1,..8 corrspond to the corner subcubes.
    **Output:**
    
    	np.array() generated subcubes (list(dtype=str)).
    """
    if not len(A.shape) == 3:
        raise ValueError("Initial array should have 3 dimensions.")
    if idx < 0 or idx > 8:
        raise ValueError("Index value should be from the set (0,1,..8).")
    if idx == 0:
        return A[int((L-l)/2):int((L+l)/2), int((L-l)/2):int((L+l)/2), int((L-l)/2):int((L+l)/2)]
    if idx == 1:
        return A[:l, :l, :l]
    if idx == 2:
        return A[:l, :l, L-l:]
    if idx == 3:
        return A[:l, L-l:, :l]
    if idx == 4:
        return A[L-l:, :l, :l]
    if idx == 5:
        return A[L-l:, L-l:, L-l:]
    if idx == 6:
        return A[:l, L-l:, L-l:]
    if idx == 7:
        return A[L-l:, :l, L-l:]
    if idx == 8:
        return A[L-l:, L-l:, :l]
