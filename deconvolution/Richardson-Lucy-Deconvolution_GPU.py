# Richardson-Lucy-Deconvolution_GPU
# Date: 5 June 2024
# Author: Anke Husmann ah38@sanger.ac.uk OpenTargets
# Version: 3
# Description: adoptation of a Jupyter Notebook by BiaPol, see below
# -------

# # Richardson-Lucy-Deconvolution on OpenCL-compatible GPUs
# (https://en.wikipedia.org/wiki/Richardson%E2%80%93Lucy_deconvolution) is a common 
# algorithm for image deconvolution in microscopy. 
# This GPU-accelerated version is implemented in the napari-plugin 
# (https://github.com/rosalindfranklininstitute/RedLionfish). 
 
# https://biapol.github.io/PoL-BioImage-Analysis-TS-GPU-Accelerated-Image-Analysis/10_Clesperanto/readme.html
 
# This script uses the following environment
# conda create -n  deconvolution python=3.9
# conda install -c conda-forge pyclesperanto-prototype
# conda activate deconvolution
# pip install pyclesperanto


import os
from skimage.io import imread
from skimage.io import imsave
import RedLionfishDeconv as rl
import argparse

# arguments to be handed:
# subdirectory folder, PSF file, channel number, and number of iterations (which has a default value)

parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", type=str, help='input subdirectory')
parser.add_argument("--PSF_file", type=str, help='PSF file')
parser.add_argument("--channel", type=str, help='channel number')
parser.add_argument("--num_iter", type=int, default=50, help='number of iterations (default = 50)')

args = parser.parse_args()

# So far we have been using theoretical PSF images (created with ImageJ). The plan is to move onto experimental 
# images.

psf = imread(args.PSF_file)
iterations = args.num_iter
channel = "_ch"+args.channel+"."

# create an output folder for the deconvolved images with the same well name but in a subdirectory called 'deconv'

inputdirectory = args.input_dir
dirs_base_input, well_name_input = os.path.split(inputdirectory)
deconv_foldername = dirs_base_input + "/deconv/" + well_name_input
os.makedirs(deconv_foldername, exist_ok = True)

# create a list of all images in folder

list_filenames = []

for dirpath, dirnames, filenames in os.walk(args.input_dir):
    for file in filenames:
        if ((channel in file) and (".tif" in file)):
            image_path = os.path.join(dirpath, file)
            list_filenames.append(image_path)

# for image_file in list_filenames: 
            image = imread(image_path)

# We can now deconvolve the image using RedLionFish's Richardson-Lucy-Deconvolution algorithm. 
# We should specify that the algorithm shall be executed on the `gpu`.

            deconvolved = rl.doRLDeconvolutionFromNpArrays(image, 
                                                            psf, 
                                                            niter=iterations, 
                                                            method='gpu', 
                                                            resAsUint8=False )
            
            

            imsave (deconv_foldername + "/decon_" + file, deconvolved)

# end of for loop of images in subdirectory / well