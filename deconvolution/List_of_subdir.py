# Title: List_of_subdir
# Date: 5 June 2024 
# Author: Anke Husmann ah38@sanger.ac.uk OpenTargets
# Version: 1
# Description: writes list of subdirectories + path into a text file
# -------
# create list of directories to be run through deconvolution
# it assumes that the images are organised into subdirectories named by well name
# it creates a text file: subdir_list.txt for the job array to schedule parallel jobs

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", type=str, help='input directory of experiment')
parser.add_argument("--list_wells", type=list, help='list of wells (default = ["all"])', default = ["all"])

args = parser.parse_args()

directory = args.input_dir

list_of_wells = args.list_wells

if list_of_wells == ["all"]:
     list_of_wells = []
     list_of_columns = ["02", "03", "04", "05", "06", "07", "08", "09", "10", "11"]
     list_of_rows = ["B", "C", "D", "E", "F", "G"]
     for r in list_of_rows:
          for c in list_of_columns:
               list_of_wells.append(r+c)


# os.walk yields a 3-typle(dirpath, dirnames, filenames)
# to get the full path and file names use : os.path.join(dirpath, name)

for dirpath, dirnames, filenames in os.walk(directory):

    for dir in dirnames:
        for wells in list_of_wells:
            if (wells in dir):
                    with open ("subdir_list.txt", mode = 'a') as f:
                        f.write(os.path.join(dirpath, dir) + "\n")

