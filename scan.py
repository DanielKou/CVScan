import cv2
import numpy
import helpers
from image import Image

def scan(image, auto=True, height=0, closing=0):
	# try to find height for best fit
	if auto:
		for height in xrange(min(650, image.get().shape[0]), 299, -50):
			for closing in xrange(6, 1, -1):
				orig = image.get().copy()
				ratio = orig.shape[0] / float(height)
				resize = image.resize('h', height)
				full_area = resize.shape[0] * resize.shape[1]

				if scanDoc(closing, orig, ratio, resize, full_area) != 0:
					exit(0)

def scanDoc(closing, orig, ratio, image, full_area):
	''' Edge detection '''
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.bilateralFilter(gray, 11, 17, 17) # trial and error numbers
	Image(gray).showImg('black & white')
	
	# Canny edge detection
	high, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	low = high / 2.0
	edge = cv2.Canny(gray, low, high) # find outlines of objects
	Image(edge).showImg('edge detection')

	# closing kernel to close gaps between black/white pixels
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (closing, closing))
	closed = cv2.morphologyEx(edge, cv2.MORPH_CLOSE, kernel)
	Image(closed).showImg('closed edges')

	''' Find contours '''
	(contours, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	total = 0

	# loop over contours
	approx_lst = []
	for contour in contours:
		contour = cv2.convexHull(contour)
		perimeter = cv2.arcLength(contour, True)
		approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
		area = cv2.contourArea(contour)

		if (area < 0.05 * full_area):	# too small to consider
			continue
		
		if len(approx) == 4:	# 4 contour points must be a paper right???
			cv2.drawContours(image, [approx], -1, (0, 255, 0), 4)
			approx_lst.append(approx)
			total += 1

	print 'Found %d pages in the image' % total
	
	if (total != 0):
		''' Perspective transform & threshold '''
		for approx in approx_lst:
			total += 1
			warp = helpers.box_transform(orig, approx.reshape(4,2) * ratio)
			Image(warp).showImg('warpped')

			scan_warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
			scan_warp = cv2.medianBlur(scan_warp, 5)
			scan_warp = cv2.adaptiveThreshold(scan_warp, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
			Image(scan_warp).showImg('final image')

	return total
