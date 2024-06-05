# Richardson-Lucy-Deconvolution_GPU
# Date: 15 April 2024
# Author: Anke Husmann ah38@sanger.ac.uk
# Version: 3
# Description: adoptation of a Jupyter Notebook by BiaPol, see below
# -------
# needed to fix some problems with looking for files and saving them

# # Richardson-Lucy-Deconvolution on OpenCL-compatible GPUs
# [Richardson-Lucy-Deconvolution](https://en.wikipedia.org/wiki/Richardson%E2%80%93Lucy_deconvolution) is a common and yet basic algorithm for image deconvolution in microscopy. In this notebook we will use a GPU-accelerated version of it that is implemented in the napari-plugin [RedLionFish](https://github.com/rosalindfranklininstitute/RedLionfish). Hence, you can use the same algorithm from the graphical user interface in napari.
# 
# https://biapol.github.io/PoL-BioImage-Analysis-TS-GPU-Accelerated-Image-Analysis/10_Clesperanto/readme.html
# 
# This script uses the following environment:
# conda create --name devbio-napari-env python=3.9 devbio-napari pyqt -c conda-forge (cannot remember whether I used this command?)
# conda create -n  deconvolution python=3.9
# conda install -c conda-forge pyclesperanto-prototype
# conda activate deconvolution
# pip install pyclesperanto
#
# 18/03/2024 ah38: I have adjusted this Jupyter Notebook to use for images on the farm. This is a python script version which makes run times shorter.

import os
from skimage.io import imread
from skimage.io import imsave
from pyclesperanto_prototype import imshow
import RedLionfishDeconv as rl
import matplotlib.pyplot as plt
import numpy as np
import argparse


# We will load an image showing fluorescent intensity along lines. This 3D image was taken with a confocal microscope.
# 
# Note (ah38) I have to make sure that the images are not saved as RGB images but as grey images.
#
# arguments to be handed:
# subdirectory folder, PSF file, channel number, and number of iterations (which has a default value)

parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", type=str, help='input subdirectory')
parser.add_argument("--PSF_file", type=str, help='PSF file')
parser.add_argument("--channel", type=str, help='channel number')
parser.add_argument("--num_iter", type=int, default=50, help='number of iterations (default = 50)')

args = parser.parse_args()
# print(args.file)

# Note (ah38): so far we have been using theoretical PSF images (created with ImageJ). The plan is to move onto experimental images after Easter (April 2024).
# psf = imread('/lustre/scratch126/opentargets/opentargets/OTAR2076/working/project_tests_AH/PSF_641_500.tif')
psf = imread(args.PSF_file)
iterations = args.num_iter
channel = "_ch"+args.channel+"."

# create an output folder for the deconvolved images
inputdirectory = args.input_dir
deconv_foldername = inputdirectory + "/deconv"
os.makedirs(deconv_foldername, exist_ok = True)

image_output_folder = "/lustre/scratch125/humgen/projects/cell_activation_tc/projects/KI67_TEST/2_feature_extraction/output/deconv_testset_mito_3012024/CD25Ki67_ch1"

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
#   imshow(deconvolved)

#   record overall sum of intensities to keep track of errors induced by deconvolution 

            sum_original = np.sum(image)
            sum_deconvolved = np.sum(deconvolved)
            perc_change = (sum_deconvolved-sum_original)/sum_deconvolved
#   print("deconvolved", sum_deconvolved)
#   print("original", sum_original)
    
            deconvolved_max = np.max(deconvolved)
#   scale_factor = 20
#   decovolved_scaled = deconvolved/scale_factor     # Maybe better to use a fixed value, otherwise we get into trouble when segmenting
#   deconvolved_scaled = decovolved_scaled.astype(np.uint16)

# save in file: information on sum_original, sum_deconvolved, perc_change and deconvolved_scaled so that the intensities can be scaled back to the original ratio
# this can potentially cause problems when the original max value is quite small, then the images will be very grainy and the thresholds will vary widely
# I don't think this is a good idea: need to think about this some more

            with open(deconv_foldername + "/info_3.txt", mode = 'a') as f:
                f.write(str(image_path) + ", " + str(sum_original) + ", " + str(sum_deconvolved) + ", " + str(perc_change) + ", " + str(deconvolved_max) + "\n")

            imsave (image_output_folder+ "/decon_" + file, deconvolved)

# end of for loop of images in subdirectory / well