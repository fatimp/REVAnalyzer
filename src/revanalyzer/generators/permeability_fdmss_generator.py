# -*- coding: utf-8 -*-
"""Module for the computation of permeability using FDMSS solver."""

import os
import subprocess
import shutil
import numpy as np
import time
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
from .utils import _read_array

fdmss_data = "fdmss_data"


def generate_permeability_fdmss(image, size, cut_step, sREV_max_size, exe_path_fdmss, directions, n_threads=1, resolution=1., datadir='data', outputdir='output', show_time=False):
    """
    Running FDMSS for all the selected subcubes.
    
    **Input:**

     	image (str): name of binary ('uint8') file representing the image;
     
     	size (int): image linear size. Note, that only cubical images can be analyzed;
     	 
     	cut_step (int): increment step of subcube size;
     	
     	sREV_max_size (int): maximal subcube size for which sREV analysis is performed;
     	
     	exe_path_fdmss (str): path to fdmss exe file;
     	
     	directions (str): 'x', 'y', 'z' or 'all'. If label of this parameter is 'all', permeability values are generated for all 3 possible flow directions;
     	
     	n_threads (int): number of CPU cores used by FDMSS, default: 1;
     	
     	resolution (float): resolution of studied sample (micrometers), default: 1;
     	
     	datadir (str): path to the folder containing image, default: 'data';
     	
     	outputdir (str): path to the output folder containing generated data, default: 'output';
     	
     	show_time (bool): Added to monitor time cost for large images,  default: False. 
    """
    if not (directions == 'x' or directions == 'y' or directions == 'z' or directions == 'all'):
        raise ValueError("Direction should be 'x', 'y', 'z' or 'all'")
    if directions == 'all':
        directions_list = ['x', 'y', 'z']
    else:
        directions_list = [directions]
    outputdir_cuts_values = os.path.join(
        outputdir, image, 'Permeability', 'cuts_values')
    os.makedirs(outputdir_cuts_values, exist_ok=True)
    os.makedirs(fdmss_data, exist_ok=True)
    for direction in directions_list:
        start_time = time.time()
        config_path = os.path.join(fdmss_data, 'config.xml')
        output_path = os.path.join(fdmss_data, 'output.xml')
        _make_fdmss_config(config_path, direction, resolution, n_threads)
        pressure = os.path.join(fdmss_data, 'pressure')
        vel = os.path.join(fdmss_data, 'vel')
        config_path = '--config='+config_path
        image_path = '--image='+os.path.join(datadir, image)
        output_path = '--summary='+output_path
        if direction == 'x':
            vel_path = '--velx='+vel
        if direction == 'y':
            vel_path = '--vely='+vel
        if direction == 'z':
            vel_path = '--velz='+vel
        pressure_path = '--pressure='+pressure
        code = subprocess.call([exe_path_fdmss, config_path, image_path, output_path,
                               vel_path, pressure_path])
        if (code != 0):
            raise RuntimeError("Error in FDMSS run occured!")
        if show_time:
            print("FMDSS run time ")
            print("--- %s seconds ---" % (time.time() - start_time))
        perm_name = os.path.join(
            outputdir_cuts_values, image)
        if directions == 'all':
            perm_name = perm_name + "_" + direction
        image_ar = _read_array(os.path.join(
            datadir, image), size, 'uint8').astype(bool)
        pressure_ar = _read_array(pressure, size, 'float32')
        vel_ar = _read_array(vel, size, 'float32')
        porosity = _get_porosity(image_ar)
        perm = _get_permeability(
            image_ar, porosity, pressure_ar, vel_ar, direction)
        with open(perm_name+".txt", "w") as f:
            f.write(str(perm))
        n_steps = int(np.ceil(size/cut_step))
        cut_sizes = [cut_step*(i+1) for i in range(n_steps-1)]
        for l in cut_sizes:
            start_time = time.time()
            cut_name = "cut0_" + str(l) + "_" + image
            perm_name = os.path.join(outputdir_cuts_values, cut_name)
            if directions == 'all':
                perm_name = perm_name + "_" + direction
            perm = _get_permeability(_cut0(image_ar, size, l), _get_porosity(
                _cut0(image_ar, size, l)), _cut0(pressure_ar, size, l), _cut0(vel_ar, size, l), direction)
            if perm < 0:
                perm = 0
            with open(perm_name + ".txt", "w") as f:
                f.write(str(perm))
            if (l <= sREV_max_size):
                perms = []
                perms.append(_get_permeability(_cut1(image_ar, size, l), _get_porosity(
                    _cut1(image_ar, size, l)), _cut1(pressure_ar, size, l), _cut1(vel_ar, size, l), direction))
                perms.append(_get_permeability(_cut2(image_ar, size, l), _get_porosity(
                    _cut2(image_ar, size, l)), _cut2(pressure_ar, size, l), _cut2(vel_ar, size, l), direction))
                perms.append(_get_permeability(_cut3(image_ar, size, l), _get_porosity(
                    _cut3(image_ar, size, l)), _cut3(pressure_ar, size, l), _cut3(vel_ar, size, l), direction))
                perms.append(_get_permeability(_cut4(image_ar, size, l), _get_porosity(
                    _cut4(image_ar, size, l)), _cut4(pressure_ar, size, l), _cut4(vel_ar, size, l), direction))
                perms.append(_get_permeability(_cut5(image_ar, size, l), _get_porosity(
                    _cut5(image_ar, size, l)), _cut5(pressure_ar, size, l), _cut5(vel_ar, size, l), direction))
                perms.append(_get_permeability(_cut6(image_ar, size, l), _get_porosity(
                    _cut6(image_ar, size, l)), _cut6(pressure_ar, size, l), _cut6(vel_ar, size, l), direction))
                perms.append(_get_permeability(_cut7(image_ar, size, l), _get_porosity(
                    _cut7(image_ar, size, l)), _cut7(pressure_ar, size, l), _cut7(vel_ar, size, l), direction))
                perms.append(_get_permeability(_cut8(image_ar, size, l), _get_porosity(
                    _cut8(image_ar, size, l)), _cut8(pressure_ar, size, l), _cut8(vel_ar, size, l), direction))
                for i in range(1, 9):
                    cut_name = "cut" + str(i) + "_" + str(l) + "_" + image
                    perm_name = os.path.join(outputdir_cuts_values, cut_name)
                    if directions == 'all':
                        perm_name = perm_name + "_" + direction
                    with open(perm_name + ".txt", "w") as f:
                        f.write(str(perms[i-1]))
            if show_time:
                print("Extraction time for cuts with l = ", l)
                print("--- %s seconds ---" % (time.time() - start_time))
    shutil.rmtree(fdmss_data)


def _make_fdmss_config(fileout, direction, resolution=1, n_threads=1):
    xml_data = """
<OverdozenPermsolverParams>
  <Parameter name="Resolution" datatype="float">
    <ParameterValue>1.0</ParameterValue>
  </Parameter>
  <Parameter name="TimeStep" datatype="float">
    <ParameterValue>0.0003</ParameterValue>
  </Parameter>
  <Parameter name="IterationsPerStep" datatype="unsigned int">
    <ParameterValue>100</ParameterValue>
  </Parameter>
  <Parameter name="MaximumStepsCount" datatype="unsigned int">
    <ParameterValue>140</ParameterValue>
  </Parameter>
  <Parameter name="InitialVelocityValue" datatype="float">
    <ParameterValue>0.001</ParameterValue>
  </Parameter>
  <Parameter name="Accuracy" datatype="float">
    <ParameterValue>0.01</ParameterValue>
  </Parameter>
  <Parameter name="BoundaryCondition" datatype="int">
    <ParameterValue>1</ParameterValue>
  </Parameter>
  <Parameter name="TerminationCondition" datatype="int">
    <ParameterValue>2</ParameterValue>
  </Parameter>
  <Parameter name="AccuracyOrder" datatype="int">
    <ParameterValue>0</ParameterValue>
  </Parameter>
  <Parameter name="ErrorSmoothingLength" datatype="unsigned int">
    <ParameterValue>10</ParameterValue>
  </Parameter>
  <Parameter name="ThreadsNumber" datatype="unsigned int">
    <ParameterValue>1</ParameterValue>
  </Parameter>
  <Parameter name="FlowDirectionAxis" datatype="char">
    <ParameterValue>AXIS</ParameterValue>
  </Parameter>
  <Parameter name="WaterLayerWidth" datatype="unsigned int">
    <ParameterValue>0</ParameterValue>
  </Parameter>
</OverdozenPermsolverParams>
"""
    root = ET.fromstring(xml_data)
    root[0][0].text = str(resolution)
    root[10][0].text = str(n_threads)
    root[11][0].text = direction
    tree = ElementTree(root)
    tree.write(fileout)


def _pressure_diff(image, pressure, axis):
    inv = ~image
    pressure = np.where(inv, pressure, 0)
    if axis == 'x':
        p_start = np.sum(pressure[:, :, 1])/np.sum(inv[:, :, 1])
        p_end = np.sum(pressure[:, :, -1])/np.sum(inv[:, :, -1])
    if axis == 'y':
        p_start = np.sum(pressure[:, 1, :])/np.sum(inv[:, 1, :])
        p_end = np.sum(pressure[:, -1, :])/np.sum(inv[:, -1, :])
    if axis == 'z':
        p_start = np.sum(pressure[1, :, :])/np.sum(inv[1, :, :])
        p_end = np.sum(pressure[-1, :, :])/np.sum(inv[-1, :, :])
    return (p_start - p_end)/image.shape[0]


def _get_permeability(image, porosity, pressure, vel, direction):
    dim = image.shape[0]
    pores = dim**3 - np.count_nonzero(image)
    p = _pressure_diff(image, pressure, direction)
    v = np.sum(vel)/pores
    return 100*v/p*porosity/0.986*1000


def _get_porosity(image):
    dim = image.shape[0]
    pores = dim**3 - np.count_nonzero(image)
    return pores/(dim**3)


def _cut0(A, L, l):
    return A[int((L-l)/2):int((L+l)/2), int((L-l)/2):int((L+l)/2), int((L-l)/2):int((L+l)/2)]


def _cut1(A, L, l):
    return A[:l, :l, :l]


def _cut2(A, L, l):
    return A[:l, :l, L-l:]


def _cut3(A, L, l):
    return A[:l, L-l:, :l]


def _cut4(A, L, l):
    return A[L-l:, :l, :l]


def _cut5(A, L, l):
    return A[L-l:, L-l:, L-l:]


def _cut6(A, L, l):
    return A[:l, L-l:, L-l:]


def _cut7(A, L, l):
    return A[L-l:, :l, L-l:]


def _cut8(A, L, l):
    return A[L-l:, L-l:, :l]
