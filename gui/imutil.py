# import the necessary packages
import datetime
import time
from threading import Thread
import cv2

class FPS:
    def __init__(self):
        # store the start time, end time and total number of frames
        # that were examined between the start and end intervals
        self._start = None
        self._end = None
        self._numFrames = 0
        self.t =0.0    # time frame is grabbed

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

class WebCamVideoStream:
    #constantly captures frames
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame 
        # from the stream
        self.stream = cv2.VideoCapture(src)

        #set resolution to maximum
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)
        
        self.t = time.time()
        (self.grabbed, self.frame) = self.stream.read()
        

        # initialize the variable used to inidicate if the thread 
        # should be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        self.fps = FPS().start()
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            # otherwise read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
            self.t = time.time()
            self.fps.update()
            #print("WebCamVideoStream")
            
    def getres(self):
        width = int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        return (width, height)
        
    def get_fps(self):
        self.fps.stop()
        return self.fps.fps()
        

    def grab_frame(self):
        # return the frame most recently read
        return self.grabbed,self.frame, self.t

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        self.stream.release()
