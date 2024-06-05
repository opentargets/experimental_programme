# Title: mywrapper_jobarrays_2.sh
# Date: 12 April 2024 
# Author: Anke Husmann ah38@sanger.ac.uk
# Version: 2
# Description: runs a job array by reading input directories from file and hands them to python script


#!/bin/bash
# running in an array, using $LSB_JOBINDEX
# should really have files and numbers as user input into wrapper script

# bsub -J "myjob[1-2]" -o array%I_%J.log /nfs/users/nfs_a/ah38/projects/jobarrays/mywrapper_jobarrays_2.sh
# bsub -J "myjob[1-2]" -q gpu-normal -n 1 -M 4000 -R "select[mem>4000] rusage[mem=4000]" -gpu "mode=shared:num=1:gmem=4000" -o array%I_%J.log /nfs/users/nfs_a/ah38/projects/jobarrays/mywrapper_jobarrays_2.sh
# bsub -J "myjob[1-48]%8" -q gpu-normal -n 1 -M 4000 -R "select[mem>4000] rusage[mem=4000]" -gpu "mode=shared:num=1:gmem=4000" -o array%I_%J.log /nfs/users/nfs_a/ah38/projects/jobarrays/mywrapper_jobarrays_2.sh
# needs path to files
# for python to be activated needs to be running miniconda environment

# This needs to run before running this script: conda activate deconvolution

MYINPUT=$(sed -n "${LSB_JOBINDEX}p" /nfs/users/nfs_a/ah38/projects/jobarrays/subdir_list_all.txt)

# channel 4 is MC, 641nm wavelength
# channel 1 is shared channel for CD25 and Ki67, 488 nm wavelength

python  /nfs/users/nfs_a/ah38/projects/jobarrays/RL_deconvolution.py --input_dir ${MYINPUT} --PSF_file /lustre/scratch126/opentargets/opentargets/OTAR2076/working/project_tests_AH/PSF_488_500.tif --channel 1 --num_iter 50 