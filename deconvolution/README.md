# Deconvolution
 Deconvolution using RL method, GPU installation

This repository uses the RL method, GPU accelerated, for deconvoluting fluorescent microscopy images - Richardson-Lucy-Deconvolution_GPU.py.
It takes as an input:
a subdirectory folder - assuming that the images are organised by well
PSF file - experimental or generated 
channel number - which imaging channel
and number of iterations (which has a default value of 50)

The point spread function - PSF - images have to be provided. These images can be generated - for example in FIJI - or measured.
They depend on wavelength and are unique to each objective and microscope.

The repository also includes the wrapper script - deconvolution-jobarrays.sh - and an additional python script - List_of_subdir.py - 
to write a text file to be fed into the wrapper script which runs as a job array on the farm.

