#################################
#	SENSEable Design Lab
#	University of Central Florida
# 	Institute for Simulation & Training
#	10/28/2020
#################################

# Replace jpg's in folder with square shaped padded png's

import sys
import os
from PIL import Image


def main(argv):
	files = os.listdir()
	for file in files:
		if file[-4:] == ".jpg":
			# Open file and get dimensions
			jpg = Image.open(file)
			height = jpg.height
			width = jpg.width
			max_dim = max(width, height)
			# Create blank new PNG
			png = Image.new('RGBA', (max_dim, max_dim), (0, 0, 0, 0))
			# Paste old image onto middle of new PNG
			if(height == max_dim):
				offset = int((max_dim - width) / 2.0)
				png.paste(jpg, (offset, 0))
			else:
				offset = int((max_dim - height) / 2.0)
				png.paste(jpg, (0, offset))
			# Delete JPG and save PNG
			jpg.close()
			os.remove(file)
			png.save(file[:-4] + ".png")


if __name__ == "__main__":
	main(sys.argv[1:])