#!/usr/bin/python
#
# python-v4l2capture
#
# This file is an example on how to capture a mjpeg video with
# python-v4l2capture.
#
# 2009, 2010 Fredrik Portstrom
#
# I, the copyright holder of this file, hereby release it into the
# public domain. This applies worldwide. In case this is not legally
# possible: I grant anyone the right to use this work for any
# purpose, without any conditions, unless such conditions are
# required by law.

from PIL import Image
import select
import v4l2capture
import time
from imutil import FPS    # for fps
import config

class cap_v4l2():
    
    def __init__(self):
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

        self.stop_time = time.time() + 20.0
        
    def start(self):
        fps = FPS()
        with open('video.mjpg', 'wb') as f:
            fps.start()
            config.capture =True
            while config.capture: #stop_time >= time.time():
                # Wait for the device to fill the buffer.
                select.select((self.video,), (), ())

                # The rest is easy :-)
                image_data = self.video.read_and_queue()
                f.write(image_data)
                fps.update()
        fps.stop()
        video.close()
        print("Saved video.mjpg (Size: " + str(self.size_x) + " x " + str(self.size_y) + ")")
        print("fps: ",fps.fps())
