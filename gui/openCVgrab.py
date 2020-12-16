#prints FPS of camera at max resolution whilst just grabbing/ retrieving

# just grabbing ~22fps
# grab and retrive ~9fps
# grab retrieve and write ~ 2.2fps

import config
import time 
from imutil import FPS
import cv2
import numpy



fps = FPS().start()
c = cv2.VideoCapture(0)
c.set(3, 10000)
c.set(4, 10000)

x= int(c.get(3))
y = int(c.get(4)) 

fourcc = cv2.VideoWriter_fourcc(*'FFV1')
out = cv2.VideoWriter('output.avi', fourcc, 24.0, (x,y))


cnt =0   #frame count local
while cnt < 100:
    
    #grab only
    #status =c.grab()
    
    #grab and retrieve
    status,img = c.retrieve(c.grab())
    
    #write 
    out.write(img)
    
    cnt += 1
    fps.update()
fps.stop()
print(fps.fps())


# with opencV fps max =2.777   
            
        
