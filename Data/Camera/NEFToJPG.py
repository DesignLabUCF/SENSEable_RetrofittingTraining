##################################
#          NEF To JPG            #
#     SENSEable Design Lab       #
##################################
# v1.0
# 1/20/2021
##################################
# To run, pass in 1 for full folder or 0 for single file and folder/file name w/ extension
# EXP: 'python NEFToJPG.py 1/0 Folder/File'
##################################
# Authors: 
# Sermarini
##################################

import sys
import os
import glob
import rawpy
import imageio

# Shout out to our boy M Kompas on StackOverflow
# https://stackoverflow.com/questions/59054975/how-to-convert-a-nef-raw-image-file-type-to-jpg-in-python-on-mac
def convert_NEF(file_name):
    print("Converting " + file_name + " to JPG...")
    with rawpy.imread(file_name) as raw:
        # Convert data
        rgb = raw.postprocess()
        # Fix filenames
        image_name = file_name[:-4] + ".jpg"
        #name_split = image_name.split("\\")
        #image_name = "Camera\\JPG\\" + name_split[2]
        # Outputs
        #imageio.imsave(image_name, rgb) 
        return rgb, image_name  

def save_NEF(rgb, full_path):
    imageio.imsave(full_path, rgb) # Save
    print(full_path, "saved!")

def main(argv):
    # Check inputs and initialize
    assert len(sys.argv) >= 2, "Error: Argument required for entire folder key (1 is yes, 0 is no) and folder/file name"
    # Full folder
    if argv[0] == "1":
        assert os.path.isdir(argv[1]), "Error: Folder " + argv[1] + " not found."
        #raw_paths = glob.glob('Camera\\Raw\\*.NEF')
        raw_paths = glob.glob(argv[1] + "\\*.NEF")
        for raw_path in raw_paths:
            save_NEF(*convert_NEF(raw_path))
    # Individual file
    else:
        # TODO VERIFY FILE EXISTS
        assert os.path.exists(argv[1]), "Error: File " + argv[1] + " not found."
        save_NEF(*convert_NEF(argv[1]))

if __name__=='__main__':
    main(sys.argv[1:])