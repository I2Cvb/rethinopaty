#title           :flattening.py
#description     :This will create a header for a python script.
#author          :Guillaume Lemaitre
#date            :2015/06/07
#version         :0.1
#notes           :
#python_version  :2.7.6  
#==============================================================================

# Import the needed libraries
# Numpy libreary
import numpy as np
# OS library
import os
from os.path import join
# SYS library
import sys

from protoclass.tool.dicom_manip import OpenVolumeNumpy
from protoclass.preprocessing.flattening import Flatten3D

# Get the path to file
filename_data = sys.argv[1]
print 'Opening the following file: {}'.format(filename_data)

# Open the data
if not (filename_data.endswith('.npz')):
    raise ValueError('flattening: The image in input is not a npz image.')
else:
    # Read the volume using the raw image
    name_var_extract = 'vol_denoised'
    vol = OpenVolumeNumpy(filename_data, name_var_extract=name_var_extract)
    
    # Apply the filtering using 8 cores
    num_cores = 8
    vol_flatten = Flatten3D(vol, num_cores=num_cores)

    # Directory where to save the data
    storing_folder = sys.argv[2]

    # Create the folder if it is not existing
    if not (os.path.exists(storing_folder)):
        os.makedirs(storing_folder)

    # Get only the filename without path directory of the input file
    _, filename_patient = os.path.split(filename_data) 
    
    # Get the input filename without .img
    filename_root, _ = os.path.splitext(filename_patient)

    # Get the filename for numpy and matlab
    filename_matlab = os.path.join(storing_folder, filename_root + '_flatten' + '.mat')
    filename_numpy = os.path.join(storing_folder, filename_root + '_flatten' + '.npz')

    # Save the matfile
    from scipy.io import savemat
    savemat(filename_matlab, {'vol_flatten': vol_flatten})

    # Save the numpy array
    np.savez(filename_numpy, vol_flatten=vol_flatten)
