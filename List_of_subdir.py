# Title: List_of_subdir
# Date: 21 March 2023 
# Author: Anke Husmann ah38@sanger.ac.uk
# Version: 1
# Description: writes list of subdirectories + path into a text file according to rules
# -------
# create list of directories to be run through deconvolution

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", type=str, help='input directory of experiment')
parser.add_argument("--list_wells", type=list, help='list of wells (default = ["all"])', default = ["all"])

args = parser.parse_args()

# the following directory has two subdirectories with _10minperm and _30Minperm: different times of fixing stains (I think)

# directory = "/lustre/scratch125/humgen/projects/cell_activation_tc/projects/KI67_TEST/2_feature_extraction/data/testset_mito/"
directory = args.input_dir

# the following list is of wells with good staining: not sure about how to deal with wells, list of 60 wells seems a bit crazy

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

