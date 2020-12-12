import cv2
import time
import config

from PyQt5.QtGui import QImage
from PyQt5.QtCore import  Qt
import select
import v4l2capture




class CameraOpenCV:
	def __init__(self, win, src=0, stream_only=False, write=False):
		self.win =win
		self.camera = cv2.VideoCapture(src)
		
		if stream_only:
			#lower resolution if only streaming
			self.camera.set(cv2.CAP_PROP_FRAME_WIDTH,640)
			self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
		else:
			#set to maximum resolution
			self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
			self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)

			width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
			height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

			self.res = (width, height)

		if write:
			fourcc = cv2.VideoWriter_fourcc(*'FFV1')
			self.out = cv2.VideoWriter('output.avi', fourcc, 24.0, self.res)

	def capture_frame(self):
		#when capturing
		return_value, frame = self.camera.read()
		self.out.write(frame)

		if config.stream:
			self.stream_frame(frame)

	def stream(self):
		#stream only,
		while config.stream:
			return_value, frame = self.camera.read()
			self.stream_frame(frame)
		self.release()

	def stream_frame(self, frame):
		#displays frame in gui window
		rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		h, w, ch = rgbImage.shape
		bytesPerLine = ch * w
		convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
		img = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
		self.win.updateStream(img)

	def release(self):
		self.camera.release()
		print("camera released")
		if write:
			self.out.release()
			print("video released")


class CameraV4L2:
	def __init__(self, win, src=0, stream_only=False, write=False):
		# Open the video device.
		self.video = v4l2capture.Video_device("/dev/video0")

		# Suggest an image size to the device. The device may choose and
		# return another size if it doesn't support the suggested one.
		self.size_x, self.size_y = self.video.set_format(1920, 1080, fourcc='FFV1')
		self.video.set_fps(60)

		# Create a buffer to store image data in. This must be done before
		# calling 'start' if v4l2capture is compiled with libv4l2. Otherwise
		# raises IOError.
		self.video.create_buffers(30)

		# Send the buffer to the device. Some devices require this to be done
		# before calling 'start'.
		self.video.queue_all_buffers()

		# Start the device. This lights the LED if it's a camera that has one.
		self.video.start()

		if stream_only:
			# lower resolution if only streaming
			self.size_x, self.size_y = self.video.set_format(640, 480, fourcc='FFV1')
		else:
			# set to maximum resolution
			self.size_x, self.size_y = self.video.set_format(1920, 1080, fourcc='FFV1')

		if write:
			fourcc = cv2.VideoWriter_fourcc(*'FFV1')
			self.out = cv2.VideoWriter('output.avi', fourcc, 24.0, self.res)

	def capture_frame(self):
		# when capturing
		return_value, frame = self.camera.read()
		self.out.write(frame)

		if config.stream:
			self.stream_frame(frame)

	def stream(self):
		# stream only,
		while config.stream:
			return_value, frame = self.camera.read()
			self.stream_frame(frame)
		self.release()

	def read(self):
		return_value, frame = self.camera.read()
		return frame

	def stream_frame(self, frame):
		# displays frame in gui window
		rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		h, w, ch = rgbImage.shape
		bytesPerLine = ch * w
		convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
		img = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
		self.win.updateStream(img)

		return image

	def release(self):
		self.camera.release()
		print("camera released")
		if write:
			self.out.release()
			print("video released")
