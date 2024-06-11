# Title: mywrapper_jobarrays.sh
# Date: 05 June 2024 
# Author: Anke Husmann ah38@sanger.ac.uk OpenTargets
# Version: 2
# Description: runs a bsub job array by reading input directories from file and hands them to python script

# GPU normal and 4GB memory worked for images of 1 field of view. Larger images need more memory

# running in an array, using $LSB_JOBINDEX

# bsub -J "myjob[1-48]%8" -q gpu-normal -n 1 -M 4000 -R "select[mem>4000] rusage[mem=4000]" -gpu "mode=shared:num=1:gmem=4000" -o array%I_%J.log /path/to/mywrapper_jobarrays.sh

# conda activate /software/hgi/envs/conda/team211/ah38/deconvolution

MYINPUT=$(sed -n "${LSB_JOBINDEX}p" /path/to/subdir_list.txt)

# channel 4 is MC, 641nm wavelength
# channel 1 is shared channel for CD25 and Ki67, 488 nm wavelength

python  /path/to/RL_deconvolution.py --input_dir ${MYINPUT} --PSF_file /path/to/PSF_488_500.tif --channel 1 --num_iter 50 