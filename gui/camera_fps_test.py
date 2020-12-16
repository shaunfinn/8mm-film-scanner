#prints FPS of camera at max resolution

import config
import time 
from imutil import FPS
from camera import CameraOpenCV


fps = FPS().start()
c = CameraOpenCV(win =None, write=True)
cnt =0   #frame count local
while cnt < 50:
    c.capture_frame()
    cnt += 1
    fps.update()
fps.stop()
print(fps.fps())


# with opencV fps max =2.777   
            
        
