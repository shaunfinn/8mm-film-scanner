import cv2

def grab_frame():
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite('preview'+'.png', image)
    print("image_update")
    camera.release()
