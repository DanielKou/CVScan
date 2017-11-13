import cv2
import numpy
import argparse
from image import Image
from scan import scan

''' Get args '''
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required = True, help = 'path to image')
ap.add_argument('-s', '--save', action = 'store_true', default = False, help = 'save image to current folder');

args = vars(ap.parse_args())

image = Image(args['image'])

#image.showImg('Image')

scan(image)
