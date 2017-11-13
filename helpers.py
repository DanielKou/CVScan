import cv2
import numpy

def points_order(points):
	box = numpy.zeros((4,2), dtype='float32')
	
	coord_sum = points.sum(axis=1)
	box[0] = points[numpy.argmin(coord_sum)]
	box[2] = points[numpy.argmax(coord_sum)]

	coord_diff = numpy.diff(points, axis=1)
	box[1] = points[numpy.argmin(coord_diff)]
	box[3] = points[numpy.argmax(coord_diff)]

	return box


def box_transform(image, points):
	box = points_order(points)
	(tl, tr, br, bl) = box

	width_top = numpy.sqrt(((tl[0] - tr[0]) ** 2) + ((tl[1] - tr[1]) ** 2))
	width_bot = numpy.sqrt(((bl[0] - br[0]) ** 2) + ((bl[1] - br[1]) ** 2))
	max_width = max(int(width_top), int(width_bot))

	height_left = numpy.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	height_right = numpy.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	max_height = max(int(height_left), int(height_right))

	final_box = numpy.array([
		[0, 0],
		[max_width - 1, 0],
		[max_width - 1, max_height - 1],
		[0, max_height - 1]],
		dtype='float32')
	
	matrix = cv2.getPerspectiveTransform(box, final_box)
	image = cv2.warpPerspective(image, matrix, (max_width, max_height))

	return image
