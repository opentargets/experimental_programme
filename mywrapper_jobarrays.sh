# Title: mywrapper_jobarrays.sh
# Date: 21 March 2023 
# Author: Anke Husmann ah38@sanger.ac.uk
# Version: 1
# Description: runs a job array by reading input directories from file and hands them to python script


#!/bin/bash
# running in an array, using $LSB_JOBINDEX
# should really have files and numbers as user input into wrapper script

# bsub -J "myjob[1-2]" -o array%I_%J.log /nfs/users/nfs_a/ah38/projects/jobarrays/mywrapper_jobarrays.sh
# bsub -J "myjob[1-2]" -q gpu-normal -n 1 -M 4000 -R "select[mem>4000] rusage[mem=4000]" -gpu "mode=shared:num=1:gmem=4000" -o array%I_%J.log /nfs/users/nfs_a/ah38/projects/jobarrays/mywrapper_jobarrays.sh
# needs path to files
# for python to be activated needs to be running miniconda environment

# This needs to run before running this script: conda activate deconvolution

MYINPUT=$(sed -n "${LSB_JOBINDEX}p" /nfs/users/nfs_a/ah38/projects/jobarrays/subdir_list_all.txt)

# need to make a directory for the deconvolved images
# mkdir "${MYINPUT}""decon/"

python  /nfs/users/nfs_a/ah38/projects/jobarrays/RL_deconvolution.py --input_dir ${MYINPUT} --PSF_file /lustre/scratch126/opentargets/opentargets/OTAR2076/working/project_tests_AH/PSF_641_IR.tif --channel 4 --num_iter 50 