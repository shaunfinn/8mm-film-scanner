import cv2
import time
import config


def preview_frame():
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite('preview'+'.png', image)
    print("image_update")
    camera.release()
    
def grab_10_frames():
    camera = cv2.VideoCapture(0)
    for i in range(10):
        return_value, image = camera.read()
        cv2.imwrite('frames/'+str(i)+'.png', image)
        print("image" + str(i))
        time.sleep(0.5)
    camera.release()

def grab_frame():
    #when capturing
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    config.frame_cnt +=1
    cv2.imwrite('frames/'+str(config.frame_cnt)+'.png', image)
    print("captured frame ", config.frame_cnt)
    camera.release()
