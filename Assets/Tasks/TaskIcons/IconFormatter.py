#################################
#	SENSEable Design Lab
#	University of Central Florida
# 	Institute for Simulation & Training
#	Init: 10/28/2020
#	Last: 9/05/2021
#################################

# Replace images in folder with square shaped padded png's

import sys
import os
from PIL import Image

input_dir = "2_IsolatedImages"
output_dir = "3_ProcessedImages"

def main(argv):
	files = os.listdir(input_dir)
	for file in files:
		if file[-4:] == ".jpg" or file[-4:] == ".png":
			print("Converting " + file + "...")
			# Open file and get dimensions
			img = Image.open(input_dir + "/" + file)
			height = img.height
			width = img.width
			max_dim = max(width, height)
			# Create blank new PNG
			png = Image.new('RGBA', (max_dim, max_dim), (0, 0, 0, 0))
			# Paste old image onto middle of new PNG
			if(height == max_dim):
				offset = int((max_dim - width) / 2.0)
				png.paste(img, (offset, 0))
			else:
				offset = int((max_dim - height) / 2.0)
				png.paste(img, (0, offset))
			# Delete img and save PNG
			img.close()
			#os.remove(file)
			png.save(output_dir + "/" + file[:-4] + ".png")


if __name__ == "__main__":
	main(sys.argv[1:])