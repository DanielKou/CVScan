import cv2
import numpy

class Image(object):
	def __init__(self, image_path):
		if isinstance(image_path, basestring):
			self.image = cv2.imread(image_path)
		else:
			self.image = image_path

	def get(self):
		return self.image

	def showImg(self, title):
		cv2.imshow(title, self.image)
		cv2.waitKey(0)

	def getSize(self):
		return self.image.shape

	def resize(self, type, size):
		if (type.lower() == 'w'):
			ratio = float(size) / self.image.shape[1]
			dim = (size, int(self.image.shape[0]) * ratio)
		elif (type.lower() == 'h'):
			ratio = float(size) / self.image.shape[0]
			dim   = (int(self.image.shape[1] * ratio), size)
		else:
			return self.image
		result = cv2.resize(self.image, dim, interpolation=cv2.INTER_AREA)
		return result
