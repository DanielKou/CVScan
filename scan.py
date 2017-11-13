import cv2
import numpy
import argparse
import helpers

''' Get args '''
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required = True, help = 'path to image')
ap.add_argument('-s', '--save', action = 'store_true', default = False, help = 'save image to current folder');

args = vars(ap.parse_args())

image = cv2.imread(args['image'])

# helpers.showImg(image)


