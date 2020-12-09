import cv2
import time
import config

from PyQt5.QtGui import QImage
from PyQt5.QtCore import  Qt
from control import Capture, Stream, StepperCtrl
from capture_video import cap_v4l2


class CameraOpenCV:
	def __init__(self, win, src=0, stream_only=False, write=False):
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

	def read(self):
		return_value, frame = self.camera.read()
		return frame


	def stream_frame(self, frame):
		#displays frame in gui window
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



class FPS:
    def __init__(self):
        # store the start time, end time and total number of frames
        # that were examined between the start and end intervals
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        # start the timer
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        # stop the timer
        self._end = datetime.datetime.now()

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFrames += 1

    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        return (self._end - self._start).total_seconds()

    def fps(self):
        # compute the (approximate) frames per second
        return self._numFrames / self.elapsed()
		
	
